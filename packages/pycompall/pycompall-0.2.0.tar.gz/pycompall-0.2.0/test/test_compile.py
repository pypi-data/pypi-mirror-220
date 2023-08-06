from typing import List, Tuple
import pytest
from pathlib import Path
from app.application import CompilationOptions, _get_pycache_pyc_from_py, compile_command, rmtree


@pytest.fixture
def temp_dir():
    temp_path = Path('./temp')
    temp_path.mkdir(exist_ok=True)
    yield temp_path
    rmtree(temp_path, missing_ok=True)


@pytest.fixture
def one_py_file(temp_dir: Path):
    file = temp_dir / 'one.py'
    file.touch()
    yield temp_dir, file
    file.unlink(missing_ok=True)


@pytest.fixture
def nested_py_file(temp_dir: Path):
    files = [
        temp_dir / 'one.py',
        temp_dir / 'two/two.py',
        temp_dir / 'two/three/three.py'
    ]
    for file in files:
        file.parent.mkdir(parents=True, exist_ok=True)
        file.touch()

    yield temp_dir, files

    for file in files:
        rmtree(file.parent, missing_ok=True)


class TestCompileOneFile:
    def test_compile_one_by_file(self, one_py_file: Tuple[Path, Path]):
        """Test compiling one file by file path, without replacing it."""
        dir, file = one_py_file
        options = CompilationOptions(recursive=False, in_place=False)
        compile_command(file, options)
        expected_pycache_file = _get_pycache_pyc_from_py(file)
        assert expected_pycache_file is not None
        assert expected_pycache_file.exists()
        assert file.exists()

    def test_compile_one_by_dir(self, one_py_file: Tuple[Path, Path]):
        """Test compiling one file by parent directory path, without replacing it."""
        dir, file = one_py_file
        options = CompilationOptions(recursive=False, in_place=False)
        compile_command(file, options)
        expected_pycache_file = _get_pycache_pyc_from_py(file)
        assert expected_pycache_file is not None
        assert expected_pycache_file.exists()
        assert file.exists()

    def test_compile_one_by_file_in_place(self, one_py_file: Tuple[Path, Path]):
        """Test compiling one file by file path, replacing it."""
        dir, file = one_py_file
        options = CompilationOptions(recursive=False, in_place=True)
        compile_command(file, options)
        expected_pyc_file = file.with_suffix('.pyc')
        assert expected_pyc_file is not None
        assert expected_pyc_file.exists()
        assert not file.exists()

    def test_compile_one_by_dir_in_place(self, one_py_file: Tuple[Path, Path]):
        """Test compiling one file by parent directory path, replacing it."""
        dir, file = one_py_file
        options = CompilationOptions(recursive=False, in_place=True)
        compile_command(file, options)
        expected_pyc_file = file.with_suffix('.pyc')
        assert expected_pyc_file is not None
        assert expected_pyc_file.exists()
        assert not file.exists()


class TestCompileNestedFiles:
    def test_compile_nested_by_file(self, nested_py_file: Tuple[Path, List[Path]]):
        """Test compiling nested files by file path, without replacing it."""
        dir, files = nested_py_file
        options = CompilationOptions(recursive=False, in_place=False)
        compile_command(files[0], options)
        expected_pycache_file = _get_pycache_pyc_from_py(files[0])
        unexpected_pycache_files = [
            _get_pycache_pyc_from_py(file) for file in files[1:]]

        assert files[0].exists()
        assert expected_pycache_file is not None and expected_pycache_file.exists()
        for file, unexpected_pycache_file in zip(files[1:], unexpected_pycache_files):
            assert file.exists()
            assert unexpected_pycache_file is None or \
                not unexpected_pycache_file.exists()

    def test_compile_nested_by_dir_non_recursive(self, nested_py_file: Tuple[Path, List[Path]]):
        """Test compiling nested files by parent directory path (non-recursive), without replacing it."""
        dir, files = nested_py_file
        options = CompilationOptions(recursive=False, in_place=False)
        compile_command(dir, options)
        expected_pycache_files = [_get_pycache_pyc_from_py(
            file) for file in dir.glob('*.py')]
        for file in files:
            assert file.exists()
        for pycache_file in expected_pycache_files:
            assert pycache_file is not None and pycache_file.exists()

    def test_compile_nested_by_dir_recursive(self, nested_py_file: Tuple[Path, List[Path]]):
        """Test compiling nested files by parent directory path (recursive), without replacing it."""
        dir, files = nested_py_file
        options = CompilationOptions(recursive=True, in_place=False)
        compile_command(dir, options)
        expected_pycache_files = [_get_pycache_pyc_from_py(
            file) for file in files]

        for file in files:
            assert file.exists()
        for pycache_file in expected_pycache_files:
            assert pycache_file is not None and pycache_file.exists()

    def test_compile_nested_by_dir_non_recursive_in_place(self, nested_py_file: Tuple[Path, List[Path]]):
        """Test compiling nested files by parent directory path (non-recursive), replacing it."""
        dir, files = nested_py_file
        expected_compiled_files = list(dir.glob('*.py'))
        compile_command(dir, CompilationOptions(
            recursive=False, in_place=True))

        for file in files:
            if file in expected_compiled_files:
                assert not file.exists()
                assert file.with_suffix('.pyc').exists()
            else:
                assert file.exists()
                assert not file.with_suffix('.pyc').exists()

    def test_compile_nested_by_dir_recursive_in_place(self, nested_py_file: Tuple[Path, List[Path]]):
        """Test compiling nested files by parent directory path (recursive), replacing it."""
        dir, files = nested_py_file
        compile_command(dir, CompilationOptions(recursive=True, in_place=True))
        for file in files:
            assert not file.exists()
            assert file.with_suffix('.pyc').exists()


