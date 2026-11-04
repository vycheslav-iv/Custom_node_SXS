// SXS — интерфейс ноды.
//
// Работает только с ПОДПИСЯМИ значений combo. Сами значения — протокол
// (classic / soft / by_connection ...) — не трогаем: их читает Python, и
// подмена options.values молча увела бы ноду в дефолт.
//
// Язык берётся из Comfy.Locale при создании ноды и переприменяется по событию
// Comfy.Locale.change, без перезапуска ComfyUI. Виджет «Язык_меню» может
// принудительно включить ru или en. Подписи входов, имени ноды и описания
// приходят из locales/{en,ru}/nodeDefs.json.
(() => {
  const { app } = window.comfyAPI?.app ?? {};
  if (!app || typeof app.registerExtension !== 'function') return;

  const NODE_KEYS = ['SXS'];
  const RANGE = ['1', '2', '3', '4', '5', '6'];

  const RU_LABELS = {
    'Язык_меню': { auto: 'Авто', ru: 'Русский', en: 'Английский' },
    'Язык_промпта': { en: 'Английский', ru: 'Русский' },
    'Управление': {
      hybrid: 'Гибридное',
      manual: 'Ручное',
      all_random: 'Всё случайно',
    },
    'Девушки': { auto: 'Авто', 0: '0', 1: '1', 2: '2', 3: '3', random: 'Случайно' },
    'Парни': { auto: 'Авто', 0: '0', 1: '1', 2: '2', 3: '3', random: 'Случайно' },
    'Распределение': {
      by_connection: 'По подключению',
      by_description: 'По описанию',
      manual: 'Вручную',
    },
    'Фокус_на': {
      auto: 'Авто',
      1: 'Персонаж 1',
      2: 'Персонаж 2',
      3: 'Персонаж 3',
      4: 'Персонаж 4',
      5: 'Персонаж 5',
      6: 'Персонаж 6',
    },
    'Политика_отсутствующего': {
      pov: 'POV',
      partial: 'Частично',
      invent: 'Досочинить',
    },
    'Пресет_сцены': {
      none: 'Нет',
      romance: 'Романтика',
      passion: 'Страсть',
      pov: 'POV',
      group: 'Группа',
      bdsm: 'BDSM',
      solo: 'Соло',
    },
    'Тип': {
      random: 'Случайно',
      classic: 'Классический',
      oral: 'Оральный',
      anal: 'Анальный',
      lesbian: 'Лесбийский',
      gay: 'Гей',
      group: 'Групповой',
      orgy: 'Оргия',
      solo_f: 'Соло (женщина)',
      solo_m: 'Соло (мужчина)',
      pov: 'POV',
      bdsm: 'BDSM',
      toys: 'С игрушками',
      fingering: 'Ласки руками',
      fisting: 'Фистинг',
      creampie: 'Кремпай',
      bukkake: 'Буккаке',
      edging: 'Эджинг',
      facesitting: 'Сидение на лице',
      strapon: 'Страпон',
      double_penetration: 'Двойное проникновение',
      threesome: 'Тройной',
      gangbang: 'Гэнгбэнг',
      public: 'Публичный',
      roleplay: 'Ролевая игра',
      "--- BASIC ---": "--- Базовые ---",
      "--- SAME_SEX ---": "--- Однополые ---",
      "--- GROUP ---": "--- Групповые ---",
      "--- SOLO ---": "--- Соло ---",
      "--- POV ---": "--- POV ---",
      "--- BDSM ---": "--- BDSM ---",
      "--- TOYS ---": "--- С игрушками ---",
      "--- EXTREME ---": "--- Экстремальные ---",
    },
    'Этап_сцены': {
      auto: 'Авто',
      start: 'Начало',
      insertion: 'Только вставляет',
      middle: 'Середина',
      finish: 'Уже кончает',
      random: 'Случайно',
    },
    'Куда_кончает': {
      auto: 'Авто',
      none: 'Не указано',
      inside: 'Внутрь',
      mouth: 'В рот',
      face: 'На лицо',
      breast: 'На грудь',
      body: 'На тело',
      back: 'На спину',
      outside: 'Наружу',
      random: 'Случайно',
    },
    'Совместимость': { strict: 'Строгая', soft: 'Мягкая' },
    'Эмоции': {
      tender: 'Нежные',
      passionate: 'Страстные',
      dominant: 'Доминирующие',
      submissive: 'Покорные',
      playful: 'Игривые',
      mix: 'Смешанные',
      seductive: 'Соблазнительные',
    },
    'Темп': { static: 'Статичный', rhythmic: 'Ритмичный', intense: 'Интенсивный', slow: 'Медленный' },
    'Одежда': {
      dressed: 'Одеты',
      partially: 'Частично',
      lingerie: 'Бельё',
      nude: 'Обнажены',
      torn: 'Порвана',
    },
    'Поза': {
      standing: 'Стоя',
      standing_side: 'Стоя боком',
      standing_one_leg: 'Стоя на одной ноге',
      lunge: 'Выпад',
      leaning_wall: 'С опорой на стену',
      sitting: 'Сидя',
      sitting_chair: 'Сидя на стуле',
      sitting_floor: 'Сидя на полу',
      sitting_cross_legged: 'Сидя по-турецки',
      sitting_leg_over_leg: 'Сидя нога на ногу',
      sitting_knees_chest: 'Сидя, колени к груди',
      on_knees: 'На коленях',
      squatting: 'На корточках',
      lying_back: 'Лёжа на спине',
      lying_stomach: 'Лёжа на животе',
      lying_side: 'Лёжа на боку',
      reclining: 'Полулёжа',
      on_all_fours: 'На четвереньках',
      dancing: 'Танцует',
      arching_back: 'Прогибается',
      straddling: 'Верхом',
      grinding: 'Трётся',
      riding: 'Едет верхом',
      thrusting: 'Толкается',
      lifting_partner: 'Поднимает партнёра',
      pinned: 'Прижата',
      seductive: 'Соблазнительная',
      passionate: 'Страстная',
      tender: 'Нежная',
      playful: 'Игривая',
      dominant: 'Доминирующая',
      submissive: 'Покорная',
      shy: 'Застенчивая',
      confident: 'Уверенная',
      hands_on_hips: 'Руки на бёдрах',
      hands_behind_head: 'Руки за головой',
      arms_crossed: 'Руки скрещены',
      hands_up: 'Руки вверх',
      arched_back: 'Прогнутая спина',
      turned_around: 'Повернулась спиной',
      posing: 'Позирует',
      air_kiss: 'Воздушный поцелуй',
      winking: 'Подмигивает',
      finger_to_lips: 'Палец к губам',
      heart_fingers: 'Сердце пальцами',
      beckoning: 'Манит',
      covering_mouth: 'Прикрывает рот',
      biting_lip: 'Кусает губу',
      legs_spread: 'Ноги раздвинуты',
      legs_wide: 'Ноги широко',
      butt_to_viewer: 'Ягодицами к зрителю',
      caressing_breast: 'Ласкает грудь',
      caressing_self: 'Ласкает себя',
      exposing_chest: 'Открывает грудь',
      fingers_in_mouth: 'Пальцы во рту',
      head_thrown_back: 'Голова запрокинута',
      licking_lips: 'Облизывает губы',
      mouth_open: 'Приоткрытый рот',
      "--- STAND ---": "--- Стоя ---",
      "--- SIT ---": "--- Сидя ---",
      "--- LYING ---": "--- Лежа ---",
      "--- DYNAMIC ---": "--- Динамичные ---",
      "--- MOOD ---": "--- Позы настроения ---",
      "--- MODELING ---": "--- Позирование ---",
      "--- GESTURE ---": "--- Подаёт знаки ---",
      "--- SEXUAL ---": "--- Сексуальные ---",
    },
    'Взгляд': { camera: 'В камеру', partner: 'На партнёра', down: 'Вниз', away: 'В сторону', closed: 'Закрыты' },
    'Кто_сверху': { auto: 'Авто', female: 'Девушка', male: 'Парень', random: 'Случайно' },
    'Положение_камеры': { front: 'Спереди', behind: 'Сзади', side: 'Сбоку', top: 'Сверху', bottom: 'Снизу', pov: 'POV' },
    'Ракурс': {
      front: 'Фронтально',
      three_quarter_front: 'Три четверти спереди',
      three_quarter_left: 'Три четверти слева',
      three_quarter_right: 'Три четверти справа',
      side: 'Сбоку',
      profile_left: 'Профиль слева',
      profile_right: 'Профиль справа',
      back: 'Сзади',
      three_quarter_back: 'Три четверти сзади',
      top: 'Сверху',
      high_angle: 'Верхний ракурс',
      eye_level: 'На уровне глаз',
      low_angle: 'Нижний ракурс',
      ground_level: 'С уровня земли',
      dutch: 'Голландский угол',
      over_shoulder: 'Через плечо',
    },
    'План': {
      full_body: 'Полный рост',
      wide: 'Общий',
      medium: 'Средний',
      waist: 'По пояс',
      chest: 'По грудь',
      close_up: 'Крупный',
      extreme_close_up: 'Детальный',
      macro: 'Макро',
      two_shot: 'Двое',
      group_shot: 'Групповой',
      pov_shot: 'POV',
      from_behind: 'Сзади',
    },
    'Фокус': {
      whole_body: 'Всё тело',
      face: 'Лицо',
      eyes: 'Глаза',
      lips: 'Губы',
      chest: 'Грудь',
      hips: 'Бёдра',
      butt: 'Ягодицы',
      crotch: 'Пах',
      legs: 'Ноги',
      hands: 'Руки',
      back: 'Спина',
      neck: 'Шея',
    },
    'Уровень_камеры': { eye_level: 'На уровне глаз', high: 'Высокий', low: 'Низкий', ground: 'С земли' },
    'Композиция': { pair: 'Пара', all: 'Все', focus: 'Фокус' },
    'Кроп': { face: 'Лицо', body: 'Тело', details: 'Детали' },
    'Куда_смотрит_камера': { face: 'Лицо', body: 'Тело', action: 'Действие', scene: 'Сцена' },
    'Зум': { none: 'Нет', closer: 'Ближе', farther: 'Дальше', macro: 'Макрос' },
    'Фон': {
      random: 'Случайно',
      // Простые
      studio: 'Студия',
      cyclorama: 'Циклорама',
      white_cyclorama: 'Белая циклорама',
      black_studio: 'Чёрная студия',
      loft_studio: 'Лофт-студия',
      minimal_studio: 'Минимал-студия',
      neon_studio: 'Неон-студия',
      vintage_studio: 'Винтажная студия',
      textured_wall: 'Текстурная стена',
      "--- Простые ---": "--- Простые ---",
      // Студия
      photo_studio: 'Фотостудия',
      interior_studio: 'Интерьерная студия',
      natural_light_studio: 'С натуральным светом',
      softbox_studio: 'С софтбоксами',
      studio_with_props: 'С реквизитом',
      studio_with_drapes: 'С драпировками',
      studio_with_mirrors: 'С зеркалами',
      studio_with_columns: 'С колоннами',
      studio_with_flowers: 'С цветами',
      "--- Студия ---": "--- Студия ---",
      // Город
      city: 'Город',
      night_city: 'Ночной город',
      rainy_city: 'Дождливый город',
      street: 'Улица',
      alley: 'Переулок',
      square: 'Площадь',
      industrial_zone: 'Промзона',
      skyscraper_roof: 'Крыша небоскрёба',
      embankment: 'Набережная',
      club: 'Клуб',
      cafe: 'Кафе',
      restaurant: 'Ресторан',
      subway: 'Метро',
      station: 'Вокзал',
      airport: 'Аэропорт',
      balcony_city_view: 'Балкон с видом на город',
      backyard: 'Задний двор',
      garage: 'Гараж',
      "--- Город ---": "--- Город ---",
      // Природа
      forest: 'Лес',
      mountains: 'Горы',
      field: 'Поле',
      garden: 'Сад',
      desert: 'Пустыня',
      snow_landscape: 'Снежный пейзаж',
      flower_meadow: 'Цветущий луг',
      autumn_park: 'Осенний парк',
      rocky_shore: 'Скалистый берег',
      foggy_forest: 'Туманный лес',
      savanna: 'Саванна',
      bamboo_grove: 'Бамбуковая роща',
      steppe: 'Степь',
      canyon: 'Каньон',
      cave: 'Пещера',
      volcano: 'Вулкан',
      glacier: 'Ледник',
      lavender_field: 'Лавандовое поле',
      vineyard: 'Виноградник',
      jungle: 'Джунгли',
      japanese_garden: 'Японский сад',
      heather_moor: 'Вересковая пустошь',
      "--- Природа ---": "--- Природа ---",
      // Вода
      tropical_island: 'Тропический остров',
      beach: 'Пляж',
      sea: 'Море',
      ocean: 'Океан',
      lake: 'Озеро',
      mountain_lake: 'Горное озеро',
      river: 'Река',
      waterfall: 'Водопад',
      pool: 'Бассейн',
      fountain: 'Фонтан',
      pond: 'Пруд',
      swamp: 'Болото',
      seabed: 'Морское дно',
      coral_reef: 'Коралловый риф',
      "--- Вода ---": "--- Вода ---",
      // Комнаты
      bedroom: 'Спальня',
      bathroom: 'Ванная',
      living_room: 'Гостиная',
      kitchen: 'Кухня',
      library: 'Библиотека',
      grand_hall: 'Большой зал',
      balcony: 'Балкон',
      terrace: 'Терраса',
      mansion: 'Особняк',
      loft: 'Лофт',
      country_house: 'Загородный дом',
      office: 'Кабинет',
      workshop: 'Мастерская',
      wardrobe: 'Гардеробная',
      winter_garden: 'Зимний сад',
      greenhouse: 'Оранжерея',
      corridor: 'Коридор',
      staircase: 'Лестница',
      veranda: 'Веранда',
      theater: 'Театр',
      museum: 'Музей',
      gallery: 'Галерея',
      throne_hall: 'Тронный зал',
      boudoir: 'Будуар',
      hotel_room: 'Гостиничный номер',
      "--- Комнаты ---": "--- Комнаты ---",
      // Фэнтези
      sunset: 'Закат',
      sunrise: 'Рассвет',
      golden_hour: 'Золотой час',
      fog: 'Туман',
      blizzard: 'Метель',
      stormy_sky: 'Грозовое небо',
      night_sky: 'Ночное небо',
      starry_night: 'Звёздное небо',
      moonlit_night: 'Лунная ночь',
      aurora: 'Северное сияние',
      rainbow: 'Радуга',
      castle: 'Замок',
      temple: 'Храм',
      ruins: 'Руины',
      space: 'Космос',
      fantasy_world: 'Фэнтези-мир',
      magic_forest: 'Магический лес',
      ancient_fortress: 'Древняя крепость',
      misty_mountains: 'Туманные горы',
      underground_grotto: 'Подземный грото',
      mystic_portal: 'Мистический портал',
      fairy_palace: 'Сказочный дворец',
      crystal_cave: 'Хрустальная пещера',
      floating_island: 'Левитирующий остров',
      cursed_graveyard: 'Проклятое кладбище',
      astral: 'Астрал',
      underwater_kingdom: 'Подводное королевство',
      romantic_world: 'Романтический мир',
      "--- Фэнтези ---": "--- Фэнтези ---",
    },
    'Освещение': {
      natural: 'Естественный',
      studio: 'Студийный',
      soft: 'Мягкий',
      hard: 'Жёсткий',
      dramatic: 'Драматичный',
      backlight: 'Контровой',
      golden_hour: 'Золотой час',
      blue_hour: 'Синий час',
      neon: 'Неон',
      candles: 'Свечи',
      flash: 'Вспышка',
      cinematic: 'Кинематографичный',
    },
    'Время_суток': {
      day: 'День',
      morning: 'Утро',
      evening: 'Вечер',
      night: 'Ночь',
      sunset: 'Закат',
      sunrise: 'Рассвет',
    },
    'Атмосфера': {
      none: 'Нет',
      candles: 'Свечи',
      rain: 'Дождь',
      steam: 'Пар',
      smoke: 'Дым',
      dust: 'Пыль',
      firelight: 'Живой огонь',
    },
    'Сеттинг': { modern: 'Современный', fantasy: 'Фэнтези', historical: 'Исторический' },
    'Формат_промпта': { natural: 'Проза', tags: 'Теги', hybrid: 'Гибрид' },
    'Модель': {
      universal: 'Универсальная',
      sdxl: 'SDXL',
      pony: 'Pony',
      illustrious: 'Illustrious',
      flux: 'Flux',
      wan: 'WAN',
    },
    'Стиль': {
      photoreal: 'Фотореализм',
      cinematic: 'Кинематографичный',
      amateur: 'Любительский',
      webcam: 'Веб-камера',
      retro: 'Ретро',
      anime: 'Аниме',
      illustration: 'Иллюстрация',
    },
    'Качество': { high: 'Высокое', medium: 'Среднее', none: 'Нет' },
    'Свобода_LLM': { strict: 'Строгая', from_lists: 'По спискам', free: 'Свободная' },
    'Пол_1': { auto: 'Авто', female: 'Женский', male: 'Мужской' },
    'Пол_2': { auto: 'Авто', female: 'Женский', male: 'Мужской' },
    'Пол_3': { auto: 'Авто', female: 'Женский', male: 'Мужской' },
    'Пол_4': { auto: 'Авто', female: 'Женский', male: 'Мужской' },
    'Пол_5': { auto: 'Авто', female: 'Женский', male: 'Мужской' },
    'Пол_6': { auto: 'Авто', female: 'Женский', male: 'Мужской' },
  };

  const GROUPS = [
    { start: 'seed', en: '═══ SETUP ═══', ru: '═══ НАСТРОЙКА ═══' },
    { start: 'Девушки', en: '═══ CHARACTERS ═══', ru: '═══ ПЕРСОНАЖИ ═══' },
    { start: 'Пресет_сцены', en: '═══ SCENE ═══', ru: '═══ СЦЕНА ═══' },
    { start: 'Позы_выбирает_LLM', en: '═══ POSE ═══', ru: '═══ ПОЗА ═══' },
    { start: 'Камера_выбирает_LLM', en: '═══ CAMERA ═══', ru: '═══ КАМЕРА ═══' },
    { start: 'Окружение_выбирает_LLM', en: '═══ ENVIRONMENT ═══', ru: '═══ ОКРУЖЕНИЕ ═══' },
    { start: 'Формат_промпта', en: '═══ STYLE & LLM ═══', ru: '═══ СТИЛЬ И LLM ═══' },
  ];

  const POSE_FIELDS = ['Поза'];
  const CAMERA_FIELDS = [
    'Ракурс', 'План', 'Фокус', 'Ракурсы_вкл', 'Планы_вкл', 'Фокусы_вкл',
    'Уровень_камеры', 'POV', 'Композиция', 'Кроп', 'Куда_смотрит_камера', 'Зум',
    'Положение_камеры',
  ];
  const ENVIRONMENT_FIELDS = [
    'Фон', 'Освещение', 'Время_суток', 'Атмосфера', 'Сеттинг',
    'Фоны_вкл', 'Свет_вкл', 'Время_вкл', 'Атмосфера_вкл', 'Сеттинг_вкл',
  ];

  function readLocale() {
    try {
      const value = app?.extensionManager?.setting?.get?.('Comfy.Locale');
      if (typeof value === 'string' && value) return value.toLowerCase();
    } catch {
      /* фронтенд без менеджера настроек */
    }
    return 'en';
  }

  function menuOverride(node) {
    const widget = widgetsOf(node).find((item) => item?.name === 'Язык_меню');
    const value = String(widget?.value ?? 'auto').toLowerCase();
    return value === 'ru' || value === 'en' ? value : '';
  }

  function activeLang(node) {
    const forced = menuOverride(node);
    if (forced) return forced;
    return readLocale().startsWith('ru') ? 'ru' : 'en';
  }

  function widgetsOf(node) {
    return Array.isArray(node?.widgets) ? node.widgets : [];
  }

  function labelFor(name, value, lang) {
    if (lang === 'ru') {
      const table = RU_LABELS[name];
      if (table && Object.prototype.hasOwnProperty.call(table, String(value))) {
        return table[String(value)];
      }
    }
    return String(value ?? '').replace(/_/g, ' ');
  }

  function applyWidgetLabels(node) {
    const lang = activeLang(node);
    for (const widget of widgetsOf(node)) {
      if (!widget) continue;
      if (widget._sxsSeparator) {
        widget._sepEl.textContent = widget._sxsSeparator[lang] || widget._sxsSeparator.en;
        continue;
      }
      widget.options = widget.options || {};
      widget.options.getOptionLabel = (value) => labelFor(widget.name, value, lang);
    }
    repaint(node);
  }

  function applyDisabled(node) {
    const values = {};
    for (const widget of widgetsOf(node)) {
      if (widget?.name) values[widget.name] = widget.value;
    }
    const master = values['Всё_выбирает_LLM'] === true;
    const typeLLM = master || values['Тип_выбирает_LLM'] === true;
    const poseLLM = master || values['Позы_выбирает_LLM'] === true;
    const cameraLLM = master || values['Камера_выбирает_LLM'] === true;
    const envLLM = master || values['Окружение_выбирает_LLM'] === true;

    const disabled = new Set();
    if (typeLLM) disabled.add('Тип');
    if (poseLLM) {
      for (const name of Object.keys(values)) {
        if (name.startsWith('Позы_группа_')) disabled.add(name);
      }
      for (const name of POSE_FIELDS) disabled.add(name);
    }
    if (cameraLLM) {
      for (const name of CAMERA_FIELDS) disabled.add(name);
    }
    if (envLLM) {
      for (const name of ENVIRONMENT_FIELDS) disabled.add(name);
    }
    const stage = String(values['Этап_сцены'] ?? 'auto');
    if (!['auto', 'random', 'finish'].includes(stage)) disabled.add('Куда_кончает');
    if (master) {
      disabled.add('Тип_выбирает_LLM');
      disabled.add('Позы_выбирает_LLM');
      disabled.add('Камера_выбирает_LLM');
      disabled.add('Окружение_выбирает_LLM');
    }

    // ── фильтрация вариантов типа сцены по включённым группам ──
    const TYPE_GROUP_MAP = {
      'Тип_группа_basic': ['classic', 'oral', 'anal', 'fingering'],
      'Тип_группа_same_sex': ['lesbian', 'gay'],
      'Тип_группа_group': ['group', 'orgy', 'threesome', 'gangbang'],
      'Тип_группа_solo': ['solo_f', 'solo_m'],
      'Тип_группа_pov': ['pov'],
      'Тип_группа_bdsm': ['bdsm', 'edging'],
      'Тип_группа_toys': ['toys', 'strapon', 'double_penetration'],
      'Тип_группа_extreme': ['fisting', 'creampie', 'bukkake', 'facesitting', 'public', 'roleplay'],
    };
    const TYPE_GROUP_LABEL = {
      'Тип_группа_basic': '--- BASIC ---',
      'Тип_группа_same_sex': '--- SAME_SEX ---',
      'Тип_группа_group': '--- GROUP ---',
      'Тип_группа_solo': '--- SOLO ---',
      'Тип_группа_pov': '--- POV ---',
      'Тип_группа_bdsm': '--- BDSM ---',
      'Тип_группа_toys': '--- TOYS ---',
      'Тип_группа_extreme': '--- EXTREME ---',
    };
    const typeWidget = widgetsOf(node).find((w) => w?.name === 'Тип');
    if (typeWidget && typeWidget.options) {
      const allowed = ['random'];
      for (const [toggle, types] of Object.entries(TYPE_GROUP_MAP)) {
        if (values[toggle] === true) {
          allowed.push(TYPE_GROUP_LABEL[toggle]);
          allowed.push(...types);
        }
      }
      typeWidget.options.values = allowed;
    }

    // ── фильтрация вариантов фона по включённым группам ──
    const BG_GROUP_MAP = {
      'Фоны_простые_вкл': ['studio', 'cyclorama', 'white_cyclorama', 'black_studio', 'loft_studio', 'minimal_studio', 'neon_studio', 'vintage_studio', 'textured_wall'],
      'Фоны_студия_вкл': ['photo_studio', 'interior_studio', 'natural_light_studio', 'softbox_studio', 'studio_with_props', 'studio_with_drapes', 'studio_with_mirrors', 'studio_with_columns', 'studio_with_flowers'],
      'Фоны_город_вкл': ['city', 'night_city', 'rainy_city', 'street', 'alley', 'square', 'industrial_zone', 'skyscraper_roof', 'embankment', 'club', 'cafe', 'restaurant', 'subway', 'station', 'airport', 'balcony_city_view', 'backyard', 'garage'],
      'Фоны_природа_вкл': ['forest', 'mountains', 'field', 'garden', 'desert', 'snow_landscape', 'flower_meadow', 'autumn_park', 'rocky_shore', 'foggy_forest', 'savanna', 'bamboo_grove', 'steppe', 'canyon', 'cave', 'volcano', 'glacier', 'lavender_field', 'vineyard', 'jungle', 'japanese_garden', 'heather_moor'],
      'Фоны_вода_вкл': ['tropical_island', 'beach', 'sea', 'ocean', 'lake', 'mountain_lake', 'river', 'waterfall', 'pool', 'fountain', 'pond', 'swamp', 'seabed', 'coral_reef'],
      'Фоны_комнаты_вкл': ['bedroom', 'bathroom', 'living_room', 'kitchen', 'library', 'grand_hall', 'balcony', 'terrace', 'mansion', 'loft', 'country_house', 'office', 'workshop', 'wardrobe', 'winter_garden', 'greenhouse', 'corridor', 'staircase', 'veranda', 'theater', 'museum', 'gallery', 'throne_hall', 'boudoir', 'hotel_room'],
      'Фоны_фэнтези_вкл': ['sunset', 'sunrise', 'golden_hour', 'fog', 'blizzard', 'stormy_sky', 'night_sky', 'starry_night', 'moonlit_night', 'aurora', 'rainbow', 'castle', 'temple', 'ruins', 'space', 'fantasy_world', 'magic_forest', 'ancient_fortress', 'misty_mountains', 'underground_grotto', 'mystic_portal', 'fairy_palace', 'crystal_cave', 'floating_island', 'cursed_graveyard', 'astral', 'underwater_kingdom', 'romantic_world'],
    };
    const BG_GROUP_LABEL = {
      'Фоны_простые_вкл': '--- Простые ---',
      'Фоны_студия_вкл': '--- Студия ---',
      'Фоны_город_вкл': '--- Город ---',
      'Фоны_природа_вкл': '--- Природа ---',
      'Фоны_вода_вкл': '--- Вода ---',
      'Фоны_комнаты_вкл': '--- Комнаты ---',
      'Фоны_фэнтези_вкл': '--- Фэнтези ---',
    };
    const bgWidget = widgetsOf(node).find((w) => w?.name === 'Фон');
    if (bgWidget && bgWidget.options) {
      const allowed = ['random'];
      for (const [toggle, types] of Object.entries(BG_GROUP_MAP)) {
        if (values[toggle] === true) {
          allowed.push(BG_GROUP_LABEL[toggle]);
          allowed.push(...types);
        }
      }
      bgWidget.options.values = allowed;
    }

    for (const widget of widgetsOf(node)) {
      if (!widget?.name) continue;
      widget.disabled = disabled.has(widget.name);
    }
    repaint(node);
  }

  function repaint(node) {
    try {
      node.setDirtyCanvas?.(true, true);
    } catch {
      /* нода вне canvas */
    }
  }

  function makeSeparator(label, group) {
    const el = document.createElement('div');
    el.className = 'sxs-sep';
    el.style.cssText = [
      'box-sizing:border-box',
      'height:22px',
      'display:flex',
      'align-items:center',
      'padding:0 8px',
      'margin:2px 0',
      'border-top:1px solid rgba(120,120,120,0.25)',
      'background:rgba(50,50,50,0.04)',
      'color:#888',
      'font:bold 10px sans-serif',
      'white-space:nowrap',
      'overflow:hidden',
      'text-overflow:ellipsis',
      'pointer-events:none',
    ].join(';');
    el.textContent = label;
    el.dataset.group = group;
    return el;
  }

  function insertSeparators(node) {
    for (let i = GROUPS.length - 1; i >= 0; i -= 1) {
      const group = GROUPS[i];
      const index = widgetsOf(node).findIndex((widget) => widget?.name === group.start);
      if (index < 0) continue;
      const label = activeLang(node) === 'ru' ? group.ru : group.en;
      const el = makeSeparator(label, group.start);
      const name = `__sxs_sep_${i}`;
      node.addDOMWidget(name, 'div', el, {
        serialize: false,
        hideInPanel: true,
        getValue: () => null,
        setValue: () => {},
        getMinHeight: () => 26,
      });
      const widget = node.widgets[node.widgets.length - 1];
      widget._sepEl = el;
      widget._sxsSeparator = { en: group.en, ru: group.ru };
      widget.serialize = false;
      node.widgets.splice(node.widgets.length - 1, 1);
      node.widgets.splice(index, 0, widget);
    }
  }

  function makeWarningWidget(node) {
    const el = document.createElement('div');
    el.className = 'sxs-warn';
    el.style.cssText = [
      'box-sizing:border-box',
      'display:none',
      'min-height:20px',
      'align-items:center',
      'padding:2px 8px',
      'margin:2px 0',
      'border-radius:4px',
      'background:rgba(200,60,60,0.18)',
      'border:1px solid rgba(220,90,90,0.55)',
      'color:#f0b0b0',
      'font:11px sans-serif',
      'white-space:pre-wrap',
      'overflow:hidden',
    ].join(';');
    node.addDOMWidget('__sxs_warn', 'div', el, {
      serialize: false,
      hideInPanel: true,
      getValue: () => null,
      setValue: () => {},
      getMinHeight: () => (el.style.display === 'none' ? 0 : 24),
    });
    const widget = node.widgets[node.widgets.length - 1];
    widget.serialize = false;
    node._sxsWarnEl = el;
    node._sxsWarnWidget = widget;
  }

  function pickWarn(message) {
    if (message == null) return '';
    if (Array.isArray(message)) return String(message[2] ?? '');
    const direct = message.WARN ?? message.warn;
    if (direct != null) return Array.isArray(direct) ? String(direct[0] ?? '') : String(direct);
    if (Array.isArray(message.output)) return String(message.output[2] ?? '');
    return '';
  }

  function showWarning(node, text) {
    const el = node._sxsWarnEl;
    if (!el) return;
    const value = String(text ?? '').trim();
    el.textContent = value;
    el.style.display = value ? 'flex' : 'none';
    el.title = value;
    repaint(node);
  }

  const tracked = new Set();

  function sync(node) {
    applyWidgetLabels(node);
    applyDisabled(node);
  }

  function track(node) {
    insertSeparators(node);
    makeWarningWidget(node);
    sync(node);
    tracked.add(node);

    for (const widget of widgetsOf(node)) {
      if (!widget?.name || widget._sxsSeparator) continue;
      const previous = widget.callback;
      widget.callback = function () {
        const result = previous?.apply(this, arguments);
        sync(node);
        return result;
      };
    }

    const previousRemoved = node.onRemoved;
    node.onRemoved = function () {
      tracked.delete(node);
      return previousRemoved?.apply(this, arguments);
    };

    const previousExecuted = node.onExecuted;
    node.onExecuted = function (message) {
      const result = previousExecuted?.apply(this, arguments);
      showWarning(node, pickWarn(message));
      return result;
    };

    const previousConfigure = node.onConfigure;
    node.onConfigure = function () {
      const result = previousConfigure?.apply(this, arguments);
      sync(node);
      return result;
    };
  }

  const onLocaleChange = () => {
    for (const node of tracked) sync(node);
  };

  try {
    app?.ui?.settings?.addEventListener?.('Comfy.Locale.change', onLocaleChange);
  } catch {
    /* фронтенд без legacy-событий настроек */
  }

  app.registerExtension({
    name: 'SXS.ScenePrompt',
    beforeRegisterNodeDef(nodeType, nodeData) {
      if (!NODE_KEYS.includes(nodeData?.name)) return;
      const previous = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = function () {
        const result = previous?.apply(this, arguments);
        track(this);
        return result;
      };
    },
  });

  globalThis.__SXS__ = {
    NODE_KEYS,
    GROUPS,
    RU_LABELS,
    RANGE,
    readLocale,
    menuOverride,
    activeLang,
    labelFor,
    applyWidgetLabels,
    applyDisabled,
    pickWarn,
  };
})();
