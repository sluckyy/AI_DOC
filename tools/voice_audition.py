#!/usr/bin/env python3
"""Blind voice audition for Dr Sam (decision D-08).

Synthesises three Dr Sam passages in every Australian, New Zealand and British
English neural voice on Azure AI Speech, at two pitch settings, and writes the
clips under random names with a rating sheet and a sealed answer key. Raters
listen without knowing the voice; you open the key afterwards.

Set-up (once):
    pip install requests
    export AZURE_SPEECH_KEY=<key from the Azure portal>      # never commit this
    export AZURE_SPEECH_REGION=australiaeast

Run:
    python tools/voice_audition.py --out audition
    python tools/voice_audition.py --list                    # voices only, no audio
    python tools/voice_audition.py --out audition --locales en-AU --pitches 0% -6%

Output:
    audition/clips/<id>.mp3        one clip per voice x passage x pitch
    audition/rating_sheet.csv      one row per clip for raters to fill in
    audition/answer_key.csv        clip id -> voice, passage, pitch (keep from raters)

The rating sheet asks each rater: perceived gender (1 = clearly masculine,
3 = could be either, 5 = clearly feminine), warmth (1 to 5), credibility (1 to 5).
Pick the voice whose gender ratings cluster at 3, then break ties on warmth.
"""
from __future__ import annotations

import argparse
import csv
import os
import random
import sys
import time
import uuid
from html import escape
from pathlib import Path

try:
    import requests
except ImportError:  # pragma: no cover
    sys.exit("pip install requests")

PASSAGES = {
    "opening": (
        "Hello, I'm Dr Sam. I'm an AI, and I work with the doctors here. "
        "Before you see the doctor I'd like to hear, in your own words, what's brought you in. "
        "Take your time."
    ),
    "reflection": (
        "So the pain started about a week ago, it's worse at night, "
        "and the thing you're most worried about is that it's the same as your dad's. "
        "Have I got that right?"
    ),
    "safety_net": (
        "What you've just described is something that needs a real person right now. "
        "Please call triple zero, or ask someone near you to. "
        "I'll stop here so you can do that."
    ),
}

DEFAULT_LOCALES = ["en-AU", "en-NZ", "en-GB"]
DEFAULT_PITCHES = ["0%", "-5%"]
RATE = "-8%"
OUTPUT_FORMAT = "audio-24khz-48kbitrate-mono-mp3"


def env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        sys.exit(f"{name} is not set")
    return value


def list_voices(region: str, key: str, locales: list[str]) -> list[dict]:
    url = f"https://{region}.tts.speech.microsoft.com/cognitiveservices/voices/list"
    response = requests.get(url, headers={"Ocp-Apim-Subscription-Key": key}, timeout=30)
    response.raise_for_status()
    voices = [
        v for v in response.json()
        if v.get("Locale") in locales and v.get("VoiceType") == "Neural"
    ]
    return sorted(voices, key=lambda v: (v["Locale"], v["ShortName"]))


def ssml(voice: str, locale: str, text: str, pitch: str) -> str:
    return (
        '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
        f'xml:lang="{locale}">'
        f'<voice name="{voice}"><prosody rate="{RATE}" pitch="{pitch}">'
        f"{escape(text)}"
        "</prosody></voice></speak>"
    )


def synthesise(region: str, key: str, body: str) -> bytes:
    url = f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": OUTPUT_FORMAT,
        "User-Agent": "aidoc-voice-audition",
    }
    for attempt in range(4):
        response = requests.post(url, headers=headers, data=body.encode("utf-8"), timeout=60)
        if response.status_code == 429:
            time.sleep(2 ** attempt)
            continue
        response.raise_for_status()
        return response.content
    raise RuntimeError("rate limited four times; try again later")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", default="audition", help="output folder")
    parser.add_argument("--locales", nargs="+", default=DEFAULT_LOCALES)
    parser.add_argument("--pitches", nargs="+", default=DEFAULT_PITCHES, help='SSML pitch values, e.g. 0%% -5%%')
    parser.add_argument("--voices", nargs="*", help="restrict to these ShortNames")
    parser.add_argument("--list", action="store_true", help="list candidate voices and exit")
    parser.add_argument("--seed", type=int, default=None, help="shuffle seed for reproducible ids")
    args = parser.parse_args()

    key = env("AZURE_SPEECH_KEY")
    region = env("AZURE_SPEECH_REGION")

    voices = list_voices(region, key, args.locales)
    if args.voices:
        wanted = set(args.voices)
        voices = [v for v in voices if v["ShortName"] in wanted]
    if not voices:
        sys.exit("no candidate voices found")

    print(f"{len(voices)} candidate voices:")
    for v in voices:
        styles = ",".join(v.get("StyleList", [])) or "-"
        print(f"  {v['ShortName']:<32} {v['Locale']}  labelled {v['Gender']:<7} styles: {styles}")
    if args.list:
        return

    out = Path(args.out)
    clips = out / "clips"
    clips.mkdir(parents=True, exist_ok=True)

    jobs = [
        (v, passage, pitch)
        for v in voices
        for passage in PASSAGES
        for pitch in args.pitches
    ]
    rng = random.Random(args.seed)
    rng.shuffle(jobs)
    print(f"synthesising {len(jobs)} clips into {clips} ...")

    key_rows, sheet_rows = [], []
    for index, (voice, passage, pitch) in enumerate(jobs, start=1):
        clip_id = uuid.uuid4().hex[:8]
        path = clips / f"{clip_id}.mp3"
        if not path.exists():
            audio = synthesise(region, key, ssml(voice["ShortName"], voice["Locale"], PASSAGES[passage], pitch))
            path.write_bytes(audio)
            time.sleep(0.3)
        key_rows.append({"clip": clip_id, "voice": voice["ShortName"], "labelled_gender": voice["Gender"],
                         "passage": passage, "pitch": pitch})
        sheet_rows.append({"clip": clip_id, "rater": "", "perceived_gender_1_masc_3_either_5_fem": "",
                           "warmth_1_5": "", "credibility_1_5": "", "notes": ""})
        print(f"  {index}/{len(jobs)} {clip_id}", end="\r")
    print()

    with (out / "answer_key.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(key_rows[0].keys()))
        writer.writeheader()
        writer.writerows(key_rows)
    with (out / "rating_sheet.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(sheet_rows[0].keys()))
        writer.writeheader()
        writer.writerows(sheet_rows)

    print(f"done. Give raters {clips} and {out / 'rating_sheet.csv'}; keep {out / 'answer_key.csv'} sealed.")


if __name__ == "__main__":
    main()
