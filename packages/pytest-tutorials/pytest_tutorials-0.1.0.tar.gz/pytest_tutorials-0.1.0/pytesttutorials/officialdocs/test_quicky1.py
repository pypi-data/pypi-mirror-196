class Quick1Utils:
    @staticmethod
    def inc(x: int) -> int:
        return x + 1


def test_answer():
    assert Quick1Utils.inc(x=3) == 4


if __name__ == "__main__":
    print()
