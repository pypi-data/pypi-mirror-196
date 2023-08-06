import pathlib
import sys
from importlib.util import spec_from_file_location, module_from_spec


def get_variable(folder, variable_name, **kwargs):
    """ attempts to load a variable somewhere in a folder

    this is poor form, ideally students submit a separate py file of a given
    name without any syntax errors

    Args:
        folder (pathlib.Path): a folder to search for a bit of text
        variable_name (str): variable you intend to load from submission

    Returns:
        variable: variable from student submission
    """
    file, module = import_module_search(folder=folder,
                                        search=variable_name,
                                        **kwargs)

    if module is not None:
        # module loaded properly
        return getattr(module, variable_name)

    # backup plan, error may occur after variable defined
    try:
        # load all code which works into local namespace
        exec(open(file).read())
    except:
        if variable_name in locals():
            # variable name exists, return it
            return locals()[variable_name]

        # variable name doesnt exist, throw error
        raise RuntimeError(f'error before {variable_name} is given (see '
                           f'above)')


def import_module_search(folder, search, name='submitted', exclude_file=None,
                         pick_on_duplicate=True):
    """ imports a module containing some string of text

    Args:
        folder (pathlib.Path): a folder to search for a bit of text
        search (str or tuple): contains search strings.  all must be present
            for file to be considered viable
        exclude_file (str or tuple): contains file names to exclude from the
            search space
        name (str): name of imported module
        pick_on_duplicate (bool): if True, will choose the alphabetically first
            file which contains search strings (prints message to user)

    Returns:
        file (pathlib.Path): file which contains search string
        module (module): module containing target strings.  returns None if
            error encountered importing module
    """
    folder = pathlib.Path(folder)

    # build seach_tup
    if isinstance(search, str):
        search_tup = search,
    else:
        search_tup = tuple(search)

    # build exclude_file_tup
    if isinstance(exclude_file, str):
        exclude_file_tup = exclude_file,
    elif exclude_file is None:
        exclude_file_tup = tuple()
    else:
        exclude_file_tup = tuple(exclude_file)

    # get list of files containing part1_dict
    file_set = set()
    for file in folder.glob('*.py'):
        with open(file) as f:
            s_file = f.read()
            for s_search in search_tup:
                if s_search not in s_file:
                    break
            else:
                file_set.add(file)

    # exclude all files which meet pattern
    file_exclude_set = set()
    for s in exclude_file_tup:
        file_exclude_set |= set(folder.glob(s))
    file_set -= file_exclude_set

    file_list = sorted([str(s) for s in file_set])
    if len(file_list) == 0:
        raise FileNotFoundError(f'no file contains targets {search_tup}')
    elif len(file_list) > 1:
        msg = f'multiple .py files which contain {search}: {file_list}'
        if pick_on_duplicate:
            print(f'using first of {msg}')
        else:
            raise FileExistsError(msg)

    # import only file found
    # https://stackoverflow.com/questions/67631/how-can-i-import-a-module-dynamically-given-the-full-path
    file = pathlib.Path(file_list[0])
    spec = spec_from_file_location(name=name, location=file_list[0])
    module = module_from_spec(spec)

    try:
        # execute module
        spec.loader.exec_module(module)
    except Exception as e:
        # error in module execution, return None in place of module
        print(f'error while running {file.name}:')
        print(e)
        return file, None

    sys.modules[name] = module
    return file, module
