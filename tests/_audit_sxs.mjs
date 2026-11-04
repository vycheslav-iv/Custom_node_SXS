// Статический аудит SXS: без ComfyUI и без браузера.
//
// Проверяет структуру проекта, документы, check.json, паритет локалей,
// UTF-8 без BOM, отсутствие CJK, контракт Python и запрещённые приёмы JS.
// Кириллица в Python здесь НЕ запрещена: русские идентификаторы виджетов
// (Тип, Поза, ...) — часть контракта ноды; английским обязан быть только
// DESCRIPTION, а не имена полей.
//
// Запуск:  cd SXS && node tests/_audit_sxs.mjs
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = fileURLToPath(new URL("..", import.meta.url));
const failures = [];
const oks = [];

function check(label, cond, extra = "") {
  if (cond) {
    oks.push(label);
    console.log(`  ok    ${label}`);
  } else {
    failures.push(label);
    console.log(`  FAIL  ${label}${extra ? "  [" + extra + "]" : ""}`);
  }
}

function read(rel) {
  return fs.readFileSync(path.join(ROOT, rel), "utf8");
}

function exists(rel) {
  return fs.existsSync(path.join(ROOT, rel));
}

function findFiles(dir, ext, out = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === ".git" || entry.name === "__pycache__") continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) findFiles(full, ext, out);
    else if (entry.name.endsWith(ext)) out.push(full);
  }
  return out;
}

function walkText(dir, out = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === ".git" || entry.name === "__pycache__") continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walkText(full, out);
    else if (/\.(py|js|mjs|json|md|txt)$/i.test(entry.name)) out.push(full);
  }
  return out;
}

const FILES = [
  "__init__.py",
  "sxs_node.py",
  "sxs_data.py",
  "sxs_phrases.py",
  "sxs_compat.py",
  "sxs_brief.py",
  "web/js/sxs.js",
  "locales/en/nodeDefs.json",
  "locales/ru/nodeDefs.json",
  "tests/_test_sxs.py",
  "tests/_smoke_sxs.mjs",
  "tests/_audit_sxs.mjs",
  "check.json",
  "README.md",
  "SPECIFICATION.md",
  ".gitignore",
];

console.log("== SXS static audit ==");
for (const rel of FILES) check(`file: ${rel}`, exists(rel));

const py = read("sxs_node.py");
const init = read("__init__.py");
const js = read("web/js/sxs.js");
const test = read("tests/_test_sxs.py");
const readme = read("README.md");
const spec = read("SPECIFICATION.md");
const checkJson = JSON.parse(read("check.json"));

