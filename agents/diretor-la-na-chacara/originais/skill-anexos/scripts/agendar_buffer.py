#!/usr/bin/env python3
"""Agendador Buffer — Lá na Chácara.
Usa BUFFER_ACCESS_TOKEN do ambiente. Nunca hardcode.
"""
import argparse, json, os, sys, urllib.parse, urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

BASE = "https://api.bufferapp.com/1"


def _token():
    t = os.environ.get("BUFFER_ACCESS_TOKEN")
    if not t:
        sys.exit("❌ BUFFER_ACCESS_TOKEN ausente. Agende manualmente no app do Buffer.")
    return t


def _get(path):
    url = f"{BASE}{path}{'&' if '?' in path else '?'}access_token={_token()}"
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.loads(r.read().decode())


def _post(path, fields):
    data = urllib.parse.urlencode({**fields, "access_token": _token()}, doseq=True).encode()
    req = urllib.request.Request(f"{BASE}{path}", data=data)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def list_profiles():
    for p in _get("/profiles.json"):
        print(f"{p['id']}  {p['service']:12s} @{p.get('service_username', '?')}")


def schedule(profile, text, media_url, when, tz):
    dt = datetime.strptime(when, "%Y-%m-%d %H:%M").replace(tzinfo=ZoneInfo(tz))
    fields = {
        "profile_ids[]": profile,
        "text": text,
        "scheduled_at": dt.isoformat(),
    }
    if media_url:
        fields["media[photo]"] = media_url
    resp = _post("/updates/create.json", fields)
    if resp.get("success"):
        print(f"✅ Agendado para {dt.isoformat()} — id {resp['updates'][0]['id']}")
    else:
        print("⚠️ Resposta inesperada (agende manualmente ou use o adaptador Kraken):")
        print(json.dumps(resp, indent=2, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list-profiles", action="store_true")
    ap.add_argument("--profile")
    ap.add_argument("--text")
    ap.add_argument("--media", help="URL pública da imagem")
    ap.add_argument("--when", help="YYYY-MM-DD HH:MM (hora local)")
    ap.add_argument("--tz", default="America/Sao_Paulo")
    a = ap.parse_args()

    if a.list_profiles:
        list_profiles()
        return
    if not (a.profile and a.text and a.when):
        ap.error("--profile, --text e --when são obrigatórios")
    schedule(a.profile, a.text, a.media, a.when, a.tz)


if __name__ == "__main__":
    main()
