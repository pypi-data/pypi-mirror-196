import pytest


class SysExitUtil:
    @staticmethod
    def f() -> None:
        raise SystemExit(1)


def test_f() -> None:
    with pytest.raises(SystemExit):
        SysExitUtil.f()


if __name__ == "__main__":
    SysExitUtil.f()