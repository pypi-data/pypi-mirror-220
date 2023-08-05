# Copyright 2021 - 2023 Universität Tübingen, DKFZ, EMBL, and Universität zu Köln
# for the German Human Genome-Phenome Archive (GHGA)
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

"""Test the utils.temp_file module."""

from ghga_service_commons.utils.temp_files import big_temp_file


def test_big_temp_file():
    """Test that the big_temp_file generator works."""

    with big_temp_file(42) as temp_file:
        assert temp_file.name.isascii()
        temp_file.seek(0)
        file_content = temp_file.read()
        assert file_content.isascii()
        assert 42 <= len(file_content) < 50
