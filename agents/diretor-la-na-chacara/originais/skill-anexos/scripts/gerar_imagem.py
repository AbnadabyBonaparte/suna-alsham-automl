#!/usr/bin/env python3
"""Gerador unificado de imagens — Lá na Chácara.
Provedores: ideogram | openai | fal
Chaves via variáveis de ambiente. NUNCA hardcode.
"""
import argparse, base64, json, os, sys, time, urllib.request

IDEOGRAM_URL = "https://api.ideogram.ai/generate"
OPENAI_URL = "https://api.openai.com/v1/images/generations"
FAL_MODEL = "fal-ai/flux-2"  # trocar para versão mais nova se a conta tiver
FAL_URL = f"https://queue.fal.run/{FAL_MODEL}"

KEYS = {
    "ideogram": "IDEOGRAM_API_KEY",
    "openai": "OPENAI_API_KEY",
    "fal": "FAL_KEY",
}


def _post(url, headers, payload, timeout=300):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json", **headers})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def _download(url, out):
    with urllib.request.urlopen(url, timeout=120) as r, open(out, "wb") as f:
        f.write(r.read())


def check():
    print("Chaves de API (presença, sem exibir valores):")
    for prov, var in {**KEYS, "buffer": "BUFFER_ACCESS_TOKEN"}.items():
        print(f"  {prov:10s} {var:22s} {'✅ presente' if os.environ.get(var) else '❌ ausente'}")


def gen_ideogram(prompt, aspect, out):
    key = os.environ[KEYS["ideogram"]]
    payload = {"image_request": {
        "prompt": prompt,
        "aspect_ratio": "ASPECT_4_5" if aspect == "4:5" else "ASPECT_1_1",
        "model": "V_2",
        "magic_prompt_option": "OFF",
    }}
    data = _post(IDEOGRAM_URL, {"Api-Key": key}, payload)
    url = data["data"][0]["url"]
    _download(url, out)


def gen_openai(prompt, aspect, out):
    key = os.environ[KEYS["openai"]]
    size = "1024x1536" if aspect == "4:5" else "1024x1024"
    payload = {"model": "gpt-image-1", "prompt": prompt, "size": size, "n": 1}
    data = _post(OPENAI_URL, {"Authorization": f"Bearer {key}"}, payload, timeout=600)
    item = data["data"][0]
    if item.get("b64_json"):
        with open(out, "wb") as f:
            f.write(base64.b64decode(item["b64_json"]))
    else:
        _download(item["url"], out)


def gen_fal(prompt, aspect, out, refs):
    key = os.environ[KEYS["fal"]]
    headers = {"Authorization": f"Key {key}"}
    payload = {"prompt": prompt, "image_size": {"width": 1024, "height": 1280}}
    if refs:
        payload["image_urls"] = refs  # URLs públicas ou data-URIs das referências
    data = _post(FAL_URL, headers, payload)
    status_url = data.get("status_url") or data.get("response_url")
    # polling da fila
    for _ in range(120):
        time.sleep(3)
        req = urllib.request.Request(data["status_url"], headers=headers)
        with urllib.request.urlopen(req, timeout=60) as r:
            st = json.loads(r.read().decode())
        if st.get("status") == "COMPLETED":
            req = urllib.request.Request(data["response_url"], headers=headers)
            with urllib.request.urlopen(req, timeout=60) as r:
                result = json.loads(r.read().decode())
            _download(result["images"][0]["url"], out)
            return
    raise TimeoutError("fal.ai: geração não completou em 6 minutos")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", choices=["ideogram", "openai", "fal"])
    ap.add_argument("--prompt")
    ap.add_argument("--out", default="card.png")
    ap.add_argument("--aspect", default="4:5")
    ap.add_argument("--refs", help="URLs de referência separadas por vírgula (fal)")
    ap.add_argument("--check", action="store_true", help="verifica presença das chaves")
    a = ap.parse_args()

    if a.check:
        check()
        return
    if not a.provider or not a.prompt:
        ap.error("--provider e --prompt são obrigatórios (ou use --check)")
    var = KEYS[a.provider]
    if not os.environ.get(var):
        sys.exit(f"❌ Variável {var} ausente. Modo prompt: cole o prompt manualmente na ferramenta.")

    refs = a.refs.split(",") if a.refs else None
    {"ideogram": lambda: gen_ideogram(a.prompt, a.aspect, a.out),
     "openai": lambda: gen_openai(a.prompt, a.aspect, a.out),
     "fal": lambda: gen_fal(a.prompt, a.aspect, a.out, refs)}[a.provider]()
    print(f"✅ Imagem salva em {a.out}")


if __name__ == "__main__":
    main()
