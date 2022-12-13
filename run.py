import pytest

from scripts.handle_path import REPORTS_DIR

# pytest.main(['-m', 'smoke'])
# pytest.main(['--reruns', '2'])
pytest.main(['--alluredir', REPORTS_DIR] )
# pytest.main([r'--alluredir=D:\work\project\OutPut\reports'])
# pytest.main(['cases/tmx_connect/test_group.py', '--alluredir', REPORTS_DIR] )
