# -*- coding: utf-8 -*-
"""SXS compatibility and casting rules.

Pure functions only: no ComfyUI imports, no torch, no I/O.  The node feeds
widget values in and gets a resolved brief out, which makes every rule
testable head-lessly.
"""
from __future__ import annotations

import hashlib
import json
import re

try:  # package import (custom_nodes/SXS) and flat import (tests) both work
    from . import sxs_data
except ImportError:  # pragma: no cover
    import sxs_data


FEMALE_RE = re.compile(
    r"\b(woman|women|girl|girls|female|lady|ladies|mother|mom|wife|she|her|"
    r"девушка|девушки|женщина|женщины|девочка|девочки|мама|мать|жена|она|её|ее)\b",
    re.IGNORECASE,
)
MALE_RE = re.compile(
    r"\b(man|men|boy|boys|male|guy|guys|father|dad|husband|he|him|his|"
    r"мужчина|мужчины|парень|парни|мальчик|мальчики|папа|отец|муж|он|его)\b",
    re.IGNORECASE,
)


def rand_int(seed: int, key: str, mod: int) -> int:
    """Deterministic integer in [0, mod)."""
    if mod <= 0:
        return 0
    digest = hashlib.md5(f"{seed}:{key}".encode("utf-8")).hexdigest()
    return int(digest[:16], 16) % mod


def rand_bool(seed: int, key: str, probability: float = 0.5) -> bool:
    return rand_int(seed, key, 10000) < int(probability * 10000)


def pick(seed: int, key: str, items):
    items = list(items or [])
    if not items:
        return None
    return items[rand_int(seed, key, len(items))]


def parse_config(raw) -> dict:
    if isinstance(raw, dict):
        return dict(raw)
    if not raw:
        return {}
    try:
        parsed = json.loads(raw)
        return parsed if isinstance(parsed, dict) else {}
    except (TypeError, ValueError):
        return {}


def infer_gender(text: str):
    """Return 'female'/'male'/None from the earliest gender marker."""
    if not text:
        return None
    female = FEMALE_RE.search(text)
    male = MALE_RE.search(text)
    if female and male:
        return "female" if female.start() <= male.start() else "male"
    if female:
        return "female"
    if male:
        return "male"
    return None


def parse_count(value, default=None):
    """'auto' -> None, 'random' -> 'random', digits -> clamped int."""
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return max(0, min(3, int(value)))
    text = str(value).strip().lower()
    if text in ("auto", ""):
        return default
    if text in ("random", "rand"):
        return "random"
    if text.isdigit():
        return max(0, min(3, int(text)))
    return default


def parse_roles(raw) -> dict:
    """Parse the optional roles JSON.  Returns an empty dict on bad input."""
    if isinstance(raw, dict):
        data = raw
    elif not raw:
        return {}
    else:
        try:
            data = json.loads(raw)
        except (TypeError, ValueError):
            return {}
    if not isinstance(data, dict):
        return {}

    out = {}
    counts = data.get("counts")
    if isinstance(counts, dict):
        female = counts.get("female", counts.get("women", counts.get("ж", counts.get("f"))))
        male = counts.get("male", counts.get("men", counts.get("м", counts.get("m"))))
        if female is not None:
            out["female"] = max(0, min(3, int(female)))
        if male is not None:
            out["male"] = max(0, min(3, int(male)))

    gender = data.get("gender") or data.get("genders")
    if isinstance(gender, dict):
        mapped = {}
        for key, value in gender.items():
            try:
                idx = int(key)
            except (TypeError, ValueError):
                continue
            token = str(value).strip().lower()
            if token in ("f", "female", "ж", "woman", "girl"):
                mapped[idx] = "female"
            elif token in ("m", "male", "м", "man", "boy"):
                mapped[idx] = "male"
        if mapped:
            out["gender"] = mapped

    pairs = data.get("pairs")
    if isinstance(pairs, list):
        clean = []
        for pair in pairs:
            if isinstance(pair, (list, tuple)) and len(pair) == 2:
                clean.append([str(pair[0]), str(pair[1])])
            elif isinstance(pair, dict):
                a = pair.get("a", pair.get("f", pair.get("1")))
                b = pair.get("b", pair.get("m", pair.get("2")))
                if a is not None and b is not None:
                    clean.append([str(a), str(b)])
        if clean:
            out["pairs"] = clean

    if "focus" in data:
        try:
            out["focus"] = int(data["focus"])
        except (TypeError, ValueError):
            pass

    return out


