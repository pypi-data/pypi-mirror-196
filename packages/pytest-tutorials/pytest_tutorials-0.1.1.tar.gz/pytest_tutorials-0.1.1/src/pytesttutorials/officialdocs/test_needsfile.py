import unittest


class TestTmpDir(unittest.TestCase):
    def test_needsfiles(self, tmp_path) -> None:
        print(f"Temp dir -> {tmp_path}")
        assert 1


if __name__ == "__main__":
    pass
