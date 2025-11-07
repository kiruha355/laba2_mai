import os
import tempfile
import shutil
import pytest


@pytest.fixture
def temp_dir():
    root = tempfile.mkdtemp()
    with open(os.path.join(root, "file.txt"), "w") as f:
        f.write("cheto")
    os.mkdir(os.path.join(root, "folder"))
    with open(os.path.join(root, "folder", "another.txt"), "w") as f:
        f.write("postavte 90 ballov pls")
    yield root
    shutil.rmtree(root)


@pytest.fixture
def change_to_temp_dir(temp_dir):
    old = os.getcwd()
    os.chdir(temp_dir)
    yield temp_dir
    os.chdir(old)


@pytest.fixture
def initial_cwd():
    old_cwd = os.getcwd()
    yield old_cwd
    os.chdir(old_cwd)
