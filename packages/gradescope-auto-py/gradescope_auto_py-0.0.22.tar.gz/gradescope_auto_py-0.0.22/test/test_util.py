import pytest

from gradescope_auto_py import __file__ as gap_file
from gradescope_auto_py.util import *

folder = pathlib.Path(gap_file).parents[1] / 'test' / 'ex_util'


def test_get_variable():
    s_out = get_variable(folder=folder, variable_name='some_variable',
                         exclude_file='other*.py')
    assert s_out == 'you found me!'

    s_out = get_variable(folder=folder, variable_name='some_variable',
                         exclude_file=('other*.py', 'target0.py'))
    assert s_out == 'target_with_error'


def test_import_module_search():
    # proper
    file, submitted = import_module_search(folder,
                                           search='some_variable',
                                           exclude_file='*1.py')
    assert submitted.some_variable == 'you found me!'
    assert file.name == 'target0.py'

    # a bit ambiguous (though it does print a message to user)
    file, submitted = import_module_search(folder, search='some_variable')
    assert submitted.some_variable == 'this isnt quite the target'
    assert file.name == 'other1.py'

    with pytest.raises(FileNotFoundError):
        import_module_search(folder, search='this string isnt in any file')

    with pytest.raises(FileExistsError):
        # two modules both have some_variable, we avoid picking either
        import_module_search(folder, search='some_variable',
                             pick_on_duplicate=False)
