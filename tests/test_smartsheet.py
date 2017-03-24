# test_smartsheet.py
import pytest
from boxcomtools.smartsheet.sheet import Sheet


@pytest.mark.gen_test
def test_smartsheet_auth(monkeypatch):
    """
    TODO (sao)
    """

@pytest.mark.gen_test
def test_smartsheet_sheet_parse_values(monkeypatch):

    params = dict(
        test1='test_value_1',
        test2='test_value_2',
        test3='test_value_3',
        test4='test_value_4'
    )

    s = Sheet(params)
    assert s.test4 == 'test_value_4'

