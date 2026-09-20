import io

import pandas as pd
from django.http import HttpResponse
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

from .payment_sheet_data import build_payment_sheet_report


def _columns(report):
    salary_total = (
        'Salary Rate Total'
        if report.salary_rate_columns == 'head_wise'
        else 'Salary Rate'
    )
    earned_total = (
        'Earned Salary Total (*incl of arrear)'
        if report.earned_salary_columns == 'head_wise'
        else 'Earned Salary (*incl of arrear)'
    )
    columns = ['S/N', 'ACN', 'Employee Name', 'Father/Husband Name', 'Designation']
    if report.salary_rate_columns == 'head_wise':
        columns.extend(f'Salary Rate - {name}' for _, name in report.salary_rate_heads)
    columns.extend([salary_total, 'PD'])
    if report.earned_salary_columns == 'head_wise':
        columns.extend(f'Earned - {name} (*incl of arrear)' for _, name in report.earned_salary_heads)
    columns.append(earned_total)
    columns.extend([
        'Incentive', report.ot_hours_label, 'OT Amount', 'Total Earned', 'Advance',
        'EPF', 'ESI', 'LWF', 'Others', 'TDS', 'Total Deduction', 'Net Payable',
    ])
    return columns, salary_total, earned_total


def _employee_row(row, report, salary_total, earned_total):
    values = {
        'S/N': row.serial,
        'ACN': row.attendance_card_no,
        'Employee Name': row.employee_name,
        'Father/Husband Name': row.father_or_husband_name,
        'Designation': row.designation,
        salary_total: row.salary_rate,
        'PD': row.paid_days or 0,
        earned_total: row.earned_salary or 0,
        'Incentive': row.incentive,
        report.ot_hours_label: row.ot_hours or 0,
        'OT Amount': row.ot_amount or 0,
        'Total Earned': row.total_earned or 0,
        'Advance': row.advance,
        'EPF': row.epf,
        'ESI': row.esi,
        'LWF': row.lwf,
        'Others': row.others,
        'TDS': row.tds,
        'Total Deduction': row.total_deductions,
        'Net Payable': row.net_payable or 0,
    }
    if report.salary_rate_columns == 'head_wise':
        for head_id, name in report.salary_rate_heads:
            values[f'Salary Rate - {name}'] = row.salary_rate_breakdown.get(head_id, 0)
    if report.earned_salary_columns == 'head_wise':
        for head_id, name in report.earned_salary_heads:
            values[f'Earned - {name} (*incl of arrear)'] = row.earned_salary_breakdown.get(head_id, 0)
    return values


def _total_row(label, totals, report, salary_total, earned_total):
    values = {
        'S/N': label,
        'ACN': '',
        'Employee Name': '',
        'Father/Husband Name': '',
        'Designation': '',
        salary_total: totals.salary_rate,
        'PD': totals.paid_days,
        earned_total: totals.earned_salary,
        'Incentive': totals.incentive,
        report.ot_hours_label: totals.ot_hours,
        'OT Amount': totals.ot_amount,
        'Total Earned': totals.total_earned,
        'Advance': totals.advance,
        'EPF': totals.epf,
        'ESI': totals.esi,
        'LWF': totals.lwf,
        'Others': totals.others,
        'TDS': totals.tds,
        'Total Deduction': totals.total_deductions,
        'Net Payable': totals.net_payable,
    }
    if report.salary_rate_columns == 'head_wise':
        for head_id, name in report.salary_rate_heads:
            values[f'Salary Rate - {name}'] = totals.salary_rate_breakdown.get(head_id, 0)
    if report.earned_salary_columns == 'head_wise':
        for head_id, name in report.earned_salary_heads:
            values[f'Earned - {name} (*incl of arrear)'] = totals.earned_salary_breakdown.get(head_id, 0)
    return values


