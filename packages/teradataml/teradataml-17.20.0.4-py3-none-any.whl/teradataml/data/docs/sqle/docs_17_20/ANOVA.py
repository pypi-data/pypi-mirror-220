def ANOVA(data=None, group_columns=None, alpha=0.05, **generic_arguments):
    """
    DESCRIPTION:
        The ANOVA() function performs one-way ANOVA (Analysis of Variance) on
        a data set with two or more groups. ANOVA is a statistical test that
        analyzes the difference between the means of more than two groups.

        The null hypothesis (H0) of ANOVA is that there is no difference among
        group means. However, if any one of the group means is significantly
        different from the overall mean, then the null hypothesis is rejected.
        You can use one-way Anova when you have data on an independent variable
        with at least three levels and a dependent variable.

        For example, assume that your independent variable is insect spray type,
        and you have data on spray type A, B, C, D, E, and F. You can use one-way
        ANOVA to determine whether there is any difference in the dependent variable,
        insect count based on the spray type used.


    PARAMETERS:
        data:
            Required Argument.
            Specifies the input teradataml DataFrame.
            Types: teradataml DataFrame

        group_columns:
            Optional Argument.
            Specifies the names of the columns in "data" to use in the computation.
            Note:
                Users must specify at least two columns in "group_columns" list.
            Types: list of Strings (str)

        alpha:
            Optional Argument.
            Specifies the probability of rejecting the null hypothesis when the null
            hypothesis is true.
            Default Value: 0.05
            Types: float

        **generic_arguments:
            Specifies the generic keyword arguments SQLE functions accept. Below
            are the generic keyword arguments:
                persist:
                    Optional Argument.
                    Specifies whether to persist the results of the
                    function in a table or not. When set to True,
                    results are persisted in a table; otherwise,
                    results are garbage collected at the end of the
                    session.
                    Default Value: False
                    Types: bool

                volatile:
                    Optional Argument.
                    Specifies whether to put the results of the
                    function in a volatile table or not. When set to
                    True, results are stored in a volatile table,
                    otherwise not.
                    Default Value: False
                    Types: bool

            Function allows the user to partition, hash, order or local
            order the input data. These generic arguments are available
            for each argument that accepts teradataml DataFrame as
            input and can be accessed as:
                * "<input_data_arg_name>_partition_column" accepts str or
                  list of str (Strings)
                * "<input_data_arg_name>_hash_column" accepts str or list
                  of str (Strings)
                * "<input_data_arg_name>_order_column" accepts str or list
                  of str (Strings)
                * "local_order_<input_data_arg_name>" accepts boolean
            Note:
                These generic arguments are supported by teradataml if
                the underlying SQL Engine function supports, else an
                exception is raised.

    RETURNS:
        Instance of ANOVA.
        Output teradataml DataFrames can be accessed using attribute
        references, such as ANOVAObj.<attribute_name>.
        Output teradataml DataFrame attribute name is:
            result


    RAISES:
        TeradataMlException, TypeError, ValueError


    EXAMPLES:
        # Notes:
        #     1. Get the connection to Vantage to execute the function.
        #     2. One must import the required functions mentioned in
        #        the example from teradataml.
        #     3. Function will raise error if not supported on the Vantage
        #        user is connected to.

        # Load the example data.
        load_example_data("teradataml", ["insect_sprays"])

        # Create teradataml DataFrame objects.
        insect_sprays = DataFrame.from_table("insect_sprays")

        # Check the list of available analytic functions.
        display_analytic_functions()

        # Example 1 : Perform one-way anova analysis on a data set with
        #             two or more groups.
        ANOVA_out_1 = ANOVA(data = insect_sprays,
                            alpha = 0.05
                            )

        # Print the result DataFrame.
        print(ANOVA_out_1.result)

        # Example 2 : Perform one-way anova analysis on a data set with more
        #             than two groups and group_columns argument specified.
        ANOVA_out_2 = ANOVA(data = insect_sprays,
                            group_columns=insect_sprays.columns[2:5],
                            alpha = 0.05
                            )

        # Print the result DataFrame.
        print(ANOVA_out_2.result)

    """
