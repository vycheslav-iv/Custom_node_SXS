// JS-смоук SXS: исполняет web/js/sxs.js в vm-контексте с заглушкой
// window/comfyAPI и проверяет:
//   • расширение регистрируется и трогает только класс SXS;
//   • подписи combo меняются RU/EN через getOptionLabel;
//   • ПРОТОКОЛЬНЫЕ значения и options.values не подменяются;
//   • смена Comfy.Locale переприменяет подписи и сепараторы на лету;
//   • «Язык_меню» переопределяет локаль;
//   • делегированные LLM поля гасятся через widget.disabled;
//   • WARN-бейдж показывает предупреждение и скрывается на пустом;
//   • onRemoved снимает ноду со слежения; нет таймеров.
//
// Запуск:  cd SXS && node tests/_smoke_sxs.mjs
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const ROOT = fileURLToPath(new URL("..", import.meta.url));
const JS = path.join(ROOT, "web", "js", "sxs.js");

const errors = [];
const oks = [];
const check = (label, cond, extra = "") => {
  (cond ? oks : errors).push(label);
  if (!cond) console.log(`  FAIL  ${label}${extra ? "  [" + extra + "]" : ""}`);
  else console.log(`  ok    ${label}`);
};

const registered = [];
const localeEvents = [];
const state = { locale: "ru" };

const app = {
  registerExtension: (ext) => registered.push(ext),
  ui: {
    settings: {
      addEventListener: (event, fn) => localeEvents.push({ event, fn }),
      removeEventListener: () => {},
    },
  },
  extensionManager: {
    setting: {
      get: (key) => {
        if (key !== "Comfy.Locale") return undefined;
        if (state.throwOnRead) throw new Error("stub failure");
        return state.locale;
      },
    },
  },
};

function makeElement() {
  return {
    className: "",
    textContent: "",
    title: "",
    dataset: {},
    style: { cssText: "", display: "none" },
  };
}

const ctx = {
  console,
  Math,
  JSON,
  Number,
  String,
  Array,
  Object,
  Set,
  Date,
  document: { createElement: makeElement },
  window: { comfyAPI: { app: { app } } },
};
ctx.globalThis = ctx;
vm.createContext(ctx);

const src = fs.readFileSync(JS, "utf8");
vm.runInContext(src, ctx, { filename: JS });

const hooks = ctx.__SXS__;
check("test hooks exposed", !!hooks && typeof hooks.applyWidgetLabels === "function");
check("single node key", !!hooks && hooks.NODE_KEYS.length === 1 && hooks.NODE_KEYS[0] === "SXS");
check("extension registered", registered.length === 1, String(registered.length));
check("extension name", registered[0]?.name === "SXS.ScenePrompt", registered[0]?.name);
check("one locale listener", localeEvents.length === 1 && localeEvents[0].event === "Comfy.Locale.change", JSON.stringify(localeEvents.map((e) => e.event)));

const NAMES = [
  "seed", "Язык_меню", "Язык_промпта", "Управление",
  "Девушки", "Парни", "Распределение", "Авто_пары", "Кто_с_кем",
  "Фокус_на", "Политика_отсутствующего", "Пол_1",
  "Пресет_сцены", "Тип", "Тип_выбирает_LLM", "Этап_сцены", "Куда_кончает",
  "Тип_группа_basic", "Совместимость", "Взаимодействия", "Эмоции", "Темп", "Одежда",
  "Позы_выбирает_LLM", "Позы_группа_stand", "Поза", "Взгляд",
  "Кто_сверху", "Положение_камеры",
  "Камера_выбирает_LLM", "Ракурс", "План", "Фокус", "Ракурсы_вкл",
  "Планы_вкл", "Фокусы_вкл", "Уровень_камеры", "POV", "Композиция",
  "Кроп", "Куда_смотрит_камера", "Зум",
  "Окружение_выбирает_LLM", "Фон", "Освещение", "Время_суток",
  "Атмосфера", "Сеттинг", "Фоны_вкл", "Свет_вкл", "Время_вкл",
  "Атмосфера_вкл", "Сеттинг_вкл",
  "Формат_промпта", "Модель", "Стиль", "Качество", "Quality_tokens",
  "Всё_выбирает_LLM", "Свобода_LLM", "Запреты", "Явные_термины",
  "config", "char_1", "char_2", "char_3", "char_4", "char_5", "char_6",
];

