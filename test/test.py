#!/bin/env python
import unittest
from GitVersioner import Version, version_as_preprocessor_macros


class ParsingTestCase(unittest.TestCase):

    def test_equality(self):
        expected = Version(1, 2, 3, "alpha.3", "213", 4, False)
        expected_copy = Version(1, 2, 3, "alpha.3", "213", 4, False)
        expected_modified = Version(1, 2, 3, "alpha.3", "213", 4, True)
        self.assertEqual(expected, expected)
        self.assertEqual(expected, expected_copy)
        self.assertNotEqual(expected, expected_modified)

    def test_None_raises(self):
        self.assertRaises(ValueError, lambda: Version.parse_from(None))

    def test_EmptyString_raises(self):
        self.assertRaises(ValueError, lambda: Version.parse_from(''))

    def test_hash_only(self):
        self.assertEqual(Version(0, 0, commit_hash="abcdefg"), Version.parse_from("abcdefg"))

    def test_hash_only_dirty(self):
        self.assertEqual(Version(0, 0, commit_hash="abcdefg", is_dirty=True), Version.parse_from("abcdefg-dirty"))

    def test_tag_only(self):
        self.assertEqual(Version(1, 2, 3), Version.parse_from("v1.2.3"))
        self.assertEqual(Version(1, 2, 3), Version.parse_from("1.2.3"))

    def test_tag_only_dirty(self):
        self.assertEqual(Version(1, 2, 3, is_dirty=True), Version.parse_from("v1.2.3-dirty"))
        self.assertEqual(Version(1, 2, 3, is_dirty=True), Version.parse_from("1.2.3-dirty"))

    def test_tag_only_no_patch(self):
        self.assertEqual(Version(1, 2, 0), Version.parse_from("v1.2"))
        self.assertEqual(Version(1, 2, 0), Version.parse_from("1.2"))

    def test_tag_only_no_patch_dirty(self):
        self.assertEqual(Version(1, 2, 0, is_dirty=True), Version.parse_from("v1.2-dirty"))
        self.assertEqual(Version(1, 2, 0, is_dirty=True), Version.parse_from("1.2-dirty"))

    def test_invalid_tag(self):
        self.assertRaises(ValueError, lambda: Version.parse_from("v1.2.3.1.1.1.1"))

    def test_commits_since(self):
        self.assertEqual(Version(1, 2, 0, None, "296cf8b", 12, False), Version.parse_from("v1.2.0-12-g296cf8b"))
        self.assertEqual(Version(1, 2, 0, None, "296cf8b", 12, True), Version.parse_from("v1.2.0-12-g296cf8b-dirty"))

    def test_pre_release_ids(self):
        self.assertEqual(Version(1, 2, 3, "alpha.3"), Version.parse_from("1.2.3-alpha.3"))
        self.assertEqual(Version(1, 2, 3, "alpha.3-special"), Version.parse_from("1.2.3-alpha.3-special"))
        self.assertEqual(Version(1, 2, 3, "alpha.3-more-special"), Version.parse_from("1.2.3-alpha.3-more-special"))
        self.assertEqual(Version(1, 2, 3, "alpha.3", None, 0, True), Version.parse_from("v1.2.3-alpha.3-dirty"))
        self.assertEqual(Version(1, 2, 3, "alpha.3", "296cf8b", 12, True),
                          Version.parse_from("v1.2.3-alpha.3-12-g296cf8b-dirty"))


class SemanticVersionTestCase(unittest.TestCase):
    def test_consists_of_major_minor_patch(self):
        self.assertEqual("1.2.0", Version(1, 2).semantic_version())
        self.assertEqual("1.2.3", Version(1, 2, 3).semantic_version())

    def test_pre_releases(self):
        self.assertEqual("1.2.3-alpha.3-special", Version(1, 2, 3, "alpha.3-special").semantic_version())

    def test_metadata_dirty(self):
        self.assertEqual("1.2.0+dirty", Version(1, 2, is_dirty=True).semantic_version())

    def test_metadata_dirty_customizable(self):
        self.assertEqual("1.2.0+dev", Version(1, 2, is_dirty=True).semantic_version('dev'))

    def test_metadata_multiple(self):
        self.assertEqual("1.2.3-alpha.3-special+12.296cf8b.dirty",
                          Version(1, 2, 3, "alpha.3-special", "296cf8b", 12, True).semantic_version())


class FormatterTestCase(unittest.TestCase):
    def test_as_preprocessor_macros(self):
        v = Version(4, 6, 1, "alpha.3-special", "296cf8b", 12, True)
        self.assertEqual(('#define SOME_MAJOR 4\n'
                          '#define SOME_MINOR 6\n'
                          '#define SOME_PATCH 1\n'
                          '#define SOME_SEM_VER \"{}\"'
                          ).format(v.semantic_version('dev')), version_as_preprocessor_macros(v, 'SOME_', 'dev'))


if __name__ == '__main__':
    unittest.main()
