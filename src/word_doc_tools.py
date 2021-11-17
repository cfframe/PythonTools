# word_doc_tools.py

import datetime
import numpy as np
import pandas as pd
from pathlib import Path
import os
import random
import shutil
from skimage.transform import resize
import sys
import zipfile
# import xml.etree.ElementTree as ET
from lxml import etree as ET


class WordDocumentTools:
    """Utilities for handling Word Document files"""

    @staticmethod
    def iterate_tables(document_path: str):

        # Start from https://newbedev.com/how-do-i-extract-data-from-a-doc-docx-file-using-python

        WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
        PARA = WORD_NAMESPACE + 'p'
        TEXT = WORD_NAMESPACE + 't'
        TABLE = WORD_NAMESPACE + 'tbl'
        ROW = WORD_NAMESPACE + 'tr'
        CELL = WORD_NAMESPACE + 'tc'

        print('File path: \n')
        print(document_path)

        with zipfile.ZipFile(document_path) as docx:
            document = docx.read('word/document.xml')
            tree = ET.XML(document)
            # tree = xml.etree.ElementTree.XML(docx.read('word/document.xml'))
            root = ET.fromstring(document)

        count = 0
        sub_count = 0

        # Avoid doubling up cells that are in tables nested within tables
        for table in tree.iter(TABLE):
            table_parent = table.getparent()
            if table_parent.tag != CELL and count < 3:
                count += 1
                print(f'TABLE-{count}-{table}----------------')

                for row in {row: row for row in table.iter(ROW) if row.getparent().getparent().tag != CELL}:
                    for cell in {cell: cell for cell in row.iter(CELL)
                                 if cell.getparent().getparent().getparent().tag != CELL}:
                        print(''.join(node.text for node in cell.iter(TEXT)))

