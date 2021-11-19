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

    WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    PARA = WORD_NAMESPACE + 'p'
    TEXT = WORD_NAMESPACE + 't'
    TABLE = WORD_NAMESPACE + 'tbl'
    ROW = WORD_NAMESPACE + 'tr'
    CELL = WORD_NAMESPACE + 'tc'

    @staticmethod
    def iterate_tables(document_path: str) -> list:
        """

        :param document_path: str - path to Microsoft Word document containing table(s)
        :return: list of json representations of tables
        """
        # Start from https://newbedev.com/how-do-i-extract-data-from-a-doc-docx-file-using-python

        print('File path: \n')
        print(document_path)

        output = []

        with zipfile.ZipFile(document_path) as docx:
            document = docx.read('word/document.xml')
            tree = ET.XML(document)

        # Avoid doubling up cells that are in tables nested within tables
        for table in tree.iter(WordDocumentTools.TABLE):
            table_parent = table.getparent()
            if table_parent.tag != WordDocumentTools.CELL:
                output.append(WordDocumentTools.json_from_word_table(table))

        return output

    @staticmethod
    def json_from_word_table(table) -> str:
        """Return json representation of a Microsoft Word table that is represented as an lxml.Element.
        Tables nested in a cell are compressed to bare text and are not treated as separate tables.

        :param table: input Microsoft Word table
        :return str: json representation
        """
        datalist = []
        for row in {row: row[0] for row in table.iter(WordDocumentTools.ROW)
                    if row.getparent().getparent().tag != WordDocumentTools.CELL}:
            row_data = []
            for cell in {cell: cell for cell in row.iter(WordDocumentTools.CELL)
                         if cell.getparent().getparent().getparent().tag != WordDocumentTools.CELL}:
                # print(''.join(node.text for node in cell.iter(TEXT)))
                row_data.append(''.join(node.text.strip() for node in cell.iter(WordDocumentTools.TEXT)))
            datalist.append(row_data)

        df = pd.DataFrame(datalist)
        # Reset column headers to first row
        df = df.rename(columns=df.iloc[0]).drop(df.index[0]).reset_index(drop=True)

        return pd.DataFrame.to_json(df)