class TestCreateEmptyInit:
    def test_create_empty_init_by_file_fails(self, one_py_file: Tuple[Path, Path]):
        dir, file = one_py_file
        with pytest.raises(ValueError):
            compile_command(file, CompilationOptions(create_empty_init=True))

    def test_create_empty_init(self, one_py_file: Tuple[Path, Path]):
        dir, file = one_py_file
        compile_command(dir, CompilationOptions(create_empty_init=True))

        assert file.exists()
        expected_pycache_file = _get_pycache_pyc_from_py(file)
        assert expected_pycache_file is not None and expected_pycache_file.exists()
        assert (dir / '__init__.py').exists()


class TestExcludeFilePattern:
    def test_exclude_all_pattern(self, nested_py_file: Tuple[Path, List[Path]]):
        dir, files = nested_py_file
        pattern = '*.py'
        options = CompilationOptions(
            recursive=True, in_place=True, exclude_files=(pattern,))
        compile_command(dir, options)
        for file in files:
            if (file.match(pattern)):
                assert file.exists()
                assert not file.with_suffix('.pyc').exists()
            else:
                assert not file.exists()
                assert file.with_suffix('.pyc').exists()

    def test_exclude_one_pattern(self, nested_py_file: Tuple[Path, List[Path]]):
        dir, files = nested_py_file
        pattern = 'one.py'
        options = CompilationOptions(
            recursive=True, in_place=True, exclude_files=(pattern,))
        compile_command(dir, options)
        for file in files:
            if (file.match(pattern)):
                assert file.exists()
                assert not file.with_suffix('.pyc').exists()
            else:
                assert not file.exists()
                assert file.with_suffix('.pyc').exists()


class TestExcludeDirPattern:
    def test_exclude_all_pattern(self, nested_py_file: Tuple[Path, List[Path]]):
        dir, files = nested_py_file
        pattern = '*'
        options = CompilationOptions(
            recursive=True, in_place=True, create_empty_init=True, exclude_dirs=(pattern,))
        compile_command(dir, options)
        for file in files:
            dir = file.parent
            init_file = dir / '__init__.py'
            assert not init_file.exists()
            assert file.exists()
            assert not file.with_suffix('.pyc').exists()

    def test_exclude_one_pattern(self, nested_py_file: Tuple[Path, List[Path]]):
        dir, files = nested_py_file
        print(dir)
        pattern = 'two'
        options = CompilationOptions(
            recursive=True, in_place=True, create_empty_init=True, exclude_dirs=(pattern,))
        compile_command(dir, options)
        for file in files:
            if 'two' in str(file):
                assert file.exists()
                assert not file.with_suffix('.pyc').exists()
            else:
                assert not file.exists()
                assert file.with_suffix('.pyc').exists()

        init_file = dir / '__init__.py'
        assert init_file.exists()

    def test_exclude_base_pattern(self, nested_py_file: Tuple[Path, List[Path]]):
        dir, files = nested_py_file
        pattern = 'temp'
        options = CompilationOptions(
            recursive=True, in_place=True, exclude_dirs=(pattern,))
        compile_command(dir, options)
        for file in files:
            assert file.exists()
            assert not file.with_suffix('.pyc').exists()

        init_file = dir / '__init__.py'
        assert not init_file.exists()