const VALUES = {
  seed: 0,
  "Язык_меню": "auto",
  "Язык_промпта": "en",
  "Управление": "hybrid",
  "Девушки": "auto",
  "Парни": "auto",
  "Распределение": "by_connection",
  "Авто_пары": true,
  "Кто_с_кем": "",
  "Фокус_на": "auto",
  "Политика_отсутствующего": "partial",
  "Пол_1": "auto",
  "Пресет_сцены": "none",
  "Тип": "classic",
  "Тип_выбирает_LLM": false,
  "Этап_сцены": "auto",
  "Куда_кончает": "auto",
  "Тип_группа_basic": true,
  "Совместимость": "strict",
  "Взаимодействия": "",
  "Эмоции": "auto",
  "Темп": "auto",
  "Одежда": "auto",
  "Позы_выбирает_LLM": false,
  "Позы_группа_stand": true,
  "Поза": "standing",
  "Взгляд": "auto",
  "Кто_сверху": "auto",
  "Положение_камеры": "auto",
  "Камера_выбирает_LLM": false,
  "Ракурс": "front",
  "План": "medium",
  "Фокус": "face",
  "Ракурсы_вкл": true,
  "Планы_вкл": true,
  "Фокусы_вкл": true,
  "Уровень_камеры": "auto",
  "POV": false,
  "Композиция": "auto",
  "Кроп": "auto",
  "Куда_смотрит_камера": "auto",
  "Зум": "none",
  "Окружение_выбирает_LLM": false,
  "Фон": "bedroom",
  "Освещение": "soft",
  "Время_суток": "auto",
  "Атмосфера": "auto",
  "Сеттинг": "auto",
  "Фоны_вкл": true,
  "Свет_вкл": true,
  "Время_вкл": true,
  "Атмосфера_вкл": true,
  "Сеттинг_вкл": true,
  "Формат_промпта": "natural",
  "Модель": "universal",
  "Стиль": "photoreal",
  "Качество": "high",
  "Quality_tokens": true,
  "Всё_выбирает_LLM": false,
  "Свобода_LLM": "from_lists",
  "Запреты": "",
  "Явные_термины": true,
  config: "",
  char_1: "",
  char_2: "",
  char_3: "",
  char_4: "",
  char_5: "",
  char_6: "",
};

function makeWidget(name) {
  const values = [VALUES[name]];
  return {
    name,
    value: VALUES[name],
    label: name,
    disabled: false,
    serialize: true,
    options: { values },
  };
}

function makeNode() {
  const node = {
    widgets: [],
    dirty: 0,
    size: [320, 200],
    addDOMWidget(name, type, element, options) {
      const widget = { name, type, element, options, value: null, serialize: true };
      this.widgets.push(widget);
      return widget;
    },
    setDirtyCanvas() {
      this.dirty += 1;
    },
  };
  node.widgets = NAMES.map(makeWidget);
  return node;
}

function wireNode(nodeType, name = "SXS") {
  registered[0].beforeRegisterNodeDef(nodeType, { name }, app);
  const instance = Object.create(nodeType.prototype);
  const base = makeNode();
  instance.widgets = base.widgets;
  instance.size = base.size;
  instance.addDOMWidget = base.addDOMWidget;
  instance.setDirtyCanvas = base.setDirtyCanvas.bind(base);
  instance.onNodeCreated();
  return { instance, base };
}

const nodeType = function NodeType() {};
nodeType.prototype.onNodeCreated = function () {};
const { instance, base } = wireNode(nodeType);
const widgets = instance.widgets;
const byName = (name) => widgets.find((w) => w.name === name);
const sepWidgets = widgets.filter((w) => w._sxsSeparator);

check("seven separators", sepWidgets.length === 7, String(sepWidgets.length));
check("first separator is SETUP (RU)", sepWidgets[0]?._sepEl.textContent === "═══ НАСТРОЙКА ═══", sepWidgets[0]?._sepEl.textContent);
check("characters separator present", sepWidgets.some((w) => w._sepEl.textContent.includes("ПЕРСОНАЖИ")));
check("poses separator present", sepWidgets.some((w) => w._sepEl.textContent.includes("ПОЗА")));

for (const name of ["Тип", "Поза", "Ракурс", "Фон", "Формат_промпта"]) {
  check(`getOptionLabel on ${name}`, typeof byName(name)?.options.getOptionLabel === "function");
}
check("RU type label", byName("Тип").options.getOptionLabel("classic") === "Классический", byName("Тип").options.getOptionLabel("classic"));
check("RU pose label", byName("Поза").options.getOptionLabel("standing") === "Стоя", byName("Поза").options.getOptionLabel("standing"));
check("RU format label", byName("Формат_промпта").options.getOptionLabel("natural") === "Проза");
check("RU gender label", byName("Пол_1").options.getOptionLabel("female") === "Женский");
check("RU stage label", byName("Этап_сцены").options.getOptionLabel("insertion") === "Только вставляет", byName("Этап_сцены").options.getOptionLabel("insertion"));
check("RU finish label", byName("Куда_кончает").options.getOptionLabel("inside") === "Внутрь", byName("Куда_кончает").options.getOptionLabel("inside"));
check("unknown value passes through", byName("Тип").options.getOptionLabel("custom_type") === "custom type", byName("Тип").options.getOptionLabel("custom_type"));
check("protocol values untouched", JSON.stringify(byName("Тип").options.values) === JSON.stringify(["classic"]));
check("widget value untouched", byName("Тип").value === "classic");