def _assign_unknown(entries, female_slots, male_slots):
    """Fill unknown genders from the remaining slot counts."""
    remaining_f, remaining_m = female_slots, male_slots
    for entry in entries:
        if entry["gender"]:
            if entry["gender"] == "female" and remaining_f > 0:
                remaining_f -= 1
            elif entry["gender"] == "male" and remaining_m > 0:
                remaining_m -= 1
    for entry in entries:
        if entry["gender"]:
            continue
        if remaining_f > 0:
            entry["gender"] = "female"
            remaining_f -= 1
        elif remaining_m > 0:
            entry["gender"] = "male"
            remaining_m -= 1
        else:
            entry["gender"] = "female"
    return entries


def resolve_characters(
    char_texts,
    gender_overrides,
    girls,
    boys,
    control,
    distribution,
    roles_raw,
    seed,
    config,
    missing_policy="partial",
    focus_raw="auto",
):
    """Resolve the cast.

    Returns (characters, counts, pairs, focus, warnings).
    """
    warnings = []
    roles = parse_roles(roles_raw)
    config = config or {}
    raw_female = parse_count(girls)
    raw_male = parse_count(boys)
    explicit_counts = type(raw_female) is int or type(raw_male) is int
    connected = [
        {"index": i, "text": text.strip(), "gender": None, "source": "connected"}
        for i, text in enumerate(char_texts, 1)
        if text and text.strip()
    ]

    for entry in connected:
        override = str(gender_overrides.get(entry["index"], "auto")).lower()
        if override in ("female", "male"):
            entry["gender"] = override
            entry["source"] = "override"
        elif roles.get("gender", {}).get(entry["index"]):
            entry["gender"] = roles["gender"][entry["index"]]
            entry["source"] = "roles"
        else:
            entry["gender"] = infer_gender(entry["text"])
        if entry["gender"] is None:
            warnings.append(
                f"gender not recognised for character {entry['index']}; "
                "assigned from the remaining slots"
            )

    # ── counts ────────────────────────────────────────────────────────────
    if control == "all_random":
        female = rand_int(seed, "cast_female", 4)
        male = rand_int(seed, "cast_male", 4)
        if female + male == 0:
            female = 1
    else:
        female = raw_female
        male = raw_male

        if distribution == "manual" and ("female" in roles or "male" in roles):
            female = roles.get("female", female if female is not None else 0)
            male = roles.get("male", male if male is not None else 0)

        inferred_f = sum(1 for e in connected if e["gender"] == "female")
        inferred_m = sum(1 for e in connected if e["gender"] == "male")

        if female == "random":
            female = rand_int(seed, "cast_female", 4)
        elif female is None:
            female = inferred_f if inferred_f else (1 if inferred_m == 0 else 0)

        if male == "random":
            male = rand_int(seed, "cast_male", 4)
        elif male is None:
            male = inferred_m if inferred_m else (1 if inferred_f == 0 else 0)

    female = max(0, min(3, int(female)))
    male = max(0, min(3, int(male)))

    if female + male == 0:
        female, male = 1, 1
        warnings.append("no participants resolved; defaulted to 1 female + 1 male")

    # ── build the cast ────────────────────────────────────────────────────
    cast = _assign_unknown(list(connected), female, male)

    if len(cast) > female + male:
        warnings.append(f"more connected characters than the requested cast; kept the first {female + male}")
        cast = cast[: female + male]

    need_f = female - sum(1 for e in cast if e["gender"] == "female")
    need_m = male - sum(1 for e in cast if e["gender"] == "male")

    # Explicit counts are a contract: fill the gaps.  With no characters
    # connected at all there is nothing to clamp to, so the default 1F+1M
    # cast is used.  Otherwise "partial" keeps only what is connected.
    fill_missing = (
        missing_policy == "invent"
        or control == "manual"
        or explicit_counts
        or not connected
    )

    if need_f + need_m > 0:
        if fill_missing:
            for _ in range(max(0, need_f)):
                cast.append({"index": len(cast) + 1, "text": "", "gender": "female", "source": "invented"})
            for _ in range(max(0, need_m)):
                cast.append({"index": len(cast) + 1, "text": "", "gender": "male", "source": "invented"})
            if missing_policy == "invent":
                warnings.append("missing partner(s) invented to satisfy the scene")
        else:
            if need_f + need_m > 0:
                warnings.append("cast clamped to the connected characters")
            female = sum(1 for e in cast if e["gender"] == "female")
            male = sum(1 for e in cast if e["gender"] == "male")

    if not cast:
        cast = [{"index": 1, "text": "", "gender": "female", "source": "invented"}]
        female, male = 1, 0
        warnings.append("empty cast; defaulted to a single female")

    # ── pairs ─────────────────────────────────────────────────────────────
    pairs = roles.get("pairs") or []
    if not pairs:
        females = [e for e in cast if e["gender"] == "female"]
        males = [e for e in cast if e["gender"] == "male"]
        if females and males:
            for i, female_entry in enumerate(females):
                male_entry = males[i % len(males)]
                pairs.append([str(female_entry["index"]), str(male_entry["index"])])
        elif len(females) >= 2:
            pairs = [[str(females[i]["index"]), str(females[i + 1]["index"])] for i in range(len(females) - 1)]
        elif len(males) >= 2:
            pairs = [[str(males[i]["index"]), str(males[i + 1]["index"])] for i in range(len(males) - 1)]

    # ── focus ─────────────────────────────────────────────────────────────
    focus = roles.get("focus")
    focus_explicit = focus is not None
    if focus is None and focus_raw not in ("auto", "", None):
        try:
            focus = int(focus_raw)
            focus_explicit = True
        except (TypeError, ValueError):
            focus = None
    if focus is None:
        focus = 1
    if not isinstance(focus, int) or focus < 1 or focus > len(cast):
        focus = 1
    if cast and not focus_explicit:
        # A POV scene is anchored on the first female when one exists.
        if any(e["gender"] == "female" for e in cast):
            first_female = next(e for e in cast if e["gender"] == "female")
            focus = first_female["index"]

    for entry in cast:
        if not entry["text"]:
            entry["text"] = "an adult female, appearance not specified" if entry["gender"] == "female" else "an adult male, appearance not specified"

    counts = {
        "female": sum(1 for e in cast if e["gender"] == "female"),
        "male": sum(1 for e in cast if e["gender"] == "male"),
    }
    return cast, counts, pairs, focus, warnings


