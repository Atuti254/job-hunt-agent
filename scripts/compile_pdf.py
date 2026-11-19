import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

def html_to_pdf(html_path: str, pdf_path: str):
    html_file = Path(html_path).resolve()
    pdf_file = Path(pdf_path).resolve()
    pdf_file.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(html_file.as_uri(), wait_until="networkidle")
        page.pdf(
            path=str(pdf_file),
            format="A4",
            margin={"top": "0.4in", "bottom": "0.4in", "left": "0.4in", "right": "0.4in"},
            print_background=True,
        )
        browser.close()
    print(f"Compiled PDF saved to: {pdf_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: uv run scripts/compile_pdf.py <input.html> <output.pdf>")
        sys.exit(1)
    html_to_pdf(sys.argv[1], sys.argv[2])
