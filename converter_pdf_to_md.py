import os
import fitz

ORIGINAL_DIR = "data/original"
MARKDOWN_DIR = "data/markdown"

os.makedirs(MARKDOWN_DIR, exist_ok=True)


def is_heading(line):
    """Check if a line is a heading (uppercase and sufficiently long)."""
    return line.strip().isupper() and len(line.strip()) > 3


def convert_heading(line):
    """Convert a line to a Markdown heading format."""
    return "# " + line.strip()


def process_lines(lines):
    """Process lines to convert headings and clean text."""
    processed = []
    for line in lines:
        if is_heading(line):
            processed.append(convert_heading(line))
        else:
            processed.append(line.strip())
    return processed


def pdf_to_markdown(pdf_path, md_path):
    """Convert a PDF file to Markdown format."""
    try:
        with fitz.open(pdf_path) as doc:  # Ensures proper cleanup
            with open(md_path, "w", encoding="utf-8") as f:
                for page_num, page in enumerate(list(doc), start=1):  # Explicitly converts doc to an iterable
                    f.write(f"# Page {page_num}\n\n")
                    text = page.get_text("text")
                    lines = text.splitlines()
                    for line in process_lines(lines):
                        f.write(line + "\n")
                    f.write("\n---\n")

        print(f"Converted: {md_path}")

    except Exception as e:
        print(
            f"Error processing {pdf_path}: {e}. "
            "Please check the file and ensure it is not corrupted or in an unsupported format."
        )


def check_and_convert():
    """Check for unconverted PDFs and convert them only if needed."""
    pdf_files = {f for f in os.listdir(ORIGINAL_DIR) if f.lower().endswith(".pdf")}
    md_files = {f.replace(".md", ".pdf") for f in os.listdir(MARKDOWN_DIR) if f.lower().endswith(".md")}
    md_converted_files = {f.replace("_converted.md", ".pdf")
                          for f in os.listdir(MARKDOWN_DIR) if f.lower().endswith("_converted.md")}

    missing_files = pdf_files - md_files - md_converted_files

    if not missing_files:
        print("All files are already converted.")
        return

    for pdf_file in missing_files:
        pdf_path = os.path.join(ORIGINAL_DIR, pdf_file)
        md_file = pdf_file.replace(".pdf", "_converted.md")  # Always create with _converted suffix
        md_path = os.path.join(MARKDOWN_DIR, md_file)

        pdf_to_markdown(pdf_path, md_path)


if __name__ == "__main__":
    check_and_convert()
