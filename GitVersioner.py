#!/bin/env python
import argparse
import re


class Version:
    def __init__(self, major, minor, patch=0, pre_release_id=None, commit_hash=None, commits_since=0, is_dirty=False):
        self.major = major
        self.minor = minor
        self.patch = patch
        self.pre_release_id = pre_release_id
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

    def semantic_version(self, dirty_suffix='dirty'):
        s = "{}.{}.{}".format(self.major, self.minor, self.patch)
        if self.pre_release_id:
            s += '-' + self.pre_release_id
        if self.commits_since:
            s += '+' + str(self.commits_since)
        if self.hash:
            s += '.' + self.hash
        if self.is_dirty:
            s += '.' + dirty_suffix
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
        if '.' not in parts[0]:
            # Without a tag, the version string only consists of the SHA1 hash of the commit and the dirty flag.
            return Version(0, 0, commit_hash=parts[0], is_dirty=is_dirty)

        tag = parts.pop(0).lstrip('v')
        version_codes = tag.split('.')
        major = int(version_codes[0])
        minor = int(version_codes[1])
        patch = int(version_codes[2]) if len(version_codes) == 3 else 0
        if len(parts) == 0:
            return Version(major, minor, patch, is_dirty=is_dirty)

        commits_since = 0
        commit_hash = None
        if re.match('g[a-f0-9]+', parts[-1]):
            # The last component matches a g'sha1', assume this our commit hash.
            # Git adds a 'g' prefix to the hash, which must be removed.
            commit_hash = parts[-1][1:]
            # If we have a commit hash, there must also be a commits_since component.
            commits_since = int(parts[-2])
            parts = parts[:-2]
            if len(parts) == 0:
                return Version(major, minor, patch, commit_hash=commit_hash, commits_since=commits_since,
                               is_dirty=is_dirty)

        # All remaining parts are build identifiers.
        pre_release_id = '-'.join(parts)

        return Version(major, minor, patch, pre_release_id, commit_hash, commits_since, is_dirty)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Splits a version string into individual components.")
    parser.add_argument('version_string', type=str, help='Version string to parse.')
    args = parser.parse_args()
    version = Version.parse_from(args.version_string)
    print('Major: {}\nMinor: {}\nPatch: {}\nSemVer: {}'.format(version.major, version.minor, version.patch,
                                                               version.semantic_version(dirty_suffix='dev')))
