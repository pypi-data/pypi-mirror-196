# Copyright (c) 2021 - present / Neuralmagic, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Code for creating and loading datasets in PyTorch
"""

# flake8: noqa

from ..base import check_torch_install as _check_torch_install
from .classification import *
from .detection import *
from .generic import *
from .recommendation import *
from .registry import *
from .video import *


_check_torch_install()  # TODO: remove once files within package load without installs
