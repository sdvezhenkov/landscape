import pytest

from app.tools.essential.request.pipe.pipe.errors.source_pipe_error import SourcePipeError
from app.tools.essential.request.pipe.pipe.errors.target_pipe_error import TargetPipeError
from app.tools.essential.request.pipe.pipe.pipe import pipe
from app.tools.essential.request.pipe.pipe.tests.conftest import TEST_MESSAGE, ExampleError, get_source, get_target


async def test_pipe():
    source_error = None
    target_error = None
    message = await pipe(
        lambda: get_source(source_error),
        lambda file: get_target(file, target_error),
    )
    assert type(message) is list
    assert message == TEST_MESSAGE

async def test_pipe_source_error():
    source_error = ExampleError()
    target_error = None
    with pytest.raises(SourcePipeError) as e:
        await pipe(
            lambda: get_source(source_error),
            lambda file: get_target(file, target_error),
        )
    assert type(e.value.__cause__) is ExampleError

async def test_pipe_target_error():
    source_error = None
    target_error = ExampleError()
    with pytest.raises(TargetPipeError) as e:
        await pipe(
            lambda: get_source(source_error),
            lambda file: get_target(file, target_error),
        )
    assert type(e.value.__cause__) is ExampleError

async def test_pipe_both_side_error():
    source_error = ExampleError()
    target_error = ExampleError()
    with pytest.raises(SourcePipeError) as e:
        await pipe(
            lambda: get_source(source_error),
            lambda file: get_target(file, target_error),
        )
    assert type(e.value.__cause__) is ExampleError
