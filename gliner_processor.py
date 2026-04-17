from gliner import GLiNER

# Lazy-loaded model — avoids blocking startup
_model = None


def get_model():
    global _model
    if _model is None:
        print("Loading GLiNER model...")
        _model = GLiNER.from_pretrained("urchade/gliner_base")
        print("GLiNER model loaded.")
    return _model


def extract_entities(text):
    labels = [
        "country",
        "person",
        "organization",
        "event",
        "date"
    ]

    entities = get_model().predict_entities(text, labels)

    # Deduplicate by (text, label) — keeps highest confidence score
    seen = {}
    for e in entities:
        key = (e["text"].lower(), e["label"])
        if key not in seen or e["score"] > seen[key]["score"]:
            seen[key] = e

    deduplicated = list(seen.values())

    return deduplicated
