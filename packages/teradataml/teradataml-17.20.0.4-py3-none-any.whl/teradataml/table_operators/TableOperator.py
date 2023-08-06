#!/usr/bin/python
# ##################################################################
#
# Copyright 2020 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
#
# Primary Owner: Trupti Purohit (trupti.purohit@teradata.com)
# Secondary Owner: Gouri Patwardhan (gouri.patwardhan@teradata.com)
#
# Function Version: 1.0
#
# Description: Base class for Teradata's Table Operators
# ##################################################################

import docker
import os
import tarfile
import subprocess
from pathlib import Path
import teradataml.dataframe as tdmldf
from teradataml.common.constants import OutputStyle, TeradataConstants
from teradataml.common.constants import TableOperatorConstants
from teradataml.common.garbagecollector import GarbageCollector
from teradataml.common.wrapper_utils import AnalyticsWrapperUtils
from teradataml.common.utils import UtilFuncs
from teradataml.dataframe.dataframe_utils import DataFrameUtils as df_utils

from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes
from teradataml.options.configure import configure
from teradataml.utils.utils import execute_sql
from teradataml.utils.validators import _Validators
from teradatasqlalchemy import (BYTEINT, SMALLINT, INTEGER, BIGINT, DECIMAL, FLOAT, NUMBER)
from teradatasqlalchemy import (TIMESTAMP, DATE, TIME)
from teradatasqlalchemy import (CHAR, VARCHAR, CLOB)
from teradatasqlalchemy import (BYTE, VARBYTE, BLOB)
from teradatasqlalchemy import (PERIOD_DATE, PERIOD_TIME, PERIOD_TIMESTAMP)
from teradatasqlalchemy import (INTERVAL_YEAR, INTERVAL_YEAR_TO_MONTH, INTERVAL_MONTH, INTERVAL_DAY,
                                INTERVAL_DAY_TO_HOUR, INTERVAL_DAY_TO_MINUTE, INTERVAL_DAY_TO_SECOND,
                                INTERVAL_HOUR, INTERVAL_HOUR_TO_MINUTE, INTERVAL_HOUR_TO_SECOND,
                                INTERVAL_MINUTE, INTERVAL_MINUTE_TO_SECOND, INTERVAL_SECOND)
from teradataml.context.context import _get_current_databasename, get_context, get_connection
from io import StringIO


