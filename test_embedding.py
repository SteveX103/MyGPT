from services.embedding_service import generate_embedding


text = """
Cloud computing provides on-demand access
to computing resources over a network.
"""

embedding = generate_embedding(text)

print("Embedding dimensions:", len(embedding))

print("\nFirst 10 values:")
print(embedding[:10])