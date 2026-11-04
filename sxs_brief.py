# -*- coding: utf-8 -*-
"""SXS prompt assembly: resolve a brief, render LLM/MODEL prompts, explain warnings."""
from __future__ import annotations

import json

try:
    from . import sxs_compat, sxs_data, sxs_phrases
except ImportError:  # pragma: no cover
    import sxs_compat
    import sxs_data
    import sxs_phrases


def _bool(value) -> bool:
    return bool(value)


def _master_seed(seed, config) -> int:
    try:
        seed = int(seed)
    except (TypeError, ValueError):
        seed = 0
    if seed == 0:
        try:
            seed = int(config.get("master_seed", 0) or 0)
        except (TypeError, ValueError):
            seed = 0
    return seed


def _resolve(values, seed, config):
    preset = values.get("Пресет_сцены", "none")
    values = sxs_compat.merge_preset(values, preset)

    seed = _master_seed(values.get("seed", 0), config)
    warnings = []

    char_texts = [values.get(f"char_{i}", "") for i in range(1, 7)]
    genders = {i: values.get(f"Пол_{i}", "auto") for i in range(1, 7)}
    characters, counts, pairs, focus, cast_warnings = sxs_compat.resolve_characters(
        char_texts=char_texts,
        gender_overrides=genders,
        girls=values.get("Девушки", "auto"),
        boys=values.get("Парни", "auto"),
        control=values.get("Управление", "hybrid"),
        distribution=values.get("Распределение", "by_connection"),
        roles_raw=values.get("Кто_с_кем", ""),
        seed=seed,
        config=config,
        missing_policy=values.get("Политика_отсутствующего", "partial"),
        focus_raw=values.get("Фокус_на", "auto"),
    )
    warnings.extend(cast_warnings)

    type_groups = sxs_compat.type_groups_from_values(values)
    requires = sxs_compat.requirements_from_toggles(values)
    allowed_t = sxs_compat.allowed_types(type_groups, counts["female"], counts["male"], requires)
    if not allowed_t:
        allowed_t = ["classic"]
        warnings.append("no scene type fits the cast; defaulted to classic")

    delegate_all = _bool(values.get("Всё_выбирает_LLM", False))
    type_llm = delegate_all or _bool(values.get("Тип_выбирает_LLM", False))
    pose_llm = delegate_all or _bool(values.get("Позы_выбирает_LLM", True))
    camera_llm = delegate_all or _bool(values.get("Камера_выбирает_LLM", False))
    env_llm = delegate_all or _bool(values.get("Окружение_выбирает_LLM", False))

    if not type_llm and values.get("Тип") not in (None, "random") and values.get("Тип") not in allowed_t:
        warnings.append(
            f"scene type '{values.get('Тип')}' is impossible for {counts['female']}F+{counts['male']}M; "
            "picked a compatible type"
        )
    scene_type = sxs_compat.resolve_type(
        values.get("Тип", "random"), allowed_t, seed, use_llm=type_llm,
        freedom=values.get("Свобода_LLM", "from_lists"),
    )

    stage_raw = values.get("Этап_сцены", "auto")
    stage_allowed = sxs_compat.allowed_stages(scene_type)
    if stage_raw not in (None, "", "auto", "random") and stage_raw not in stage_allowed:
        warnings.append(
            f"scene stage '{stage_raw}' is impossible for type '{scene_type}'; "
            "picked an allowed stage"
        )
    stage = sxs_compat.resolve_stage(stage_raw, stage_allowed, seed)
    finish_raw = values.get("Куда_кончает", "auto")
    finish_allowed = sxs_compat.allowed_finish_targets(
        scene_type, stage, counts["female"], counts["male"],
    )
    if stage == "finish" and finish_raw not in (None, "", "auto", "none", "random") and finish_raw not in finish_allowed:
        warnings.append(
            f"finish target '{finish_raw}' is impossible for type '{scene_type}'; "
            "picked an allowed target"
        )
    finish_target = sxs_compat.resolve_finish_target(
        finish_raw, finish_allowed, seed, stage,
    )

    pose_groups = sxs_compat.pose_groups_from_values(values)
    allowed_p = sxs_compat.allowed_poses(pose_groups)
    if not allowed_p:
        allowed_p = list(sxs_data.POSES)
        warnings.append("no pose group enabled; using all poses")
    if not pose_llm and values.get("Поза") not in (None, "random") and values.get("Поза") not in allowed_p:
        warnings.append(f"pose '{values.get('Поза')}' is not in the enabled groups; picked an allowed pose")
    pose = sxs_compat.resolve_choice(
        values.get("Поза", "random"), allowed_p, seed, "pose", use_llm=pose_llm,
        freedom=values.get("Свобода_LLM", "from_lists"),
    )

    emotion = sxs_compat.resolve_choice(
        values.get("Эмоции", "auto"), [x for x in sxs_data.EMOTIONS if x != "auto"],
        seed, "emotion",
    )
    tempo = sxs_compat.resolve_choice(
        values.get("Темп", "auto"), [x for x in sxs_data.TEMPOS if x != "auto"],
        seed, "tempo",
    )
    clothing = sxs_compat.resolve_choice(
        values.get("Одежда", "auto"), [x for x in sxs_data.CLOTHING if x != "auto"],
        seed, "clothing",
    )

    gaze = sxs_compat.resolve_choice(
        values.get("Взгляд", "auto"), [x for x in sxs_data.GAZES if x != "auto"],
        seed, "gaze",
    )
    who_top = sxs_compat.resolve_who_top(
        values.get("Кто_сверху", "auto"), seed, counts["female"], counts["male"],
    )

    # ── camera ────────────────────────────────────────────────────────────
    def camera_choice(widget, key, pool, llm=False):
        if not pool:
            return "auto"
        return sxs_compat.resolve_choice(values.get(widget), pool, seed, key, use_llm=llm)

    angles = list(sxs_data.ANGLES) if _bool(values.get("Ракурсы_вкл", True)) else []
    shots = list(sxs_data.SHOTS) if _bool(values.get("Планы_вкл", True)) else []
    focuses = list(sxs_data.FOCUS) if _bool(values.get("Фокусы_вкл", True)) else []

    position = values.get("Положение_камеры", "auto")
    if _bool(values.get("POV", False)) and position in ("auto", "none", ""):
        position = "pov"

    camera = {
        "position": sxs_compat.resolve_choice(
            position, sxs_data.CAMERA_POSITIONS, seed, "camera_position",
        ),
        "angle": camera_choice("Ракурс", "camera_angle", angles, camera_llm),
        "shot": camera_choice("План", "camera_shot", shots, camera_llm),
        "focus": camera_choice("Фокус", "camera_focus", focuses, camera_llm),
        "level": camera_choice("Уровень_камеры", "camera_level", sxs_data.CAMERA_LEVELS, camera_llm),
        "pov": _bool(values.get("POV", False)),
        "composition": camera_choice("Композиция", "camera_composition", sxs_data.COMPOSITIONS, camera_llm),
        "crop": camera_choice("Кроп", "camera_crop", sxs_data.CROPS, camera_llm),
        "target": camera_choice("Куда_смотрит_камера", "camera_target", sxs_data.CAMERA_TARGETS, camera_llm),
        "zoom": camera_choice("Зум", "camera_zoom", sxs_data.ZOOMS, camera_llm),
    }

    # ── environment ───────────────────────────────────────────────────────
    def env_choice(widget, key, pool):
        if not pool:
            return "auto"
        return sxs_compat.resolve_choice(values.get(widget), pool, seed, key, use_llm=env_llm)

    # Build background pool from enabled groups
    bg_pool = []
    if _bool(values.get("Фоны_вкл", True)):
        if _bool(values.get("Фоны_простые_вкл", True)):
            bg_pool.extend(sxs_data.BG_SIMPLE)
        if _bool(values.get("Фоны_студия_вкл", True)):
            bg_pool.extend(sxs_data.BG_STUDIO)
        if _bool(values.get("Фоны_город_вкл", True)):
            bg_pool.extend(sxs_data.BG_CITY)
        if _bool(values.get("Фоны_природа_вкл", True)):
            bg_pool.extend(sxs_data.BG_NATURE)
        if _bool(values.get("Фоны_вода_вкл", True)):
            bg_pool.extend(sxs_data.BG_WATER)
        if _bool(values.get("Фоны_комнаты_вкл", True)):
            bg_pool.extend(sxs_data.BG_ROOM)
        if _bool(values.get("Фоны_фэнтези_вкл", True)):
            bg_pool.extend(sxs_data.BG_FANTASY)
    backgrounds = bg_pool if bg_pool else list(sxs_data.BACKGROUNDS)
    lighting = list(sxs_data.LIGHTING) if _bool(values.get("Свет_вкл", True)) else []
    times = list(sxs_data.TIMES) if _bool(values.get("Время_вкл", True)) else []
    atmospheres = list(sxs_data.ATMOSPHERES) if _bool(values.get("Атмосфера_вкл", True)) else []
    settings = list(sxs_data.SETTINGS) if _bool(values.get("Сеттинг_вкл", True)) else []

    environment = {
        "background": env_choice("Фон", "background", backgrounds),
        "lighting": env_choice("Освещение", "lighting", lighting),
        "time": env_choice("Время_суток", "time", [x for x in times if x != "auto"]) if times else "auto",
        "atmosphere": env_choice("Атмосфера", "atmosphere", [x for x in atmospheres if x != "auto"]) if atmospheres else "auto",
        "setting": env_choice("Сеттинг", "setting", [x for x in settings if x != "auto"]) if settings else "auto",
    }

    brief = {
        "seed": seed,
        "format": values.get("Формат_промпта", "natural"),
        "model": values.get("Модель", "universal"),
        "freedom": values.get("Свобода_LLM", "from_lists"),
        "control": values.get("Управление", "hybrid"),
        "distribution": values.get("Распределение", "by_connection"),
        "missing_policy": values.get("Политика_отсутствующего", "partial"),
        "counts": counts,
        "characters": [
            {"index": c["index"], "gender": c["gender"], "text": c["text"]}
            for c in characters
        ],
        "pairs": pairs,
        "focus": focus,
        "type": scene_type,
        "stage": stage,
        "finish_target": finish_target,
        "emotion": emotion,
        "tempo": tempo,
        "clothing": clothing,
        "interactions": sxs_compat.valid_interactions(values.get("Взаимодействия", "")),
        "pose": pose,
        "gaze": gaze,
        "who_top": who_top,
        "camera": camera,
        "environment": environment,
        "style": {
            "style": values.get("Стиль", "photoreal"),
            "quality": values.get("Качество", "high"),
            "quality_tokens": _bool(values.get("Quality_tokens", True)),
        },
        "explicit": _bool(values.get("Явные_термины", True)),
        "forbidden": str(values.get("Запреты", "") or "").strip(),
        "warnings": warnings,
    }

    if _bool(values.get("Всё_выбирает_LLM", False)):
        brief["warnings"].append("all random fields delegated to the LLM")

    return brief


