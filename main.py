import json
from generator import generate_document
from output import save_pdf
from docling_processor import extract_data
from gliner_processor import extract_entities


def main():
    topic = input("Enter topic: ")
    pages = int(input("Enter number of pages: "))

    print(f"\nGenerating document on: '{topic}' ({pages} page(s))...\n")

    # ─────────────────────────────────────────
    # STEP 1: Generate content via Ollama LLM
    # ─────────────────────────────────────────
    data = generate_document(topic, pages)
    print("Document generated successfully.\n")

    # ─────────────────────────────────────────
    # STEP 2: Save as PDF using ReportLab
    # ─────────────────────────────────────────
    save_pdf(data, topic)

    # ─────────────────────────────────────────
    # STEP 3: Parse PDF with Docling
    # ─────────────────────────────────────────
    print("Parsing PDF with Docling...")
    doc_data = extract_data("dataset.pdf")

    text = doc_data["text"]
    sections = doc_data.get("sections", [])

    with open("extracted_text.txt", "w", encoding="utf-8") as f:
        f.write(text)

    with open("docling_output.json", "w", encoding="utf-8") as f:
        json.dump(doc_data["json"], f, indent=2, ensure_ascii=False)

    with open("structured_output.json", "w", encoding="utf-8") as f:
        json.dump(sections, f, indent=2, ensure_ascii=False)

    print(f"Docling extracted {len(sections)} section(s).\n")

    # ─────────────────────────────────────────
    # STEP 4: Named Entity Recognition — GLiNER
    # ─────────────────────────────────────────
    print("Running GLiNER entity extraction...")
    entities = extract_entities(text)

    print(f"\n--- Extracted Entities ({len(entities)} unique) ---\n")
    for e in entities[:15]:
        score = round(e["score"], 3)
        print(f"  {e['text']:<30} → {e['label']:<15} (score: {score})")

    with open("entities.json", "w", encoding="utf-8") as f:
        json.dump(entities, f, indent=2, ensure_ascii=False)

    # ─────────────────────────────────────────
    # STEP 5: Summary
    # ─────────────────────────────────────────
    print("\n✅ Pipeline complete. Output files:")
    print("   • dataset.pdf            — generated document")
    print("   • extracted_text.txt     — plain text from Docling")
    print("   • docling_output.json    — full Docling JSON")
    print("   • structured_output.json — section-by-section structure")
    print("   • entities.json          — named entities from GLiNER\n")


if __name__ == "__main__":
    main()
