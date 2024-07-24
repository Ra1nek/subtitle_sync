import unittest
from subtitle_sync.logic.subtitle_sync import parse_srt, format_subtitle

class TestSubtitleSyncFunctions(unittest.TestCase):

    def test_parse_srt(self):
        content = """1
00:00:00,000 --> 00:00:10,000
Hello world

2
00:00:10,000 --> 00:00:20,000
This is a test subtitle
"""
        expected = [
            ('1', '00:00:00,000 --> 00:00:10,000', 'Hello world'),
            ('2', '00:00:10,000 --> 00:00:20,000', 'This is a test subtitle')
        ]
        result = parse_srt(content)
        self.assertEqual(result, expected)

    def test_format_subtitle(self):
        self.assertEqual(format_subtitle("  hello world "), "hello world")
        self.assertEqual(format_subtitle("   test subtitle "), "test subtitle")
        self.assertEqual(format_subtitle("  EXAMPLE "), "EXAMPLE")

if __name__ == "__main__":
    unittest.main()
