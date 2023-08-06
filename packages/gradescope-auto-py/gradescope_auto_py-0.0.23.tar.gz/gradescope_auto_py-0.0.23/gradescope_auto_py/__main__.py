#!/usr/bin/env python3
import argparse

import gradescope_auto_py as gap


def main(*args, **kwargs):
    parser = argparse.ArgumentParser(
        description='auto grader python code in gradescope (see doc at: '
                    'https://github.com/matthigger/gradescope_auto_py/)')
    parser.add_argument('-c', '--cases', dest='file_afp', action='append',
                        help='file which contains test cases: an assert statement '
                             'with some "(3 pts)" or similar in its message')
    parser.add_argument('-o', '--out', dest='file_zip', default='auto.zip',
                        help='autograder zip file produced')
    parser.add_argument('-r', '--run', dest='file_run', action='store',
                        default=None, nargs='+',
                        help='name of file to run to perform testing. defaults '
                             'to the unique .py file submitted by student.')
    parser.add_argument('-a', '--add', dest='file_add', action='append',
                        help='this file will be copied next to student submission '
                             'before testing.', default=list())
    parser.add_argument('-f', '--folder', dest='folder_local', type=str,
                        default=None,
                        help='folder containing test cases & supplementary files.'
                             'defaults to current folder.  because the full '
                             'path of additional files (passed with -a) will be '
                             'recreated on when autograder is done, this option '
                             'is useful to distinguish the part of your path '
                             'which is "local"')
    parser.add_argument('-v', dest='file_validate_tup', action='append',
                        default=list(), nargs='+',
                        help='throw a student-readable error message if a file '
                             'with this name is not submitted.  no points are '
                             'earned if students fail to submit a file with this '
                             'name')
    parser.add_argument('-i', '--ipynb', action='store_true',
                        dest='ipynb_flag',
                        help='converts all ipynb to py files before running')

    # allows testing
    args = parser.parse_args(*args, **kwargs)

    # parse file_validate_dict
    file_validate_dict = dict()
    for tup in args.file_validate_tup:
        if len(tup) == 1:
            file, = tup
            pt_penalty = None
        elif len(tup) == 2:
            file, pt_penalty = tup
            pt_penalty = float(pt_penalty)
        else:
            raise ValueError('-v must have 1 or 2 following arguments')
        file_validate_dict[file] = pt_penalty

    grader_config = gap.GraderConfig.from_py(
        file_afp_tup=args.file_afp,
        pattern_run_tup=args.file_run,
        file_add_tup=args.file_add,
        folder_local=args.folder_local,
        file_validate_dict=file_validate_dict,
        ipynb_flag=args.ipynb_flag)

    grader_config.build_zip(file_zip=args.file_zip)


if __name__ == '__main__':
    main()
