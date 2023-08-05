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

import sys

from powerapi.cli.parsing_manager import RootConfigParsingManager, SubgroupConfigParsingManager
from powerapi.cli.config_parser import store_true
from powerapi.cli.config_parser import MissingValueException
from powerapi.exception import BadTypeException, BadContextException, UnknownArgException

POWERAPI_ENVIRONMENT_VARIABLE_PREFIX = 'POWERAPI_'
POWERAPI_OUTPUT_ENVIRONMENT_VARIABLE_PREFIX = POWERAPI_ENVIRONMENT_VARIABLE_PREFIX + 'OUTPUT_'
POWERAPI_INPUT_ENVIRONMENT_VARIABLE_PREFIX = POWERAPI_ENVIRONMENT_VARIABLE_PREFIX + 'INPUT_'
POWERAPI_REPORT_MODIFIER_ENVIRONMENT_VARIABLE_PREFIX = POWERAPI_ENVIRONMENT_VARIABLE_PREFIX + 'REPORT_MODIFIER_'


def extract_file_names(arg, val, args, acc):
    """
    action used to convert string from --files parameter into a list of file name
    """
    acc[arg] = val.split(",")
    return args, acc


class CommonCLIParsingManager(RootConfigParsingManager):
    """
    PowerAPI basic config parser
    """

    def __init__(self):
        RootConfigParsingManager.__init__(self)

        # Environment variables prefix

        self.add_argument_prefix(argument_prefix=POWERAPI_ENVIRONMENT_VARIABLE_PREFIX)
        # Subgroups
        self.add_subgroup(name='report_modifier',
                          prefix=POWERAPI_REPORT_MODIFIER_ENVIRONMENT_VARIABLE_PREFIX,
                          help_text="Specify a report modifier to change input report values : "
                                    "--report_modifier ARG1 ARG2 ...")

        self.add_subgroup(name='input',
                          prefix=POWERAPI_INPUT_ENVIRONMENT_VARIABLE_PREFIX,
                          help_text="specify a database input : --db_input database_name ARG1 ARG2 ... ")

        self.add_subgroup(name='output',
                          prefix=POWERAPI_OUTPUT_ENVIRONMENT_VARIABLE_PREFIX,
                          help_text="specify a database output : --db_output database_name ARG1 ARG2 ...")

        # Parsers

        self.add_argument(
            "v",
            "verbose",
            is_flag=True,
            action=store_true,
            default_value=False,
            help_text="enable verbose mode",
        )
        self.add_argument(
            "s",
            "stream",
            is_flag=True,
            action=store_true,
            default_value=False,
            help_text="enable stream mode",
        )

        subparser_libvirt_mapper_modifier = SubgroupConfigParsingManager("libvirt_mapper")
        subparser_libvirt_mapper_modifier.add_argument(
            "u", "uri", help_text="libvirt daemon uri", default_value=""
        )
        subparser_libvirt_mapper_modifier.add_argument(
            "d",
            "domain_regexp",
            help_text="regexp used to extract domain from cgroup string",
        )
        subparser_libvirt_mapper_modifier.add_argument("n", "name", help_text="")
        self.add_subgroup_parser(
            subgroup_name="report_modifier",
            subgroup_parser=subparser_libvirt_mapper_modifier
        )

        subparser_mongo_input = SubgroupConfigParsingManager("mongodb")
        subparser_mongo_input.add_argument("u", "uri", help_text="specify MongoDB uri")
        subparser_mongo_input.add_argument(
            "d",
            "db",
            help_text="specify MongoDB database name",
        )
        subparser_mongo_input.add_argument(
            "c", "collection", help_text="specify MongoDB database collection"
        )
        subparser_mongo_input.add_argument(
            "n", "name", help_text="specify puller name", default_value="puller_mongodb"
        )
        subparser_mongo_input.add_argument(
            "m",
            "model",
            help_text="specify data type that will be stored in the database",
            default_value="HWPCReport",
        )
        self.add_subgroup_parser(
            subgroup_name="input",
            subgroup_parser=subparser_mongo_input
        )

        subparser_socket_input = SubgroupConfigParsingManager("socket")
        subparser_socket_input.add_argument(
            "p", "port", argument_type=int, help_text="specify port to bind the socket"
        )
        subparser_socket_input.add_argument(
            "n", "name", help_text="specify puller name", default_value="puller_socket"
        )
        subparser_socket_input.add_argument(
            "m",
            "model",
            help_text="specify data type that will be sent through the socket",
            default_value="HWPCReport",
        )
        self.add_subgroup_parser(
            subgroup_name="input",
            subgroup_parser=subparser_socket_input
        )

        subparser_csv_input = SubgroupConfigParsingManager("csv")
        subparser_csv_input.add_argument(
            "f",
            "files",
            help_text="specify input csv files with this format : file1,file2,file3",
            action=extract_file_names,
            default_value=[],
        )
        subparser_csv_input.add_argument(
            "m",
            "model",
            help_text="specify data type that will be stored in the database",
            default_value="HWPCReport",
        )
        subparser_csv_input.add_argument(
            "n", "name", help_text="specify puller name", default_value="puller_csv"
        )
        self.add_subgroup_parser(
            subgroup_name="input",
            subgroup_parser=subparser_csv_input
        )

        subparser_file_input = SubgroupConfigParsingManager("filedb")
        subparser_file_input.add_argument(
            "m",
            "model",
            help_text="specify data type that will be stored in the database",
            default_value="HWPCReport",
        )
        subparser_file_input.add_argument("f", "filename", help_text="specify file name")
        subparser_file_input.add_argument(
            "n", "name", help_text="specify pusher name", default_value="pusher_filedb"
        )
        self.add_subgroup_parser(
            subgroup_name="input",
            subgroup_parser=subparser_file_input
        )

        subparser_file_output = SubgroupConfigParsingManager("filedb")
        subparser_file_output.add_argument(
            "m",
            "model",
            help_text="specify data type that will be stored in the database",
            default_value="PowerReport",
        )
        subparser_file_output.add_argument("f", "filename", help_text="specify file name")
        subparser_file_output.add_argument(
            "n", "name", help_text="specify pusher name", default_value="pusher_filedb"
        )
        self.add_subgroup_parser(
            subgroup_name="output",
            subgroup_parser=subparser_file_output
        )

        subparser_virtiofs_output = SubgroupConfigParsingManager("virtiofs")
        help_text = "regexp used to extract vm name from report."
        help_text += "The regexp must match the name of the target in the HWPC-report and a group must"
        subparser_virtiofs_output.add_argument("r", "vm_name_regexp", help_text=help_text)
        subparser_virtiofs_output.add_argument(
            "d",
            "root_directory_name",
            help_text="directory where VM directory will be stored",
        )
        subparser_virtiofs_output.add_argument(
            "p",
            "vm_directory_name_prefix",
            help_text="first part of the VM directory name",
            default_value="",
        )
        subparser_virtiofs_output.add_argument(
            "s",
            "vm_directory_name_suffix",
            help_text="last part of the VM directory name",
            default_value="",
        )
        subparser_virtiofs_output.add_argument(
            "m",
            "model",
            help_text="specify data type that will be stored in the database",
            default_value="PowerReport",
        )
        subparser_virtiofs_output.add_argument(
            "n", "name", help_text="specify pusher name", default_value="pusher_virtiofs"
        )
        self.add_subgroup_parser(
            subgroup_name="output",
            subgroup_parser=subparser_virtiofs_output
        )

        subparser_mongo_output = SubgroupConfigParsingManager("mongodb")
        subparser_mongo_output.add_argument("u", "uri", help_text="specify MongoDB uri")
        subparser_mongo_output.add_argument(
            "d", "db", help_text="specify MongoDB database name"
        )
        subparser_mongo_output.add_argument(
            "c", "collection", help_text="specify MongoDB database collection"
        )

        subparser_mongo_output.add_argument(
            "m",
            "model",
            help_text="specify data type that will be stored in the database",
            default_value="PowerReport",
        )
        subparser_mongo_output.add_argument(
            "n", "name", help_text="specify pusher name", default_value="pusher_mongodb"
        )
        self.add_subgroup_parser(
            subgroup_name="output",
            subgroup_parser=subparser_mongo_output
        )

        subparser_prom_output = SubgroupConfigParsingManager("prom")
        subparser_prom_output.add_argument("t", "tags", help_text="specify report tags")
        subparser_prom_output.add_argument("u", "uri", help_text="specify server uri")
        subparser_prom_output.add_argument(
            "p", "port", help_text="specify server port", argument_type=int
        )
        subparser_prom_output.add_argument(
            "M", "metric_name", help_text="specify metric name"
        )
        subparser_prom_output.add_argument(
            "d",
            "metric_description",
            help_text="specify metric description",
            default_value="energy consumption",
        )
        help_text = "specify number of second for the value must be aggregated before compute statistics on them"
        subparser_prom_output.add_argument(
            "A", "aggregation_period", help_text=help_text, default_value=15, argument_type=int
        )

        subparser_prom_output.add_argument(
            "m",
            "model",
            help_text="specify data type that will be stored in the database",
            default_value="PowerReport",
        )
        subparser_prom_output.add_argument(
            "n", "name", help_text="specify pusher name", default_value="pusher_prom"
        )
        self.add_subgroup_parser(
            subgroup_name="output",
            subgroup_parser=subparser_prom_output
        )

        subparser_direct_prom_output = SubgroupConfigParsingManager("direct_prom")
        subparser_direct_prom_output.add_argument(
            "t", "tags", help_text="specify report tags"
        )
        subparser_direct_prom_output.add_argument("a", "uri", help_text="specify server uri")
        subparser_direct_prom_output.add_argument(
            "p", "port", help_text="specify server port", argument_type=int
        )
        subparser_direct_prom_output.add_argument(
            "M", "metric_name", help_text="specify metric name"
        )
        subparser_direct_prom_output.add_argument(
            "d",
            "metric_description",
            help_text="specify metric description",
            default_value="energy consumption",
        )
        subparser_direct_prom_output.add_argument(
            "m",
            "model",
            help_text="specify data type that will be stored in the database",
            default_value="PowerReport",
        )
        subparser_direct_prom_output.add_argument(
            "n", "name", help_text="specify pusher name", default_value="pusher_prom"
        )
        self.add_subgroup_parser(
            subgroup_name="output",
            subgroup_parser=subparser_direct_prom_output
        )

        subparser_csv_output = SubgroupConfigParsingManager("csv")
        subparser_csv_output.add_argument(
            "d",
            "directory",
            help_text="specify directory where where output  csv files will be writen",
        )
        subparser_csv_output.add_argument(
            "m",
            "model",
            help_text="specify data type that will be stored in the database",
            default_value="PowerReport",
        )

        subparser_csv_output.add_argument("t", "tags", help_text="specify report tags")
        subparser_csv_output.add_argument(
            "n", "name", help_text="specify pusher name", default_value="pusher_csv"
        )
        self.add_subgroup_parser(
            subgroup_name="output",
            subgroup_parser=subparser_csv_output
        )

        subparser_influx_output = SubgroupConfigParsingManager("influxdb")
        subparser_influx_output.add_argument("u", "uri", help_text="specify InfluxDB uri")
        subparser_influx_output.add_argument("t", "tags", help_text="specify report tags")
        subparser_influx_output.add_argument(
            "d", "db", help_text="specify InfluxDB database name"
        )
        subparser_influx_output.add_argument(
            "p", "port", help_text="specify InfluxDB connection port", argument_type=int
        )
        subparser_influx_output.add_argument(
            "m",
            "model",
            help_text="specify data type that will be stored in the database",
            default_value="PowerReport",
        )
        subparser_influx_output.add_argument(
            "n", "name", help_text="specify pusher name", default_value="pusher_influxdb"
        )
        self.add_subgroup_parser(
            subgroup_name="output",
            subgroup_parser=subparser_influx_output
        )

        subparser_opentsdb_output = SubgroupConfigParsingManager("opentsdb")
        subparser_opentsdb_output.add_argument("u", "uri", help_text="specify openTSDB host")
        subparser_opentsdb_output.add_argument(
            "p", "port", help_text="specify openTSDB connection port", argument_type=int
        )
        subparser_opentsdb_output.add_argument(
            "metric_name", help_text="specify metric name"
        )

        subparser_opentsdb_output.add_argument(
            "m",
            "model",
            help_text="specify data type that will be stored in the database",
            default_value="PowerReport",
        )
        subparser_opentsdb_output.add_argument(
            "n", "name", help_text="specify pusher name", default_value="pusher_opentsdb"
        )
        self.add_subgroup_parser(
            subgroup_name="output",
            subgroup_parser=subparser_opentsdb_output
        )

        subparser_influx2_output = SubgroupConfigParsingManager("influxdb2")
        subparser_influx2_output.add_argument("u", "uri", help_text="specify InfluxDB uri")
        subparser_influx2_output.add_argument("t", "tags", help_text="specify report tags")
        subparser_influx2_output.add_argument("k", "token",
                                              help_text="specify token for accessing the database")
        subparser_influx2_output.add_argument("g", "org",
                                              help_text="specify organisation for accessing the database")

        subparser_influx2_output.add_argument(
            "d", "db", help_text="specify InfluxDB database name"
        )
        subparser_influx2_output.add_argument(
            "p", "port", help_text="specify InfluxDB connection port", argument_type=int
        )
        subparser_influx2_output.add_argument(
            "m",
            "model",
            help_text="specify data type that will be store in the database",
            default_value="PowerReport",
        )
        subparser_influx2_output.add_argument(
            "n", "name", help_text="specify pusher name", default_value="pusher_influxdb2"
        )

        self.add_subgroup_parser(
            subgroup_name="output",
            subgroup_parser=subparser_influx2_output
        )

    def parse_argv(self):
        """ """
        try:
            return self.parse(sys.argv[1:])

        except MissingValueException as exn:
            msg = "CLI error : argument " + exn.argument_name + " : expect a value"
            print(msg, file=sys.stderr)

        except BadTypeException as exn:
            msg = "Configuration error : " + exn.msg
            print(msg, file=sys.stderr)

        except UnknownArgException as exn:
            msg = "CLI error : unknown argument " + exn.argument_name
            print(msg, file=sys.stderr)

        except BadContextException as exn:
            msg = "CLI error : argument " + exn.argument_name
            msg += " not used in the correct context\nUse it with the following arguments :"
            for main_arg_name, context_name in exn.context_list:
                msg += "\n  --" + main_arg_name + " " + context_name
            print(msg, file=sys.stderr)

        sys.exit()