check("python: class SXS", /class\s+SXS\s*:/.test(py));
check("python: build function", /def\s+build\s*\(/.test(py));
check("python: IS_CHANGED", /def\s+IS_CHANGED\s*\(/.test(py));
check("python: category", /CATEGORY\s*=\s*"My_custom_nodes\/SXS"/.test(py));
check("python: FUNCTION build", /FUNCTION\s*=\s*"build"/.test(py));
check("python: 5 return types", /RETURN_TYPES\s*=\s*\(\s*"STRING",\s*"STRING",\s*"STRING",\s*"INT",\s*"STRING"\s*\)/.test(py));
check("python: return names", /RETURN_NAMES\s*=\s*\(\s*"LLM PROMPT",\s*"MODEL PROMPT",\s*"WARN",\s*"SEED",\s*"CONFIG"\s*\)/.test(py));
check("python: DESCRIPTION is English", (() => {
  const match = py.match(/DESCRIPTION\s*=\s*\(([\s\S]*?)\)\s*\n\s*@classmethod/);
  return !!match && !/[\u0400-\u04FF]/.test(match[1]);
})());
check("python: optional config", /"config"\s*:\s*\(\s*"STRING"/.test(py));
check("python: optional char_1..char_6", /f"char_\{i\}"/.test(py) && /range\(1,\s*7\)/.test(py));
check("python: no negative widget", !/"Негатив|negative_prompt|"negative"/i.test(py));
check("python: no age widget", !/"Возраст|"(?:age|Age)"\s*:/i.test(py));
check("python: no length widget", !/"Длина|"(?:length|Length)"\s*:/i.test(py));
check("python: pose LLM default ON", /required\["Позы_выбирает_LLM"\]\s*=\s*_bool\(True\)/.test(py));

check("init: mapping", /NODE_CLASS_MAPPINGS\s*=\s*\{\s*"SXS"\s*:\s*SXS\s*\}/.test(init));
check("init: display name", /SXS Scene Prompt/.test(init));
check("init: web directory", /WEB_DIRECTORY\s*=\s*"\.\/web\/js"/.test(init));

check("js: extension registered", /app\.registerExtension\s*\(/.test(js));
check("js: only SXS", /const\s+NODE_KEYS\s*=\s*\[\s*['"]SXS['"]\s*\]/.test(js));
check("js: getOptionLabel", /getOptionLabel/.test(js));
check("js: locale event", /Comfy\.Locale\.change/.test(js));
check("js: addDOMWidget", /addDOMWidget\s*\(/.test(js));
check("js: separators serialized off", /serialize:\s*false/.test(js));
check("js: hideInPanel", /hideInPanel:\s*true/.test(js));
check("js: warning onExecuted", /onExecuted\s*=/.test(js));
check("js: disabled via widget.disabled", /\.disabled\s*=/.test(js));
check("js: no options.values assignment", !/options\s*\.\s*values\s*=/.test(js));
check("js: no widget.value assignment", !/\.value\s*=\s*/.test(js));
check("js: no setTimeout", !/setTimeout\s*\(/.test(js));
check("js: no setInterval", !/setInterval\s*\(/.test(js));
check("js: no computeSize", !/computeSize\s*=/.test(js));
check("js: no scripts/app.js", !/scripts\/app\.js/.test(js));
check("js: no style.height", !/style\.height\s*=/.test(js));

check("tests: three files", ["_test_sxs.py", "_smoke_sxs.mjs", "_audit_sxs.mjs"].every((f) => exists(`tests/${f}`)));
check("tests: live probe", exists("tests/_probe_live_sxs.py"));
check("tests: python uses ROOT", /Path\(__file__\)\.resolve\(\)\.parent\.parent/.test(test));
check("tests: python prints FAIL", /FAIL:\s*\{FAILS\}/.test(test));
check("doc: README has install", /##\s+Установка/.test(readme));
check("doc: README has outputs", /##\s+Выходы/.test(readme));
check("doc: README has delegation", /##\s+Делегирование LLM/.test(readme));
check("doc: SPEC has contract", /##\s+3\.\s+Контракт ComfyUI/.test(spec));
check("doc: SPEC has locales", /##\s+7\.\s+Интерфейс и локализация/.test(spec));

check("check.json: three checks", Array.isArray(checkJson.checks) && checkJson.checks.length === 3);
check("check.json: python expects", checkJson.checks?.[0]?.expect?.includes("FAIL: 0") === true);
check("check.json: smoke expects", checkJson.checks?.[1]?.expect?.includes("SMOKE OK") === true);
check("check.json: audit expects", checkJson.checks?.[2]?.expect?.includes("аудит чист") === true);
check("check.json: no missing command file", (() => {
  return (checkJson.checks || []).every((item) => {
    const match = String(item.cmd || "").match(/(?:python|node)\s+(tests\/[^\s]+)/);
    return !!match && exists(match[1]);
  });
})());

const en = JSON.parse(read("locales/en/nodeDefs.json"));
const ru = JSON.parse(read("locales/ru/nodeDefs.json"));
const enNode = en.SXS || {};
const ruNode = ru.SXS || {};
check("locales: node key", !!enNode && !!ruNode);
check("locales: display name", enNode.display_name === "SXS Scene Prompt" && !!ruNode.display_name);
check("locales: description", !!enNode.description && !!ruNode.description);
check("locales: input parity", JSON.stringify(Object.keys(enNode.inputs || {}).sort()) === JSON.stringify(Object.keys(ruNode.inputs || {}).sort()));
check("locales: 95 inputs", Object.keys(enNode.inputs || {}).length === 95, String(Object.keys(enNode.inputs || {}).length));
check("locales: 5 outputs", Object.keys(enNode.outputs || {}).length === 5 && Object.keys(ruNode.outputs || {}).length === 5);
check("locales: output parity", JSON.stringify(Object.keys(enNode.outputs || {}).sort()) === JSON.stringify(Object.keys(ruNode.outputs || {}).sort()));
check("locales: every input has name", Object.values(enNode.inputs || {}).every((v) => !!v?.name) && Object.values(ruNode.inputs || {}).every((v) => !!v?.name));
check("locales: every input has tooltip", Object.values(enNode.inputs || {}).every((v) => !!v?.tooltip) && Object.values(ruNode.inputs || {}).every((v) => !!v?.tooltip));
check("locales: protocol field present", !!enNode.inputs?.["Тип"] && !!enNode.inputs?.["Позы_выбирает_LLM"]);
check("locales: scene stage present", !!enNode.inputs?.["Этап_сцены"] && !!ruNode.inputs?.["Этап_сцены"]);
check("locales: finish target present", !!enNode.inputs?.["Куда_кончает"] && !!ruNode.inputs?.["Куда_кончает"]);
check("locales: RU type label", !!ruNode.inputs?.["Тип"]?.name && /[А-Яа-яЁё]/.test(ruNode.inputs["Тип"].name));
check("locales: EN type label ASCII", /^[\x20-\x7E]+$/.test(enNode.inputs?.["Тип"]?.name || ""));

const textFiles = walkText(ROOT);
const cjk = /[\u4E00-\u9FFF\u3040-\u30FF\uAC00-\uD7AF]/;
const bomFiles = [];
const cjkFiles = [];
for (const file of textFiles) {
  const raw = fs.readFileSync(file);
  if (raw.length >= 3 && raw[0] === 0xef && raw[1] === 0xbb && raw[2] === 0xbf) bomFiles.push(path.relative(ROOT, file));
  if (cjk.test(raw.toString("utf8"))) cjkFiles.push(path.relative(ROOT, file));
}
check("encoding: no BOM", bomFiles.length === 0, bomFiles.join(", "));
check("encoding: no CJK", cjkFiles.length === 0, cjkFiles.join(", "));

const pyFiles = findFiles(ROOT, ".py").map((f) => path.relative(ROOT, f)).sort();
check("python files present", pyFiles.filter((f) => !f.startsWith("tests")).length === 6, pyFiles.join(", "));
check("test python files present", pyFiles.filter((f) => f.startsWith("tests")).length === 2, pyFiles.join(", "));
check(".gitignore: cache", /__pycache__/.test(read(".gitignore")));

console.log("");
console.log(`ok: ${oks.length}   FAIL: ${failures.length}`);
if (failures.length) {
  console.log("АУДИТ НЕ ПРОЙДЕН");
  process.exit(1);
}
console.log("аудит чист");
