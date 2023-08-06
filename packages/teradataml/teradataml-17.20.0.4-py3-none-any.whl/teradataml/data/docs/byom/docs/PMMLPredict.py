def PMMLPredict(modeldata=None, newdata=None, accumulate=None, model_output_fields=None, overwrite_cached_models=None,
                newdata_partition_column="ANY", newdata_order_column=None, modeldata_order_column=None):
    """
    DESCRIPTION:
        This function is used to score data in Vantage with a model that has been
        created outside Vantage and exported to Vantage using PMML format.


    PARAMETERS:
        modeldata:
            Required Argument.
            Specifies the model teradataml DataFrame to be used for scoring.

        modeldata_order_column:
            Optional Argument.
            Specifies Order By columns for "modeldata".
            Values to this argument can be provided as a list, if multiple
            columns are used for ordering.
            Types: str OR list of Strings (str)

        newdata:
            Required Argument.
            Specifies the input teradataml DataFrame that contains the data to be scored.

        newdata_partition_column:
            Optional Argument.
            Specifies Partition By columns for "newdata".
            Values to this argument can be provided as a list, if multiple
            columns are used for partition.
            Default Value: ANY
            Types: str OR list of Strings (str)

        newdata_order_column:
            Optional Argument.
            Specifies Order By columns for "newdata".
            Values to this argument can be provided as a list, if multiple
            columns are used for ordering.
            Types: str OR list of Strings (str)

        accumulate:
            Required Argument.
            Specifies the names of the input columns from "newdata" DataFrame
            to copy to the output DataFrame.
            Types: str OR list of Strings (str)

        model_output_fields:
            Optional Argument.
            Specifies the columns of the json output that the user wants to
            specify as individual columns instead of the entire json report.
            Types: str OR list of strs

        overwrite_cached_models:
            Optional Argument.
            Specifies the model name that needs to be removed from the cache.
            Use * to remove all cached models.
            Types: str OR list of strs

    RETURNS:
        Instance of PMMLPredict.
        Output teradataml DataFrames can be accessed using attribute
        references, such as PMMLPredictObj.<attribute_name>.
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
        #     4. To execute BYOM functions, set 'configure.byom_install_location' to the
        #        database name where BYOM functions are installed.

        # Import required libraries / functions.
        import os, teradataml
        from teradataml import DataFrame, load_example_data, create_context
        from teradataml import save_byom, retrieve_byom, configure, display_analytic_functions

        # Load example data.
        load_example_data("byom", "iris_test")

        # Create teradataml DataFrame objects.
        iris_test = DataFrame.from_table("iris_test")

        # Set install location of BYOM functions.
        configure.byom_install_location = "mldb"

        # Check the list of available analytic functions.
        display_analytic_functions(type="BYOM")

        # Example 1: This example runs a query with GLM model and
        #            "overwrite_cached_models". This will erase entire cache.

        # Load model file into Vantage.
        model_file = os.path.join(os.path.dirname(teradataml.__file__), "data", "models", "iris_db_glm_model.pmml")
        save_byom("iris_db_glm_model", model_file, "byom_models")

        # Retrieve model.
        modeldata = retrieve_byom("iris_db_glm_model", table_name="byom_models")

        result = PMMLPredict(
                modeldata = modeldata,
                newdata = iris_test,
                accumulate = ['id', 'sepal_length', 'petal_length'],
                overwrite_cached_models = '*',
                )

        # Print the results.
        print(result.result)

        # Example 2: This example runs a query with XGBoost model and
        #            "overwrite_cached_models". This will erase entire cache.

        # Load model file into Vantage.
        model_file = os.path.join(os.path.dirname(teradataml.__file__), "data", "models", "iris_db_xgb_model.pmml")
        save_byom("iris_db_xgb_model", model_file, "byom_models")

        # Retrieve model.
        modeldata = retrieve_byom("iris_db_xgb_model", table_name="byom_models")

        result = PMMLPredict(
                modeldata = modeldata,
                newdata = iris_test,
                accumulate = ['id', 'sepal_length', 'petal_length'],
                overwrite_cached_models = '*',
                )

        # Print the results.
        print(result.result)

    """