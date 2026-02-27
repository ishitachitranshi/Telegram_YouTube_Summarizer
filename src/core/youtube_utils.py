import re
import sys
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
import json


def extract_video_id(url: str) -> Optional[str]:
    if not url:
        return None
    patterns = [
        r"youtu\.be/([A-Za-z0-9_-]{6,})",
        r"[?&]v=([A-Za-z0-9_-]{6,})",
        r"youtube\.com/shorts/([A-Za-z0-9_-]{6,})"
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return None


def sec_to_hhmmss(sec: float) -> str:
    sec = int(sec or 0)
    h = sec // 3600
    m = (sec % 3600) // 60
    s = sec % 60
    return f"{h:02d}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"


def _run_ytdlp(args: List[str]) -> Tuple[int, str]:
    cmd = [sys.executable, "-m", "yt_dlp"] + args
    try:
        out = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
        return 0, out
    except subprocess.CalledProcessError as e:
        return e.returncode, e.output or str(e)


def _parse_json3(text: str) -> List[Dict[str, Any]]:
    data = json.loads(text)
    events = data.get("events", [])
    items = []
    for ev in events:
        t = ev.get("tStartMs")
        segs = ev.get("segs")
        if t and segs:
            txt = "".join(s.get("utf8", "") for s in segs).strip()
            if txt:
                items.append({"start": float(t) / 1000.0, "text": txt})
    return items


def fetch_transcript(video_id: str, langs: List[str]):
    url = f"https://www.youtube.com/watch?v={video_id}"
    wd = Path.cwd()

    for lang in langs:
        code, _ = _run_ytdlp([
            "--skip-download",
            "--write-auto-subs",
            "--sub-langs", lang,
            "--sub-format", "json3",
            "-o", "%(id)s.%(ext)s",
            url
        ])
        if code == 0:
            files = list(wd.glob(f"{video_id}*.json3"))
            for f in files:
                text = f.read_text(encoding="utf-8", errors="ignore")
                items = _parse_json3(text)
                if items:
                    return items, lang
    return [], None


def get_transcript(url: str, preferred_langs=None):
    vid = extract_video_id(url)
    if not vid:
        return None, [], "error", None

    if preferred_langs is None:
        preferred_langs = ["en"]

    items, used_lang = fetch_transcript(vid, preferred_langs)

    if not items:
        return vid, [], "error", None

    return vid, items, "captions", used_lang
