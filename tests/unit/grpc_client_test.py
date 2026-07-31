# sample test
import pytest


@pytest.mark.asyncio
async def test_something_async() -> None:
    result = await _return_async(True)
    assert result


async def _return_async(passed_in_result: bool) -> bool:
    return passed_in_result
