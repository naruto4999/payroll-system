from fpdf import FPDF

from fpdf import FPDF

class FPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Hello, World!', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)

# Create instance of FPDF class
def generate_attendance_register(request_data):
    pdf = FPDF()

    # Add a page
    pdf.add_page()

    # Set font
    pdf.set_font("Arial", size = 12)

    # Add a cell
    pdf.cell(200, 10, txt = "Welcome to FPDF!", ln = True, align = 'C')

    # Save the pdf with name .pdf
    buffer = pdf.output(dest='S').encode('latin1')
    yield buffer