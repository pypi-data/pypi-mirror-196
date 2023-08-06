"""Tests whether the adder function indeed adds 2 to a given input."""
import unittest

from typeguard import typechecked

from src.gpt_docs_and_tests.adder import add_two


class Test_adder(unittest.TestCase):
    """Object used to test a parse_creds function."""

    # Initialize test object
    @typechecked
    def __init__(self, *args, **kwargs):  # type:ignore[no-untyped-def]
        super().__init__(*args, **kwargs)

    @typechecked
    def test_add_two_input_5(self) -> None:
        """Tests if add_two function adds 2 to an integer."""

        actual_result: int = add_two(x=5)
        expected_result: int = 7
        self.assertEqual(expected_result, actual_result)


if __name__ == "__main__":
    unittest.main()
