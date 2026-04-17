from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def save_pdf(data, topic, filename="dataset.pdf"):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    elements = []

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=18,
        spaceAfter=12,
    )

    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        spaceAfter=8,
    )

    normal_style = ParagraphStyle(
        "NormalStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=14,
        spaceAfter=8,
    )

    table_data = []
    in_table = False
    table_rendered = False

    def render_table():
        """Render and append the current table_data to elements."""
        nonlocal table_rendered, table_data, in_table

        if not table_data:
            return

        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 12))

        table_rendered = True
        table_data = []
        in_table = False

    for line in data:
        line = line.strip().replace("**", "")

        if "---" in line:
            continue

        # Title
        if line.startswith("TITLE:"):
            title = line.replace("TITLE:", "").strip()
            elements.append(Paragraph(title, title_style))
            elements.append(Spacer(1, 12))

        # Introduction heading
        elif line.lower().startswith("introduction"):
            elements.append(Spacer(1, 10))
            elements.append(Paragraph("Introduction", heading_style))

        # Section heading
        elif line.lower().startswith("section"):
            parts = line.split(":", 1)
            heading = parts[1].strip() if len(parts) > 1 else line.strip()
            elements.append(Spacer(1, 10))
            elements.append(Paragraph(heading, heading_style))

        # Table start marker
        elif line.startswith("TABLE:"):
            in_table = True
            table_data = []
            table_rendered = False
            elements.append(Spacer(1, 10))

        # Table row (pipe-separated)
        elif "|" in line:
            row = [cell.strip() for cell in line.split("|") if cell.strip()]
            if row:
                # Skip rows with inconsistent column count
                if table_data and len(row) != len(table_data[0]):
                    continue
                if row not in table_data:
                    table_data.append(row)
            in_table = True

        # Conclusion — render pending table first
        elif line.lower().startswith("conclusion"):
            if table_data and not table_rendered:
                render_table()
            in_table = False
            elements.append(Spacer(1, 10))
            elements.append(Paragraph("Conclusion", heading_style))

        # Non-pipe line while in table mode — flush table, then render as normal text
        elif in_table:
            if table_data and not table_rendered:
                render_table()
            elements.append(Paragraph(line, normal_style))

        # Normal body text
        else:
            elements.append(Paragraph(line, normal_style))

    # Final table flush (if not yet rendered)
    if table_data and not table_rendered:
        render_table()

    doc.build(elements)
    print(f"PDF saved as {filename}")
