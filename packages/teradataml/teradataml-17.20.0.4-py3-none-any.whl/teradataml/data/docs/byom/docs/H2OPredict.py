def H2OPredict(modeldata=None, newdata=None, accumulate=None, model_output_fields=None, overwrite_cached_models=None,
               model_type="OpenSource", enable_options=None, newdata_partition_column="ANY", newdata_order_column=None,
               modeldata_order_column=None):
    """
    DESCRIPTION:
        The H2OPredict function performs a prediction on each row of the input table
        using a model previously trained in H2O and then loaded into the database.
        The model uses an interchange format called as MOJO and it is loaded to
        Teradata database in a table by the user as a blob.
        The model table prepared by user should have a model id for each model
        (residing as a MOJO object) created by the user.

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
            Specifies the input teradataml DataFrame that contains the data to be
            scored.

        newdata_partition_column:
            Optional Argument
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
            Types: str OR list of Strings (str)

        overwrite_cached_models:
            Optional Argument.
            Specifies the model name that needs to be removed from the cache.
            Use * to remove all cached models.
            Types: str OR list of Strings (str)

        model_type:
            Optional Argument.
            Specifies the model type for H2O model prediction.
            Default Value: "OpenSource"
            Permitted Values: DAI, OpenSource
            Types: str OR list of Strings (str)

        enable_options:
            Optional Argument.
            Specifies the options to be enabled for H2O model prediction.
            Permitted Values: contributions, stageProbabilities, leafNodeAssignments
            Types: str OR list of Strings (str)

    RETURNS:
        Instance of H2OPredict.
        Output teradataml DataFrame can be accessed using attribute
        references, such as  H2OPredictObj.<attribute_name>.
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
        from teradataml import save_byom, retrieve_byom, load_example_data,
        from teradataml import configure, display_analytic_functions

        # Load example data.
        load_example_data("byom", "iris_test")

        # Create teradataml DataFrame objects.
        iris_test = DataFrame.from_table("iris_test")

        # Set install location of BYOM functions.
        configure.byom_install_location = "mldb"

        # Check the list of available analytic functions.
        display_analytic_functions(type="BYOM")

        # Example 1: This example runs a query with GLM model, "model_type",
        #            "enable_options", "model_output_fields" and "overwrite.cached.models".
        #            This will erase entire cache.

        # Load model file into Vantage.
        model_file = os.path.join(os.path.dirname(teradataml.__file__), "data", "models", "iris_mojo_glm_h2o_model")
        save_byom("iris_mojo_glm_h2o_model", model_file, "byom_models")

        # Retrieve model.
        modeldata = retrieve_byom("iris_mojo_glm_h2o_model", table_name="byom_models")

        result = H2OPredict(newdata=iris_test,
                            newdata_partition_column='id',
                            newdata_order_column='id',
                            modeldata=modeldata,
                            modeldata_order_column='model_id',
                            model_output_fields=['label', 'classProbabilities'],
                            accumulate=['id', 'sepal_length', 'petal_length'],
                            overwrite_cached_models='*',
                            enable_options='stageProbabilities',
                            model_type='OpenSource'
                            )

        # Print the results.
        print(result.result)

        # Example 2: This example runs a query with XGBoost model, "model_type",
        #            "enable_options", "model_output_fields" and "overwrite.cached.models".
        #            This will erase entire cache.

        # Load model file into Vantage.
        model_file = os.path.join(os.path.dirname(teradataml.__file__), "data", "models", "iris_mojo_xgb_h2o_model")
        save_byom("iris_mojo_xgb_h2o_model", model_file, "byom_models")

        # Retrieve model.
        modeldata = retrieve_byom("iris_mojo_xgb_h2o_model", table_name="byom_models")

        result = H2OPredict(newdata=iris_test,
                            newdata_partition_column='id',
                            newdata_order_column='id',
                            modeldata=modeldata,
                            modeldata_order_column='model_id',
                            model_output_fields=['label', 'classProbabilities'],
                            accumulate=['id', 'sepal_length', 'petal_length'],
                            overwrite_cached_models='*',
                            enable_options='stageProbabilities',
                            model_type='OpenSource'
                            )

        # Print the results.
        print(result.result)

        # Example 3: This example runs a query with a licensed model with id 'licensed_model1'
        #            from the table 'byom_licensed_models' and associated license key stored in column
        #            'license_key' of the table 'license' present in the schema 'mldb'.

        # Retrieve model.
        modeldata = retrieve_byom('licensed_model1',
                                  table_name='byom_licensed_models',
                                  license='license_key',
                                  is_license_column=True,
                                  license_table_name='license',
                                  license_schema_name='mldb')
        result = H2OPredict(newdata=iris_test,
                            newdata_partition_column='id',
                            newdata_order_column='id',
                            modeldata=modeldata,
                            modeldata_order_column='model_id',
                            model_output_fields=['label', 'classProbabilities'],
                            accumulate=['id', 'sepal_length', 'petal_length'],
                            overwrite_cached_models='*',
                            enable_options='stageProbabilities',
                            model_type='OpenSource'
                            )
        # Print the results.
        print(result.result)

    """