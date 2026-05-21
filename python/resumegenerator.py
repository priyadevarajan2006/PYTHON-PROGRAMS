import io
from flask import Flask, request, send_file, render_template_string
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

app = Flask(__name__)

# --- WEB UI DESIGN (Embedded directly for IDLE) ---
HTML_FORM = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Resume Generator</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
</head>
<body class="bg-slate-50 text-slate-800 min-h-screen flex items-center justify-center p-6">
    <div class="bg-white p-8 rounded-xl shadow-md w-full max-w-3xl border border-slate-100">
        <h1 class="text-3xl font-bold text-slate-900 mb-2">Resume Builder</h1>
        
        <form action="/" method="POST" class="space-y-8">
            
            <!--  BASIC INFORMATION -->
            <div>
                <h2 class="text-xl font-bold text-indigo-900 border-b pb-2 border-slate-200 mb-4">TITLE: BASIC INFORMATION (Page 1)</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-slate-600 mb-1">Full Name</label>
                        <input type="text" name="name" required placeholder="John Doe" class="w-full border border-slate-300 rounded-md p-2 outline-none">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-slate-600 mb-1">Email Address</label>
                        <input type="email" name="email" required placeholder="johndoe@email.com" class="w-full border border-slate-300 rounded-md p-2 outline-none">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-slate-600 mb-1">Date of Birth</label>
                        <input type="date" name="dateofbirth" required class="w-full border border-slate-300 rounded-md p-2 outline-none">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-slate-600 mb-1">Age</label>
                        <input type="number" name="age" required placeholder="24" class="w-full border border-slate-300 rounded-md p-2 outline-none">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-slate-600 mb-1">Gender</label>
                        <select name="gender" class="w-full border border-slate-300 rounded-md p-2 outline-none">
                            <option value="Male">Male</option>
                            <option value="Female">Female</option>
                            <option value="Non-binary">Non-binary</option>
                            <option value="Prefer not to say">Prefer not to say</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-slate-600 mb-1">Years of Experience</label>
                        <input type="text" name="experience" placeholder="e.g., 2 Years / Fresher" class="w-full border border-slate-300 rounded-md p-2 outline-none">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-slate-600 mb-1">Father's Name</label>
                        <input type="text" name="fathername" required placeholder="Robert Doe" class="w-full border border-slate-300 rounded-md p-2 outline-none">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-slate-600 mb-1">Mother's Name</label>
                        <input type="text" name="mothername" required placeholder="Mary Doe" class="w-full border border-slate-300 rounded-md p-2 outline-none">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-slate-600 mb-1">Highest Qualification</label>
                        <input type="text" name="qualification" required placeholder="B.Tech in Computer Science" class="w-full border border-slate-300 rounded-md p-2 outline-none">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-slate-600 mb-1">Religion</label>
                        <input type="text" name="religion" placeholder="Christianity / Islam / Hinduism / None" class="w-full border border-slate-300 rounded-md p-2 outline-none">
                    </div>
                    <div class="md:col-span-2">
                        <label class="block text-sm font-medium text-slate-600 mb-1">Nationality</label>
                        <input type="text" name="nationality" required placeholder="American / Indian / etc." class="w-full border border-slate-300 rounded-md p-2 outline-none">
                    </div>
                    <div class="md:col-span-2">
                        <label class="block text-sm font-medium text-slate-600 mb-1">Declaration</label>
                        <textarea name="declaration" rows="3" class="w-full border border-slate-300 rounded-md p-2 outline-none">I hereby declare that all the details furnished above are true and correct to the best of my knowledge and belief.</textarea>
                    </div>
                </div>
            </div>

            <!-- SECTION 2: RESUME DETAILS -->
            <div>
                <h2 class="text-xl font-bold text-indigo-900 border-b pb-2 border-slate-200 mb-4">TITLE: RESUME DETAILS (Page 2)</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-slate-600 mb-1">Branch / Specialization</label>
                        <input type="text" name="branch" placeholder="Information Technology" class="w-full border border-slate-300 rounded-md p-2 outline-none">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-slate-600 mb-1">Graduation Year</label>
                        <input type="text" name="grad_year" placeholder="2025" class="w-full border border-slate-300 rounded-md p-2 outline-none">
                    </div>
                    <div class="md:col-span-2">
                        <label class="block text-sm font-medium text-slate-600 mb-1">Mini Project Details</label>
                        <textarea name="mini_project" rows="2" placeholder="Title and brief outline of your mini project..." class="w-full border border-slate-300 rounded-md p-2 outline-none"></textarea>
                    </div>
                    <div class="md:col-span-2">
                        <label class="block text-sm font-medium text-slate-600 mb-1">Main Project Details</label>
                        <textarea name="main_project" rows="3" placeholder="Title and extensive features of your main graduation project..." class="w-full border border-slate-300 rounded-md p-2 outline-none"></textarea>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-slate-600 mb-1">Area of Interest</label>
                        <input type="text" name="interest" placeholder="Machine Learning, Web Security" class="w-full border border-slate-300 rounded-md p-2 outline-none">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-slate-600 mb-1">Core Skills</label>
                        <input type="text" name="skills" placeholder="Python, SQL, React, Git" class="w-full border border-slate-300 rounded-md p-2 outline-none">
                    </div>
                </div>
            </div>

            <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 px-4 rounded-md shadow transition-colors">
                Generate 2-Page PDF Resume
            </button>
        </form>
    </div>
