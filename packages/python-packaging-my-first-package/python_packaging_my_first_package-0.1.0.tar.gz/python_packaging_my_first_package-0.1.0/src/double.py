from typing import TypeVar

T = TypeVar("T", int, str, float)


def double(arg: T) -> T:
    """My docstring"""
    return arg * 2


if __name__ == "__main__":
    print(double(3))