def allowed_types(type_groups, female, male, requires):
    """Types that the current cast can actually perform."""
    requires = set(requires or ())
    out = []
    for group, enabled in type_groups.items():
        if not enabled:
            continue
        for token in sxs_data.TYPE_GROUPS.get(group, []):
            rule = sxs_data.TYPE_RULES[token]
            if female < rule["minF"] or male < rule["minM"] or female + male < rule["minTotal"]:
                continue
            if any(req not in requires for req in rule["requires"]):
                continue
            if token not in out:
                out.append(token)
    return out


def resolve_type(value, allowed, seed, use_llm=False, freedom="from_lists"):
    if use_llm:
        return {"mode": "llm_choice", "allowed": list(allowed)}
    if value == "random" or value not in allowed:
        chosen = pick(seed, "type", allowed)
        return chosen if chosen else "classic"
    return value


def resolve_choice(value, allowed, seed, key, use_llm=False, freedom="from_lists"):
    """Resolve a delegated/random single choice.

    'auto'/'none'/'' are preserved so optional fields can stay omitted.
    """
    if use_llm:
        return {"mode": "llm_choice", "allowed": list(allowed)}
    if value in ("auto", "none", "", None):
        return value
    if value == "random" or value not in allowed:
        chosen = pick(seed, key, allowed)
        return chosen if chosen is not None else value
    return value


