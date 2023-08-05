#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
#############################################################
#                                                           #
#      Copyright @ 2023 -  Dashingsoft corp.                #
#      All rights reserved.                                 #
#                                                           #
#      Pyarmor                                              #
#                                                           #
#      Version: 8.0.1 -                                     #
#                                                           #
#############################################################
#
#
#  @File: pyarmor/runtime/__init__.py
#
#  @Author: Jondy Zhao (pyarmor@163.com)
#
#  @Create Date: Mon Feb 13 09:17:27 CST 2023
#
import zipfile

__VERSION__ = '1.0'


class PyarmorRuntime(object):

    def get(self, plat):
        path = __file__.replace('__init__.py', 'libs.zip')
        prefix = plat.replace('darwin', 'macos').replace('.', '_')
        with zipfile.ZipFile(path) as f:
            for name in f.namelist:
                if name.startswith(prefix):
                    return name[len(prefix)+1:], f.read(name)
