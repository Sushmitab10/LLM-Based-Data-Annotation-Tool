from annotation_service import mock_annotate

test_sentences = [
    "I love this product",
    "This is an excellent application",
    "The service is very bad",
    "I am not happy with the result",
    "The product is available"
]

print("\nAI Annotation Demo Results")
print("-" * 40)

for sentence in test_sentences:
    result = mock_annotate(sentence)

    print("Text:", sentence)
    print("Label:", result["label"])
    print("Source:", result["source"])
    print("-" * 40)