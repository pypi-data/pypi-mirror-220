# Created by Kenneth Xian on 2022/1/17.

import sys
import os
import shutil
import numpy as np

from ezoognn.libloader import find_lib
from setuptools import find_packages

# need to use distutils.core for correct placement of cython dll
if '--inplace' in sys.argv:
    from distutils.core import setup
    from distutils.extension import Extension
else:
    from setuptools import setup
    from setuptools.extension import Extension

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

ROOT_DIR = CURRENT_DIR + "/../.."
DELETE_LST = ["build", "ezoognn/__pycache__",
              "ezoognn/ezoocall.cpp", "dist", "ezoognn.egg-info"]

libs_dirs = set()
libs_full_name = find_lib(ROOT_DIR)
libraries = []

jinja_py_file = []
setup_kwargs = {}

def cleanup():
    try:
        os.remove(os.path.join(CURRENT_DIR, "MANIFEST.in"))
    except:
        pass

    for path in DELETE_LST:
        try:
            deleted_file = os.path.join(CURRENT_DIR, path)
            print("delete: ", deleted_file)
            if os.path.isfile(deleted_file):
                os.remove(deleted_file)
            else:
                shutil.rmtree(deleted_file)
        except:
            pass

    for path in libs_full_name:
        _, libname = os.path.split(path)
        try:
            deleted_file = os.path.join(CURRENT_DIR, "ezoognn", libname)
            os.remove(deleted_file)
            print("delete: ", deleted_file)
        except:
            pass


if "clean" in sys.argv:
    cleanup()


def get_jinja_path():
    return [CURRENT_DIR + os.sep + 'ezoognn' + os.sep + 'loader' + os.sep + 'dataset' + os.sep + 'jinja_py' + os.sep]


def get_jinja_file_list(path_list=get_jinja_path()):
    for path in path_list:
        for item in os.listdir(path):
            if os.path.isdir(os.path.join(path, item)):
                get_jinja_file_list(os.path.join(path, item))
            else:
                jinja_py_file.append(path + item)


def prepare_libs():
    for lib_full_name in libs_full_name:
        lib_dir, file_name = os.path.split(lib_full_name)
        libs_dirs.add(lib_dir)
        libraries.append(file_name.split('.')[0][3:])
    global setup_kwargs
    with open("MANIFEST.in", "w") as manifest:
        for path in libs_full_name:
            shutil.copy(path, os.path.join(CURRENT_DIR, 'ezoognn'))
            _, libname = os.path.split(path)
            print("include ezoognn/%s\n" % libname)
            manifest.write("include ezoognn/%s\n" % libname)
        for path in jinja_py_file:
            _, template_name = os.path.split(path)
            print("include ezoognn/loader/dataset/jinja_py/%s\n" % template_name)
            manifest.write("include ezoognn/loader/dataset/jinja_py/%s\n" % template_name)

    setup_kwargs = {
        "include_package_data": True
    }


def config_cython():
    try:
        from Cython.Build import cythonize

        ret = []
        path = CURRENT_DIR + "/ezoognn"
        library_dirs = list(libs_dirs)

        for fn in os.listdir(path):
            if not fn.endswith(".pyx"):
                continue
            ret.append(Extension(
                "ezoognn.{}".format(fn[:-4]),
                ["ezoognn/{}".format(fn)],
                include_dirs=[CURRENT_DIR + "/cpp/db_impl/include",
                              np.get_include()],
                library_dirs=library_dirs,
                libraries=libraries,
                language="c++",
                extra_compile_args=["-std=c++20"]))
        return cythonize(ret, force=True, compiler_directives={'language_level': "3"})
    except ImportError:
        print("WARNING: Cython is not installed, will compile without cython module")
        return []


if __name__ == '__main__':
    get_jinja_file_list()
    prepare_libs()
    setup(name="ezoognn",
          version="2.0.1",
          description="eZoo GNN Python SDK",
          long_description = "The Python SDK for loading data from eZoo graph and running GNN training.",
          python_requires=">=3.7",
          author="eZoo",
          author_email="ezoo@ezoodb.com",
          url= "https://www.ezoodb.com",
          ext_modules=config_cython(),
          packages=find_packages(),
          install_requires=['pyvis'],
          **setup_kwargs
          )
