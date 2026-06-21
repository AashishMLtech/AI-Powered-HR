from app.ai.client_factory import get_llm_client
from app.utils.word_counter import count_words, truncate_at_sentence_boundary


async def rewrite_jd(raw_text: str, title: str) -> str:
    client = get_llm_client()
    jd = await client.rewrite_jd(raw_text=raw_text, title=title)
    if count_words(jd) <= 800:
        return jd
    return truncate_at_sentence_boundary(jd, max_words=800)