def concretize(value, seed=0, key="choice"):
    """Replace every llm_choice node with one concrete allowed value."""
    if isinstance(value, dict):
        if value.get("mode") == "llm_choice":
            allowed = value.get("allowed") or []
            return sxs_compat.pick(seed, key, allowed) or (allowed[0] if allowed else "")
        return {k: concretize(v, seed, f"{key}.{k}") for k, v in value.items()}
    if isinstance(value, list):
        return [concretize(v, seed, f"{key}.{i}") for i, v in enumerate(value)]
    return value


def _allowed_section(brief):
    lines = []

    def walk(node, path):
        if isinstance(node, dict):
            if node.get("mode") == "llm_choice":
                allowed = node.get("allowed") or []
                lines.append(f"{path}: {', '.join(allowed) if allowed else '(none)'}")
                return
            for key, value in node.items():
                walk(value, f"{path}.{key}" if path else key)

    walk(brief.get("type"), "type")
    walk(brief.get("pose"), "pose")
    walk(brief.get("camera"), "camera")
    walk(brief.get("environment"), "environment")
    if not lines:
        return "(none; all values are fixed in BRIEF)"
    return "\n".join(lines)


def build_llm_prompt(brief, lang="en"):
    lang = "ru" if str(lang).lower().startswith("ru") else "en"
    system = sxs_phrases.SYSTEM[lang]
    rules = sxs_phrases.RULES[lang].format(
        format=sxs_phrases.t("format", brief.get("format", "natural"), lang),
        model=sxs_phrases.t("model", brief.get("model", "universal"), lang),
        freedom=sxs_phrases.t("freedom", brief.get("freedom", "from_lists"), lang),
        forbidden=(
            f"\n- Additional bans from the user: {brief['forbidden']}."
            if brief.get("forbidden") else ""
        ),
    )
    payload = {k: v for k, v in brief.items() if k != "warnings"}
    return (
        "[SYSTEM]\n"
        f"{system}\n\n"
        "[BRIEF]\n"
        f"{json.dumps(payload, ensure_ascii=False, indent=2)}\n\n"
        "[ALLOWED]\n"
        f"{_allowed_section(payload)}\n\n"
        "[RULES]\n"
        f"{rules}"
    )


