from subprocess import run

# run(["eval $(micromamba shell hook --shell=)"])
import pytest

if __name__ == "__main__":
    pytest.main(["/home/dan/sqlalchemy-views/tests/test_views.py", "--sw"])
