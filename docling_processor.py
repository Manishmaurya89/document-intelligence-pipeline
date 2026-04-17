from docling.document_converter import DocumentConverter


def is_heading(text):
    """
    Improved heuristic to detect headings.
    Avoids classifying short body sentences as headings.
    """
    words = text.split()

    # Too long to be a heading
    if len(words) >= 6:
        return False

    # Sentences ending in punctuation are body text, not headings
    if text.endswith((".", "?", "!", ":", ",")):
        return False

    # Must start with an uppercase letter
    if not text[0].isupper():
        return False

    return True


def extract_sections(doc_json):
    sections = []
    texts = doc_json.get("texts", [])

    current_section = {
        "heading": "Introduction",
        "content": ""
    }

    for t in texts:
        content = t.get("text", "").strip()

        if not content:
            continue

        if is_heading(content):
            if current_section["content"]:
                sections.append(current_section)

            current_section = {
                "heading": content,
                "content": ""
            }
        else:
            current_section["content"] += " " + content

    if current_section["content"]:
        sections.append(current_section)

    return sections


def extract_data(file_path):
    converter = DocumentConverter()
    result = converter.convert(file_path)

    doc = result.document
    doc_dict = doc.export_to_dict()

    # Extract plain text
    full_text = ""
    for t in doc_dict.get("texts", []):
        full_text += t.get("text", "") + "\n"

    # Extract structured sections
    sections = extract_sections(doc_dict)

    return {
        "text": full_text,
        "json": doc_dict,
        "sections": sections
    }