def generate_payment_sheet_xlsx(user, request_data, employee_salaries):
    report = build_payment_sheet_report(user, request_data, employee_salaries, 'xlsx')
    columns, salary_total, earned_total = _columns(report)
    employees_data = []

    for section in report.sections:
        if report.grouped:
            department_row = dict.fromkeys(columns, '')
            department_row['S/N'] = f"{section.department_name or 'No Department'} dept_name_finder"
            employees_data.append(department_row)

        employees_data.extend(
            _employee_row(row, report, salary_total, earned_total)
            for row in section.rows
        )

        # Preserve the old behavior: no department total was printed for
        # employees without a department.
        if report.grouped and section.department_id is not None:
            employees_data.append(
                _total_row('Department Total', section.totals, report, salary_total, earned_total)
            )
            employees_data.append(dict.fromkeys(columns, ''))

    employees_data.append(
        _total_row('Grand Total', report.totals, report, salary_total, earned_total)
    )

    df = pd.DataFrame(employees_data, columns=columns)
    if not report.show_lwf:
        df.drop(columns=['LWF'], inplace=True)

    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, header=False, startrow=2, sheet_name='Sheet1')
        worksheet = writer.sheets['Sheet1']
        worksheet.sheet_view.showGridLines = False
        worksheet.freeze_panes = 'F3'

        fills = {
            'identity': PatternFill('solid', fgColor='C6E0B4'),
            'salary': PatternFill('solid', fgColor='F4CCCC'),
            'salary_group': PatternFill('solid', fgColor='C97D7D'),
            'earned': PatternFill('solid', fgColor='9FC5E8'),
            'earned_group': PatternFill('solid', fgColor='3D85C6'),
            'attendance': PatternFill('solid', fgColor='B7DEE8'),
            'deduction': PatternFill('solid', fgColor='FCE5CD'),
            'payable': PatternFill('solid', fgColor='A9D18E'),
            'department': PatternFill('solid', fgColor='D9EAF7'),
            'department_total': PatternFill('solid', fgColor='BDD7EE'),
            'grand_total': PatternFill('solid', fgColor='F4B6C2'),
            'alternate': PatternFill('solid', fgColor='F7FAFC'),
        }
        thin_gray = Side(style='thin', color='A6A6A6')
        border = Border(left=thin_gray, right=thin_gray, top=thin_gray, bottom=thin_gray)
        header_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        column_positions = {name: index for index, name in enumerate(df.columns, start=1)}
        salary_columns = [
            name for name in df.columns
            if name == salary_total or name.startswith('Salary Rate - ')
        ]
        earned_columns = [
            name for name in df.columns
            if name == earned_total or name.startswith('Earned - ')
        ]

        grouped_columns = set(salary_columns + earned_columns)
        for column_name, column_index in column_positions.items():
            if column_name in grouped_columns:
                worksheet.cell(row=2, column=column_index, value=column_name)
                continue
            worksheet.cell(row=1, column=column_index, value=column_name)
            worksheet.merge_cells(
                start_row=1,
                start_column=column_index,
                end_row=2,
                end_column=column_index,
            )

        for label, group_columns in (
            ('SALARY RATE', salary_columns),
            ('EARNED SALARY', earned_columns),
        ):
            first_column = column_positions[group_columns[0]]
            last_column = column_positions[group_columns[-1]]
            if first_column != last_column:
                worksheet.merge_cells(
                    start_row=1,
                    start_column=first_column,
                    end_row=1,
                    end_column=last_column,
                )
            worksheet.cell(row=1, column=first_column, value=label)

        deduction_columns = {
            'Advance', 'EPF', 'ESI', 'LWF', 'Others', 'TDS', 'Total Deduction',
        }
        attendance_columns = {
            'PD', 'Incentive', report.ot_hours_label, 'OT Amount', 'Total Earned',
        }
        for column_name, column_index in column_positions.items():
            if column_name in salary_columns:
                fill = fills['salary']
            elif column_name in earned_columns:
                fill = fills['earned']
            elif column_name in deduction_columns:
                fill = fills['deduction']
            elif column_name == 'Net Payable':
                fill = fills['payable']
            elif column_name in attendance_columns:
                fill = fills['attendance']
            else:
                fill = fills['identity']
            for row_number in (1, 2):
                cell = worksheet.cell(row=row_number, column=column_index)
                if cell.fill.fill_type is None:
                    cell.fill = fill
                cell.font = Font(bold=True, color='1F1F1F')
                cell.alignment = header_alignment
                cell.border = border

        for group_columns, fill_name in (
            (salary_columns, 'salary_group'),
            (earned_columns, 'earned_group'),
        ):
            group_cell = worksheet.cell(
                row=1,
                column=column_positions[group_columns[0]],
            )
            group_cell.fill = fills[fill_name]
            group_cell.font = Font(bold=True, color='FFFFFF', size=11)

        worksheet.row_dimensions[1].height = 24
        worksheet.row_dimensions[2].height = 42
        department_total_row_numbers = []
        department_heading_row_numbers = []
        data_start_row = 3

        if report.grouped:
            for row_idx in range(data_start_row, data_start_row + len(df)):
                first_col_value = worksheet.cell(row=row_idx, column=1).value
                if not isinstance(first_col_value, str):
                    continue
                words = first_col_value.split()
                if len(words) <= 1:
                    continue
                if words[-1] == 'dept_name_finder':
                    worksheet.cell(row=row_idx, column=1).value = ' '.join(words[:-1])
                    department_heading_row_numbers.append(row_idx)
                elif words[-1] == 'Total' and words[0] == 'Department':
                    department_total_row_numbers.append(row_idx)

        last_row = data_start_row + len(df) - 1
        for row_number in range(data_start_row, last_row + 1):
            first_value = worksheet.cell(row=row_number, column=1).value
            if row_number in department_heading_row_numbers:
                worksheet.merge_cells(
                    start_row=row_number,
                    start_column=1,
                    end_row=row_number,
                    end_column=len(df.columns),
                )
                cell = worksheet.cell(row=row_number, column=1)
                cell.fill = fills['department']
                cell.font = Font(bold=True, color='1F4E78', size=11)
                cell.alignment = Alignment(vertical='center')
                worksheet.row_dimensions[row_number].height = 22
                continue

            is_total = row_number in department_total_row_numbers or row_number == last_row
            is_employee = isinstance(first_value, (int, float))
            for column_index in range(1, len(df.columns) + 1):
                cell = worksheet.cell(row=row_number, column=column_index)
                cell.border = border
                cell.alignment = Alignment(vertical='center')
                if is_employee and (row_number - data_start_row) % 2:
                    cell.fill = fills['alternate']
                if row_number in department_total_row_numbers:
                    cell.fill = fills['department_total']
                    cell.font = Font(bold=True, color='1F4E78')
                elif row_number == last_row:
                    cell.fill = fills['grand_total']
                    cell.font = Font(bold=True, color='7030A0')
                if column_index > 5 and isinstance(cell.value, (int, float)):
                    cell.number_format = '#,##0.00'
            if is_total:
                worksheet.row_dimensions[row_number].height = 21

        for column_index, column_name in enumerate(df.columns, start=1):
            values = [column_name]
            values.extend(
                worksheet.cell(row=row_number, column=column_index).value
                for row_number in range(data_start_row, last_row + 1)
            )
            max_length = max(len(str(value)) for value in values if value is not None) + 2
            worksheet.column_dimensions[get_column_letter(column_index)].width = min(
                max(max_length, 8), 24
            )

    response = HttpResponse(
        content=excel_buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename="pf_statement.xlsx"'
    excel_buffer.close()
    return response
