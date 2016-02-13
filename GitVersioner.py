#!/bin/env python
import argparse


class Version:
    def __init__(self, major, minor, patch=0, commit_hash=None, commits_since=0 , is_dirty=False):
        self.major = major
        self.minor = minor
        self.patch = patch
        self.hash = commit_hash
        self.commits_since = commits_since
        self.is_dirty = is_dirty

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    def semantic_version(self):
        s = "{}.{}.{}".format(self.major, self.minor, self.patch)
        if self.commits_since:
            s += '+' + str(self.commits_since)
        if self.hash:
            s += '[' + self.hash + ']'
        if self.is_dirty:
            s += '-dirty'
        return s

    @classmethod
    def parse_from(cls, version_string: str):
        """
        Splits a version string (retrieved e.g. by calling `git describe --tags --dirty --always`) into different parts.

        :param version_string: The version string.
        :return: Version object
        """
        if not version_string:
            raise ValueError("version_string must be a non-empty string")

        parts = version_string.split('-')

        is_dirty = parts[-1] == 'dirty'
        if is_dirty:
            parts = parts[:-1]

        major = 0
        minor = 0
        patch = 0
        commits_since = 0
        commit_hash = None

        has_tag = '.' in parts[0]
        if has_tag:
            # We have a valid tag.
            tag = parts.pop(0).lstrip('v')
            version_codes = tag.split('.')
            major = int(version_codes[0])
            minor = int(version_codes[1])
            patch = int(version_codes[2]) if len(version_codes) == 3 else 0

            try:
                commits_since = int(parts[0])
                parts.pop(0)
            except (IndexError, ValueError):
                # There are no commits since.
                pass

        try:
            commit_hash = parts.pop(0)
            if has_tag:
                # Git prefixes the SHA1 hash with a 'g', but only if it follows a tag.
                commit_hash = commit_hash[1:]
        except IndexError:
            # There is no hash left.
            pass

        return Version(major, minor, patch, commit_hash, commits_since, is_dirty)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Splits a version string into individual components.")
    parser.add_argument('version_string', type=str, help='Version string to parse.')
    args = parser.parse_args()
    version = Version.parse_from(args.version_string)
    print('Major: {}\nMinor: {}\nPatch: {}\nSemVer: {}'.format(version.major, version.minor, version.patch,
                                                               version.semantic_version()))
