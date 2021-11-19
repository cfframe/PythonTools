# word_doc_tools_test_case.py

import datetime
import filecmp
import numpy as np
import os
import shutil
import unittest
import zipfile

from pathlib import Path
from lxml import etree as ET
from src.file_tools import FileTools
from src.word_doc_tools import WordDocumentTools


class WordDocumentToolsTestCase(unittest.TestCase):
    """Test names are generally self-explanatory and so docstrings not provided on an individual basis other
    than by exception.

    Keyword arguments:
    TestCase -- standard class required for tests based on unittest.case
    """

    def setUp(self):
        """Fixtures used by tests."""
        self.Root = Path(__file__).parent

        self.TestWordDocSimpleTablePath = os.path.join(self.Root, 'TestWordDocSimpleTable.docx')
        self.TestWordDocTableAcrossPagePath = os.path.join(self.Root, 'TestWordDocTableAcrossPage.docx')
        self.TestWordDocNestedTablePath = os.path.join(self.Root, 'TestWordDocNestedTable.docx')
        self.TestWordDocThreeTablesPath = os.path.join(self.Root, 'TestWordDocThreeTables.docx')
        self.TableJsonSimple = '{"Field":{"0":"SimpleId","1":"AField","2":"AnotherField"},"Description":{"0":"Unique ' \
                               'identifier.","1":"Stuff","2":"More stuff"},"Typeofvariable":{"0":"INT","1":"CHAR 30",' \
                               '"2":"CHAR 30"}}'
        self.TableJsonAcrossPage = \
            '{"Fieldname":{"0":"LongTableId","1":"Field2","2":"Field3","3":"Field4","4":"Field5","5":"Field6",' \
            '"6":"Field7","7":"Field8"},"Description":{"0":"Long table ID","1":"Dummy text. Video provides a powerful ' \
            'way to help you prove your point. When you click Online Video, you can paste in the embed code for the ' \
            'video you want to add.","2":"More dummy text.Type of episode . This value can be : \\u201c1\\u201d,' \
            '\\u201d2\\u201d or \\u201d3\\u201d .Video provides a powerful way to help youprove your point. When you ' \
            'click Online Video, you can paste in the embed code for the video you want to add.","3":"Dummy text.",' \
            '"4":"Dummy text.","5":"Dummy text. Numbers starting by \\u2018000000001\\u2019.","6":"Even more dummy ' \
            'text.","7":"Quick admission indicator. Can be:\\u201cX\\u201d for Yes.\\u201c\\u201d for No."},' \
            '"Typeofvariable":{"0":"INT","1":"CHAR  10","2":"CHAR  1","3":"CHAR  10","4":"CHAR  6","5":"CHAR  9",' \
            '"6":"CHAR  1","7":"CHAR  1"}}'

        self.TableJsonHasSubTable = \
            '{"Fieldname":{"0":"TableWithSubId","1":"SubTableInDescription","2":"SpaceToTrim","3":"AnotherField"},' \
            '"Description":{"0":"Unique identifier. Number starting by \\u20181\\u2019.","1":"Gender identifier.M = ' \
            'MaleU = unknownF = Female","2":"Surname1.","3":"Middlename."},"Typeofvariable":{"0":"INT","1":"CHAR 1",' \
            '"2":"CHAR 30","3":"CHAR 30"}}'

        self.dummy = 'dummy'

    @staticmethod
    def get_first_table_helper(document_path: str) -> ET.Element:
        """ Unable at present to reasonably easily directly generate an lxml Element object that has a table.
        This helper loads a test document which should have at least one table and returns the first table.

        :param document_path: Path to a Word document
        :return Element: table
        """
        with zipfile.ZipFile(document_path) as docx:
            document = docx.read('word/document.xml')
            tree = ET.XML(document)

        for table in tree.iter(WordDocumentTools.TABLE):
            return table

        return None

    def test_json_from_word_table__simple_table(self):
        expected = self.TableJsonSimple
        test_table = self.get_first_table_helper(self.TestWordDocSimpleTablePath)
        actual = WordDocumentTools.json_from_word_table(test_table)
        self.assertTrue(expected == actual)

    def test_json_from_word_table__table_across_page(self):
        expected = self.TableJsonAcrossPage
        test_table = self.get_first_table_helper(self.TestWordDocTableAcrossPagePath)
        actual = WordDocumentTools.json_from_word_table(test_table)
        self.assertTrue(expected == actual)

    def test_json_from_word_table__handle_sub_table(self):
        expected = self.TableJsonHasSubTable
        test_table = self.get_first_table_helper(self.TestWordDocNestedTablePath)
        actual = WordDocumentTools.json_from_word_table(test_table)
        self.assertTrue(expected == actual)

    def test_iterate_tables__doc_with_three_top_level_tables__returns_list_of_three(self):
        expected = 3
        actual = len(WordDocumentTools.iterate_tables(self.TestWordDocThreeTablesPath))
        self.assertTrue(expected == actual)