class TableOperator:

    def __init__(self,
                 data=None,
                 script_name=None,
                 files_local_path=None,
                 delimiter="\t",
                 returns=None,
                 quotechar=None,
                 data_partition_column=None,
                 data_hash_column=None,
                 data_order_column=None,
                 is_local_order=False,
                 sort_ascending=True,
                 nulls_first=True):
        """
        DESCRIPTION:
            Table Operators are a type of User-Defined Function, only available when connected to a
            Vantage.

        PARAMETERS:
            data:
                Optional Argument.
                Specifies a teradataml DataFrame containing the input data for the script.

            script_name:
                Required Argument.
                Specifies the name of the user script.
                Types: str

            files_local_path:
                Required Argument.
                Specifies the absolute local path where the user script and all supporting files
                like model files, input data file reside.
                Types: str

            delimiter:
                Optional Argument.
                Specifies a delimiter to use when reading columns from a row and
                writing result columns.
                The delimiter is a single character chosen from the set of punctuation characters.
                Types: str

            returns:
                Required Argument.
                Specifies the output column definition.
                Types: Dictionary specifying column name to teradatasqlalchemy type mapping.
                Default: None

            data_hash_column:
                Optional Argument.
                Specifies the column to be used for hashing.
                The rows in the data are redistributed to AMPs based on the hash value of the
                column specified. The user-installed script file then runs once on each AMP.
                If there is no data_hash_column, then the entire result set,
                delivered by the function, constitutes a single group or partition.
                Types: str
                Note:
                    "data_hash_column" can not be specified along with "data_partition_column",
                    "is_local_order" and "data_order_column".

            data_partition_column:
                Optional Argument.
                Specifies Partition By columns for data.
                Values to this argument can be provided as a list, if multiple
                columns are used for partition.
                Default Value: ANY
                Types: str OR list of Strings (str)
                Notes:
                    1) "data_partition_column" can not be specified along with "data_hash_column".
                    2) "data_partition_column" can not be specified along with "is_local_order = True".

            is_local_order:
                Optional Argument.
                Specifies a boolean value to determine whether the input data is to be ordered locally
                or not. 'sort_ascending' specifies the order in which the values in a group, or partition,
                are sorted. This argument is ignored, if data_order_column is None.
                When set to 'True', qualified rows are ordered locally in preparation to be input
                to the function.
                Default Value: False
                Types: bool
                Note:
                    "is_local_order" can not be specified along with "data_hash_column".
                    When "is_local_order" is set to 'True', "data_order_column" should be specified,
                    and the columns specified in "data_order_column" are used for local ordering.

            data_order_column:
                Optional Argument.
                Specifies Order By columns for data.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                This argument is used with in both cases: "is_local_order = True"
                and "is_local_order = False".
                Types: str OR list of Strings (str)
                Note:
                    "data_order_column" can not be specified along with "data_hash_column".

            sort_ascending:
                Optional Argument.
                Specifies a boolean value to determine if the input data is to be sorted on
                the data_order_column column in ascending or descending order.
                When this is set to 'True' data is sorted in ascending order,
                otherwise data is sorted in descending order.
                This argument is ignored, if data_order_column is None.
                Default Value: True
                Types: bool

            nulls_first:
                Optional Argument.
                Specifies a boolean value to determine whether NULLS from input data are listed
                first or last during ordering.
                When this is set to 'True' NULLS are listed first, otherwise NULLS are listed last.
                This argument is ignored, if data_order_column is None.
                Default Value: True
                Types: bool

        RETURNS:
             An instance of TableOperator class.

        RAISES:
            TeradataMlException

        EXAMPLES:
            # Apply class extends this base class.
            apply_obj = Apply(data=barrierdf,
                              script_name='mapper.py',
                              files_local_path= '/root/data/scripts/',
                              apply_command='python3 mapper.py',
                              data_order_column="Id",
                              is_local_order=False,
                              nulls_first=False,
                              sort_ascending=False,
                              env_name = "test_env",
                              returns={"word": VARCHAR(15), "count_input": VARCHAR(2)},
                              style='csv',
                              delimiter=',')
        """
        self.result = None
        self._tblop_query = None
        self.data = data
        self.script_name = script_name
        self.files_local_path = files_local_path
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.returns = returns
        self.data_partition_column = data_partition_column
        self.data_hash_column = data_hash_column
        self.data_order_column = data_order_column
        self.is_local_order = is_local_order
        self.sort_ascending = sort_ascending
        self.nulls_first = nulls_first

        # Datatypes supported in returns clause of a table operator.
        self._supported_returns_datatypes = (BYTEINT, SMALLINT, INTEGER, BIGINT, DECIMAL, FLOAT, NUMBER,
                             TIMESTAMP, DATE, TIME, CHAR, VARCHAR, CLOB, BYTE, VARBYTE,
                             BLOB, PERIOD_DATE, PERIOD_TIME, PERIOD_TIMESTAMP, INTERVAL_YEAR,
                             INTERVAL_YEAR_TO_MONTH, INTERVAL_MONTH, INTERVAL_DAY, INTERVAL_DAY_TO_HOUR,
                             INTERVAL_DAY_TO_MINUTE, INTERVAL_DAY_TO_SECOND, INTERVAL_HOUR,
                             INTERVAL_HOUR_TO_MINUTE, INTERVAL_HOUR_TO_SECOND, INTERVAL_MINUTE,
                             INTERVAL_MINUTE_TO_SECOND, INTERVAL_SECOND
                             )

        # Create AnalyticsWrapperUtils instance which contains validation functions.
        # This is required for is_default_or_not check.
        # Rest all validation is done using _Validators.
        self.__awu = AnalyticsWrapperUtils()

        self.awu_matrix = []
        self.awu_matrix.append(["data", self.data, True, (tdmldf.dataframe.DataFrame)])
        self.awu_matrix.append(["data_partition_column", self.data_partition_column, True, (str, list), True])
        self.awu_matrix.append(["data_hash_column", self.data_hash_column, True, (str, list), True])
        self.awu_matrix.append(["data_order_column", self.data_order_column, True, (str, list), True])
        self.awu_matrix.append(["is_local_order", self.is_local_order, True, (bool)])
        self.awu_matrix.append(["sort_ascending", self.sort_ascending, True, (bool)])
        self.awu_matrix.append(["nulls_first", self.nulls_first, True, (bool)])
        self.awu_matrix.append(["script_name", self.script_name, True, (str), True])
        self.awu_matrix.append(["files_local_path", self.files_local_path, True, (str), True])
        self.awu_matrix.append(["delimiter", self.delimiter, True, (str), False])
        self.awu_matrix.append(["quotechar", self.quotechar, True, (str), False])

        # Perform the function validations.
        self._validate()

    def _validate(self, for_data_args=False):
        """
        Function to validate Table Operator Function arguments, which verifies missing
        arguments, input argument and table types. Also processes the
        argument values.
        @param: for_data_args: Specifies whether the validation is for only arguments related to data or not.
                               When set to True, validation is only for data arguments. Otherwise, validation
                               is for all arguments. By default, system validates all the arguments.
        """

        if not for_data_args:
            # Make sure that a non-NULL value has been supplied for all mandatory arguments
            _Validators._validate_missing_required_arguments(self.awu_matrix)

            # Validate argument types
            _Validators._validate_function_arguments(self.awu_matrix,
                                                     skip_empty_check={"quotechar": ["\n", "\t"],
                                                                       "delimiter": ["\n"]})

        if self.data is not None:
            # Hash and order by can be used together as long as is_local_order = True.
            if all([self.data_hash_column,
                    self.data_order_column]) and not self.is_local_order:
                raise TeradataMlException(
                    Messages.get_message(MessageCodes.CANNOT_USE_TOGETHER_WITH,
                                         "data_hash_column' and 'data_order_column",
                                         "is_local_order=False"),
                    MessageCodes.CANNOT_USE_TOGETHER_WITH)

            # Either hash or partition can be used.
            if all([self.data_hash_column, self.data_partition_column]):
                raise TeradataMlException(Messages.get_message(MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT,
                                                               "data_hash_column", "data_partition_column"),
                                          MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT)

            # Either local order by or partition by can be used.
            if all([self.is_local_order, self.data_partition_column]):
                raise TeradataMlException(Messages.get_message(MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT,
                                                               "is_local_order=True",
                                                               "data_partition_column"),
                                          MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT)

            # local order by requires column name.
            if self.is_local_order and self.data_order_column is None:
                raise TeradataMlException(Messages.get_message(MessageCodes.DEPENDENT_ARG_MISSING,
                                                               "data_order_column",
                                                               "is_local_order=True"),
                                          MessageCodes.DEPENDENT_ARG_MISSING)

            if self.__awu._is_default_or_not(self.data_partition_column, "ANY"):
                _Validators._validate_dataframe_has_argument_columns(self.data_partition_column, "data_partition_column",
                                                                    self.data, "data", True)

            _Validators._validate_dataframe_has_argument_columns(self.data_order_column, "data_order_column",
                                                                    self.data, "data", False)

            _Validators._validate_dataframe_has_argument_columns(self.data_hash_column, "data_hash_column",
                                                                    self.data, "data", False)

        if not for_data_args:
            # Check for length of the arguments "delimiter" and "quotechar".
            if self.delimiter is not None:
                _Validators._validate_str_arg_length('delimiter', self.delimiter, 'EQ', 1)

            if self.quotechar is not None:
                _Validators._validate_str_arg_length('quotechar', self.quotechar, 'EQ', 1)

            # The arguments 'quotechar' and 'delimiter' cannot take newline character.
            if self.delimiter == '\n':
                raise TeradataMlException(Messages.get_message(MessageCodes.NOT_ALLOWED_VALUES,
                                                               "\n", "delimiter"),
                                          MessageCodes.NOT_ALLOWED_VALUES)
            if self.quotechar == '\n':
                raise TeradataMlException(Messages.get_message(MessageCodes.NOT_ALLOWED_VALUES,
                                                               "\n", "quotechar"),
                                          MessageCodes.NOT_ALLOWED_VALUES)

            # The arguments 'quotechar' and 'delimiter' cannot have the same value.
            if self.delimiter == self.quotechar:
                raise TeradataMlException(Messages.get_message(MessageCodes.ARGUMENT_VALUE_SAME,
                                                               "delimiter", "quotechar"),
                                          MessageCodes.ARGUMENT_VALUE_SAME)

    def set_data(self,
                 data,
                 data_partition_column=None,
                 data_hash_column=None,
                 data_order_column=None,
                 is_local_order=False,
                 sort_ascending=True,
                 nulls_first=True):
        """
        DESCRIPTION:
            Function enables user to set data and data related arguments without having to
            re-create Script object.

        PARAMETERS:
            data:
                Required Argument.
                Specifies a teradataml DataFrame containing the input data for the script.

            data_hash_column:
                Optional Argument.
                Specifies the column to be used for hashing.
                The rows in the data are redistributed to AMPs based on the
                hash value of the column specified.
                The user installed script then runs once on each AMP.
                If there is no data_partition_column, then the entire result set delivered
                by the function, constitutes a single group or partition.
                Types: str
                Note:
                    "data_hash_column" can not be specified along with
                    "data_partition_column", "is_local_order" and "data_order_column".

            data_partition_column:
                Optional Argument.
                Specifies Partition By columns for data.
                Values to this argument can be provided as a list, if multiple
                columns are used for partition.
                Default Value: ANY
                Types: str OR list of Strings (str)
                Note:
                    1) "data_partition_column" can not be specified along with
                       "data_hash_column".
                    2) "data_partition_column" can not be specified along with
                       "is_local_order = True".

            is_local_order:
                Optional Argument.
                Specifies a boolean value to determine whether the input data is to be
                ordered locally or not. Order by specifies the order in which the
                values in a group or partition are sorted.  Local Order By specifies
                orders qualified rows on each AMP in preparation to be input to a table
                function. This argument is ignored, if "data_order_column" is None. When
                set to True, data is ordered locally.
                Default Value: False
                Types: bool
                Note:
                    1) "is_local_order" can not be specified along with
                       "data_hash_column".
                    2) When "is_local_order" is set to True, "data_order_column" should be
                       specified, and the columns specified in "data_order_column" are
                       used for local ordering.

            data_order_column:
                Optional Argument.
                Specifies Order By columns for data.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                This argument is used in both cases:
                "is_local_order = True" and "is_local_order = False".
                Types: str OR list of Strings (str)
                Note:
                    "data_order_column" can not be specified along with
                    "data_hash_column".

            sort_ascending:
                Optional Argument.
                Specifies a boolean value to determine if the result set is to be sorted
                on the column specified in "data_order_column", in ascending or descending
                order.
                The sorting is ascending when this argument is set to True, and descending
                when set to False.
                This argument is ignored, if "data_order_column" is None.
                Default Value: True
                Types: bool

            nulls_first:
                Optional Argument.
                Specifies a boolean value to determine whether NULLS are listed first or
                last during ordering.
                This argument is ignored, if "data_order_column" is None.
                NULLS are listed first when this argument is set to True, and
                last when set to False.
                Default Value: True
                Types: bool

        RETURNS:
            None.

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> self.set_data(df)
        """

        awu_matrix_setter = []
        awu_matrix_setter.append(["data", data, True, (tdmldf.dataframe.DataFrame)])
        awu_matrix_setter.append(["data_partition_column", data_partition_column,
                                  True, (str, list), True])
        awu_matrix_setter.append(["data_hash_column", data_hash_column, True,
                                       (str, list), True])
        awu_matrix_setter.append(["data_order_column", data_order_column, True,
                                  (str, list), True])
        awu_matrix_setter.append(["is_local_order", is_local_order, True, (bool)])
        awu_matrix_setter.append(["sort_ascending", sort_ascending, True, (bool)])
        awu_matrix_setter.append(["nulls_first", nulls_first, True, (bool)])

        # Perform the function validations
        _Validators._validate_missing_required_arguments([["data", data, False,
                                                           (tdmldf.dataframe.DataFrame)]])
        _Validators._validate_function_arguments(awu_matrix_setter)

        self.data = data
        self.data_partition_column = data_partition_column
        self.data_hash_column = data_hash_column
        self.data_order_column = data_order_column
        self.is_local_order = is_local_order
        self.sort_ascending = sort_ascending
        self.nulls_first = nulls_first

    def _execute(self, output_style='VIEW'):
        """
        Function to execute Table Operator queries.
        Create DataFrames for the required Table Operator output.
        """
        table_type = TeradataConstants.TERADATA_VIEW
        if output_style == OutputStyle.OUTPUT_TABLE.value:
            table_type = TeradataConstants.TERADATA_TABLE

        # Generate STDOUT table name and add it to the output table list.
        tblop_stdout_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_tblop_out_",
                                                                          use_default_database=True, gc_on_quit=True,
                                                                          quote=False,
                                                                          table_type=table_type
                                                                          )

        try:
            if output_style == OutputStyle.OUTPUT_TABLE.value:
                UtilFuncs._create_table(tblop_stdout_temp_tablename, self._tblop_query)
            else:
                UtilFuncs._create_view(tblop_stdout_temp_tablename, self._tblop_query)
        except Exception as emsg:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_EXEC_SQL_FAILED, str(emsg)),
                                      MessageCodes.TDMLDF_EXEC_SQL_FAILED)


        self.result = self.__awu._create_data_set_object(
            df_input=UtilFuncs._extract_table_name(tblop_stdout_temp_tablename), source_type="table",
            database_name=UtilFuncs._extract_db_name(tblop_stdout_temp_tablename))

        return self.result

    def _returns_clause_validation(self):
        """
        DESCRIPTION:
            Function validates 'returns' clause for a table operator query.

        PARAMETERS:
            None.

        RETURNS:
            None

        RAISES:
            Error if argument is not of valid datatype.

        EXAMPLES:
            self._returns_clause_validation()
        """
        # Validate keys and datatypes in returns.
        if self.returns is not None:
            awu_matrix_returns = []
            for key in self.returns.keys():
                awu_matrix_returns.append(["keys in returns", key, False, (str), True])
                awu_matrix_returns.append(["values in returns", self.returns[key], False, self._supported_returns_datatypes])
            _Validators._validate_function_arguments(awu_matrix_returns)

    def setup_test_env(self, docker_image_location):
        """
                DESCRIPTION:
                    Function enables user to load already downloaded sandbox image.
                    This will enable users to run the Python scripts on client machine outside of
                    Open Analytics Framework.

                PARAMETERS:
                    docker_image_location:
                        Required Argument.
                        Specifies the location of image on user's system.
                        Types: str
                        Note:
                            For location to download docker image refer teradataml User Guide.

                RETURNS:
                    None.

                RAISES:
                    TeradataMlException

                EXAMPLES:
                    # Load example data.
                    load_example_data("Script", ["barrier"])

                    # Example - The script mapper.py reads in a line of text input ("Old Macdonald Had A Farm") from csv and
                    # splits the line into individual words, emitting a new row for each word.

                    # Create teradataml DataFrame objects.
                    >>> barrierdf = DataFrame.from_table("barrier")

                    # Create remote user environment.
                    >>> test_env = create_env('test_env', 'python_3.7.9', 'Demo environment');
                    User environment test_env created.

                    # Create an Apply object that allows user to execute script using Open Analytics Framework.
                    >>> apply_obj = Apply(data=barrierdf,
                                script_name='mapper.py',
                                files_local_path='data/scripts',
                                apply_command='python mapper.py',
                                delimiter=',',
                                env_name = "test_env",
                                data_partition_column="Id",
                                returns={"word": VARCHAR(15), "count_input": VARCHAR(2)}
                                )

                    # Run user script locally within docker container and using data from csv.
                    # This helps the user to fix script level issues outside of Open Analytics Framework.
                    # Setup the environment by providing local path to docker image file.
                    >>> apply_obj.setup_test_env(docker_image_location='/tmp/sto_sandbox_docker_image.tar'))
                    Loading image from /tmp/sto_sandbox_docker_image.tar. It may take few minutes.
                    Image loaded successfully.
        """
        self.awu_matrix_setup=[]
        self.awu_matrix_setup.append((["docker_image_location", docker_image_location, False, (str), True]))

        # Validate missing arguments
        _Validators._validate_missing_required_arguments(self.awu_matrix_setup)

        # Validate argument types
        _Validators._validate_function_arguments(self.awu_matrix_setup)

        # Load image from user provided location
        client = docker.from_env()
        if not Path(docker_image_location).exists():
            raise TeradataMlException(
                Messages.get_message(MessageCodes.INPUT_FILE_NOT_FOUND).format(docker_image_location),
                MessageCodes.INPUT_FILE_NOT_FOUND)
        else:
            try:
                print("Loading image from {0}. It may take few minutes.".format(docker_image_location))
                with open(docker_image_location, 'rb') as f:
                    client.images.load(f)
                print("Image loaded successfully.")
            except:
                raise

        # Set _latest_sandbox_exists to True - which indicates sandbox image for STO exists on the system
        configure._latest_sandbox_exists = True


    def setup_sto_env(self, docker_image_location):
        """
        DESCRIPTION:
            Function enables user to load already downloaded sandbox image.

        PARAMETERS:
            docker_image_location:
                Required Argument.
                Specifies the location of image on user's system.
                Types: str

                Note:
                    For location to download docker image refer teradataml User Guide.

        RETURNS:
            None.

        RAISES:
            TeradataMlException

        EXAMPLES:
            # Note - Refer to User Guide for setting search path and required permissions.
            # Load example data.
            load_example_data("Script", ["barrier"])

            # Example - The script mapper.py reads in a line of text input
            # ("Old Macdonald Had A Farm") from csv and
            # splits the line into individual words, emitting a new row for each word.

            # Create teradataml DataFrame objects.
            >>> barrierdf = DataFrame.from_table("barrier")

            # Set SEARCHUIFDBPATH.
            >>> execute_sql("SET SESSION SEARCHUIFDBPATH = alice;")

            # Create a Script object that allows us to execute script on Vantage.
            >>> import os
            >>> td_path = os.path.dirname(teradataml.__file__)
            >>> from teradatasqlalchemy import VARCHAR
            >>> sto = Script(data=barrierdf,
            ...              script_name='mapper.py',
            ...              files_local_path= os.path.join(td_path, 'data', 'scripts'),
            ...              script_command='python ./alice/mapper.py',
            ...              data_order_column="Id",
            ...              is_local_order=False,
            ...              nulls_first=False,
            ...              sort_ascending=False,
            ...              charset='latin',
            ...              returns=OrderedDict([("word", VARCHAR(15)),("count_input", VARCHAR(2))]))

            # Run user script locally within docker container and using data from csv.
            # This helps the user to fix script level issues outside Vantage.
            # Setup the environment by providing local path to docker image file.
            >>> sto.setup_sto_env(docker_image_location='/tmp/sto_sandbox_docker_image.tar')
            Loading image from /tmp/sto_sandbox_docker_image.tar. It may take few minutes.
            Image loaded successfully.
            Starting a container for stosandbox:1.0 image.
            Container d7c73cb498c79a082180576bb5b10bb07b52efdd3026856146fc15e91147b19f
            started successfully.

        """
        self.awu_matrix_setup = []
        self.awu_matrix_setup.append((["docker_image_location", docker_image_location,
                                       False, (str), True]))

        # Validate missing arguments.
        _Validators._validate_missing_required_arguments(self.awu_matrix_setup)

        # Validate argument types.
        _Validators._validate_function_arguments(self.awu_matrix_setup)

        from teradataml.table_operators.sandbox_container_util import setup_sandbox_env
        setup_sandbox_env(sandbox_image_location=docker_image_location,
                          sandbox_image_name='stosandbox:1.0')

        # Set _latest_sandbox_exists to True - which indicates sandbox image for STO
        # exists on the system.
        from teradataml.options.configure import configure
        configure._latest_sandbox_exists = True

    def test_script(self, supporting_files=None, input_data_file=None, script_args="",
                    exec_mode='sandbox', **kwargs):
        """
        DESCRIPTION:
            Function enables user to run script in docker container environment outside
            Vantage.
            Input data for user script is read from file.

        PARAMETERS:
            supporting_files:
                Optional Argument
                Specifies a file or list of supporting files like model files to be
                copied to the container.
                Types: string or list of str

            input_data_file:
                Required Argument.
                Specifies the name of the input data file.
                It should have a path relative to the location specified in
                "files_local_path" argument.
                If set to None, read data from AMP, else from file passed in the argument
                'input_data_file'.
                File should have at least permissions of mode 644.
                Types: str

            script_args:
                Optional Argument.
                Specifies command line arguments required by the user script.
                Types: str

            exec_mode:
                Optional Argument.
                Specifies the mode in which user wants to test the script.
                If set to 'sandbox', the user script will run within the sandbox
                environment, else it will run locally on user's system.
                Permitted Values: 'sandbox', 'local'
                Default Value: 'sandbox'
                Types: str

            kwargs:
                Optional Argument.
                Specifies the keyword arguments required for testing.
                Keys can be:
                    data_row_limit:
                        Optional Argument. Ignored when data is read from file.
                        Specifies the number of rows to be taken from all amps when
                        reading from a table or view on Vantage.
                        Default Value: 1000
                        Types: int

                    password:
                        Optional Argument. Required when reading from database.
                        Specifies the password to connect to vantage where the data
                        resides.
                        Types: str

                    data_file_delimiter:
                        Optional Argument.
                        Specifies the delimiter used in the input data file. This
                        argument can be specified when data is read from file.
                        Default Value: '\t'
                        Types: str

                    data_file_header:
                        Optional Argument.
                        Specifies whether the input data file contains header. This
                        argument can be specified when data is read from file.
                        Default Value: True
                        Types: bool

                    timeout:
                        Optional Argument.
                        Specifies the timeout for docker API calls when running in
                        sandbox mode.
                        Default Value: 5000
                        Types: int

                    data_file_quote_char:
                        Optional Argument.
                        Specifies the quotechar used in the input data file.
                        This argument can be specified when data is read from file.
                        Default Value: '"'

                    logmech:
                        Optional Argument.
                        Specifies the type of logon mechanism to establish a connection to
                        Teradata Vantage.
                        Permitted Values: 'TD2', 'TDNEGO', 'LDAP', 'KRB5' & 'JWT'.
                            TD2:
                                The Teradata 2 (TD2) mechanism provides authentication
                                using a Vantage username and password. This is the default
                                logon mechanism using which the connection is established
                                to Vantage.

                            TDNEGO:
                                A security mechanism that automatically determines the
                                actual mechanism required, based on policy, without user's
                                involvement. The actual mechanism is determined by the
                                TDGSS server configuration and by the security policy's
                                mechanism restrictions.

                            LDAP:
                                A directory-based user logon to Vantage with a directory
                                username and password and is authenticated by the directory.

                            KRB5 (Kerberos):
                                A directory-based user logon to Vantage with a domain
                                username and password and is authenticated by
                                Kerberos (KRB5 mechanism).
                                Note:
                                    User must have a valid ticket-granting ticket in
                                    order to use this logon mechanism.

                            JWT:
                                The JSON Web Token (JWT) authentication mechanism enables
                                single sign-on (SSO) to the Vantage after the user
                                successfully authenticates to Teradata UDA User Service.
                                Note:
                                    User must use logdata parameter when using 'JWT' as
                                    the logon mechanism.
                        Default Value: TD2
                        Types: str

                        Note:
                            teradataml expects the client environments are already setup with appropriate
                            security mechanisms and are in working conditions.
                            For more information please refer Teradata Vantage™ - Advanced SQL Engine
                            Security Administration at https://www.info.teradata.com/

                    logdata:
                        Optional Argument.
                        Specifies parameters to the LOGMECH command beyond those needed by
                        the logon mechanism, such as user ID, password and tokens
                        (in case of JWT) to successfully authenticate the user.
                        Types: str

                Types: dict

        RETURNS:
            Output from user script.

        RAISES:
            TeradataMlException

        EXAMPLES:
            # Assumption - sto is Script() object. Please refer to help(Script)
            # for creating Script object.
            # Run user script in sandbox mode with input from data file.

            >>> sto.test_script(input_data_file='../barrier.csv',
            ...                 data_file_delimiter=',',
            ...                 data_file_quote_char='"',
            ...                 data_file_header=True,
            ...                 exec_mode='sandbox')

            ############ STDOUT Output ############
                    word  count_input
            0          1            1
            1        Old            1
            2  Macdonald            1
            3        Had            1
            4          A            1
            5       Farm            1
            >>>

            # Run user script in local mode with input from table.
            >>> sto.test_script(data_row_limit=300, password='alice', exec_mode='local')

            ############ STDOUT Output ############
                    word  count_input
            0          1            1
            1        Old            1
            2  Macdonald            1
            3        Had            1
            4          A            1
            5       Farm            1

            # Run user script in sandbox mode with logmech as 'TD2'.
            >>> sto.test_script(script_args="4 5 10 6 480", password="alice", logmech="TD2")

            # Run user script in sandbox mode with logmech as 'TDNEGO'.
            >>> sto.test_script(script_args="4 5 10 6 480", password="alice", logmech="TDNEGO")

            # Run user script in sandbox mode with logmech as 'LDAP'.
            >>> sto.test_script(script_args="4 5 10 6 480", password="alice", logmech="LDAP")

            # Run user script in sandbox mode with logmech as 'KRB5'.
            >>> sto.test_script(script_args="4 5 10 6 480", password="alice", logmech="KRB5")

            # Run user script in sandbox mode with logmech as 'JWT'.
            >>> sto.test_script(script_args="4 5 10 6 480", password="alice",
                                logmech='JWT', logdata='token=eyJpc...h8dA')

        """
        logmech_valid_values = ['TD2', 'TDNEGO', 'LDAP', 'KRB5', 'JWT']

        awu_matrix_test = []
        awu_matrix_test.append((["supporting_files", supporting_files, True,
                                 (str, list), True]))
        awu_matrix_test.append((["input_data_file", input_data_file, True, (str), True]))
        awu_matrix_test.append((["script_args", script_args, True, (str), False]))
        awu_matrix_test.append((["exec_mode", exec_mode, True, (str), True,
                                 [TableOperatorConstants.SANDBOX_EXEC.value,
                                  TableOperatorConstants.LOCAL_EXEC.value]]))

        data_row_limit = kwargs.pop("data_row_limit", 1000)
        awu_matrix_test.append((["data_row_limit", data_row_limit, True, (int), True]))

        data_file_delimiter = kwargs.pop("data_file_delimiter", '\t')
        awu_matrix_test.append((["data_file_delimiter", data_file_delimiter, True,
                                 (str), False]))

        data_file_quote_char = kwargs.pop("data_file_quote_char", '"')
        awu_matrix_test.append((["data_file_quote_char", data_file_quote_char, True,
                                 (str), False]))

        data_file_header = kwargs.pop("data_file_header", True)
        awu_matrix_test.append((["data_file_header", data_file_header, True, (bool)]))

        timeout = kwargs.pop("timeout", 5000)
        awu_matrix_test.append((["timeout", timeout, True, (int), True]))

        logmech = kwargs.pop("logmech", "TD2")
        awu_matrix_test.append(
            ["logmech", logmech, True, (str), True, logmech_valid_values])

        logdata = kwargs.pop("logdata", None)
        awu_matrix_test.append(["logdata", logdata, True, (str), True])

        # Validate argument types.
        _Validators._validate_function_arguments(awu_matrix_test)

        # Validate timeout value.
        _Validators._validate_positive_int(timeout, "timeout")

        self._validate()

        if logmech == "JWT" and not logdata:
            raise TeradataMlException(
                Messages.get_message(MessageCodes.DEPENDENT_ARG_MISSING, 'logdata',
                                     'logmech=JWT'),
                MessageCodes.DEPENDENT_ARG_MISSING)

        if data_row_limit <= 0:
            raise ValueError(Messages.get_message(MessageCodes.TDMLDF_POSITIVE_INT).
                             format("data_row_limit", "greater than"))

        # Either of 'input_data_file' or 'password' argument is required.
        password = kwargs.pop("password", None)

        # The check of EITHER_THIS_OR_THAT_ARGUMENT is applicable only when the exec_mode is sandbox.
        # Hence adding the check exec_mode != "local".
        # When exec_mode is local, the connection object is used to get the values in the table.
        if exec_mode != "local" and not (input_data_file or (self.data and password)):
            message = Messages.get_message(MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT,
                                           "input_data_file", "Script data and password")
            raise TeradataMlException(message, MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT)
        elif exec_mode == "local" and not (input_data_file or self.data):
            message = Messages.get_message(MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT,
                                           "input_data_file", "Script data")
            raise TeradataMlException(message, MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT)

        if not self.script_name and self.files_local_path:
            message = Messages.get_message(MessageCodes.MISSING_ARGS,
                                           "script_name and files_local_path")
            raise TeradataMlException(message, MessageCodes.MISSING_ARGS)

        if input_data_file:
            if self.files_local_path is None:
                message = Messages.get_message(MessageCodes.DEPENDENT_ARG_MISSING,
                                               "files_local_path", "input_data_file")
                raise TeradataMlException(message, MessageCodes.DEPENDENT_ARG_MISSING)
            else:
                # Check if file exists.
                fpath = os.path.join(self.files_local_path,
                                     input_data_file)
                _Validators._validate_file_exists(fpath)

        if self.script_name and self.files_local_path:
            # Check if file exists.
            fpath = os.path.join(self.files_local_path,
                                 os.path.basename(self.script_name))
            _Validators._validate_file_exists(fpath)

        if exec_mode.upper() == TableOperatorConstants.LOCAL_EXEC.value:
            user_script_path = os.path.join(self.files_local_path, self.script_name)
            import sys
            cmd = [str(sys.executable), user_script_path]
            cmd.extend(script_args)

            if input_data_file is not None:
                input_file_path = os.path.join(self.files_local_path, input_data_file)

                # Run user script locally with input from a file.
                exec_cmd_output = self.__local_run_user_script_input_file(
                    cmd, input_file_path, data_file_delimiter, data_file_quote_char, data_file_header)
                try:
                    return self.__process_test_script_output(exec_cmd_output)
                except Exception as exp:
                    raise

            else:
                if self.data.shape[0] > data_row_limit:
                    raise ValueError(
                        Messages.get_message(MessageCodes.DATAFRAME_LIMIT_ERROR,
                                             'data_row_limit', 'data_row_limit',
                                             data_row_limit))

                if not self.data._table_name:
                    self.data._table_name = df_utils._execute_node_return_db_object_name(
                        self.data._nodeid, self.data._metaexpr)

                table_name = UtilFuncs._extract_table_name(self.data._table_name)

                # Run user script locally with input from db.
                exec_cmd_output = self.__local_run_user_script_input_db(cmd, table_name)
                try:
                    return self.__process_test_script_output(exec_cmd_output)
                except Exception as exp:
                    raise
        else:
            # Execution Mode - sandbox.
            # Read container_id from configure.sandbox_container_id, if it is None then
            # raise an exception
            container_id = configure.sandbox_container_id
            if container_id is None:
                message = Messages.get_message(MessageCodes.SANDBOX_CONTAINER_NOT_FOUND)
                raise TeradataMlException(message,
                                          MessageCodes.SANDBOX_CONTAINER_NOT_FOUND)

            # Set path inside docker container. This is where files will be copied to.
            # os.path.join() will not work here because the path is not dependent on
            # client platform. Sandbox environment is linux based here.
            _path_in_docker_container = "/home/tdatuser"
            user_script_path = "{}/{}".format(_path_in_docker_container, self.script_name)

            if input_data_file is not None:
                input_file_name = os.path.basename(input_data_file)
                input_file_path = "{}/{}".format(_path_in_docker_container,
                                                 input_file_name)
                # Create script_executor.
                self._create_executor_script(user_script_path=user_script_path,
                                             user_script_args=script_args,
                                             data_file_path=input_file_path,
                                             data_file_delimiter=data_file_delimiter,
                                             data_file_quote_char=data_file_quote_char,
                                             data_file_header=data_file_header)
            else:
                # Read input from db.
                if self.data.shape[0] > data_row_limit:
                    raise ValueError(
                        Messages.get_message(MessageCodes.DATAFRAME_LIMIT_ERROR,
                                             'data_row_limit', 'data_row_limit',
                                             data_row_limit))
                db_host = get_context().url.host

                user_name = get_context().url.username

                if not self.data._table_name:
                    self.data._table_name = df_utils._execute_node_return_db_object_name(
                        self.data._nodeid, self.data._metaexpr)
                table_name = UtilFuncs._extract_table_name(self.data._table_name)

                db_name = _get_current_databasename()

                # Create script_executor.
                self._create_executor_script(user_script_path=user_script_path,
                                             user_script_args=script_args,
                                             db_host=db_host,
                                             user_name=user_name,
                                             passwd=password,
                                             table_name=table_name,
                                             db_name=db_name,
                                             logmech=logmech,
                                             logdata=logdata)

            client = docker.APIClient(timeout=timeout)

            # Copy files to container indicated in configure.sandbox_container_id.
            files_to_copy = [self.script_name]

            if supporting_files is not None:
                if isinstance(supporting_files, str):
                    supporting_files = [supporting_files]

                if len(supporting_files) == 0 \
                        or any(file in [None, "None", ""] for file in supporting_files):
                    raise ValueError(
                        Messages.get_message(MessageCodes.LIST_SELECT_NONE_OR_EMPTY,
                                             'supporting_files'))
                else:
                    files_to_copy.extend(supporting_files)

            if input_data_file is not None:
                files_to_copy.append(input_data_file)

            for filename in files_to_copy:
                file_path = os.path.join(self.files_local_path, filename)
                # Check if file exists.
                _Validators._validate_file_exists(file_path)

                # Copy file to docker container.

                self._copy_to_docker_container(client, file_path,
                                               _path_in_docker_container,
                                               container_id)

            # Copy script_executor to docker container.
            self._copy_to_docker_container(client, self.script_path,
                                           _path_in_docker_container,
                                           container_id)

            script_executor_file_name = os.path.basename(self.script_path)
            exec_cmd = ("python3 {0}/{1}".format(_path_in_docker_container,
                                                 script_executor_file_name))

            try:
                # Setup an exec instance in the container.
                exec_cmd_create = client.exec_create(container_id, exec_cmd)

                # Start exec instance and run user script.
                exec_cmd_output = client.exec_start(exec_cmd_create, demux=True)

                # Inspect the output for success or failure.
                inspect_out = client.exec_inspect(exec_cmd_create)

                # Extract the exit code.
                exit_code = inspect_out['ExitCode']

                if exec_cmd_output[0] is not None:
                    executor_output = exec_cmd_output[0].decode()

                executor_error = ""
                if exec_cmd_output[1] is not None:
                    executor_error = exec_cmd_output[1].decode()

                # Exit code 1 indicates any error thrown by subprocess.
                # Exit code 126 indicates permission problem or command is not executable.
                # Exit code 127 indicates possible typos in shell script with
                # unrecognizable characters.
                if exit_code == 1 or exit_code == 126 or exit_code == 127:
                    message = Messages.get_message(
                        MessageCodes.SANDBOX_SCRIPT_ERROR).format(executor_error)
                    raise TeradataMlException(message,
                                              MessageCodes.SANDBOX_SCRIPT_ERROR)
                # Exit code 2 indicates either username or password is invalid.
                elif exit_code == 2:
                    message = Messages.get_message(
                        MessageCodes.SANDBOX_CONNECTION_ERROR).format(executor_error)
                    raise TeradataMlException(message,
                                              MessageCodes.SANDBOX_CONNECTION_ERROR)
                # Exit code 3 indicates problem with query.
                elif exit_code == 3:
                    message = Messages.get_message(
                        MessageCodes.SANDBOX_QUERY_ERROR).format(executor_error)
                    raise TeradataMlException(message,
                                              MessageCodes.SANDBOX_QUERY_ERROR)
                # Exit code 4 indicates all other exceptions / errors.
                elif exit_code == 4:
                    message = Messages.get_message(
                        MessageCodes.SANDBOX_CONTAINER_ERROR).format(executor_error)
                    raise TeradataMlException(message,
                                              MessageCodes.SANDBOX_CONTAINER_ERROR)
                elif exit_code != 0:
                    # Any error other than exit code 1, 2, 3, 4
                    message = Messages.get_message(
                        MessageCodes.SANDBOX_CONTAINER_ERROR).format(executor_error)
                    raise TeradataMlException(message,
                                              MessageCodes.SANDBOX_CONTAINER_ERROR)
                else:
                    return self.__process_test_script_output(executor_output)
            except Exception as exp:
                message = Messages.get_message(
                    MessageCodes.SANDBOX_CONTAINER_ERROR).format(str(exp))
                raise TeradataMlException(message,
                                          MessageCodes.SANDBOX_CONTAINER_ERROR)

    def __local_run_user_script_input_file(self, cmd, input_file_path,
                                           data_file_delimiter='\t',
                                           data_file_quote_char='"',
                                           data_file_header=True):
        """
        DESCRIPTION:
            Function to run the user script in local mode with input from file.

        PARAMETERS:
            cmd:
                Required Argument.
                Specifies the command for running the user script.
                Types: str

            input_file_path:
                Required Argument.
                Specifies the absolute local path of input data file.
                Types: str

            data_file_delimiter:
                Optional Argument.
                Specifies the delimiter used in input data file.
                Default Value: '\t'
                Types: str

            data_file_quote_char:
                Optional Argument.
                Specifies the quote character used in input data file.
                Default Value: '"'
                Types: str

            data_file_header:
                Optional Argument.
                Specifies whether the input data file has header.
                Default Value: True
                Types: bool

        RETURNS:
            The string output of the command that is run on input data file.

        RAISES:
            Exception.

        EXAMPLES:
            self.__local_run_user_script_input_file(cmd ="cmd",
                                                    input_file_path = "input_file_path",
                                                    data_file_delimiter = "data_file_delimiter",
                                                    data_file_quote_char = "data_file_quote_char",
                                                    data_file_header = True)

        """
        with open(input_file_path) as data_file:
            import csv
            from pandas import isna as pd_isna

            data_handle = StringIO()

            # Read data from input file.
            ip_data = csv.reader(data_file,
                                 delimiter=data_file_delimiter,
                                 quotechar=data_file_quote_char)
            # Skip the first row of input file if data_file_header is True.
            if data_file_header:
                next(ip_data)
            for row in ip_data:
                if self.quotechar is not None:
                    # A NULL value should not be enclosed in quotes.
                    # The CSV module has no support for such output with writer,
                    # and hence the custom formatting.
                    line = ['' if pd_isna(s) else "{}{}{}".format(self.quotechar,
                                                                  str(s),
                                                                  self.quotechar)
                            for s in row]
                else:
                    line = ['' if pd_isna(s) else str(s) for s in row]

                complete_line = (self.delimiter.join(line))

                data_handle.write(complete_line)
                data_handle.write("\n")

            return self.__run_user_script_subprocess(cmd, data_handle)

    def __run_user_script_subprocess(self, cmd, data_handle):
        """
        DESCRIPTION:
            Function to run the user script in a new process and return the output.

        PARAMETERS:
            cmd:
                Required Argument.
                Specifies the command for running the script.
                Types: str

            data_handle:
                Required Argument.
                Specifies the data handle for the input data required by the user script.

        RETURNS:
            Output of user script on input data supplied in data_handle.

        RAISES:
            None.

        EXAMPLES:
            self.__run_user_script_subprocess(cmd = "exec_cmd_output",
                                              data_handle = data_handle)

        """
        # Launching new process to run the user script.
        try:
            proc = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            process_output, process_error = proc.communicate(data_handle.getvalue().encode())
            data_handle.close()

            if proc.returncode == 0:
                return process_output.decode("utf-8").rstrip("\r|\n")
            else:
                message = Messages.get_message(MessageCodes.SCRIPT_LOCAL_RUN_ERROR).\
                    format(process_error)
                raise TeradataMlException(message, MessageCodes.SCRIPT_LOCAL_RUN_ERROR)
        except Exception as e:
            raise e

    def __process_test_script_output(self, exec_cmd_output):
        """
        DESCRIPTION:
            Function to format the output of the user script.

        PARAMETERS:
            exec_cmd_output:
                Required Argument.
                Specifies the output returned by the user script.
                Types: str

        RETURNS:
            The test script output as Pandas DataFrame.

        RAISES:
            Exception.

        EXAMPLES:
            self.__process_test_script_output(exec_cmd_output = "exec_cmd_output")
        """
        try:
            kwargs = dict()
            if self.quotechar is not None:
                kwargs['quotechar'] = self.quotechar
                kwargs['quoting'] = 1  # QUOTE_ALL

            output = StringIO(exec_cmd_output)

            from pandas import read_csv as pd_read_csv

            # Form a pandas dataframe.
            df = pd_read_csv(output, sep=self.delimiter, index_col=False, header=None,
                             names=list(self.returns.keys()), **kwargs)
            return df

        except Exception as exp:
            raise exp

    def __local_run_user_script_input_db(self, cmd, table_name):
        """
        DESCRIPTION:
            Function to run the user script in local mode with input from db.

        PARAMETERS:
            cmd:
                Required Argument.
                Specifies the command for running the user script.
                Types: str

            table_name:
                Required Argument.
                Specifies the table name for input to user script.
                Types: str

        RETURNS:
            The string output of the command that is run on the Vantage table.

        RAISES:
            Exception.

        EXAMPLES:
            self.__local_run_user_script_input_db(cmd = "cmd", table_name = "table_name")

        """
        db_data_handle = StringIO()
        try:
            con = get_connection()
            # Query for reading data from DB.
            query = ("SELECT * FROM {} ORDER BY 1;".format(table_name))
            cur = execute_sql(query)
            row = cur.fetchone()
            from pandas import isna as pd_isna
            while row:
                if self.quotechar is not None:
                    # A NULL value should not be enclosed in quotes.
                    # The CSV module has no support for such output with writer,
                    # and hence the custom formatting.
                    line = ['' if pd_isna(s) else "{}{}{}".format(self.quotechar,
                                                                  str(s),
                                                                  self.quotechar)
                            for s in row]
                else:
                    line = ['' if pd_isna(s) else str(s) for s in row]

                complete_line = (self.delimiter.join(line))
                db_data_handle.write(complete_line)
                db_data_handle.write("\n")
                row = cur.fetchone()
        except Exception as exp:
            raise exp

        return self.__run_user_script_subprocess(cmd, db_data_handle)

    def _create_executor_script(self, user_script_path,
                                 user_script_args=None,
                                 data_file_path=None,
                                 data_file_delimiter='\t',
                                 data_file_quote_char='"',
                                 data_file_header=True,
                                 db_name=None,
                                 db_host=None,
                                 user_name=None,
                                 passwd=None,
                                 logmech=None,
                                 logdata=None,
                                 table_name=None):
        """
        DESCRIPTION:
            Internal function that will generate 'script_executor.py' to be copied to
            sandbox environment.

        PARAMETERS:
            user_script_path:
                Required Argument.
                Specifies the path to user script inside docker container.
                Types: str

            user_script_args:
                Optional Argument.
                Specifies command line arguments required by the user script.
                Types: str

            data_file_path:
                Required Argument.
                Specifies the path to input data file inside docker container.
                Types: str

            data_file_delimiter:
                Optional Argument.
                Specifies the delimiter used in input data file.
                Default Value: "\t" (tab)
                Types: character of length 1

            data_file_quote_char:
                Optional Argument.
                Specifies the quote character used in input data file.
                Default Value: '"'
                Types: character of length 1

            data_file_header:
                Optional Argument.
                Specifies whether the input data file has header.
                Default Value: True
                Types: bool

            db_name:
                Optional Argument.
                Specifies the current database name.
                Default Value: None
                Types: str

            db_host:
                Optional Argument.
                Specifies the host name.
                Default Value: None
                Types: str

            user_name:
                Optional Argument.
                Specifies the user name.
                Default Value: None
                Types: str

            passwd:
                Optional Argument.
                Specifies the password for user name in "user_name".
                Default Value: None
                Types: str

            table_name:
                Optional Argument.
                Specifies the table name where input data is present.
                Default Value: None
                Types: str

        RETURNS:
            None.

        RAISES:
            None.

        EXAMPLES:
            # Example 1: Create executor script when input data is to be read from a file.

            self._create_executor_script(user_script_path=user_script_path,
                                          user_script_args=script_args,
                                          data_file_path=input_file_path,
                                          data_file_delimiter=data_file_delimiter,
                                          data_file_quote_char=data_file_quote_char,
                                          data_file_header=data_file_header)

            # Example 2: Create executor script when input data is to be read from db.

            self._create_executor_script(user_script_path=user_script_path,
                                          user_script_args=script_args,
                                          db_host=db_host,
                                          user_name=user_name,
                                          passwd=password,
                                          table_name=table_name,
                                          db_name=db_name)

        """
        __data_source = "db"
        if data_file_path:
            __data_source = "file"

        temp_script_name = UtilFuncs._generate_temp_script_name(prefix="script_executor",
                                                                use_default_database=True,
                                                                gc_on_quit=True,
                                                                quote=True,
                                                                script_type=TeradataConstants.TERADATA_LOCAL_SCRIPT)

        # Remove quotes from the file name after removing the database name.
        script_alias = UtilFuncs._teradata_unquote_arg(
            UtilFuncs._extract_table_name(temp_script_name), quote='"')

        # script_name is the actual file name (basename).
        script_name = "{script_name}.py".format(script_name=script_alias)

        # Create script in .teradataml directory.
        ###

        script_dir = GarbageCollector._get_temp_dir_name()

        # script_path is the actual path where we want to generate the user script at.
        self.script_path = os.path.join(script_dir, script_name)

        template_dir = os.path.join(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))),
            "table_operators", "templates")
        try:
            # Write to the script based on the template.
            #
            from teradataml.common.constants import TableOperatorConstants
            executor_file = os.path.join(template_dir,
                                         TableOperatorConstants.SCRIPT_TEMPLATE.value)
            with open(executor_file, 'r') as input_file:
                with open(self.script_path, 'w') as output_file:
                    os.chmod(self.script_path, 0o644)
                    output_file.write(
                        input_file.read().format(
                            DATA_SOURCE=UtilFuncs._serialize_and_encode(__data_source),
                            DELIMITER=UtilFuncs._serialize_and_encode(self.delimiter),
                            QUOTECHAR=UtilFuncs._serialize_and_encode(self.quotechar),
                            USER_SCRIPT_PATH=UtilFuncs._serialize_and_encode(
                                user_script_path),
                            SCRIPT_ARGS=UtilFuncs._serialize_and_encode(user_script_args),
                            DATA_FILE_PATH=UtilFuncs._serialize_and_encode(
                                data_file_path),
                            INPUT_DATA_FILE_DELIMITER=UtilFuncs._serialize_and_encode(
                                data_file_delimiter),
                            INPUT_DATA_FILE_QUOTE_CHAR=UtilFuncs._serialize_and_encode(
                                data_file_quote_char),
                            INPUT_DATA_FILE_HEADER=UtilFuncs._serialize_and_encode(
                                data_file_header),
                            DB_HOST=UtilFuncs._serialize_and_encode(db_host),
                            DB_USER=UtilFuncs._serialize_and_encode(user_name),
                            DB_PASS=UtilFuncs._serialize_and_encode(passwd),
                            DB_NAME=UtilFuncs._serialize_and_encode(db_name),
                            TABLE_NAME=UtilFuncs._serialize_and_encode(table_name),
                            LOGMECH=UtilFuncs._serialize_and_encode(logmech),
                            LOGDATA=UtilFuncs._serialize_and_encode(logdata)
                        ))
        except Exception:
            # Cleanup if we end up here in case of an error.
            GarbageCollector._delete_local_file(self.script_path)
            raise

    def _copy_to_docker_container(self, client,
                                   local_file_path,
                                   path_in_docker_container,
                                   container):
        """
        DESCRIPTION:
            Function to copy files to docker container.

        PARAMETERS:
            client:
                Required Argument.
                Specifies the connection object for docker.
                Types: str

            local_file_path:
                Required Argument.
                Specifies the path to the file to be copied.
                Types: str

            path_in_docker_container:
                Required Argument.
                Specifies destination path in the docker container where file will be
                copied to.
                Types: str

            container:
                Required Argument.
                Specifies container id.
                Types: str

            RETURNS:
                None.

            RAISES:
                TeradataMLException.

        """
        # Create tar file.
        tar_file_path = "{}.tar".format(local_file_path)
        file_name = os.path.basename(local_file_path)
        tar = tarfile.open(tar_file_path, mode='w')
        try:
            tar.add(local_file_path, arcname=file_name)
        finally:
            tar.close()
        data = open(tar_file_path, 'rb').read()

        try:
            # Copy file to docker container.
            copy_status = client.put_archive(container, path_in_docker_container, data)
            os.remove(tar_file_path)

            if copy_status:
                return
        except Exception as exp:
            message = Messages.get_message(
                MessageCodes.SANDBOX_CONTAINER_ERROR).format(str(exp))
            raise TeradataMlException(message, MessageCodes.SANDBOX_CONTAINER_ERROR)

    def __repr__(self):
        """
        Returns the string representation for the class instance.
        """
        if self.result is None:
            repr_string = "Result is empty. Please run execute_script first."
        else:
            repr_string = "############ STDOUT Output ############"
            repr_string = "{}\n\n{}".format(repr_string, self.result)
        return repr_string

