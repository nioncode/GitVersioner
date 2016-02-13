#!/bin/env python
import unittest
from GitVersioner import Version


class ParsingTestCase(unittest.TestCase):

    def test_equality(self):
        expected = Version(1, 2, 3, "213", 4, False)
        expected_copy = Version(1, 2, 3, "213", 4, False)
        expected_modified = Version(1, 2, 3, "213", 4, True)
        self.assertEqual(expected, expected)
        self.assertEqual(expected, expected_copy)
        self.assertNotEqual(expected, expected_modified)

    def test_None_raises(self):
        self.assertRaises(ValueError, lambda: Version.parse_from(None))

    def test_EmptyString_raises(self):
        self.assertRaises(ValueError, lambda: Version.parse_from(''))

    def test_hash_only(self):
        self.assertEquals(Version(0, 0, 0, "abcdefg", 0, False), Version.parse_from("abcdefg"))

    def test_hash_only_dirty(self):
        self.assertEquals(Version(0, 0, 0, "abcdefg", 0, True), Version.parse_from("abcdefg-dirty"))

    def test_tag_only(self):
        self.assertEquals(Version(1, 2, 3, None, 0, False), Version.parse_from("v1.2.3"))
        self.assertEquals(Version(1, 2, 3, None, 0, False), Version.parse_from("1.2.3"))

    def test_tag_only_dirty(self):
        self.assertEquals(Version(1, 2, 3, None, 0, True), Version.parse_from("v1.2.3-dirty"))
        self.assertEquals(Version(1, 2, 3, None, 0, True), Version.parse_from("1.2.3-dirty"))

    def test_tag_only_no_patch(self):
        self.assertEquals(Version(1, 2, 0, None, 0, False), Version.parse_from("v1.2"))
        self.assertEquals(Version(1, 2, 0, None, 0, False), Version.parse_from("1.2"))

    def test_tag_only_no_patch_dirty(self):
        self.assertEquals(Version(1, 2, 0, None, 0, True), Version.parse_from("v1.2-dirty"))
        self.assertEquals(Version(1, 2, 0, None, 0, True), Version.parse_from("1.2-dirty"))

    def test_commits_since(self):
        self.assertEquals(Version(1, 2, 0, "296cf8b", 12, False), Version.parse_from("v1.2.0-12-g296cf8b"))
        self.assertEquals(Version(1, 2, 0, "296cf8b", 12, True), Version.parse_from("v1.2.0-12-g296cf8b-dirty"))


if __name__ == '__main__':
    unittest.main()
