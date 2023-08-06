# Pycompall Package
Pycompall is a wrapper around the default `compileall` Python utility to compile `.py` to `.pyc` files to provide a more configurable interface and as a build tool when configuring python files.

This package is also useful for code obfuscation, especially since most `.py` files can be substituted for their compiled bytecode equivalents most of the time.


## Installation
```sh
pip install pycompall
```

## Usage
`pycompall compile [OPTIONS] [PATH]`. 

Without any options, this will compile all `.py` files in the current directory (or file) into the default `__pycache__` directory.

### Options
#### `-r`, `--recursive`

Recurse through subdirectories.

#### `--in-place`

Remove original `.py` files and replace them with compiled `.pyc` files.

#### `--create-empty-init`

Create an empty `__init__.py` file in the base directory path specified after compilation. Useful for interacting with other build tools such as colcon that require a package to have an `__init__.py` file.

- Note: this only adds the file in the **base directory** specified, regardless of whether the `--recursive` flag is specified.

#### `--exclude-files TEXT`  

Exclude pattern(s) for files to be excluded during                    compilation and replacement.

- Note: this option supports globbing patterns with python's `Path.match` method, but this requires globs to be passed as strings to the tool, so you must wrap the glob in quotes (e.g. `pycompall compile --exclude-files '*.py'`).
- To specify multiple files to exclude, write the flag again (e.g. `pycompall compile --exclude-files '*test.py' --exclude-files 'test/*.py'`)

#### `--exclude-dirs TEXT` 

Exclude pattern(s) for directories to be excluded during compilation and replacement. Note that if the directory is skipped and --create-empty-init is True, the `__init__.py` file will not be created.

- Note: this option supports globbing patterns with python's `Path.match` method, but this requires globs to be passed as strings to the tool, so you must wrap the glob in quotes (e.g. `pycompall compile --exclude-dirs 'test*'`).
- To specify multiple directories to exclude, write the flag again (e.g. `pycompall compile --exclude-dirs 'test' --exclude-dirs 'utils'`)

#### `--ignore-symlinks`

Sometimes symlinks causes problems. Enable this flag to ignore symlinks.