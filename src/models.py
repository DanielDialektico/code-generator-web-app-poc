import os
import pandas as pd

class CodeManager:
    """
    The CodeManager class is responsible for managing and generating unique codes based on combinations
    of three values: division_code, area_code, and doc_code. The generated codes are stored in an Excel file.

    Attributes:
    -----------
    excel_file : str
        The name or path of the Excel file where the codes are stored and loaded from. Default is 'codes.xlsx'.
    codes : list
        A list that contains all the codes generated so far. Each code is a tuple with the structure
        (division_code, area_code, doc_code, num_code, full_code).
    code_counters : dict
        A dictionary that keeps track of the number of codes generated for each combination of 
        (division_code, area_code, doc_code). This is used to generate sequential codes.
    """

    def __init__(self, excel_file='codes.xlsx'):
        """
        Initializes the CodeManager instance.

        Parameters:
        -----------
        excel_file : str, optional
            The name or path of the Excel file where codes will be stored. Default is 'codes.xlsx'.
        """
        self.excel_file = excel_file
        self.codes = []
        self.code_counters = {}
        self.load_existing_codes()

    def load_existing_codes(self):
        """
        Loads existing codes from the Excel file if it exists.

        This method reads the Excel file into a pandas DataFrame, converts the DataFrame to a list of tuples,
        and updates the internal list of codes and code counters to reflect the existing data.
        """
        if os.path.exists(self.excel_file):
            df_existing = pd.read_excel(self.excel_file)
            self.codes = df_existing.values.tolist()
            for _, row in df_existing.iterrows():
                key = (row['CD'], row['Área'], row['Doc'])
                if key in self.code_counters:
                    self.code_counters[key] = max(self.code_counters[key], int(row['Consecutivo']))
                else:
                    self.code_counters[key] = int(row['Consecutivo'])

    def save_to_excel(self):
        """
        Saves the current list of codes to the specified Excel file.

        This method creates a pandas DataFrame from the internal codes list and writes it to the Excel file
        with the specified column names. The index is not included in the output file.
        """
        df = pd.DataFrame(self.codes, columns=['Division_Code', 'Area_Code', 'Doc_Code', 'ID', 'Code'])
        df.to_excel(self.excel_file, index=False)

    def generate_code(self, division_code, area_code, doc_code):
        """
        Generates a new unique code for the specified combination of division_code, area_code, and doc_code.

        Parameters:
        -----------
        division_code : str
            The division code for the new code.
        area_code : str
            The area code for the new code.
        doc_code : str
            The document code for the new code.

        Returns:
        --------
        full_code : str
            The newly generated full code in the format 'DIV-AREA-DOC-001'.
        """
        key = (division_code, area_code, doc_code)
        if key in self.code_counters:
            self.code_counters[key] += 1
        else:
            self.code_counters[key] = 1

        num_code = f'{self.code_counters[key]:03}'
        full_code = f'{division_code}-{area_code}-{doc_code}-{num_code}'
        self.codes.append((division_code, area_code, doc_code, num_code, full_code))
        self.save_to_excel()
        return full_code