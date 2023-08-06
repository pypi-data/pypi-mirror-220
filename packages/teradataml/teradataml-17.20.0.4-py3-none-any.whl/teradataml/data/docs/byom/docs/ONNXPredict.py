def ONNXPredict(newdata=None, modeldata=None, accumulate=None, model_output_fields=None, overwrite_cached_models="false",
                show_model_input_fields_map=False, model_input_fields_map=None, **generic_arguments):

    """
    DESCRIPTION:
        The ONNXPredict() function is used to score data in Vantage with a model that has
        been created outside Vantage and exported to Vantage using ONNX format.


    PARAMETERS:
        newdata:
            Required Argument.
            Specifies the teradataml DataFrame containing the input test data.
            Types: teradataml DataFrame

        modeldata:
            Required Argument.
            Specifies the teradataml DataFrame containing the model data
            to be used for scoring.
            Types: teradataml DataFrame

        accumulate:
            Required Argument.
            Specifies the name(s) of input teradataml DataFrame column(s) to copy to the output.
            Types: str OR list of Strings (str)

        model_output_fields:
            Optional Argument.
            Specifies the column(s) of the json output that the user wants to
            specify as individual columns instead of the entire json_report.
            Types: str OR list of Strings (str)

        overwrite_cached_models:
            Optional Argument.
            Specifies the model name that needs to be removed from the cache.
            "*" can also be used to remove the models.
            Default Value: "false"
            Permitted Values: true, t, yes, y, 1, false, f, no, n, 0, *,
                              current_cached_model
            Types: str

        show_model_input_fields_map:
            Optional Argument.
            Specifies whether to show default or expanded "model_input_fields_map" based on input
            model for defaults or "model_input_fields_map" for expansion.
            Default Value: False
            Types: bool

        model_input_fields_map:
            Optional Argument.
            Specifies the mapping of input columns to tensor input names.
            Types: str OR list of Strings (str)

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
        Instance of ONNXPredict.
        Output teradataml DataFrames can be accessed using attribute
        references, such as ONNXPredictObj.<attribute_name>.
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
        from teradataml import DataFrame, load_example_data, configure
        from teradataml import save_byom, retrieve_byom, display_analytic_functions

        # Load the example data.
        load_example_data("byom", ["iris_test"])

        # Create teradataml DataFrame objects.
        iris_test = DataFrame("iris_test")

        # Set install location of BYOM functions.
        configure.byom_install_location = "mldb"

        # Check the list of available analytic functions.
        display_analytic_functions(type="BYOM")

        # Load model file into Vantage.
        model_file_path = os.path.join(os.path.dirname(teradataml.__file__), "data", "models")
        skl_model_file = os.path.join(model_file_path,
                                      "iris_db_dt_model_sklearn.onnx")
        skl_floattensor_model_file = os.path.join(model_file_path,
                                                  "iris_db_dt_model_sklearn_floattensor.onnx")

        # Save ONNX models.
        save_byom("iris_db_dt_model_sklearn",
                  skl_model_file, "byom_models")
        save_byom("iris_db_dt_model_sklearn_floattensor",
                  skl_floattensor_model_file, "byom_models")

        # Retrieve ONNX model.
        # The 'iris_db_dt_model_sklearn' created with each input variable mapped
        # to a single input tensor, then converted this model into ONNX format
        # with scikit-learn-onnx, and then used to predict the flower species.
        # This model model trained using iris_test dataset with scikit-learn.
        skl_model = retrieve_byom("iris_db_dt_model_sklearn",
                                  table_name="byom_models")

        # The 'iris_db_dt_model_sklearn_floattensor' created by using an input array of
        # four float32 values and named float_input, then converted this model into ONNX
        # format with scikit-learn-onnx, and then used to predict the flower species.
        # This model trained using iris_test dataset with scikit-learn.
        skl_floattensor_model = retrieve_byom("iris_db_dt_model_sklearn_floattensor",
                                    table_name="byom_models")

        # Example 1: This example predicts the flower species using trained
        #            'skl_model' model.
        ONNXPredict_out = ONNXPredict(accumulate="id",
                                      newdata=iris_test,
                                      modeldata=skl_model)

        # Print the results.
        print(ONNXPredict_out.result)


        # Example 2: This example predicts the flower species using trained
        #            'skl_floattensor_model' model, where input DataFrame columns match the order
        #            used when generating the model, by specifying "model_input_fields_map"
        #            to define the columns.
        ONNXPredict_out1 = ONNXPredict(accumulate="id",
                                       model_output_fields="output_probability",
                                       overwrite_cached_models="*",
                                       model_input_fields_map='float_input=sepal_length, sepal_width, petal_length, petal_width',
                                       newdata=iris_test,
                                       modeldata=skl_floattensor_model)


        # Print the result DataFrame.
        print(ONNXPredict_out1.result)

    """
