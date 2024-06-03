import os
import subprocess
from flask import Blueprint, request, send_file, render_template_string

cvMaker_bp = Blueprint('cvMaker', __name__)


@cvMaker_bp.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    formData = request.json
    print(formData)

    # Render the LaTeX template with formData
    latex_template_path = 'app/cvMaker/templates/template.tex'
    with open(latex_template_path) as f:
        latex_template = f.read()

    rendered_latex = render_template_string(latex_template, formData=formData)

    # Define the path for the temporary LaTeX and PDF files
    temp_dir = os.path.join(os.path.dirname(__file__), 'temp_files')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    tex_path = os.path.join(temp_dir, 'resume.tex')
    pdf_path = os.path.join(temp_dir, 'resume.pdf')

    # Save the rendered LaTeX to a file
    with open(tex_path, 'w') as tex_file:
        tex_file.write(rendered_latex)

    # Run pdflatex to convert the LaTeX file to PDF
    try:
        result = subprocess.run(['pdflatex', '-output-directory', temp_dir, tex_path], check=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
        print(result.stderr.decode())
    except subprocess.CalledProcessError as e:
        print(e.stdout.decode())
        print(e.stderr.decode())
        return str(e), 500

    # Check if the PDF file was created
    if not os.path.exists(pdf_path):
        return 'Error: PDF file was not created.', 500

    return send_file(pdf_path, as_attachment=True, download_name='resume.pdf')