</body>
</html>
"""

def generate_pdf(data):
    buffer = io.BytesIO()
    # 0.5-inch margins
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    
    PRIMARY_COLOR = colors.HexColor("#1A365D")  # Deep Navy
    TEXT_COLOR = colors.HexColor("#2D3748")     # Off-black
    LINE_COLOR = colors.HexColor("#CBD5E1")     # Light separator lines
    
    styles = getSampleStyleSheet()
    
    # Custom Typography Styles
    main_title_style = ParagraphStyle('MainTitle', fontName='Helvetica-Bold', fontSize=22, leading=26, textColor=PRIMARY_COLOR, alignment=1, spaceAfter=20)
    section_heading_style = ParagraphStyle('SectionHeading', fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=PRIMARY_COLOR, spaceBefore=15, spaceAfter=6)
    body_style = ParagraphStyle('Body', fontName='Helvetica', fontSize=10, leading=15, textColor=TEXT_COLOR)
    bold_body_style = ParagraphStyle('BoldBody', fontName='Helvetica-Bold', fontSize=10, leading=15, textColor=TEXT_COLOR)

    def add_section_header(title):
        story.append(Paragraph(title.upper(), section_heading_style))
        t = Table([['']], colWidths=[540], rowHeights=[1])
        t.setStyle(TableStyle([('LINEABOVE', (0,0), (-1,-1), 1, LINE_COLOR), ('BOTTOMPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 0)]))
        story.append(t)
        story.append(Spacer(1, 10))

    # ================= PAGE 1: BASIC INFORMATION =================
    story.append(Paragraph("BASIC INFORMATION", main_title_style))
    
    # Grid formatting layout for personal meta details via ReportLab Table
    personal_info_data = [
        [Paragraph("<b>Full Name:</b>", body_style), Paragraph(data.get('name'), body_style)],
        [Paragraph("<b>Email Address:</b>", body_style), Paragraph(data.get('email'), body_style)],
        [Paragraph("<b>Date of Birth:</b>", body_style), Paragraph(data.get('dateofbirth'), body_style)],
        [Paragraph("<b>Age:</b>", body_style), Paragraph(data.get('age'), body_style)],
        [Paragraph("<b>Gender:</b>", body_style), Paragraph(data.get('gender'), body_style)],
        [Paragraph("<b>Years of Experience:</b>", body_style), Paragraph(data.get('experience', 'N/A'), body_style)],
        [Paragraph("<b>Father's Name:</b>", body_style), Paragraph(data.get('fathername'), body_style)],
        [Paragraph("<b>Mother's Name:</b>", body_style), Paragraph(data.get('mothername'), body_style)],
        [Paragraph("<b>Highest Qualification:</b>", body_style), Paragraph(data.get('qualification'), body_style)],
        [Paragraph("<b>Religion:</b>", body_style), Paragraph(data.get('religion', 'N/A'), body_style)],
        [Paragraph("<b>Nationality:</b>", body_style), Paragraph(data.get('nationality'), body_style)],
    ]
    
    info_table = Table(personal_info_data, colWidths=[150, 390])
    info_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 25))
    
    # Declaration added explicitly at bottom of Page 1
    if data.get('declaration'):
        add_section_header("Declaration")
        story.append(Paragraph(data.get('declaration'), body_style))
    
    # Hard Page Break forces everything else to the second sheet
    story.append(PageBreak())
    
    # ================= PAGE 2: RESUME DETAILS =================
    story.append(Paragraph("RESUME DETAILS", main_title_style))
    
    # Academic & Profile Details Block
    add_section_header("Education & Profile")
    edu_details_data = [
        [Paragraph("<b>Branch / Stream:</b>", body_style), Paragraph(data.get('branch', 'N/A'), body_style)],
        [Paragraph("<b>Graduation Year:</b>", body_style), Paragraph(data.get('grad_year', 'N/A'), body_style)],
    ]
    edu_table = Table(edu_details_data, colWidths=[150, 390])
    edu_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 8), ('LEFTPADDING', (0,0), (-1,-1), 0)]))
    story.append(edu_table)
    story.append(Spacer(1, 10))
    
    # Projects Block
    if data.get('mini_project') or data.get('main_project'):
        add_section_header("Projects")
        if data.get('mini_project'):
            story.append(Paragraph("<b>Mini Project:</b>", bold_body_style))
            story.append(Paragraph(data.get('mini_project'), body_style))
            story.append(Spacer(1, 10))
        if data.get('main_project'):
            story.append(Paragraph("<b>Main Project:</b>", bold_body_style))
            story.append(Paragraph(data.get('main_project'), body_style))
            story.append(Spacer(1, 10))
            
    # Professional Core Skills
    if data.get('skills'):
        add_section_header("Technical Skills")
        story.append(Paragraph(data.get('skills'), body_style))
        story.append(Spacer(1, 10))
        
    # Areas of Interest
    if data.get('interest'):
        add_section_header("Areas of Interest")
        story.append(Paragraph(data.get('interest'), body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_data = request.form.to_dict()
        pdf_buffer = generate_pdf(user_data)
        filename = f"{user_data.get('name', 'resume').replace(' ', '_')}_resume.pdf"
        return send_file(pdf_buffer, as_attachment=True, download_name=filename, mimetype='application/pdf')
        
    return render_template_string(HTML_FORM)

if __name__ == '__main__':
    # Standard configuration to run inside IDLE's runtime smoothly
    app.run(debug=True, port=8080, use_reloader=False)
