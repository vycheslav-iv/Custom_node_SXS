# -*- coding: utf-8 -*-
"""Live probe for SXS against a running ComfyUI (127.0.0.1:8188).

Not part of check.py: needs a running server and a queue.  Verifies that the
node is actually registered, builds a default prompt, executes it with four
PreviewAny sinks and checks the four text outputs.

Run:  cd SXS && python tests/_probe_live_sxs.py
"""
from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.request
import uuid

BASE = "http://127.0.0.1:8188"


def get(path):
    with urllib.request.urlopen(BASE + path, timeout=15) as r:
        return json.loads(r.read().decode("utf-8"))


def post(path, payload):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        BASE + path, data=data, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def default_value(spec):
    if not isinstance(spec, (list, tuple)) or not spec:
        return None
    kind = spec[0]
    opts = spec[1] if len(spec) > 1 and isinstance(spec[1], dict) else {}
    if isinstance(kind, list):
        return opts.get("default", kind[0] if kind else "")
    if "default" in opts:
        return opts["default"]
    return {"INT": 0, "FLOAT": 0.0, "STRING": "", "BOOLEAN": False}.get(kind, "")


def text_of(history, node_id):
    out = (history.get("outputs") or {}).get(str(node_id)) or {}
    for key in ("text", "string", "value"):
        value = out.get(key)
        if isinstance(value, list) and value:
            return value[0]
        if isinstance(value, str):
            return value
    return None


def main():
    try:
        info = get("/object_info/SXS").get("SXS")
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            print("FAIL: SXS not registered — restart ComfyUI after sync.py")
            return 2
        raise
    if not info:
        print("FAIL: no SXS in /object_info — restart ComfyUI after sync.py")
        return 2

    required = info["input"]["required"]
    optional = info["input"].get("optional", {})
    total = len(required) + len(optional)
    print(f"object_info: {total} inputs ({len(required)} required, {len(optional)} optional)")

    inputs = {name: default_value(spec) for name, spec in required.items()}
    inputs["seed"] = 12345
    inputs["char_1"] = "woman"
    inputs["char_2"] = "man"
    inputs["Тип"] = "classic"
    inputs["Этап_сцены"] = "finish"
    inputs["Куда_кончает"] = "inside"
    graph = {"1": {"class_type": "SXS", "inputs": inputs}}
    for idx, slot in enumerate((0, 1, 2, 4), start=10):
        graph[str(idx)] = {
            "class_type": "PreviewAny",
            "inputs": {"source": ["1", slot]},
        }

    prompt_id = post("/prompt", {"prompt": graph, "client_id": uuid.uuid4().hex})["prompt_id"]
    deadline = time.time() + 90
    history = None
    while time.time() < deadline:
        entries = get(f"/history/{prompt_id}")
        if prompt_id in entries:
            history = entries[prompt_id]
            break
        time.sleep(1)
    if history is None:
        print("FAIL: execution did not finish in 90s")
        return 1
    status = history.get("status") or {}
    if status.get("status_str") == "error" or status.get("completed") is False:
        print("FAIL: execution error:")
        print(json.dumps(status, ensure_ascii=False, indent=2)[:4000])
        return 1

    values = [text_of(history, idx) for idx in (10, 11, 12, 13)]
    labels = ("LLM PROMPT", "MODEL PROMPT", "WARN", "CONFIG")
    failures = []
    for label, value in zip(labels, values):
        if not isinstance(value, str):
            failures.append(f"{label} is missing")
        elif label != "WARN" and not value.strip():
            failures.append(f"{label} is empty")
        else:
            print(f"  ok  {label}: {len(value)} chars")

    if values[0] and "[SYSTEM]" not in values[0]:
        failures.append("LLM PROMPT has no [SYSTEM]")
    if values[1] and not values[1].strip():
        failures.append("MODEL PROMPT is empty")
    if values[1] and "ejaculating inside" not in values[1].lower():
        failures.append("MODEL PROMPT lost the finish target")
    if values[3]:
        try:
            cfg = json.loads(values[3])
            if cfg.get("stage") != "finish" or cfg.get("finish_target") != "inside":
                failures.append("CONFIG does not carry stage/finish_target")
        except Exception:
            failures.append("CONFIG is not valid JSON")

    if failures:
        print("FAIL: " + "; ".join(failures))
        return 1
    print("LIVE PROBE OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
