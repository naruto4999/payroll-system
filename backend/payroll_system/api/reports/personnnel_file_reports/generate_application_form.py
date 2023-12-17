def generate_application_form(report, default_cell_height, default_cell_height_for_heading, employee, left_margin, right_margin):
    report.add_page()
    report.set_font("Helvetica", size=8)
    report.cell(w=0, h=default_cell_height, text='Application Form', align="C", new_x="RIGHT", new_y='TOP', border=1)

    # # Save the pdf with name .pdf
    # buffer = bytes(report.output())
    # yield buffer