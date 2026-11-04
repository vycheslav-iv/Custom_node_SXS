# -*- coding: utf-8 -*-
"""SXS protocol data.

Every value here is an ENGLISH protocol token. Translations live in
sxs_phrases.py (prompt prose) and web/js/sxs.js (widget labels).  Never
translate a token: Python compares and stores tokens.
"""
from __future__ import annotations

TYPES = [
    "classic", "oral", "anal", "lesbian", "gay", "group", "orgy",
    "solo_f", "solo_m", "pov", "bdsm", "toys", "fingering", "fisting",
    "creampie", "bukkake", "edging", "facesitting", "strapon",
    "double_penetration", "threesome", "gangbang", "public", "roleplay",
]

TYPE_GROUPS = {
    "basic": ["classic", "oral", "anal", "fingering"],
    "same_sex": ["lesbian", "gay"],
    "group": ["group", "orgy", "threesome", "gangbang"],
    "solo": ["solo_f", "solo_m"],
    "pov": ["pov"],
    "bdsm": ["bdsm", "edging"],
    "toys": ["toys", "strapon", "double_penetration"],
    "extreme": ["fisting", "creampie", "bukkake", "facesitting", "public", "roleplay"],
}

# minF, minM, minTotal, requires (toy/strapon/dp)
TYPE_RULES = {
    "classic": {"minF": 1, "minM": 1, "minTotal": 2, "requires": ()},
    "oral": {"minF": 1, "minM": 1, "minTotal": 2, "requires": ()},
    "anal": {"minF": 1, "minM": 1, "minTotal": 2, "requires": ()},
    "lesbian": {"minF": 2, "minM": 0, "minTotal": 2, "requires": ()},
    "gay": {"minF": 0, "minM": 2, "minTotal": 2, "requires": ()},
    "group": {"minF": 1, "minM": 1, "minTotal": 3, "requires": ()},
    "orgy": {"minF": 2, "minM": 2, "minTotal": 4, "requires": ()},
    "solo_f": {"minF": 1, "minM": 0, "minTotal": 1, "requires": ()},
    "solo_m": {"minF": 0, "minM": 1, "minTotal": 1, "requires": ()},
    "pov": {"minF": 1, "minM": 1, "minTotal": 2, "requires": ()},
    "bdsm": {"minF": 1, "minM": 1, "minTotal": 2, "requires": ()},
    "toys": {"minF": 1, "minM": 0, "minTotal": 1, "requires": ("toy",)},
    "fingering": {"minF": 1, "minM": 1, "minTotal": 2, "requires": ()},
    "fisting": {"minF": 1, "minM": 1, "minTotal": 2, "requires": ()},
    "creampie": {"minF": 1, "minM": 1, "minTotal": 2, "requires": ()},
    "bukkake": {"minF": 1, "minM": 2, "minTotal": 3, "requires": ()},
    "edging": {"minF": 1, "minM": 1, "minTotal": 2, "requires": ()},
    "facesitting": {"minF": 1, "minM": 1, "minTotal": 2, "requires": ()},
    "strapon": {"minF": 2, "minM": 0, "minTotal": 2, "requires": ("strapon",)},
    "double_penetration": {"minF": 1, "minM": 2, "minTotal": 3, "requires": ("dp",)},
    "threesome": {"minF": 1, "minM": 2, "minTotal": 3, "requires": ()},
    "gangbang": {"minF": 1, "minM": 3, "minTotal": 4, "requires": ()},
    "public": {"minF": 1, "minM": 1, "minTotal": 2, "requires": ()},
    "roleplay": {"minF": 1, "minM": 1, "minTotal": 2, "requires": ()},
}

