# Python 2 Package Finder

If you're unlucky enough to still work on a legacy Python 2 codebase you may have to add new packages to your project, however all maintained packages have dropped support for Python 2 years ago. This tool will automatically find the last version of a package that was flagged as supporting a specific version of Python.

## Install

The recommended way to install is to use `pipx`:

```pipx install py2-package-finder```

## Usage

```py2-package-finder [PACKAGE_NAME]```

You can specify a different Python version using

```py2-package-finder --python 3.4 [PACKAGE_NAME]```
