from pathlib import Path
import click
from app.application import CompilationOptions, compile_command


@click.group()
def cli():
    pass


@cli.command()
@click.option('--recursive', '-r', is_flag=True, default=False, help='Recurse through subdirectories.')
@click.option('--in-place', is_flag=True, default=False, help='Remove .py and replace them with compiled .pyc files.')
@click.option('--create-empty-init', is_flag=True, default=False, help='Create an empty __init__.py file in the base directory path specified after compilation. Useful for interacting with tools such as colcon.')
@click.option('--exclude-files', multiple=True, help='Exclude pattern(s) for files to be excluded during compilation and replacement.')
@click.option('--exclude-dirs', multiple=True, help='Exclude pattern(s) for directories to be excluded during compilation and replacement. If the directory is skipped and --create-empty-init is True, the __init__.py file will not be created.')
@click.option('--ignore-symlinks', is_flag=True, default=False, help='Sometimes symlinks cause problems. Enable this flag to ignore symlinks.')
@click.option('--optimize', is_flag=True, default=False, help='Perform bytecode optimisation')
@click.option('--overly-optimize', is_flag=True, default=False, help='Perform bytecode optimisation and remove docstrings.')
@click.argument('paths', type=click.Path(exists=True), nargs=-1)
def compile(paths, recursive, in_place, create_empty_init, exclude_files, exclude_dirs, ignore_symlinks, optimize, overly_optimize):
    optimization_level = 0
    if (optimize):
        optimization_level = 1
    if (overly_optimize):
        optimization_level = 2
    options = CompilationOptions(
        recursive=recursive,
        in_place=in_place,
        create_empty_init=create_empty_init,
        exclude_files=exclude_files,
        exclude_dirs=exclude_dirs,
        ignore_symlinks=ignore_symlinks,
        optimize=optimization_level
    )
    for path in paths:
        compile_command(
            Path(path),
            options
        )
