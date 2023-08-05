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
General helper functions for datasets in sparseml
"""

import os


__all__ = [
    "IMAGENET_RGB_MEANS",
    "IMAGENET_RGB_STDS",
    "default_dataset_path",
]


IMAGENET_RGB_MEANS = [0.485, 0.456, 0.406]
IMAGENET_RGB_STDS = [0.229, 0.224, 0.225]


def default_dataset_path(name: str) -> str:
    """
    :param name: name of the dataset to get a path for
    :return: the default path to save the dataset at
    """
    path = os.getenv("NM_ML_DATASETS_PATH", "")

    if not path:
        path = os.path.join("~", ".cache", "nm_datasets")

    path = os.path.join(path, name)

    return path
