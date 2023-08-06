"""
Unpublished work.
Copyright (c) 2023 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: shivani.kondewar@teradata.com
Secondary Owner: pradeep.garre@teradata.com
This includes common functionalities required
by other classes which can be reused according to the need.

"""

from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messages import Messages, MessageCodes
from teradataml.utils.validators import _Validators


def execute_sql(statement, parameters=None):
    """
    DESCRIPTION:
        Executes the SQL statement by using provided parameters.
        Note:
            Execution of stored procedures and user defined functions is not supported.

    PARAMETERS:
        statement:
            Required Argument.
            Specifies the SQL statement to execute.
            Types: str

        parameters:
            Optional Argument.
            Specifies parameters to be used in case of parameterized query.
            Types: list of list, list of tuple

    RETURNS:
        Cursor object.

    RAISES:
        TeradataMlException, teradatasql.OperationalError, TypeError, ValueError

    EXAMPLES:
        # Example 1: Create a table and insert values into the table using SQL.
        # Create a table.
        execute_sql("Create table table1 (col_1 int, col_2 varchar(10), col_3 float);")

        # Insert values in the table created above.
        execute_sql("Insert into table1 values (1, 'col_val', 2.0);")

        # Insert values in the table using a parameterized query.
        execute_sql(statement="Insert into table1 values (?, ?, ?);",
                    parameters=[[1, 'col_val_1', 10.0],
                                [2, 'col_val_2', 20.0]])

        # Example 2: Execute parameterized 'SELECT' query.
        result_cursor = execute_sql(statement="Select * from table1 where col_1=? and col_3=?;",
                                    parameters=[(1, 10.0),(1, 20.0)])

        # Example 3: Run Help Column query on table.
        result_cursor = execute_sql('Help column table1.*;')

    """
    # Validate argument types
    arg_info_matrix = []
    arg_info_matrix.append(["statement", statement, False, str, True])
    arg_info_matrix.append(["parameters", parameters, True, (tuple, list), False])

    _Validators._validate_function_arguments(arg_info_matrix)

    from teradataml.context.context import get_context
    if get_context() is not None:
        tdsql_con = get_context().raw_connection().driver_connection
        cursor = tdsql_con.cursor()
        return cursor.execute(statement, parameters)
    else:
        raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_CONTEXT_CONNECTION),
                                  MessageCodes.INVALID_CONTEXT_CONNECTION)
