# -*- coding: utf-8 -*-
"""SXS: scene brief -> LLM prompt / model prompt.

The node never generates text itself.  It resolves a deterministic scene
brief from widgets (and optional KonstCharacter inputs), then renders
[SYSTEM]/[BRIEF]/[ALLOWED]/[RULES] for an external LLM and a ready-to-use
MODEL PROMPT for the image/video model.
"""
from __future__ import annotations

import hashlib
import json

try:
    from . import sxs_brief, sxs_compat, sxs_data
except ImportError:  # pragma: no cover
    import sxs_brief
    import sxs_compat
    import sxs_data


def _combo(values, default):
    return (list(values), {"default": default})


def _bool(default):
    return ("BOOLEAN", {"default": default})


_TYPE_DEFAULT = {
    "basic": True,
    "same_sex": True,
    "group": True,
    "solo": True,
    "pov": True,
    "bdsm": False,
    "toys": False,
    "extreme": False,
}


class SXS:
    CATEGORY = "My_custom_nodes/SXS"
    FUNCTION = "build"
    RETURN_TYPES = ("STRING", "STRING", "STRING", "INT", "STRING")
    RETURN_NAMES = ("LLM PROMPT", "MODEL PROMPT", "WARN", "SEED", "CONFIG")
    DESCRIPTION = (
        "Builds an adult scene brief from KonstCharacter descriptions and "
        "renders an LLM prompt plus a ready-to-use model prompt."
    )

    @classmethod
    def INPUT_TYPES(cls):
        required = {
            "seed": ("INT", {
                "default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF,
                "control_after_generate": "randomize",
            }),
            "Язык_меню": _combo(["auto", "ru", "en"], "auto"),
            "Язык_промпта": _combo(["en", "ru"], "en"),
            "Управление": _combo(sxs_data.CONTROLS, "hybrid"),

            "Девушки": _combo(["auto", "0", "1", "2", "3", "random"], "auto"),
            "Парни": _combo(["auto", "0", "1", "2", "3", "random"], "auto"),
            "Распределение": _combo(sxs_data.DISTRIBUTIONS, "by_connection"),
            "Авто_пары": _bool(True),
            "Кто_с_кем": ("STRING", {"default": "", "multiline": True}),
            "Фокус_на": _combo(["auto", "1", "2", "3", "4", "5", "6"], "auto"),
            "Политика_отсутствующего": _combo(sxs_data.MISSING_POLICIES, "partial"),
        }
        for i in range(1, 7):
            required[f"Пол_{i}"] = _combo(["auto", "female", "male"], "auto")

        required.update({
            "Пресет_сцены": _combo(
                ["none", "romance", "passion", "pov", "group", "bdsm", "solo"], "none"
            ),
            "Тип": _combo(["random"] + sxs_data.TYPES, "random"),
            "Тип_выбирает_LLM": _bool(False),
            "Этап_сцены": _combo(sxs_data.STAGE_VALUES, "auto"),
            "Куда_кончает": _combo(sxs_data.FINISH_TARGETS, "auto"),
        })
        for group in sxs_data.TYPE_GROUPS:
            required[f"Тип_группа_{group}"] = _bool(_TYPE_DEFAULT.get(group, False))

        required.update({
            "Совместимость": _combo(["strict", "soft"], "strict"),
            "Взаимодействия": ("STRING", {"default": "", "multiline": True}),
            "Эмоции": _combo(["auto"] + [x for x in sxs_data.EMOTIONS if x != "auto"], "auto"),
            "Темп": _combo(["auto"] + [x for x in sxs_data.TEMPOS if x != "auto"], "auto"),
            "Одежда": _combo(["auto"] + [x for x in sxs_data.CLOTHING if x != "auto"], "auto"),
        })

        required["Позы_выбирает_LLM"] = _bool(True)
        for group in sxs_data.POSE_GROUPS:
            required[f"Позы_группа_{group}"] = _bool(True)
        required.update({
            "Поза": _combo(sxs_data.POSE_DISPLAY, "random"),
            "Взгляд": _combo(["auto"] + [x for x in sxs_data.GAZES if x != "auto"], "auto"),
            "Кто_сверху": _combo(sxs_data.WHO_TOP, "auto"),
            "Положение_камеры": _combo(["auto"] + sxs_data.CAMERA_POSITIONS, "auto"),
        })

        required.update({
            "Камера_выбирает_LLM": _bool(False),
            "Ракурс": _combo(["random"] + sxs_data.ANGLES, "random"),
            "План": _combo(["random"] + sxs_data.SHOTS, "random"),
            "Фокус": _combo(["random"] + sxs_data.FOCUS, "random"),
            "Ракурсы_вкл": _bool(True),
            "Планы_вкл": _bool(True),
            "Фокусы_вкл": _bool(True),
            "Уровень_камеры": _combo(["auto"] + sxs_data.CAMERA_LEVELS, "auto"),
            "POV": _bool(False),
            "Композиция": _combo(["auto"] + sxs_data.COMPOSITIONS, "auto"),
            "Кроп": _combo(["auto"] + sxs_data.CROPS, "auto"),
            "Куда_смотрит_камера": _combo(["auto"] + sxs_data.CAMERA_TARGETS, "auto"),
            "Зум": _combo(sxs_data.ZOOMS, "none"),
        })

        required.update({
            "Окружение_выбирает_LLM": _bool(False),
            "Фон": _combo(["random"] + sxs_data.BACKGROUNDS, "random"),
            "Освещение": _combo(["random"] + sxs_data.LIGHTING, "random"),
            "Время_суток": _combo(["auto"] + [x for x in sxs_data.TIMES if x != "auto"], "auto"),
            "Атмосфера": _combo(["auto"] + [x for x in sxs_data.ATMOSPHERES if x != "auto"], "auto"),
            "Сеттинг": _combo(["auto"] + [x for x in sxs_data.SETTINGS if x != "auto"], "auto"),
            "Фоны_вкл": _bool(True),
            "Фоны_простые_вкл": _bool(True),
            "Фоны_студия_вкл": _bool(True),
            "Фоны_город_вкл": _bool(True),
            "Фоны_природа_вкл": _bool(True),
            "Фоны_вода_вкл": _bool(True),
            "Фоны_комнаты_вкл": _bool(True),
            "Фоны_фэнтези_вкл": _bool(True),
            "Свет_вкл": _bool(True),
            "Время_вкл": _bool(True),
            "Атмосфера_вкл": _bool(True),
            "Сеттинг_вкл": _bool(True),
        })

        required.update({
            "Формат_промпта": _combo(sxs_data.FORMATS, "natural"),
            "Модель": _combo(sxs_data.MODELS, "universal"),
            "Стиль": _combo(sxs_data.STYLES, "photoreal"),
            "Качество": _combo(sxs_data.QUALITIES, "high"),
            "Quality_tokens": _bool(True),
            "Всё_выбирает_LLM": _bool(False),
            "Свобода_LLM": _combo(sxs_data.FREEDOMS, "from_lists"),
            "Запреты": ("STRING", {"default": "", "multiline": True}),
            "Явные_термины": _bool(True),
        })

        optional = {
            "config": ("STRING", {"default": "", "forceInput": True, "multiline": True}),
        }
        for i in range(1, 7):
            optional[f"char_{i}"] = ("STRING", {"default": "", "forceInput": True, "multiline": True})

        return {"required": required, "optional": optional}

    def build(self, **kwargs):
        config = sxs_compat.parse_config(kwargs.get("config", ""))
        return sxs_brief.build_outputs(kwargs, config)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        payload = json.dumps(kwargs, sort_keys=True, default=str, ensure_ascii=False)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()
