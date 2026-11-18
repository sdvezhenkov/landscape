import pytest

from app.tools.essential.env.get_env import get_env


def test_get_env_existing(
        monkeypatch,
):
    monkeypatch.setenv('TEST_KEY', 'TEST_VALUE')
    assert get_env('TEST_KEY') == 'TEST_VALUE'

def test_get_env(
        monkeypatch,
):
    monkeypatch.delenv('TEST_KEY', raising=False)
    assert get_env('TEST_KEY', 'TEST_VALUE') == 'TEST_VALUE'

def test_get_env_error(
        monkeypatch,
):
    monkeypatch.delenv('TEST_KEY', raising=False)
    with pytest.raises(KeyError):
        get_env('TEST_KEY')
