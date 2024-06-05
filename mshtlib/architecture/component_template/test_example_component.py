from unittest import TestCase

from src.components import ComponentExample


class SentenceSVOFormatterTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.component = ComponentExample()

    def forward(self):
        result = self.component()
        return result

    def test_1_case(self):
        pass
