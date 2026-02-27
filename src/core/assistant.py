import re
import math
from typing import Dict, Any, List

from .youtube_utils import get_transcript
from .chunking import chunk_transcript


def detect_requested_lang(text: str):
    ascii_ratio = sum(1 for c in text if ord(c) < 128) / max(1, len(text))
    return "en" if ascii_ratio > 0.7 else "hi"


def tokenize(text):
    return re.findall(r"\w+", text.lower())


def tfidf_rank(chunks, query, top_k=3):
    query_tokens = tokenize(query)
    scores = []

    for chunk in chunks:
        tokens = tokenize(chunk["text"])
        score = sum(tokens.count(q) for q in query_tokens)
        scores.append((score, chunk))

    scores.sort(reverse=True, key=lambda x: x[0])
    return [c for s, c in scores[:top_k] if s > 0]


class YouTubeResearchAssistant:

    def __init__(self):
        self.sessions: Dict[int, Dict[str, Any]] = {}

    def handle_youtube_link(self, chat_id, url, lang):
        vid, items, kind, used_lang = get_transcript(url, ["hi", "en"])

        if not items:
            return "Transcript not available."

        chunks = chunk_transcript(items)
        self.sessions[chat_id] = {"chunks": chunks}

        preview = "\n".join(
            f"[{c['ts']}] {c['text'][:120]}..." for c in chunks[:5]
        )

        return f"Transcript fetched.\n\nPreview:\n{preview}\n\nAsk questions."

    def answer_question(self, chat_id, question, lang):
        if chat_id not in self.sessions:
            return "Send YouTube link first."

        chunks = self.sessions[chat_id]["chunks"]
        matches = tfidf_rank(chunks, question)

        if not matches:
            return "This topic is not covered in the video."

        result = "Found in video:\n\n"
        for m in matches:
            result += f"[{m['ts']}] {m['text']}\n\n"

        return result
