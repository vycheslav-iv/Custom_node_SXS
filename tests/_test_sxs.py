# -*- coding: utf-8 -*-
"""SXS: headless Python sandbox.

Run:  cd SXS && python tests/_test_sxs.py
Prints one line per check and the final "FAIL: N"/"ТЕСТ ПРОЙДЕН" pair that
check.json expects.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

FAILS = 0
OKS = 0


CHECK_COUNT = 0
FAILED_CHECKS = []
def check(label, cond, extra=""):
    global FAILS, OKS, CHECK_COUNT, FAILED_CHECKS
    CHECK_COUNT += 1
    if cond:
        OKS += 1
        print(f"  ok    {label}")
    else:
        FAILED_CHECKS.append((CHECK_COUNT, label, extra))
        with open("check_debug.txt", "a", encoding="utf-8") as f:
            f.write("DEBUG_FAIL {}: {} cond={} extra={}\n".format(CHECK_COUNT, label, repr(cond), repr(extra)))
        FAILS += 1
        print(f"  FAIL  {CHECK_COUNT}: {label}" + (f"  [{extra}]" if extra else ""))


def base():
    return {
        "seed": 0,
        "Язык_меню": "auto",
        "Язык_промпта": "en",
        "Управление": "hybrid",
        "Девушки": "auto",
        "Парни": "auto",
        "Распределение": "by_connection",
        "Авто_пары": True,
        "Кто_с_кем": "",
        "Фокус_на": "auto",
        "Политика_отсутствующего": "partial",
        "Пол_1": "auto", "Пол_2": "auto", "Пол_3": "auto",
        "Пол_4": "auto", "Пол_5": "auto", "Пол_6": "auto",
        "Пресет_сцены": "none",
        "Тип": "random",
        "Тип_выбирает_LLM": False,
        "Этап_сцены": "auto",
        "Куда_кончает": "auto",
        "Тип_группа_basic": True,
        "Тип_группа_same_sex": True,
        "Тип_группа_group": True,
        "Тип_группа_solo": True,
        "Тип_группа_pov": True,
        "Тип_группа_bdsm": False,
        "Тип_группа_toys": False,
        "Тип_группа_extreme": False,
        "Совместимость": "strict",
        "Взаимодействия": "",
        "Эмоции": "auto",
        "Темп": "auto",
        "Одежда": "auto",
        "Позы_выбирает_LLM": True,
        "Позы_группа_stand": True,
        "Позы_группа_sit": True,
        "Позы_группа_lying": True,
        "Позы_группа_dynamic": True,
        "Позы_группа_mood": True,
        "Позы_группа_modeling": True,
        "Позы_группа_gesture": True,
        "Позы_группа_sexual": True,
        "Поза": "random",
        "Взгляд": "auto",
        "Кто_сверху": "auto",
        "Положение_камеры": "auto",
        "Камера_выбирает_LLM": False,
        "Ракурс": "random",
        "План": "random",
        "Фокус": "random",
        "Ракурсы_вкл": True,
        "Планы_вкл": True,
        "Фокусы_вкл": True,
        "Уровень_камеры": "auto",
        "POV": False,
        "Композиция": "auto",
        "Кроп": "auto",
        "Куда_смотрит_камера": "auto",
        "Зум": "none",
        "Окружение_выбирает_LLM": False,
        "Фон": "random",
        "Освещение": "random",
        "Время_суток": "auto",
        "Атмосфера": "auto",
        "Сеттинг": "auto",
        "Фоны_вкл": True,
        "Фоны_простые_вкл": True,
        "Фоны_студия_вкл": True,
        "Фоны_город_вкл": True,
        "Фоны_природа_вкл": True,
        "Фоны_вода_вкл": True,
        "Фоны_комнаты_вкл": True,
        "Фоны_фэнтези_вкл": True,
        "Свет_вкл": True,
        "Время_вкл": True,
        "Атмосфера_вкл": True,
        "Сеттинг_вкл": True,
        "Формат_промпта": "natural",
        "Модель": "universal",
        "Стиль": "photoreal",
        "Качество": "high",
        "Quality_tokens": True,
        "Всё_выбирает_LLM": False,
        "Свобода_LLM": "from_lists",
        "Запреты": "",
        "Явные_термины": True,
        "config": "",
        "char_1": "", "char_2": "", "char_3": "",
        "char_4": "", "char_5": "", "char_6": "",
    }


def run(**overrides):
    import sxs_node
    data = base()
    data.update(overrides)
    return sxs_node.SXS().build(**data)


print("== SXS python sandbox ==")

try:
    import sxs_data
    import sxs_compat
    import sxs_brief
    import sxs_phrases
    import sxs_node
except Exception as exc:  # pragma: no cover - red phase
    check("modules import", False, f"{type(exc).__name__}: {exc}")
    print(f"\nFAIL: {FAILS}")
    sys.exit(1)

check("modules import", True)

# ── schema ────────────────────────────────────────────────────────────────
schema = sxs_node.SXS.INPUT_TYPES()
req = schema.get("required", {})
opt = schema.get("optional", {})
check("schema: required dict", isinstance(req, dict) and len(req) > 60, str(len(req)))
check("schema: optional config", "config" in opt)
check("schema: optional char_1..6", all(f"char_{i}" in opt for i in range(1, 7)))
check("schema: seed", "seed" in req)
check("schema: menu/prompt language", "Язык_меню" in req and "Язык_промпта" in req)
check("schema: no negative widgets", not any("Негатив" in k or "negative" in k.lower() for k in list(req) + list(opt)))
check("schema: no age widgets", not any("Возраст" in k or "age" in k.lower() for k in list(req) + list(opt)))
check("schema: no length widget", not any("Длина" in k or "length" in k.lower() for k in list(req) + list(opt)))
check("schema: pose LLM default ON", req.get("Позы_выбирает_LLM", (None,))[1].get("default") is True)
check("schema: natural default", req.get("Формат_промпта", (None,))[1].get("default") == "natural")
check("schema: scene stage", "Этап_сцены" in req and req["Этап_сцены"][1].get("default") == "auto")
check("schema: finish target", "Куда_кончает" in req and req["Куда_кончает"][1].get("default") == "auto")

locales = {}
for lang in ("en", "ru"):
    path = ROOT / "locales" / lang / "nodeDefs.json"
    check(f"locales: {lang} exists", path.is_file(), str(path))
    if path.is_file():
        raw = path.read_bytes()
        check(f"locales: {lang} no BOM", not raw.startswith(b"\xef\xbb\xbf"))
        locales[lang] = json.loads(raw.decode("utf-8"))
if len(locales) == 2:
    en = locales["en"].get("SXS", {})
    ru = locales["ru"].get("SXS", {})
    schema_names = set(req) | set(opt)
    check("locales: node key", bool(en) and bool(ru))
    check("locales: input parity", set(en.get("inputs", {})) == set(ru.get("inputs", {})))
    check("locales: inputs cover schema", set(en.get("inputs", {})) == schema_names,
          str(schema_names ^ set(en.get("inputs", {}))))
    check("locales: output parity", set(en.get("outputs", {})) == set(ru.get("outputs", {})) == {"LLM PROMPT", "MODEL PROMPT", "WARN", "SEED", "CONFIG"})
    check("locales: en display name", en.get("display_name") == "SXS Scene Prompt", str(en.get("display_name")))
    check("locales: ru display name", ru.get("display_name") == "SXS: промпт сцены", str(ru.get("display_name")))
    check("locales: descriptions non-empty", bool(en.get("description")) and bool(ru.get("description")))

check("return types 5", sxs_node.SXS.RETURN_TYPES == ("STRING", "STRING", "STRING", "INT", "STRING"), str(sxs_node.SXS.RETURN_TYPES))
check("return names", sxs_node.SXS.RETURN_NAMES == ("LLM PROMPT", "MODEL PROMPT", "WARN", "SEED", "CONFIG"), str(sxs_node.SXS.RETURN_NAMES))
check("function", sxs_node.SXS.FUNCTION == "build")
check("category", sxs_node.SXS.CATEGORY == "My_custom_nodes/SXS")

# ── data ──────────────────────────────────────────────────────────────────
check("data: 24 types", len(sxs_data.TYPES) == 24, str(len(sxs_data.TYPES)))
check("data: every type has a rule", all(t in sxs_data.TYPE_RULES for t in sxs_data.TYPES))
check("data: every type in one group", sorted(sum(sxs_data.TYPE_GROUPS.values(), [])) == sorted(sxs_data.TYPES))
check("data: 8 pose groups", len(sxs_data.POSE_GROUPS) == 8, str(len(sxs_data.POSE_GROUPS)))
check("data: all pose groups non-empty", all(v for v in sxs_data.POSE_GROUPS.values()))
check("data: all types reachable", set(sxs_data.TYPES) == set(sxs_data.TYPE_RULES))
check("data: all matrix rules have min/max", all(
    {"minF", "minM", "minTotal"} <= set(r) for r in sxs_data.TYPE_RULES.values()
))
check("data: stage protocol", sxs_data.STAGE_VALUES == ["auto", "start", "insertion", "middle", "finish", "random"], str(sxs_data.STAGE_VALUES))
check("data: finish targets", "inside" in sxs_data.FINISH_TARGETS and "random" in sxs_data.FINISH_TARGETS)

# ── build basics ──────────────────────────────────────────────────────────
out = run()
check("build: 5 outputs", isinstance(out, tuple) and len(out) == 5, str(type(out)))
llm, model, warn, used_seed, cfg = out
check("build: deterministic types", isinstance(llm, str) and isinstance(model, str) and isinstance(warn, str) and isinstance(used_seed, int) and isinstance(cfg, str))
check("build: seed 0 -> int", used_seed >= 0)
check("build: config parses", isinstance(json.loads(cfg), dict))
check("build: LLM has sections", all(tag in llm for tag in ("[BRIEF]", "[ALLOWED]", "[RULES]")))
check("build: MODEL non-empty", len(model) > 40, str(len(model)))
check("build: no negative key in CONFIG", "negative" not in json.loads(cfg))
check("build: no negative output", "negative" not in model.lower() and "негатив" not in model.lower())

# ── determinism ───────────────────────────────────────────────────────────
a = run(seed=12345)
b = run(seed=12345)
c = run(seed=99999)
check("determinism: same seed same prompt", a[0] == b[0] and a[1] == b[1])
check("determinism: different seed differs", a[0] != c[0] or a[1] != c[1])

# ── config / seed ─────────────────────────────────────────────────────────
cfg_json = json.dumps({"master_seed": 777, "menu_lang": "ru", "age": 27, "gender_female": 1}, ensure_ascii=False)
out = run(seed=0, config=cfg_json)
check("config: master_seed inherited", out[3] == 777, str(out[3]))

# ── characters / gender ───────────────────────────────────────────────────
chars = {
    "char_1": "woman, 27 years old, red hair",
    "char_2": "man, 31 years old, beard",
    "char_3": "девушка, 24 года, блондинка",
}
out = run(**chars)
cfg = json.loads(out[4])
check("chars: three participants", len(cfg["characters"]) == 3, str(len(cfg["characters"])))
check("chars: gender inferred", [c["gender"] for c in cfg["characters"]] == ["female", "male", "female"], str([c["gender"] for c in cfg["characters"]]))
out = run(**chars, **{"Пол_1": "male"})
cfg = json.loads(out[4])
check("chars: explicit gender override", cfg["characters"][0]["gender"] == "male")

out = run(char_1="person, 30 years old")
cfg = json.loads(out[4])
check("chars: unknown gender warns", "пол" in out[2].lower() or "gender" in out[2].lower(), out[2])

out = run(**{**chars, "Девушки": "2", "Парни": "1"})
cfg = json.loads(out[4])
check("counts: explicit 2F+1M", cfg["counts"] == {"female": 2, "male": 1}, str(cfg["counts"]))
out = run(**{**chars, "Девушки": "3", "Парни": "3"})
cfg = json.loads(out[4])
check("counts: capped at 3+3", cfg["counts"] == {"female": 3, "male": 3}, str(cfg["counts"]))

# ── compatibility ─────────────────────────────────────────────────────────
out = run(char_1="woman", char_2="man", Тип="lesbian", Совместимость="strict")
cfg = json.loads(out[4])
check("compat: lesbian impossible with 1F+1M", cfg["type"] != "lesbian", cfg["type"])
check("compat: warns on conflict", bool(out[2].strip()))

out = run(char_1="woman", char_2="man", Тип="classic", Совместимость="strict")
cfg = json.loads(out[4])
check("compat: classic allowed", cfg["type"] == "classic", cfg["type"])

out = run(char_1="woman", char_2="man", char_3="man", Тип="gangbang", Совместимость="strict")
cfg = json.loads(out[4])
check("compat: gangbang needs 3M", cfg["type"] != "gangbang", cfg["type"])

out = run(char_1="woman", char_2="man", char_3="woman", char_4="man", Тип="orgy", Совместимость="strict")
cfg = json.loads(out[4])
check("compat: orgy 2F+2M allowed", cfg["type"] == "orgy", cfg["type"])

# ── delegation ────────────────────────────────────────────────────────────
out = run(Позы_выбирает_LLM=True)
brief = json.loads(out[0].split("[BRIEF]", 1)[1].split("[ALLOWED]", 1)[0])
check("delegation: pose is llm_choice", brief["pose"]["mode"] == "llm_choice", str(brief["pose"]))
check("delegation: pose allowed non-empty", len(brief["pose"]["allowed"]) > 0)
out = run(Позы_выбирает_LLM=False, Поза="standing")
brief = json.loads(out[0].split("[BRIEF]", 1)[1].split("[ALLOWED]", 1)[0])
check("delegation: pose concrete", brief["pose"] == "standing", str(brief["pose"]))

# ── scene stage / finish target ───────────────────────────────────────────
out = run(char_1="woman", char_2="man", Тип="classic", Этап_сцены="insertion")
check("stage: insertion prose", "first insertion" in out[1].lower(), out[1])
out = run(char_1="woman", char_2="man", Тип="classic", Этап_сцены="finish", Куда_кончает="inside")
check("stage: finish inside prose", "ejaculating inside" in out[1].lower(), out[1])
out = run(char_1="woman", char_2="man", Тип="classic", Этап_сцены="finish", Куда_кончает="face", Язык_промпта="ru")
check("stage: ru finish face prose", "кончая налицо" in out[1].replace(" ", "") or "кончая на лицо" in out[1], out[1])

out = run(char_1="woman", char_2="man", Тип="oral", Этап_сцены="random")
cfg = json.loads(out[4])
check("stage: random respects oral filter", cfg.get("stage") in ("start", "middle", "finish"), str(cfg.get("stage")))
a_stage = run(char_1="woman", char_2="man", Тип="oral", Этап_сцены="random", seed=777)[4]
b_stage = run(char_1="woman", char_2="man", Тип="oral", Этап_сцены="random", seed=777)[4]
check("stage: random deterministic", a_stage == b_stage)

out = run(char_1="woman", char_2="man", Тип="oral", Этап_сцены="insertion")
cfg = json.loads(out[4])
check("stage: impossible insertion filtered", cfg.get("stage") != "insertion", str(cfg.get("stage")))
check("stage: impossible insertion warns", "insertion" in out[2].lower() or "этап" in out[2].lower(), out[2])

out = run(char_1="woman", char_2="man", Тип="oral", Этап_сцены="finish", Куда_кончает="inside")
cfg = json.loads(out[4])
check("finish: inside filtered for oral", cfg.get("finish_target") != "inside", str(cfg.get("finish_target")))
check("finish: inside warning", "inside" in out[2].lower() or "куда" in out[2].lower(), out[2])

out = run(char_1="woman", Парни="0", Тип="solo_f", Этап_сцены="finish", Куда_кончает="inside")
cfg = json.loads(out[4])
check("finish: no male -> none", cfg.get("finish_target") == "none", str(cfg.get("finish_target")))
check("finish: no male warns", "inside" in out[2].lower() or "куда" in out[2].lower(), out[2])

out = run(Всё_выбирает_LLM=True)
brief = json.loads(out[0].split("[BRIEF]", 1)[1].split("[ALLOWED]", 1)[0])
check("delegation: master sets type", brief["type"]["mode"] == "llm_choice")
check("delegation: master sets pose", brief["pose"]["mode"] == "llm_choice")
check("delegation: master sets camera", brief["camera"]["angle"]["mode"] == "llm_choice")
check("delegation: master sets environment", brief["environment"]["background"]["mode"] == "llm_choice")

# ── presets ───────────────────────────────────────────────────────────────
out = run(Пресет_сцены="romance")
cfg = json.loads(out[4])
check("preset: romance type", cfg["type"] == "classic", cfg["type"])
check("preset: romance emotion", cfg["emotion"] == "tender", cfg["emotion"])
check("preset: romance tempo", cfg["tempo"] == "slow", cfg["tempo"])

out = run(Пресет_сцены="pov")
cfg = json.loads(out[4])
check("preset: pov type", cfg["type"] == "pov", cfg["type"])
check("preset: pov camera", cfg["camera"]["position"] == "pov", str(cfg["camera"]["position"]))

# ── formats / language ────────────────────────────────────────────────────
out = run(Формат_промпта="tags")
check("format: tags has commas", "," in out[1])
out = run(Формат_промпта="natural")
check("format: natural has sentence", "." in out[1])
out = run(Формат_промпта="hybrid")
check("format: hybrid has both", "." in out[1] and "," in out[1])

out = run(Язык_промпта="ru")
check("language: ru model prompt has Cyrillic", bool(re.search(r"[\u0400-\u04FF]", out[1])))
out = run(Язык_промпта="en")
check("language: en model prompt has no Cyrillic", not re.search(r"[\u0400-\u04FF]", out[1]))

# ── pairs / focus ─────────────────────────────────────────────────────────
out = run(char_1="woman", char_2="man", char_3="woman", char_4="man", Авто_пары=True)
cfg = json.loads(out[4])
check("pairs: auto pairs present", isinstance(cfg.get("pairs"), list) and len(cfg["pairs"]) >= 1, str(cfg.get("pairs")))
out = run(char_1="woman", char_2="man", **{"Кто_с_кем": '{"pairs": [["1","2"]]}'})
cfg = json.loads(out[4])
check("pairs: manual json", cfg.get("pairs") == [["1", "2"]], str(cfg.get("pairs")))
out = run(char_1="woman", char_2="man", Фокус_на="2")
cfg = json.loads(out[4])
check("focus: index honoured", cfg.get("focus") == 2, str(cfg.get("focus")))

# ── warnings ──────────────────────────────────────────────────────────────
out = run(char_1="woman", char_2="man", Пресет_сцены="romance")
check("warn: valid run is quiet", out[2] == "", out[2])

print(f"\nDEBUG: CHECK_COUNT={CHECK_COUNT} FAILS={FAILS} OKS={OKS}")
with open("check_debug.txt", "a", encoding="utf-8") as f:
    f.write("FAILED_CHECKS={}\n".format(FAILED_CHECKS))
print(f"DEBUG: FAILED_CHECKS={FAILED_CHECKS}")
print(f"\nFAIL: {FAILS}")
if FAILS:
    sys.exit(1)
print("ТЕСТ ПРОЙДЕН")
