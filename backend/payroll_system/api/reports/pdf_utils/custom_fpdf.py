
from fpdf import FPDF
from fpdf.enums import MethodReturnValue, XPos, YPos, Align

class CustomFPDF(FPDF):
    def multi_cell_with_limit(self, w, h=None, text='', border=0, align=Align.J, fill=False, min_lines=0,
                              max_lines=1, border_each_line=False, new_x=XPos.RIGHT, new_y=YPos.NEXT):

        """
            Custom multi-cell implementation with a max_lines limit.

            Parameters:
            ----------
            w : float
                The width of the cell.
            h : float or None, optional
                The height of the cell. If None, the height is automatically calculated.
            text : str, optional
                The text to be printed in the cell. Default is an empty string.
            border : int or str, optional
                The border of the cell. Can be:
                    - 0 (no border, default)
                    - 1 (frame border)
                    - 'L', 'T', 'R', 'B' (individually for left, top, right, bottom).
            align : Align, optional
                Text alignment. Possible values are:
                    - Align.L (left)
                    - Align.C (center)
                    - Align.R (right)
                    - Align.J (justified).
            fill : bool, optional
                Whether to fill the background of the cell. Default is False.
            max_lines : int, optional
                The maximum number of lines to display. Default is 0 (no limit).
            link : str, optional
                URL or link to be added to the cell. Default is an empty string.
            new_x : XPos, optional
                Horizontal position after the cell. Possible values:
                    - XPos.RIGHT (move right)
                    - XPos.LEFT (move left)
                    - XPos.NEXT (move to next line).
            new_y : YPos, optional
                Vertical position after the cell. Possible values:
                    - YPos.NEXT (move to next line)
                    - YPos.TOP (move to top of the page).

            Returns:
            -------
            None
        """
        lines = self.multi_cell(w=w, h=h, text=text, border=0, align=align, fill=fill, 
                                dry_run=True, output=MethodReturnValue.LINES, new_x=new_x, new_y=new_y)
        print(lines)
        original_lines_length = len(lines)
        number_of_lines_to_add = 0
        c_margin_adjustment = round(self.c_margin, 2) * 2
        last_line_first_word = ''


        if max_lines > 0 and len(lines)>max_lines:
            last_line_first_word = lines[-1].split()[0]
            lines = lines[:max_lines]
        if len(lines) < min_lines:
            number_of_lines_to_add = min_lines-len(lines)
            print(f"number of lines to add: {number_of_lines_to_add}")

        print(f"Lines after appending: {lines}")
        if len(lines) < original_lines_length:
            last_line = lines[-1]+' '+last_line_first_word
            ellipsis_width = self.get_string_width("...")
            print(f"Rounded C Margin {round(self.c_margin, 2)}, Not Rounded: {self.c_margin}")
            print(f"Blank line string width: {round(self.get_string_width(' '), 2)}")
            
            while self.get_string_width(last_line) + ellipsis_width + c_margin_adjustment > w and len(last_line) > 0:
                last_line = last_line[:-1]

            last_line += "..."
            lines[-1] = last_line

        if not border_each_line:
            final_text = ' '.join(lines)
            if min_lines<1 or len(lines)>=min_lines:
                self.multi_cell(w=w, h=h, text=final_text, border=border, align=align, fill=fill, 
                                new_x=new_x, new_y=new_y)
            else:
                upper_multi_cell_border = 0
                lower_multi_cell_border = 0
                if border!=0:
                    if not isinstance(border, int):
                        upper_multi_cell_border = border.replace('B', '')
                        lower_multi_cell_border = border.replace('T', '')
                    elif border==1:
                        upper_multi_cell_border = 'TLR'
                        lower_multi_cell_border = 'BLR'
                print(upper_multi_cell_border)
                print(lower_multi_cell_border)
                lines = self.multi_cell(w=w, h=h, text=number_of_lines_to_add*int((w-c_margin_adjustment)/self.get_string_width(' '))*' ', border=0, align=align, fill=fill, 
                                dry_run=True, output=MethodReturnValue.LINES, new_x=new_x, new_y=new_y)
                print(f"Adjusting lines: {lines}")

                self.multi_cell(w=w, h=h, text=final_text, border=upper_multi_cell_border, align=align, fill=fill, new_x='LEFT', new_y='NEXT')
                self.multi_cell(w=w, h=h, text=number_of_lines_to_add*int((w-c_margin_adjustment)/self.get_string_width(' '))*' ', border=lower_multi_cell_border, align=align, fill=fill, new_x=new_x, new_y=new_y)

        else:
            for i, line in enumerate(lines):
                self.cell(w=w, h=h, text=line, border=border, align=align, fill=fill, new_x="LEFT" if (i < len(lines)-1 or number_of_lines_to_add>0) else new_x, new_y="NEXT" if (i < len(lines)-1 or number_of_lines_to_add>0) else new_y)
            if number_of_lines_to_add>0:
                for i in range(number_of_lines_to_add):
                    self.cell(w=w, h=h, text=' ', border=border, align=align, fill=fill, new_x="LEFT" if i < number_of_lines_to_add-1 else new_x, new_y="NEXT" if i < number_of_lines_to_add-1 else new_y)

