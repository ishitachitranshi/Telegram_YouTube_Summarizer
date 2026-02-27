from typing import List, Dict, Any


def sec_to_hhmmss(sec: float) -> str:
    sec = int(sec or 0)
    m = sec // 60
    s = sec % 60
    return f"{m:02d}:{s:02d}"


def chunk_transcript(items: List[Dict[str, Any]], max_chars: int = 1200):
    chunks = []
    buffer = []
    length = 0
    start_ts = 0

    for item in items:
        text = item.get("text", "").strip()
        if not text:
            continue

        if not buffer:
            start_ts = item.get("start", 0)

        if length + len(text) > max_chars:
            chunks.append({
                "ts": sec_to_hhmmss(start_ts),
                "text": " ".join(buffer)
            })
            buffer = []
            length = 0
            start_ts = item.get("start", 0)

        buffer.append(text)
        length += len(text)

    if buffer:
        chunks.append({
            "ts": sec_to_hhmmss(start_ts),
            "text": " ".join(buffer)
        })

    return chunks
