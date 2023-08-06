# Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import absolute_import
import logging
import os
import sys

user_specified_dirs = []

def is_built_with_ort() -> bool:
    return True if "ON" == "ON" else False

def is_built_with_paddle() -> bool:
    return True if "OFF" == "ON" else False


def is_built_with_openvino() ->bool:
    return True if "OFF" == "ON" else False


def add_system_search_paths():
    # TODO(qiuyanjun): add Linux system paths
    sys_paths = os.environ["path"].strip().split(";")
    for sys_path in sys_paths:
        if os.path.exists(sys_path) and sys.version_info[:2] >= (3, 8):
            try:
                os.add_dll_directory(sys_path)
            except:
                continue


def add_dll_search_dir(dir_path):
    os.environ["path"] = dir_path + ";" + os.environ["path"]
    sys.path.insert(0, dir_path)
    if sys.version_info[:2] >= (3, 8):
        print("add_dll_search_dir:" + dir_path)
        os.add_dll_directory(dir_path)

if os.name == "nt":
    current_path = os.path.abspath(__file__)
    dirname = os.path.dirname(current_path)
    add_dll_search_dir(dirname)
    # third_libs_dir = os.path.join(dirname, "libs")
    # add_dll_search_dir(os.path.join(third_libs_dir, "third_libs"))
    # all_dirs = user_specified_dirs + [third_libs_dir]
    # for dir in all_dirs:
    #     if os.path.exists(dir):
    #         add_dll_search_dir(dir)
    #         for root, dirs, filenames in os.walk(dir):
    #             for d in dirs:
    #                 if d == "lib" or d == "bin":
    #                     add_dll_search_dir(os.path.join(dirname, root, d))
    #
    # print(os.environ['PATH'])

    print(os.environ['PATH'])


try:
    if os.name == 'nt':
        from da_python_main import *
    else:
        from .libs.da_python_main import *
except:
    raise RuntimeError("da_python initalized failed!")

def create(license, model):
    return bind_create(license, model)
