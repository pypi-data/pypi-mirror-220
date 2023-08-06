# Created by Kenneth Xian on 2022/1/20.

import ctypes
import sys
import os


def searchfile(path, file_name, build_lib_files):
    for item in os.listdir(path):
        if os.path.isdir(os.path.join(path, item)):
            searchfile(os.path.join(path, item), file_name, build_lib_files)
        else:
            if file_name == item:
                build_lib_files.append(os.path.join(path, item))


def find_lib(dir):
    if sys.platform.startswith('darwin'):
        lib_name = ['libgraphd.dylib', 'libgnnd.dylib',
                    'libgraph.dylib', 'libgnn.dylib']
    else:
        lib_name = ['libgraphd.so', 'libgnnd.so', 'libgraph.so', 'libgnn.so']

    # Search the built libraries
    build_lib_files = []
    for i, lib in enumerate(lib_name):
        searchfile(dir, lib, build_lib_files)
        # Only the first one left
        if len(build_lib_files) - 1 > i:
            build_lib_files = build_lib_files[:i+1]

    # (libgraph.so && libgnn.so)release have priority; then debug
    release_build_lib_files = [lib_f for lib_f in build_lib_files
                               if lib_f.endswith('libgraph.so')
                               or lib_f.endswith('libgnn.so')
                               or lib_f.endswith('libgraph.dylib')
                               or lib_f.endswith('libgnn.dylib')]
    debug_build_lib_files = [lib_f for lib_f in build_lib_files
                             if lib_f.endswith('libgraphd.so')
                             or lib_f.endswith('libgnnd.so')
                             or lib_f.endswith('libgraphd.dylib')
                             or lib_f.endswith('libgnnd.dylib')]
    lib_found = []
    if len(release_build_lib_files) == 2:
        lib_found = release_build_lib_files
    elif len(debug_build_lib_files) == 2:
        lib_found = debug_build_lib_files
    else:
        print('No corresponding link library found !!!')

    print('Loading library: ', lib_found)
    return lib_found


def load_lib():
    curr_dir = os.path.dirname(os.path.abspath(os.path.expanduser(__file__)))
    lib_found = find_lib(curr_dir)
    if len(lib_found) == 0:
        lib_found = find_lib(os.path.join(curr_dir, "..", "..", ".."))

    if len(lib_found) == 0:
        return

    graph_lib = ctypes.CDLL(lib_found[0])
    gnn_lib = ctypes.CDLL(lib_found[1])

    return graph_lib, gnn_lib


G_LIB = load_lib()
