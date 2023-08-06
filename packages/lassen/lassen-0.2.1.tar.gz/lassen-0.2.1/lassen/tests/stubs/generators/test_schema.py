from typing import Dict, List, Optional, Union

import pytest

from lassen.stubs.generators.schema import make_optional


@pytest.mark.parametrize(
    "input_type, expected_output",
    [
        (int, Union[int, type(None)]),
        (int, int | None),
        (str, Union[str, type(None)]),
        (List[int], Union[List[int], type(None)]),
        (Dict[str, int], Union[Dict[str, int], type(None)]),
        (Union[int, str], Union[int, str, type(None)]),
        (Union[int, None], Union[int, None]),
        (Optional[int], Union[int, None]),
        (Optional[str], Union[str, None]),
    ],
)
def test_make_optional(input_type, expected_output):
    assert make_optional(input_type) == expected_output