# Preset overrides. Explicit widgets win; a preset fills only untouched
# (auto/random/none) fields.
PRESETS = {
    "romance": {
        "Тип": "classic", "Эмоции": "tender", "Темп": "slow",
        "Одежда": "partially", "Освещение": "soft", "Фон": "bedroom",
        "Атмосфера": "candles", "План": "medium",
        "Взаимодействия": "kiss, caress",
    },
    "passion": {
        "Тип": "classic", "Эмоции": "passionate", "Темп": "intense",
        "Одежда": "partially", "Освещение": "dramatic", "Фон": "bedroom",
        "Взаимодействия": "kiss, caress, penetration",
    },
    "pov": {
        "Тип": "pov", "Положение_камеры": "pov", "POV": True,
        "План": "pov_shot", "Композиция": "focus",
    },
    "group": {
        "Тип": "group", "Эмоции": "playful", "Темп": "rhythmic",
        "Композиция": "all", "План": "group_shot",
    },
    "bdsm": {
        "Тип": "bdsm", "Эмоции": "dominant", "Темп": "intense",
        "Одежда": "partially", "Освещение": "dramatic", "Фон": "dungeon",
        "Тип_группа_bdsm": True, "Тип_группа_toys": True,
    },
    "solo": {
        "Тип": "solo_f", "Композиция": "focus", "План": "medium",
        "Эмоции": "seductive",
    },
}

POSE_GROUPS = {
    "stand": [
        "standing", "standing_side", "standing_one_leg", "lunge",
        "leaning_wall",
    ],
    "sit": [
        "sitting", "sitting_chair", "sitting_floor", "sitting_cross_legged",
        "sitting_leg_over_leg", "sitting_knees_chest", "on_knees", "squatting",
    ],
    "lying": [
        "lying_back", "lying_stomach", "lying_side", "reclining",
        "on_all_fours",
    ],
    "dynamic": [
        "dancing", "arching_back", "straddling", "grinding", "riding",
        "thrusting", "lifting_partner", "pinned",
    ],
    "mood": [
        "seductive", "passionate", "tender", "playful", "dominant",
        "submissive", "shy", "confident",
    ],
    "modeling": [
        "hands_on_hips", "hands_behind_head", "arms_crossed", "hands_up",
        "arched_back", "turned_around", "posing",
    ],
    "gesture": [
        "air_kiss", "winking", "finger_to_lips", "heart_fingers", "beckoning",
        "covering_mouth", "biting_lip",
    ],
    "sexual": [
        "legs_spread", "legs_wide", "butt_to_viewer", "caressing_breast",
        "caressing_self", "exposing_chest", "fingers_in_mouth",
        "head_thrown_back", "licking_lips", "mouth_open",
    ],
}

POSES = [token for group in POSE_GROUPS.values() for token in group]

ANGLES = [
    "front", "three_quarter_front", "three_quarter_left",
    "three_quarter_right", "side", "profile_left", "profile_right", "back",
    "three_quarter_back", "top", "high_angle", "eye_level", "low_angle",
    "ground_level", "dutch", "over_shoulder",
]

SHOTS = [
    "full_body", "wide", "medium", "waist", "chest", "close_up",
    "extreme_close_up", "macro", "two_shot", "group_shot", "pov_shot",
    "from_behind",
]

FOCUS = [
    "whole_body", "face", "eyes", "lips", "chest", "hips", "butt", "crotch",
    "legs", "hands", "back", "neck",
]

CAMERA_LEVELS = ["eye_level", "high", "low", "ground"]
COMPOSITIONS = ["pair", "all", "focus"]
CROPS = ["face", "body", "details"]
CAMERA_TARGETS = ["face", "body", "action", "scene"]
ZOOMS = ["none", "closer", "farther", "macro"]
CAMERA_POSITIONS = ["front", "behind", "side", "top", "bottom", "pov"]
WHO_TOP = ["auto", "female", "male", "random"]
STAGE_VALUES = ["auto", "start", "insertion", "middle", "finish", "random"]
FINISH_TARGETS = [
    "auto", "none", "inside", "mouth", "face", "breast", "body", "back",
    "outside", "random",
]
NON_INSERTION_TYPES = {
    "oral", "fingering", "facesitting", "bukkake", "solo_f", "solo_m",
}
GAZES = ["auto", "camera", "partner", "down", "away", "closed"]

# Background groups for realistic environments
BG_SIMPLE = [
    "studio", "cyclorama", "white_cyclorama", "black_studio", "loft_studio",
    "minimal_studio", "neon_studio", "vintage_studio", "textured_wall",
]

BG_STUDIO = [
    "photo_studio", "interior_studio", "natural_light_studio", "softbox_studio",
    "studio_with_props", "studio_with_drapes", "studio_with_mirrors",
    "studio_with_columns", "studio_with_flowers",
]

