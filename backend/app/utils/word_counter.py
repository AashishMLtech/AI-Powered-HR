import re


def count_words(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def truncate_at_sentence_boundary(text: str, max_words: int = 800) -> str:
    words = text.split()
    if len(words) <= max_words:
        return text

    clipped = " ".join(words[:max_words])
    last_stop = max(clipped.rfind("."), clipped.rfind("!"), clipped.rfind("?"))
    if last_stop > 100:
        return clipped[: last_stop + 1]
    return clipped
