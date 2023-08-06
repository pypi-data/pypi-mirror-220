#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tuning utility."""
import os
import pickle
from collections import OrderedDict
from typing import List, Optional, Any

import prettytable

from neural_compressor.utils import logger
from neural_compressor.utils.utility import print_table, dump_table, OpEntry


class OrderedDefaultDict(OrderedDict):
    """Ordered default dict."""

    def __missing__(self, key):
        """Initialize value for the missing key."""
        self[key] = value = OrderedDefaultDict()
        return value


def extract_data_type(data_type: str) -> str:
    """Extract data type and signed from data type.

    Args:
        data_type: The original data type such as uint8, int8.

    Returns:
        (signed or unsigned, data type without signed)
    """
    return ('signed', data_type) if data_type[0] != 'u' else ('unsigned', data_type[1:])


def reverted_data_type(signed_flag: str, data_type: str) -> str:
    """Revert the data type."""
    return data_type if signed_flag == 'signed' else 'u' + data_type


def get_adaptor_name(adaptor):
    """Get adaptor name.

    Args:
        adaptor: adaptor instance.
    """
    adaptor_name = type(adaptor).__name__.lower()
    adaptor_name_lst = ['onnx', 'tensorflow', 'pytorch']
    for name in adaptor_name_lst:
        if adaptor_name.startswith(name):
            return name
    return ""


def build_slave_faker_model():
    """Slave does not have a model, so construct a fake model.

    Returns:
        object:  a class object where all properties and methods are virtual.
    """
    from ...utils import logger
    class FakerModel:

        def __call__(self, *args, **kwargs):
            logger.warning("Slave node has no quantized model, please handle it yourself.")

        def __getitem__(self, key):
            return self.__getattr__(str(key))

        def __getattr__(self, name):
            logger.warning("Slave node has no quantized model, please handle it yourself.")
            return self

    return FakerModel()
