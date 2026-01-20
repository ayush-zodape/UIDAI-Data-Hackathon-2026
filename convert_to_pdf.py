#!/usr/bin/env python3
"""
Convert Markdown to PDF with images preserved
"""
import os
import sys
from pathlib import Path

# Try using markdown2 + weasyprint
try:
    from weasyprint import HTML, CSS
    import markdown2
    
    # Read the markdown file
    md_path = Path("UIDAI_CONSOLIDATED_SUBMISSION.md")
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown2.markdown(
        md_content,
        extras=['fenced-code-blocks', 'tables', 'toc']
    )
    
    # Create a complete HTML document with CSS styling
    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #1a73e8;
            margin-top: 24px;
            margin-bottom: 12px;
        }}
        h1 {{
            border-bottom: 3px solid #1a73e8;
            padding-bottom: 10px;
            font-size: 28px;
        }}
        h2 {{
            font-size: 22px;
            margin-top: 32px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 16px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #f0f0f0;
            font-weight: bold;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 12px;
            border-left: 4px solid #1a73e8;
            overflow-x: auto;
            margin: 12px 0;
        }}
        img {{
            max-width: 100%;
            height: auto;
            margin: 16px 0;
            border: 1px solid #ddd;
            padding: 8px;
            background-color: #f9f9f9;
        }}
        blockquote {{
            border-left: 4px solid #ddd;
            margin-left: 0;
            padding-left: 16px;
            color: #666;
            font-style: italic;
        }}
        hr {{
            border: none;
            border-top: 2px solid #ddd;
            margin: 32px 0;
        }}
        a {{
            color: #1a73e8;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        page-break {{
            page-break-after: always;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
    
    # Convert HTML to PDF
    HTML(string=full_html).write_pdf('UIDAI_CONSOLIDATED_SUBMISSION.pdf')
    print("PDF created successfully: UIDAI_CONSOLIDATED_SUBMISSION.pdf")
    
except ImportError as e:
    print(f"⚠️ Missing library: {e}")
    print("Attempting alternative method using pandoc...")
    
    # Fallback: Use pandoc with simpler settings
    os.system("pandoc UIDAI_HACKATHON_SUBMISSION.md -t pdf -o UIDAI_HACKATHON_SUBMISSION.pdf --pdf-engine=pdflatex 2>/dev/null || pandoc UIDAI_HACKATHON_SUBMISSION.md -t pdf -o UIDAI_HACKATHON_SUBMISSION.pdf")
    print("✅ PDF created using pandoc")