BG_CITY = [
    "city", "night_city", "rainy_city", "street", "alley", "square",
    "industrial_zone", "skyscraper_roof", "embankment", "club", "cafe",
    "restaurant", "subway", "station", "airport", "balcony_city_view",
    "backyard", "garage",
]

BG_NATURE = [
    "forest", "mountains", "field", "garden", "desert", "snow_landscape",
    "flower_meadow", "autumn_park", "rocky_shore", "foggy_forest",
    "savanna", "bamboo_grove", "steppe", "canyon", "cave", "volcano",
    "glacier", "lavender_field", "vineyard", "jungle", "japanese_garden",
    "heather_moor",
]

BG_WATER = [
    "tropical_island", "beach", "sea", "ocean", "lake", "mountain_lake",
    "river", "waterfall", "pool", "fountain", "pond", "swamp",
    "seabed", "coral_reef",
]

BG_ROOM = [
    "bedroom", "bathroom", "living_room", "kitchen", "library", "grand_hall",
    "balcony", "terrace", "mansion", "loft", "country_house", "office",
    "workshop", "wardrobe", "winter_garden", "greenhouse", "corridor",
    "staircase", "veranda", "theater", "museum", "gallery", "throne_hall",
    "boudoir", "hotel_room",
]

BG_FANTASY = [
    "sunset", "sunrise", "golden_hour", "fog", "blizzard", "stormy_sky",
    "night_sky", "starry_night", "moonlit_night", "aurora", "rainbow",
    "castle", "temple", "ruins", "space", "fantasy_world", "magic_forest",
    "ancient_fortress", "misty_mountains", "underground_grotto", "mystic_portal",
    "fairy_palace", "crystal_cave", "floating_island", "cursed_graveyard",
    "astral", "underwater_kingdom", "romantic_world",
]

# Combined list for backward compatibility (all groups)
BACKGROUNDS = (
    BG_SIMPLE + BG_STUDIO + BG_CITY + BG_NATURE + BG_WATER + BG_ROOM + BG_FANTASY
)

LIGHTING = [
    "natural", "studio", "soft", "hard", "dramatic", "backlight",
    "golden_hour", "blue_hour", "neon", "candles", "flash", "cinematic",
]

TIMES = ["auto", "day", "morning", "evening", "night", "sunset", "sunrise"]
ATMOSPHERES = ["auto", "none", "candles", "rain", "steam", "smoke", "dust", "firelight"]
SETTINGS = ["auto", "modern", "fantasy", "historical"]
STYLES = ["photoreal", "cinematic", "amateur", "retro", "webcam", "anime", "illustration"]
QUALITIES = ["high", "medium", "none"]
EMOTIONS = ["auto", "tender", "passionate", "dominant", "submissive", "playful", "mix", "seductive"]
TEMPOS = ["auto", "static", "rhythmic", "intense", "slow"]
CLOTHING = ["auto", "dressed", "partially", "lingerie", "nude", "torn"]
INTERACTIONS = [
    "kiss", "caress", "oral", "penetration", "eye_contact", "undress",
    "spanking", "choking", "hair_pull", "dirty_talk",
]
FORMATS = ["natural", "tags", "hybrid"]
MODELS = ["universal", "sdxl", "pony", "illustrious", "flux", "wan"]
CONTROLS = ["hybrid", "manual", "all_random"]
DISTRIBUTIONS = ["by_connection", "by_description", "manual"]
MISSING_POLICIES = ["pov", "partial", "invent"]
FREEDOMS = ["strict", "from_lists", "free"]

# Scene type -> a short label used inside the prompt prose.
TYPE_PROMPT = {
    "classic": "classic sex",
    "oral": "oral sex",
    "anal": "anal sex",
    "lesbian": "lesbian sex",
    "gay": "gay sex",
    "group": "group sex",
    "orgy": "an orgy",
    "solo_f": "female solo",
    "solo_m": "male solo",
    "pov": "POV sex",
    "bdsm": "BDSM play",
    "toys": "sex with toys",
    "fingering": "fingering",
    "fisting": "fisting",
    "creampie": "creampie",
    "bukkake": "bukkake",
    "edging": "edging",
    "facesitting": "facesitting",
    "strapon": "strapon sex",
    "double_penetration": "double penetration",
    "threesome": "threesome",
    "gangbang": "gangbang",
    "public": "public sex",
    "roleplay": "sexual roleplay",
}
