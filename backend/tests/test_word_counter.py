from app.utils.word_counter import count_words, truncate_at_sentence_boundary


def test_count_words():
    assert count_words("One two, three.") == 3


def test_truncate_at_sentence_boundary():
    text = "One two three. " + "word " * 900
    result = truncate_at_sentence_boundary(text, max_words=5)
    assert len(result.split()) <= 5
