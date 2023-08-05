# Copyright (c) 2021, INRIA
# Copyright (c) 2021, University of Lille
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import logging
import os

from typing import Dict

from powerapi.exception import MissingArgumentException, NotAllowedArgumentValueException, FileDoesNotExistException


class ConfigValidator:
    """
    Validate powerapi config and initialize missing default values
    """
    @staticmethod
    def validate(config: Dict):
        """
        Validate powerapi config and initialize missing default values
        """
        if 'verbose' not in config:
            config['verbose'] = logging.NOTSET
        if 'stream' not in config:
            config['stream'] = False
        if 'output' not in config:
            logging.error("no output configuration found")
            raise MissingArgumentException(argument_name='output')

        for output_type in config['output']:
            output_config = config['output'][output_type]
            if 'model' not in output_config:
                output_config['model'] = 'HWPCReport'
            if 'name' not in output_config:
                output_config['name'] = 'default_pusher'

        if 'input' not in config:
            logging.error("no input configuration found")
            raise MissingArgumentException(argument_name='input')

        for input_id in config['input']:
            input_config = config['input'][input_id]
            if input_config['type'] == 'csv' \
                    and ('files' not in input_config or input_config['files'] is None or len(input_config['files']) == 0):
                logging.error("no files parameter found for csv input")
                raise MissingArgumentException(argument_name='files')

            if input_config['type'] == 'csv' and config['stream']:
                logging.error("stream mode cannot be used for csv input")
                raise NotAllowedArgumentValueException("Stream mode cannot be used for csv input")

            if 'model' not in input_config:
                input_config['model'] = 'PowerReport'
            if 'name' not in input_config:
                input_config['name'] = 'default_puller'

        ConfigValidator._validate_input(config)

    @staticmethod
    def _validate_input(config: Dict):
        for key, input_config in config['input'].items():
            if input_config['type'] == 'csv':
                list_of_files = input_config['files']

                if isinstance(list_of_files, str):
                    list_of_files = input_config['files'].split(",")
                    config['input'][key]['files'] = list_of_files

                for file_name in list_of_files:
                    if not os.access(file_name, os.R_OK):
                        raise FileDoesNotExistException(file_name=file_name)
