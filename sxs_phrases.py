# -*- coding: utf-8 -*-
"""Russian/English prose for SXS.

This is the only Python module allowed to contain Cyrillic.  Protocol tokens
stay in sxs_data.py; this file turns them into human phrases and holds the
[SYSTEM]/[RULES] templates used by the prompt builder.
"""
from __future__ import annotations

PHRASES = {
    "en": {
        "type": {
            "classic": "classic sex", "oral": "oral sex", "anal": "anal sex",
            "lesbian": "lesbian sex", "gay": "gay sex", "group": "group sex",
            "orgy": "an orgy", "solo_f": "female solo", "solo_m": "male solo",
            "pov": "POV sex", "bdsm": "BDSM play", "toys": "sex with toys",
            "fingering": "fingering", "fisting": "fisting", "creampie": "creampie",
            "bukkake": "bukkake", "edging": "edging", "facesitting": "facesitting",
            "strapon": "strapon sex", "double_penetration": "double penetration",
            "threesome": "a threesome", "gangbang": "a gangbang",
            "public": "public sex", "roleplay": "sexual roleplay",
        },
        "stage": {
            "auto": "", "start": "at the very beginning of the scene, before penetration",
            "insertion": "at the moment of first insertion",
            "middle": "in the middle of the scene",
            "finish": "at the climax, already ejaculating",
        },
        "finish_target": {
            "none": "at the climax",
            "inside": "at the climax, ejaculating inside",
            "mouth": "at the climax, ejaculating in the mouth",
            "face": "at the climax, ejaculating on the face",
            "breast": "at the climax, ejaculating on the breasts",
            "body": "at the climax, ejaculating on the body",
            "back": "at the climax, ejaculating on the back",
            "outside": "at the climax, ejaculating outside",
        },
        "pose": {
            "standing": "standing", "standing_side": "standing sideways",
            "standing_one_leg": "standing on one leg", "lunge": "in a lunge",
            "leaning_wall": "leaning against a wall", "sitting": "sitting",
            "sitting_chair": "sitting on a chair", "sitting_floor": "sitting on the floor",
            "sitting_cross_legged": "sitting cross-legged",
            "sitting_leg_over_leg": "sitting with legs crossed",
            "sitting_knees_chest": "sitting with knees to the chest",
            "on_knees": "on the knees", "squatting": "squatting",
            "lying_back": "lying on the back", "lying_stomach": "lying on the stomach",
            "lying_side": "lying on the side", "reclining": "reclining",
            "on_all_fours": "on all fours", "dancing": "dancing",
            "arching_back": "arching the back", "straddling": "straddling a partner",
            "grinding": "grinding", "riding": "riding", "thrusting": "thrusting",
            "lifting_partner": "lifting a partner", "pinned": "pinned down",
            "seductive": "in a seductive pose", "passionate": "in a passionate pose",
            "tender": "in a tender pose", "playful": "in a playful pose",
            "dominant": "in a dominant pose", "submissive": "in a submissive pose",
            "shy": "in a shy pose", "confident": "in a confident pose",
            "hands_on_hips": "hands on the hips", "hands_behind_head": "hands behind the head",
            "arms_crossed": "arms crossed", "hands_up": "hands up",
            "turned_around": "turned around", "posing": "posing",
            "air_kiss": "blowing a kiss", "winking": "winking",
            "finger_to_lips": "finger to the lips", "heart_fingers": "heart fingers",
            "beckoning": "beckoning", "covering_mouth": "covering the mouth",
            "biting_lip": "biting the lip", "legs_spread": "legs spread",
            "legs_wide": "legs wide apart", "butt_to_viewer": "butt toward the viewer",
            "caressing_breast": "caressing the breast", "caressing_self": "caressing herself",
            "exposing_chest": "exposing the chest", "fingers_in_mouth": "fingers in the mouth",
            "head_thrown_back": "head thrown back", "licking_lips": "licking the lips",
            "mouth_open": "mouth open",
        },
        "angle": {
            "front": "front view", "three_quarter_front": "three-quarter front view",
            "three_quarter_left": "three-quarter left view",
            "three_quarter_right": "three-quarter right view", "side": "side view",
            "profile_left": "left profile", "profile_right": "right profile",
            "back": "back view", "three_quarter_back": "three-quarter back view",
            "top": "top view", "high_angle": "high angle", "eye_level": "eye level",
            "low_angle": "low angle", "ground_level": "ground level",
            "dutch": "dutch angle", "over_shoulder": "over-the-shoulder view",
        },
        "shot": {
            "full_body": "full body shot", "wide": "wide shot", "medium": "medium shot",
            "waist": "waist-up shot", "chest": "chest-up shot", "close_up": "close-up",
            "extreme_close_up": "extreme close-up", "macro": "macro shot",
            "two_shot": "two-shot", "group_shot": "group shot", "pov_shot": "POV shot",
            "from_behind": "shot from behind",
        },
        "focus": {
            "whole_body": "whole body in focus", "face": "face in focus",
            "eyes": "eyes in focus", "lips": "lips in focus", "chest": "chest in focus",
            "hips": "hips in focus", "butt": "butt in focus", "crotch": "crotch in focus",
            "legs": "legs in focus", "hands": "hands in focus", "back": "back in focus",
            "neck": "neck in focus",
        },
        "camera_level": {
            "eye_level": "eye level", "high": "high camera", "low": "low camera",
            "ground": "ground-level camera",
        },
        "composition": {
            "pair": "pair composition", "all": "all participants in frame",
            "focus": "focused composition",
        },
        "crop": {"face": "face crop", "body": "body crop", "details": "detail crop"},
        "camera_target": {
            "face": "camera aimed at the face", "body": "camera aimed at the body",
            "action": "camera aimed at the action", "scene": "camera aimed at the scene",
        },
        "zoom": {"none": "", "closer": "zoom in", "farther": "zoom out", "macro": "extreme close-up, macro, 10-20cm distance"},
        "camera_position": {
            "front": "camera in front", "behind": "camera behind",
            "side": "camera at the side", "top": "camera above",
            "bottom": "camera below", "pov": "POV camera",
        },
        "who_top": {
            "auto": "", "female": "woman on top", "male": "man on top",
            "random": "random top",
        },
        "gaze": {
            "auto": "", "camera": "looking at the camera", "partner": "looking at the partner",
            "down": "looking down", "away": "looking away", "closed": "eyes closed",
        },
        "background": {
            "plain": "a plain background", "white": "a white background",
            "black": "a black background", "gray": "a gray background",
            "gradient": "a gradient background", "studio": "a studio",
            "bedroom": "a bedroom", "hotel": "a hotel room", "living_room": "a living room",
            "bathroom": "a bathroom", "kitchen": "a kitchen", "office": "an office",
            "city": "a city", "street": "a street", "nature": "nature",
            "forest": "a forest", "beach": "a beach", "water": "water",
            "pool": "a pool", "fantasy": "a fantasy setting", "dungeon": "a dungeon",
        },
        "lighting": {
            "natural": "natural light", "studio": "studio light", "soft": "soft light",
            "hard": "hard light", "dramatic": "dramatic light", "backlight": "backlight",
            "golden_hour": "golden hour light", "blue_hour": "blue hour light",
            "neon": "neon light", "candles": "candlelight", "flash": "flash light",
            "cinematic": "cinematic lighting",
        },
        "time": {
            "auto": "", "day": "daytime", "morning": "morning", "evening": "evening",
            "night": "night", "sunset": "sunset", "sunrise": "sunrise",
        },
        "atmosphere": {
            "auto": "", "none": "", "candles": "candles", "rain": "rain",
            "steam": "steam", "smoke": "smoke", "dust": "dust", "firelight": "firelight",
        },
        "setting": {
            "auto": "", "modern": "modern setting", "fantasy": "fantasy setting",
            "historical": "historical setting",
        },
        "interaction": {
            "kiss": "kissing", "caress": "caressing", "oral": "performing oral sex",
            "penetration": "penetration", "eye_contact": "eye contact", "undress": "undressing",
            "spanking": "spanking", "choking": "light choking", "hair_pull": "hair pulling",
            "dirty_talk": "dirty talk",
        },
        "style": {
            "photoreal": "photorealistic", "cinematic": "cinematic",
            "amateur": "amateur photo", "retro": "retro", "webcam": "webcam",
            "anime": "anime", "illustration": "illustration",
        },
        "quality": {"high": "high quality", "medium": "medium quality", "none": ""},
        "model": {
            "universal": "universal model", "sdxl": "SDXL", "pony": "Pony",
            "illustrious": "Illustrious", "flux": "Flux", "wan": "WAN",
        },
        "format": {
            "natural": "natural language", "tags": "comma-separated tags",
            "hybrid": "natural language plus tags",
        },
        "freedom": {
            "strict": "strictly from the allowed lists",
            "from_lists": "from the allowed lists, combining them freely",
            "free": "free wording inside the scene",
        },
        "missing": {
            "pov": "the missing partner is the POV camera",
            "partial": "only the connected characters are present",
            "invent": "invent the missing partner to satisfy the scene",
        },
        "control": {
            "hybrid": "explicit widgets win, the rest is random",
            "manual": "use only explicit widget values",
            "all_random": "ignore counts and randomize the cast",
        },
        "distribution": {
            "by_connection": "counts from connected characters",
            "by_description": "counts from the descriptions",
            "manual": "counts from the roles JSON",
        },
    },
    "ru": {
        "type": {
            "classic": "классический секс", "oral": "оральный секс",
            "anal": "анальный секс", "lesbian": "лесбийский секс",
            "gay": "гей-секс", "group": "групповой секс", "orgy": "оргия",
            "solo_f": "женское соло", "solo_m": "мужское соло", "pov": "POV-секс",
            "bdsm": "BDSM-игра", "toys": "секс с игрушками",
            "fingering": "стимуляция пальцами", "fisting": "фистинг",
            "creampie": "кримпай", "bukkake": "буккаке", "edging": "эджинг",
            "facesitting": "facesitting", "strapon": "секс со страпоном",
            "double_penetration": "двойное проникновение",
            "threesome": "секс втроём", "gangbang": "гангбэнг",
            "public": "секс в публичном месте", "roleplay": "сексуальная ролевая игра",
        },
        "stage": {
            "auto": "", "start": "в самом начале сцены, до проникновения",
            "insertion": "в момент первого проникновения",
            "middle": "в середине сцены",
            "finish": "на пике, уже кончая",
        },
        "finish_target": {
            "none": "на пике",
            "inside": "на пике, кончая внутрь",
            "mouth": "на пике, кончая в рот",
            "face": "на пике, кончая на лицо",
            "breast": "на пике, кончая на грудь",
            "body": "на пике, кончая на тело",
            "back": "на пике, кончая на спину",
            "outside": "на пике, кончая наружу",
        },
        "pose": {
            "standing": "стоя", "standing_side": "стоя боком",
            "standing_one_leg": "стоя на одной ноге", "lunge": "в выпаде",
            "leaning_wall": "опираясь на стену", "sitting": "сидя",
            "sitting_chair": "сидя на стуле", "sitting_floor": "сидя на полу",
            "sitting_cross_legged": "сидя по-турецки",
            "sitting_leg_over_leg": "сидя нога на ногу",
            "sitting_knees_chest": "сидя, колени к груди",
            "on_knees": "на коленях", "squatting": "на корточках",
            "lying_back": "лёжа на спине", "lying_stomach": "лёжа на животе",
            "lying_side": "лёжа на боку", "reclining": "полулёжа",
            "on_all_fours": "на четвереньках", "dancing": "танцуя",
            "arching_back": "прогибаясь в спине", "straddling": "верхом на партнёре",
            "grinding": "притираясь", "riding": "верхом", "thrusting": "толкаясь",
            "lifting_partner": "поднимая партнёра", "pinned": "прижатая",
            "seductive": "в соблазнительной позе", "passionate": "в страстной позе",
            "tender": "в нежной позе", "playful": "в игривой позе",
            "dominant": "в доминирующей позе", "submissive": "в подчинённой позе",
            "shy": "в застенчивой позе", "confident": "в уверенной позе",
            "hands_on_hips": "руки на бёдрах", "hands_behind_head": "руки за головой",
            "arms_crossed": "руки скрещены", "hands_up": "руки вверх",
            "turned_around": "повернувшись спиной", "posing": "позируя",
            "air_kiss": "воздушный поцелуй", "winking": "подмигивая",
            "finger_to_lips": "палец у губ", "heart_fingers": "сердечко пальцами",
            "beckoning": "маня жестом", "covering_mouth": "прикрывая рот",
            "biting_lip": "кусая губу", "legs_spread": "ноги разведены",
            "legs_wide": "ноги широко разведены", "butt_to_viewer": "попой к зрителю",
            "caressing_breast": "лаская грудь", "caressing_self": "лаская себя",
            "exposing_chest": "обнажая грудь", "fingers_in_mouth": "пальцы во рту",
            "head_thrown_back": "запрокинув голову", "licking_lips": "облизывая губы",
            "mouth_open": "приоткрыв рот",
        },
        "angle": {
            "front": "вид спереди", "three_quarter_front": "вид в три четверти спереди",
            "three_quarter_left": "вид в три четверти слева",
            "three_quarter_right": "вид в три четверти справа", "side": "вид сбоку",
            "profile_left": "профиль слева", "profile_right": "профиль справа",
            "back": "вид сзади", "three_quarter_back": "вид в три четверти сзади",
            "top": "вид сверху", "high_angle": "верхний ракурс",
            "eye_level": "на уровне глаз", "low_angle": "нижний ракурс",
            "ground_level": "с уровня пола", "dutch": "голландский угол",
            "over_shoulder": "через плечо",
        },
        "shot": {
            "full_body": "общий план в полный рост", "wide": "широкий план",
            "medium": "средний план", "waist": "по пояс", "chest": "по грудь",
            "close_up": "крупный план", "extreme_close_up": "очень крупный план",
            "macro": "макроплан", "two_shot": "двойной план",
            "group_shot": "групповой план", "pov_shot": "POV-план",
            "from_behind": "съёмка сзади",
        },
        "focus": {
            "whole_body": "в фокусе всё тело", "face": "в фокусе лицо",
            "eyes": "в фокусе глаза", "lips": "в фокусе губы",
            "chest": "в фокусе грудь", "hips": "в фокусе бёдра",
            "butt": "в фокусе ягодицы", "crotch": "в фокусе промежность",
            "legs": "в фокусе ноги", "hands": "в фокусе руки",
            "back": "в фокусе спина", "neck": "в фокусе шея",
        },
        "camera_level": {
            "eye_level": "на уровне глаз", "high": "камера сверху",
            "low": "камера снизу", "ground": "камера с уровня пола",
        },
        "composition": {
            "pair": "композиция пары", "all": "все участники в кадре",
            "focus": "сфокусированная композиция",
        },
        "crop": {"face": "кроп лица", "body": "кроп тела", "details": "кроп деталей"},
        "camera_target": {
            "face": "камера на лице", "body": "камера на теле",
            "action": "камера на действии", "scene": "камера на сцене",
        },
        "zoom": {"none": "", "closer": "приблизить", "farther": "отдалить", "macro": "экстремальный крупный план, макрос, дистанция 10-20 см"},
        "camera_position": {
            "front": "камера спереди", "behind": "камера сзади",
            "side": "камера сбоку", "top": "камера сверху",
            "bottom": "камера снизу", "pov": "POV-камера",
        },
        "who_top": {
            "auto": "", "female": "женщина сверху", "male": "мужчина сверху",
            "random": "случайный верх",
        },
        "gaze": {
            "auto": "", "camera": "смотрит в камеру", "partner": "смотрит на партнёра",
            "down": "смотрит вниз", "away": "отводит взгляд", "closed": "глаза закрыты",
        },
        "background": {
            "plain": "однотонный фон", "white": "белый фон", "black": "чёрный фон",
            "gray": "серый фон", "gradient": "градиентный фон", "studio": "студия",
            "bedroom": "спальня", "hotel": "номер отеля", "living_room": "гостиная",
            "bathroom": "ванная", "kitchen": "кухня", "office": "офис",
            "city": "город", "street": "улица", "nature": "природа",
            "forest": "лес", "beach": "пляж", "water": "вода", "pool": "бассейн",
            "fantasy": "фэнтези-локация", "dungeon": "подземелье",
        },
        "lighting": {
            "natural": "естественный свет", "studio": "студийный свет",
            "soft": "мягкий свет", "hard": "жёсткий свет",
            "dramatic": "драматичный свет", "backlight": "контровой свет",
            "golden_hour": "золотой час", "blue_hour": "синий час",
            "neon": "неоновый свет", "candles": "свет свечей",
            "flash": "вспышка", "cinematic": "кинематографичный свет",
        },
        "time": {
            "auto": "", "day": "день", "morning": "утро", "evening": "вечер",
            "night": "ночь", "sunset": "закат", "sunrise": "рассвет",
        },
        "atmosphere": {
            "auto": "", "none": "", "candles": "свечи", "rain": "дождь",
            "steam": "пар", "smoke": "дым", "dust": "пыль", "firelight": "отблески огня",
        },
        "setting": {
            "auto": "", "modern": "современный сеттинг", "fantasy": "фэнтези-сеттинг",
            "historical": "исторический сеттинг",
        },
        "interaction": {
            "kiss": "поцелуи", "caress": "ласки", "oral": "оральная ласка",
            "penetration": "проникновение", "eye_contact": "зрительный контакт",
            "undress": "раздевание", "spanking": "шлепки", "choking": "лёгкое удушение",
            "hair_pull": "тянуть за волосы", "dirty_talk": "грязные разговоры",
        },
        "style": {
            "photoreal": "фотореализм", "cinematic": "кинематографичность",
            "amateur": "любительское фото", "retro": "ретро", "webcam": "веб-камера",
            "anime": "аниме", "illustration": "иллюстрация",
        },
        "quality": {"high": "высокое качество", "medium": "среднее качество", "none": ""},
        "model": {
            "universal": "универсальная модель", "sdxl": "SDXL", "pony": "Pony",
            "illustrious": "Illustrious", "flux": "Flux", "wan": "WAN",
        },
        "format": {
            "natural": "естественный язык", "tags": "теги через запятую",
            "hybrid": "естественный язык плюс теги",
        },
        "freedom": {
            "strict": "строго из разрешённых списков",
            "from_lists": "из разрешённых списков, свободно комбинируя",
            "free": "свободная формулировка внутри сцены",
        },
        "missing": {
            "pov": "отсутствующий партнёр — это POV-камера",
            "partial": "присутствуют только подключённые персонажи",
            "invent": "придумать недостающего партнёра под сцену",
        },
        "control": {
            "hybrid": "явные виджеты важнее, остальное случайно",
            "manual": "только явные значения виджетов",
            "all_random": "игнорировать количества и рандомизировать состав",
        },
        "distribution": {
            "by_connection": "количество по подключённым персонажам",
            "by_description": "количество по описаниям",
            "manual": "количество из JSON ролей",
        },
    },
}

