import pytest


@pytest.mark.usefixtures("init_test")
class TestScp:
    @pytest.mark.parametrize('case', [1, 2, 3])
    def test_print_num(self, case, init_test):
        print(case)