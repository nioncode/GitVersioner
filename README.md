# Git Versioner
Git Versioner takes a version string (e.g. from `git describe`) and splits it up into separate components.

The resulting `Version` object can then easily be printed according to [Semantic Versioning](http://semver.org/) rules.

It also provides a command line option to print the result as C preprocessor macros, so that it can easily be included in a build script.

You can pass any version string to GitVersioner, it does not need to come from `git describe` directly.
The following and more are supported:

- Git tags:
    - Plain: v1.2.3
    - Pre-Releases: v1.2.3-beta6
    - Dirty workspace: v1.2-dirty
    - Git describe output: v1.2-50-gf00000d
- Version number without leading 'v':
    - 1.2
    - 1.2-beta6

## Overview
The resulting semantic version always follows this pattern:

- Major.Minor.Patch (if one of them is not found in the tag or no tag is present at all, 0 will be used)
- Any pre-release identifiers (separated from the version number by a '-')
- Build metadata (commit count since last tag, commit hash, etc.), separated from previous string by '+'

That means, the Major, Minor, and Patch parts will always be a pure numerical representation. Any additional information will be put in the Semantic Versioning string. 

## Usage

    ./GitVersioner.py -h
    usage: GitVersioner.py [-h] [-f FILE | -g [GIT_DIR]] [-d DIRTY_SUFFIX] [-m]
                           [-p PREFIX]
                           [version_string]

    Splits a version string into individual components.

    positional arguments:
      version_string        Version string to parse. If omitted, the version will
                            be read from stdin. Will be ignored if either -f or -g
                            are given.

    optional arguments:
      -h, --help            show this help message and exit
      -f FILE, --file FILE  Read version string from file. Only interprets the
                            first line of the given file.
      -g [GIT_DIR], --git-dir [GIT_DIR]
                            Invoke `git describe` on optional directory. Default:
                            current working directory
      -d DIRTY_SUFFIX, --dirty-suffix DIRTY_SUFFIX
                            Suffix to use when the build version is dirty.
                            Default: 'dirty'

    Macros:
      C preprocessor options

      -m, --macros          Output C preprocessor style macros
      -p PREFIX, --prefix PREFIX
                            Prefix to add before each preprocessor variable

### Example

#### Simple version
    GitVersioner.py v1.1

> Major: 1<br>
> Minor: 1<br>
> Patch: 0<br>
> SemVer: 1.1.0

#### Pre-Releases
    GitVersioner.py v1.1-alpha.3

> Major: 1<br>
> Minor: 1<br>
> Patch: 0<br>
> SemVer: 1.1.0-alpha.3

#### Support for git describe features
    GitVersioner.py v1.1.0-23-gf096607-dirty

> Major: 1<br>
> Minor: 1<br>
> Patch: 0<br>
> SemVer: 1.1.0+23.f096607.dirty

#### Preprocessor output with custom prefix

    GitVersioner.py v1.1.0-23-gf096607-dirty --macros --prefix "WOW_"

> \#define WOW_MAJOR 1<br>
> \#define WOW_MINOR 1<br>
> \#define WOW_PATCH 0<br>
> \#define WOW_SEM_VER "1.1.0+23.f096607.dirty"