def _join(parts):
    return ", ".join(str(p) for p in parts if p not in (None, "", "auto", "none"))


def build_model_prompt(brief, lang="en"):
    lang = "ru" if str(lang).lower().startswith("ru") else "en"
    b = concretize(brief, brief.get("seed", 0))

    def t(category, token):
        if isinstance(token, dict) or token in (None, "", "auto", "none"):
            return ""
        return sxs_phrases.t(category, token, lang)

    characters = [c.get("text", "") for c in b.get("characters", []) if c.get("text")]
    cast = "; ".join(characters)

    scene_type = t("type", b.get("type"))
    if b.get("stage") == "finish" and b.get("finish_target") not in (None, "", "auto", "none"):
        stage = t("finish_target", b.get("finish_target"))
    else:
        stage = t("stage", b.get("stage"))
    pose = t("pose", b.get("pose"))
    emotion = t("emotion", b.get("emotion"))
    tempo = t("tempo", b.get("tempo"))
    clothing = t("clothing", b.get("clothing"))
    gaze = t("gaze", b.get("gaze"))
    who_top = t("who_top", b.get("who_top"))

    interactions = [t("interaction", x) for x in b.get("interactions", [])]
    camera = b.get("camera") or {}
    environment = b.get("environment") or {}
    style = b.get("style") or {}

    cam_parts = [
        t("camera_position", camera.get("position")),
        t("angle", camera.get("angle")),
        t("shot", camera.get("shot")),
        t("camera_level", camera.get("level")),
        t("composition", camera.get("composition")),
        t("crop", camera.get("crop")),
        t("camera_target", camera.get("target")),
        t("zoom", camera.get("zoom")),
    ]
    env_parts = [
        t("background", environment.get("background")),
        t("lighting", environment.get("lighting")),
        t("time", environment.get("time")),
        t("atmosphere", environment.get("atmosphere")),
        t("setting", environment.get("setting")),
    ]

    pieces = []
    if cast:
        pieces.append(cast)
    if scene_type:
        pieces.append(scene_type)
    if stage:
        pieces.append(stage)
    if pose:
        pieces.append(pose)
    if who_top:
        pieces.append(who_top)
    if emotion:
        pieces.append(emotion)
    if tempo:
        pieces.append(tempo)
    if clothing:
        pieces.append(clothing)
    if gaze:
        pieces.append(gaze)
    if interactions:
        pieces.append(", ".join(interactions))
    if cam_parts:
        pieces.append(", ".join(p for p in cam_parts if p))
    if env_parts:
        pieces.append(", ".join(p for p in env_parts if p))
    if b.get("missing_policy") == "pov":
        pieces.append(sxs_phrases.t("missing", "pov", lang))
    if style.get("style"):
        pieces.append(t("style", style.get("style")))
    if style.get("quality"):
        pieces.append(t("quality", style.get("quality")))

    natural = ". ".join(p.strip(". ") for p in pieces if p).strip()
    if natural:
        natural += "."

    tags = []
    if style.get("style"):
        tags.append(t("style", style.get("style")))
    if style.get("quality"):
        tags.append(t("quality", style.get("quality")))
    if scene_type:
        tags.append(scene_type)
    if stage:
        tags.append(stage)
    if pose:
        tags.append(pose)
    if emotion:
        tags.append(emotion)
    if tempo:
        tags.append(tempo)
    if clothing:
        tags.append(clothing)
    if gaze:
        tags.append(gaze)
    tags.extend(interactions)
    tags.extend(p for p in cam_parts if p)
    tags.extend(p for p in env_parts if p)
    if style.get("quality_tokens"):
        tags.extend(["detailed", "sharp focus"])
    tag_line = ", ".join(dict.fromkeys(t for t in tags if t))

    fmt = b.get("format", "natural")
    if fmt == "tags":
        return tag_line
    if fmt == "hybrid":
        return f"{natural} | {tag_line}" if natural and tag_line else (natural or tag_line)
    return natural or tag_line


def build_outputs(values, config):
    config = config or {}
    brief = _resolve(values, values.get("seed", 0), config)
    lang = values.get("Язык_промпта", "en")
    llm = build_llm_prompt(brief, lang)
    model = build_model_prompt(brief, lang)
    warn = "; ".join(w for w in brief.get("warnings", []) if w)
    payload = {k: v for k, v in brief.items() if k != "warnings"}
    return llm, model, warn, int(brief["seed"]), json.dumps(payload, ensure_ascii=False)
