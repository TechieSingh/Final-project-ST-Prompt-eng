"""
Script to convert Markdown documentation to PDF format.
This script uses markdown2 and weasyprint to create a professional PDF document.

Requirements:
    pip install markdown2 weasyprint

Alternative: Use pandoc (if installed)
    pandoc docs/PDF_DOCUMENTATION_TEMPLATE.md -o PROJECT_DOCUMENTATION.pdf
"""

import os
import sys
from pathlib import Path

def convert_with_pandoc(input_file, output_file):
    """Convert markdown to PDF using pandoc (if available)."""
    import subprocess
    try:
        cmd = ['pandoc', input_file, '-o', output_file, '--pdf-engine=xelatex', 
               '-V', 'geometry:margin=1in', '--toc', '--toc-depth=2']
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Successfully created PDF: {output_file}")
            return True
        else:
            print(f"❌ Pandoc error: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ Pandoc not found. Install pandoc or use alternative method.")
        return False

def convert_with_weasyprint(input_file, output_file):
    """Convert markdown to PDF using markdown2 and weasyprint."""
    try:
        import markdown2
        from weasyprint import HTML, CSS
        
        # Read markdown file
        with open(input_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Convert markdown to HTML
        html_content = markdown2.markdown(markdown_content, extras=['tables', 'fenced-code-blocks'])
        
        # Add CSS styling
        html_doc = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @page {{
                    size: A4;
                    margin: 1in;
                }}
                body {{
                    font-family: 'Times New Roman', serif;
                    line-height: 1.6;
                    color: #333;
                }}
                h1 {{
                    color: #667eea;
                    border-bottom: 3px solid #667eea;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #667eea;
                    margin-top: 30px;
                    border-bottom: 2px solid #667eea;
                    padding-bottom: 5px;
                }}
                h3 {{
                    color: #555;
                    margin-top: 20px;
                }}
                code {{
                    background-color: #f4f4f4;
                    padding: 2px 5px;
                    border-radius: 3px;
                    font-family: 'Courier New', monospace;
                }}
                pre {{
                    background-color: #f4f4f4;
                    padding: 15px;
                    border-radius: 5px;
                    overflow-x: auto;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin: 20px 0;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 12px;
                    text-align: left;
                }}
                th {{
                    background-color: #667eea;
                    color: white;
                }}
            </style>
        </head>
        <body>
        {html_content}
        </body>
        </html>
        """
        
        # Generate PDF
        HTML(string=html_doc).write_pdf(output_file)
        print(f"✅ Successfully created PDF: {output_file}")
        return True
        
    except ImportError:
        print("❌ Required packages not found. Install with: pip install markdown2 weasyprint")
        return False
    except Exception as e:
        print(f"❌ Error creating PDF: {str(e)}")
        return False

def main():
    """Main conversion function."""
    # Determine input and output files
    project_root = Path(__file__).parent
    input_file = project_root / "docs" / "PDF_DOCUMENTATION_TEMPLATE.md"
    output_file = project_root / "PROJECT_DOCUMENTATION.pdf"
    
    # Check if input file exists
    if not input_file.exists():
        print(f"❌ Input file not found: {input_file}")
        print("📝 Using PROJECT_DOCUMENTATION.md as alternative...")
        input_file = project_root / "docs" / "PROJECT_DOCUMENTATION.md"
        if not input_file.exists():
            print(f"❌ Alternative file also not found: {input_file}")
            sys.exit(1)
    
    print(f"📄 Converting: {input_file}")
    print(f"📄 Output: {output_file}")
    print()
    
    # Try pandoc first (better quality)
    if convert_with_pandoc(str(input_file), str(output_file)):
        return
    
    # Fallback to weasyprint
    print("🔄 Trying alternative method (weasyprint)...")
    if convert_with_weasyprint(str(input_file), str(output_file)):
        return
    
    # If both fail, provide instructions
    print("\n" + "="*60)
    print("📋 MANUAL CONVERSION INSTRUCTIONS:")
    print("="*60)
    print("\nOption 1: Use Pandoc (Recommended)")
    print("  Install: https://pandoc.org/installing.html")
    print(f"  Command: pandoc {input_file} -o {output_file} --pdf-engine=xelatex --toc")
    print("\nOption 2: Use Online Converter")
    print("  - Visit: https://www.markdowntopdf.com/")
    print(f"  - Upload: {input_file}")
    print("  - Download PDF")
    print("\nOption 3: Use VS Code Extension")
    print("  - Install 'Markdown PDF' extension")
    print("  - Open the markdown file")
    print("  - Right-click → 'Markdown PDF: Export (pdf)'")
    print("\nOption 4: Use Word/Google Docs")
    print("  - Copy markdown content")
    print("  - Paste into Word/Google Docs")
    print("  - Export as PDF")
    print("="*60)

if __name__ == "__main__":
    main()

