import json
from docx import Document

def extract_docx_content(docx_file):
    doc = Document(docx_file)

    content = {
        "document": [],
        "metadata": {
            "page_count": 0  # Unfortunately, python-docx doesn't support page numbers. Page count may be handled by external tools.
        }
    }

    current_section = None

    for para in doc.paragraphs:
        # Extract headings as sections
        if para.style.name.startswith('Heading'):
            # When a new section is found, add the previous section to the document structure
            if current_section:
                content['document'].append(current_section)
            # Create a new section with the heading
            current_section = {
                "section_title": para.text,
                "section_level": para.style.name,  # E.g., 'Heading 1', 'Heading 2'
                "content": []
            }
        else:
            # Add the paragraph to the current section's content
            if current_section:
                current_section["content"].append({"paragraph": para.text})
            else:
                # In case there's content before a heading
                if not content['document']:
                    content['document'].append({"section_title": "Introduction", "content": []})
                content['document'][0]["content"].append({"paragraph": para.text})

    # Append the last section if exists
    if current_section:
        content['document'].append(current_section)

    return content

def save_as_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Example usage
docx_file_path = 'Medarbetarhandbok.docx'
output_json_path = 'output.json'

docx_content = extract_docx_content(docx_file_path)
save_as_json(docx_content, output_json_path)

print(f"Document content successfully saved to {output_json_path}")