def preset_overrides(preset: str) -> dict:
    return dict(sxs_data.PRESETS.get(preset, {}))


def merge_preset(values: dict, preset: str) -> dict:
    """Apply a preset only where the widget still holds its neutral value."""
    out = dict(values)
    for key, value in preset_overrides(preset).items():
        current = out.get(key)
        neutral = current in (None, "", "auto", "random", "none")
        if key == "POV":
            neutral = current is False
        if key.startswith("Тип_группа_"):
            neutral = current is False
        if neutral:
            out[key] = value
    return out


def requirements_from_toggles(values: dict) -> set:
    req = set()
    if values.get("Тип_группа_toys"):
        req.update(("toy", "strapon", "dp"))
    return req


def type_groups_from_values(values: dict) -> dict:
    return {
        group: bool(values.get(f"Тип_группа_{group}", False))
        for group in sxs_data.TYPE_GROUPS
    }


def pose_groups_from_values(values: dict) -> dict:
    return {
        group: bool(values.get(f"Позы_группа_{group}", True))
        for group in sxs_data.POSE_GROUPS
    }


def allowed_poses(pose_groups):
    out = []
    for group, enabled in pose_groups.items():
        if enabled:
            out.extend(sxs_data.POSE_GROUPS.get(group, []))
    return out


def resolve_who_top(value, seed, female, male):
    if value == "auto":
        if female and not male:
            return "female"
        if male and not female:
            return "male"
        return pick(seed, "who_top", ["female", "male"]) or "female"
    if value == "random":
        return pick(seed, "who_top", ["female", "male"]) or "female"
    if value in ("female", "male"):
        return value
    return "female"


def parse_interactions(raw):
    if isinstance(raw, (list, tuple)):
        return [str(x).strip() for x in raw if str(x).strip()]
    if not raw:
        return []
    return [x.strip() for x in re.split(r"[,;\n]+", str(raw)) if x.strip()]


def valid_interactions(raw):
    parsed = parse_interactions(raw)
    if not parsed:
        return []
    return [x for x in parsed if x in sxs_data.INTERACTIONS] or parsed


def allowed_stages(scene_type):
    """Stages that make sense for the resolved scene type."""
    if isinstance(scene_type, dict) or scene_type in (None, "", "auto", "random"):
        return ["start", "insertion", "middle", "finish"]
    if scene_type in sxs_data.NON_INSERTION_TYPES:
        return ["start", "middle", "finish"]
    return ["start", "insertion", "middle", "finish"]


def allowed_finish_targets(scene_type, stage, female, male):
    """Where ejaculation can land for this scene; ['none'] when impossible."""
    if stage != "finish" or male <= 0:
        return ["none"]
    if isinstance(scene_type, dict) or not scene_type:
        return ["inside", "mouth", "face", "breast", "body", "back", "outside"]
    if scene_type == "solo_m":
        return ["body", "outside"]
    if scene_type == "oral":
        return ["mouth", "face", "breast", "body", "outside"]
    if scene_type == "bukkake":
        return ["face", "mouth", "breast", "body"]
    if scene_type == "creampie":
        return ["inside"]
    if scene_type == "facesitting":
        return ["body", "outside"]
    if scene_type == "fingering":
        return ["face", "breast", "body", "back", "outside"]
    return ["inside", "mouth", "face", "breast", "body", "back", "outside"]


def resolve_stage(value, allowed, seed):
    if value in (None, "", "auto", "none"):
        return "auto"
    if value == "random" or value not in allowed:
        return pick(seed, "scene_stage", allowed) or "middle"
    return value


def resolve_finish_target(value, allowed, seed, stage):
    if stage != "finish" or not allowed or allowed == ["none"]:
        return "none"
    if value in (None, "", "auto"):
        return "auto"
    if value == "none":
        return "none"
    if value == "random" or value not in allowed:
        return pick(seed, "finish_target", allowed) or "none"
    return value
