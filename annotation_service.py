def mock_annotate(text):
    """
    Temporary demo annotation.
    This is NOT an actual LLM prediction.
    """

    text = text.lower()

    positive_words = [
        "love", "excellent", "good",
        "great", "happy", "amazing"
    ]

    negative_words = [
        "bad", "poor", "hate",
        "unhappy", "not happy", "terrible"
    ]

    if any(word in text for word in negative_words):
        label = "Negative"

    elif any(word in text for word in positive_words):
        label = "Positive"

    else:
        label = "Neutral"

    return {
        "text": text,
        "label": label,
        "source": "Demo mode"
    }