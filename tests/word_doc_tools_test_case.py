# word_doc_tools_test_case.py

import datetime
import filecmp
import numpy as np
import os
import shutil
import unittest

from pathlib import Path
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

        self.TestWordDocPath = os.path.join(self.Root, 'TestWordDoc.docx')
        self.dummy = 'dummy'

    def test_iterate_tables(self):

        WordDocumentTools.iterate_tables(self.TestWordDocPath)
        self.fail()

