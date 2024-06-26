import pytest
from .user_funcs import DaysSuffixManager


@pytest.mark.parametrize("num, expected_suffix",
                         [
                            (1, 'день'), (2, 'дня'), (3, 'дня'), (4, 'дня'),
                            (5, 'дней'), (10, 'дней'), (11, 'дней'), (12, 'дней'),
                            (13, 'дней'), (14, 'дней'), (20, 'дней'), (21, 'день'),
                            (22, 'дня'), (23, 'дня'), (24, 'дня'), (25, 'дней'),
                            (100, 'дней'), (101, 'день'), (102, 'дня'),
                            (112, 'дней'), (122, 'дня'), (121, 'день')
                          ]
                         )
def test_change_suffix(num, expected_suffix):
    dsm = DaysSuffixManager(num)
    assert dsm.change_suffix() == expected_suffix
