
import pprint
from src.file_tools import FileTools as ft

folder_path = r"C:\Users\cframe\OneDrive - Sopra Steria\Documents\Training\Python Basics"

for file in ['Python_Basic_Advanced_Sessions_Feb23.ipynb', 'Python_Advanced_2.ipynb', 'Python_GUI_Updated.ipynb']:
    print(f'FILE: *********** {file} ***************')
    file_path = f'{folder_path}\\{file}'
    imports = ft.list_lines_with_term(file_path=file_path, term='import', exceptions='#')

    imports = list(set(imports))
    imports.sort()

    for line in imports:
        print(line)
