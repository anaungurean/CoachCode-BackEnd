import os
from flask import Blueprint, request, send_file, render_template_string
import pdfkit

cvMaker_bp = Blueprint('cvMaker', __name__)

@cvMaker_bp.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    formData = request.json
    print(formData)


    html_template_path = os.path.join(os.path.dirname(__file__), 'templates', 'template.html')
    with open(html_template_path, 'r') as file:
        html_template = file.read()


    # Render the HTML template with formData
    rendered_html = render_template_string(html_template, formData=formData)

    # Define the path for the temporary PDF file
    temp_dir = os.path.join(os.path.dirname(__file__), 'temp_files')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    pdf_path = os.path.join(temp_dir, 'resume.pdf')

    # Specify the path to wkhtmltopdf executable
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

    # Configure options for pdfkit (optional)
    options = {
        'page-size': 'A4',
           'margin-top': '0mm',
              'margin-right': '0mm',
                    'margin-bottom': '0mm',
                        'margin-left': '0mm',
        'enable-local-file-access': '',


    }

    # Convert the HTML to PDF using pdfkit
    pdfkit.from_string(rendered_html, pdf_path, options=options, configuration=config)

    # Check if the PDF file was created
    if not os.path.exists(pdf_path):
        return 'Error: PDF file was not created.', 500

    return send_file(pdf_path, as_attachment=True, download_name='resume.pdf')
