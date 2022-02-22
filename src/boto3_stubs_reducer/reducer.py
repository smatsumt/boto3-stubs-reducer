#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Delete not-installed module @overload from boto3-stubs interface file
"""

import argparse
import ast
import importlib
import logging
import os
from pathlib import Path
import shutil

import astunparse

logger = logging.getLogger(__name__)

TARGETS = ["boto3-stubs/__init__.py", "boto3-stubs/__init__.pyi", "boto3-stubs/session.pyi"]
MYPY_CHECK_TARGET_INDEX = 1  # Use "boto3-stubs/__init__.pyi" for mypy check.
ORIG_PREFIX = ".orig"
REDUCER_HEADER = "# GENERATED BY boto3-stub-reducer\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--log-level', default=os.getenv('LOGGING_LEVEL', 'INFO'))
    parser.add_argument('-p', '--package-path', type=str, default="", help='')
    args = parser.parse_args()

    logging.basicConfig(level=args.log_level)

    main_reduce(args.package_path)


def main_reduce(package_path: str) -> None:
    package_path_ = package_path or default_lib_path()
    # list up target files
    target_path_list = [Path(package_path_) / t for t in TARGETS]
    target_path_list = [p for p in target_path_list if p.exists()]  # only for existing files
    orig_path_list = [Path(str(p) + ORIG_PREFIX) for p in target_path_list]

    # keep original files
    for t_path, orig_path in zip(target_path_list, orig_path_list):
        if not orig_path.is_file() or not t_path.read_text().startswith(REDUCER_HEADER):
            shutil.copy(t_path, orig_path)

    # check installed mypy modules
    orig_path = orig_path_list[MYPY_CHECK_TARGET_INDEX]
    ast_tree = ast.parse(orig_path.read_text(), str(orig_path))
    known_modules = parse_known_modules(ast_tree)

    # reduce!
    for t_path, orig_path in zip(target_path_list, orig_path_list):
        ast_tree = ast.parse(orig_path.read_text(), str(orig_path))
        ast_tree.body = convert_ast_body(known_modules, ast_tree.body)
        t_path.write_text(REDUCER_HEADER + astunparse.unparse(ast_tree))
        print(f"reduce {t_path}")

    # finished!
    print(f"Replacing boto3-stubs successfully.")


def parse_known_modules(ast_tree) -> set:
    """
    Return known modules parsing __init__.pyi

    Invest known modules by importing mypy modules in __init__.pyi
    """
    result = set()
    for ast_obj in ast_tree.body:
        if isinstance(ast_obj, ast.Import):
            continue
        if not isinstance(ast_obj, ast.ImportFrom):
            return result

        module_path: str = ast_obj.module
        module_name = module_path.split(".")[0]
        # try import, and add it if import succeeded
        try:
            importlib.import_module(module_name)
            names_set = {x.name for x in ast_obj.names}
            result.update(names_set)
        except ImportError:
            pass


def convert_ast_body(known_modules: set, ast_body: list) -> list:
    """
    Convert parsed AST with deleting unknown modules (it means mypy is not installed)
    """
    return list(filter(None, map(map_unknown_to_none(known_modules), ast_body)))


def map_unknown_to_none(known_modules: set):
    """
    Return ast_obj filtering function

    Filters out with @overload function returning invalid (mypy is not installed) class.
    Assume "import" statement is top-level (not inside try block)
    """
    def _map_unknown_to_none(ast_obj):
        # convert Session class
        if isinstance(ast_obj, ast.ClassDef) and ast_obj.name == "Session":
            ast_obj.body = convert_ast_body(known_modules, ast_obj.body)
            return ast_obj

        # return ast_obj if it is not function decorated with @overload
        if not isinstance(ast_obj, ast.FunctionDef):
            return ast_obj
        if len(ast_obj.decorator_list) < 1 or ast_obj.decorator_list[0].id != "overload":
            return ast_obj

        # examine the target return type
        return ast_obj if ast_obj.returns.id in known_modules else None
    return _map_unknown_to_none


def default_lib_path() -> str:
    """ Get boto3 library path """
    try:
        import boto3
        boto3_path = Path(boto3.__file__)
        return str(boto3_path.parent.parent)
    except ImportError as e:
        raise ModuleNotFoundError(
            "boto3 is not found. Please specify replacing site-package path with --package-path(-p) option"
        ) from e


if __name__ == '__main__':
    main()