SYSTEM = {
    "en": (
        "You write adult (18+) sexual scene prompts for an image or video model. "
        "Every character is an adult. Preserve each character's appearance exactly as described. "
        "Do not add participants, acts, or body features that are not in the brief. "
        "Do not write a negative prompt. Never mention minors, animals, or non-consent. "
        "Use explicit sexual terminology when the brief asks for it. "
        "Return one ready-to-use prompt in the requested format, with no explanations."
    ),
    "ru": (
        "Ты пишешь промпты взрослых (18+) сексуальных сцен для модели изображений или видео. "
        "Все персонажи — взрослые. Сохраняй внешность каждого персонажа точно как в описании. "
        "Не добавляй участников, действия или черты тела, которых нет в брифе. "
        "Не пиши негативный промпт. Никогда не упоминай несовершеннолетних, животных или неконсент. "
        "Используй явные сексуальные термины, если бриф этого требует. "
        "Верни один готовый промпт в запрошенном формате, без пояснений."
    ),
}

RULES = {
    "en": (
        "- Format: {format}.\n"
        "- Target model: {model}.\n"
        "- Freedom: {freedom}.\n"
        "- Keep the number of participants and their genders exactly as in the brief.\n"
        "- Keep the scene physically possible for the chosen type.\n"
        "- Preserve the character descriptions; do not replace faces, hair, or body.\n"
        "- If a field is marked llm_choice, choose ONE value from its allowed list.\n"
        "- Do not output a negative prompt or a list of bans.{forbidden}"
    ),
    "ru": (
        "- Формат: {format}.\n"
        "- Целевая модель: {model}.\n"
        "- Свобода: {freedom}.\n"
        "- Сохраняй число участников и их пол точно как в брифе.\n"
        "- Сцена должна быть физически возможна для выбранного типа.\n"
        "- Сохраняй описания персонажей; не заменяй лица, волосы или тело.\n"
        "- Если поле помечено llm_choice, выбери ОДНО значение из его allowed.\n"
        "- Не выводи негативный промпт и список запретов.{forbidden}"
    ),
}


def phrase(category: str, token: str, lang: str = "en") -> str:
    """Translate a protocol token into prose; unknown tokens pass through."""
    table = PHRASES.get(lang) or PHRASES["en"]
    return (table.get(category) or {}).get(token, token)


def t(category: str, token: str, lang: str = "en") -> str:
    return phrase(category, token, lang)