state.locale = "en";
localeEvents[0].fn();
check("EN type label after event", byName("Тип").options.getOptionLabel("classic") === "classic", byName("Тип").options.getOptionLabel("classic"));
check("EN stage label after event", byName("Этап_сцены").options.getOptionLabel("insertion") === "insertion");
check("EN separator after event", sepWidgets[0]._sepEl.textContent === "═══ SETUP ═══", sepWidgets[0]._sepEl.textContent);
state.locale = "ru-RU";
localeEvents[0].fn();
check("ru-RU counts as Russian", byName("Тип").options.getOptionLabel("classic") === "Классический");
state.locale = "de";
localeEvents[0].fn();
check("other locale falls back to English", byName("Тип").options.getOptionLabel("classic") === "classic");

state.locale = "en";
byName("Язык_меню").value = "ru";
byName("Язык_меню").callback("ru");
check("menu override forces Russian", byName("Тип").options.getOptionLabel("classic") === "Классический", byName("Тип").options.getOptionLabel("classic"));
check("activeLang sees override", hooks.activeLang(instance) === "ru", hooks.activeLang(instance));
byName("Язык_меню").value = "auto";
byName("Язык_меню").callback("auto");

state.locale = "ru";
byName("Этап_сцены").value = "insertion";
byName("Этап_сцены").callback("insertion");
check("non-finish stage disables finish target", byName("Куда_кончает").disabled === true);
byName("Этап_сцены").value = "finish";
byName("Этап_сцены").callback("finish");
check("finish stage enables finish target", byName("Куда_кончает").disabled === false);

byName("Позы_выбирает_LLM").value = true;
byName("Позы_выбирает_LLM").callback(true);
check("pose delegated disables pose", byName("Поза").disabled === true);
check("pose delegated keeps toggle enabled", byName("Позы_выбирает_LLM").disabled === false);
check("pose delegated disables groups", byName("Позы_группа_stand").disabled === true);
byName("Позы_выбирает_LLM").value = false;
byName("Позы_выбирает_LLM").callback(false);
check("pose released enables pose", byName("Поза").disabled === false);

byName("Всё_выбирает_LLM").value = true;
byName("Всё_выбирает_LLM").callback(true);
check("master disables type", byName("Тип").disabled === true);
check("master disables camera", byName("Ракурс").disabled === true);
check("master disables environment", byName("Фон").disabled === true);
check("master disables sub toggles", byName("Камера_выбирает_LLM").disabled === true);
byName("Всё_выбирает_LLM").value = false;
byName("Всё_выбирает_LLM").callback(false);
check("master released re-enables type", byName("Тип").disabled === false);

check("warn hidden initially", instance._sxsWarnEl.style.display === "none");
instance.onExecuted({ WARN: ["cast mismatch"] });
check("warn badge shown", instance._sxsWarnEl.style.display === "flex" && instance._sxsWarnEl.textContent === "cast mismatch", instance._sxsWarnEl.textContent);
instance.onExecuted({ WARN: [""] });
check("warn badge hidden on empty", instance._sxsWarnEl.style.display === "none");

check("readLocale survives throwing settings", (() => {
  state.throwOnRead = true;
  const value = hooks.readLocale();
  state.throwOnRead = false;
  return value === "en";
})());

{
  state.locale = "ru";
  const removedType = function NodeType2() {};
  removedType.prototype.onNodeCreated = function () {};
  const { instance: second } = wireNode(removedType);
  const typeWidget = second.widgets.find((w) => w.name === "Тип");
  check("second node labelled", typeWidget.options.getOptionLabel("classic") === "Классический");
  second.onRemoved?.();
  state.locale = "en";
  localeEvents[0].fn();
  check("removed node is no longer updated", typeWidget.options.getOptionLabel("classic") === "Классический", typeWidget.options.getOptionLabel("classic"));
  state.locale = "ru";
}

{
  const foreignType = function NodeType3() {};
  const before = foreignType.prototype.onNodeCreated;
  registered[0].beforeRegisterNodeDef(foreignType, { name: "Other" }, app);
  check("foreign node untouched", foreignType.prototype.onNodeCreated === before);
}

check("no setTimeout", !/setTimeout\s*\(/.test(src));
check("no setInterval", !/setInterval\s*\(/.test(src));
check("no options.values assignment", !/options\s*\.\s*values\s*=/.test(src));
check("no computeSize override", !/\.computeSize\s*=/.test(src));
check("no legacy import", !/scripts\/app\.js/.test(src));

console.log("");
console.log(`ok: ${oks.length}   FAIL: ${errors.length}`);
if (errors.length) {
  console.log("SMOKE FAILED");
  process.exit(1);
}
console.log("SMOKE OK");
