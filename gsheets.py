import gspread

class GSheets():
    def __init__(self, spreadsheet = None, worksheet = None) -> None:
        self.g_client = gspread.service_account(filename='/home/farid/python-projects/subnetting/Python-Sheets-API-Key.json')
        self.spreadsheet = self.g_client.open(spreadsheet)
        if type(worksheet) is int:
            self.worksheet = self.spreadsheet.get_worksheet(worksheet)
        else:
            self.worksheet = self.spreadsheet.worksheet(worksheet)

    def set_spreadsheet(self, title: str):
        self.spreadsheet = self.g_client.open(title)

    def set_worksheet(self, index__name ):
        if type(index__name) is str:
            self.worksheet = self.spreadsheet.get_worksheet(index__name)
        elif type(index__name) is int:
            self.worksheet = self.spreadsheet.worksheet(index__name)

    def get_cellvalue(self, *args):
        """
        Return a value from a specified cell

            args[0] : str|int -- A1 Notation|row
        
            args[1] : int -- column
        """
        if len(args) == 1:
            return self.worksheet.acell(args[0]).value
        else:
            return self.worksheet.cell(args[0], args[1]).value
    
    def get_values(self, row: bool, index: int):
        """
        Get values froma an entire row or column

            row : bool -- row=True, column=False
        
            index : int -- position
        """
        if row:
            return self.worksheet.row_values(index)
        else:
            return self.worksheet.col_values(index)

    def set_cellvalue(self, *args):
        """
        Set a value to a specified cell

            args[0] : {str|int} -- A1 Notation|row
        
            args[1] : {str|int} -- Value|column

            args[2] : int -- |Value
        """
        if len(args) == 2:
            return self.worksheet.update(args[0], args[1])
        elif len(args) == 3:
            return self.worksheet.update(args[0], args[1], args[2])
