# ##################################################################
#
# Copyright 2021 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
#
# Primary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# Secondary Owner:
#
# This file implements teradataml GeoDataFrame.
# teradataml GeoDataFrame allows user to access table on Vantage
# containing Geometry or Geospatial data.
#
# ##################################################################
import sqlalchemy
from teradataml.common.constants import GeospatialConstants, TeradataTypes
from teradataml.common.messagecodes import MessageCodes
from teradataml.common.messages import Messages
from teradataml.common.utils import UtilFuncs
from teradataml.common.exceptions import TeradataMlException
from teradataml.dataframe.dataframe import DataFrame
from teradataml.geospatial.geodataframecolumn import GeoDataFrameColumn
from teradataml.plot.plot import _Plot
from teradataml.utils.validators import _Validators
from teradatasqlalchemy import (GEOMETRY, MBR, MBB)

class GeoDataFrame(DataFrame):
    """
    The teradataml GeoDataFrame enables data manipulation, exploration, and
    analysis on tables, views, and queries on Teradata Vantage that contains
    Geospatial data.
    """
    def __init__(self, table_name=None, index=True, index_label=None,
                 query=None, materialize=False):
        """
        Constructor for teradataml GeoDataFrame.

        PARAMETERS:
            table_name:
                Optional Argument.
                The table name or view name in Teradata Vantage referenced by this DataFrame.
                Types: str

            index:
                Optional Argument.
                True if using index column for sorting, otherwise False.
                Default Value: True
                Types: bool

            index_label:
                Optional Argument.
                Column/s used for sorting.
                Types: str OR list of Strings (str)

            query:
                Optional Argument.
                SQL query for this Dataframe. Used by class method from_query.
                Types: str

            materialize:
                Optional Argument.
                Whether to materialize DataFrame or not when created.
                Used by class method from_query.

                One should use enable materialization, when the query passed
                to from_query(), is expected to produce non-deterministic
                results, when it is executed multiple times. Using this option
                will help user to have deterministic results in the resulting
                teradataml GeoDataFrame.
                Default Value: False (No materialization)
                Types: bool

        EXAMPLES:
            from teradataml.dataframe.dataframe import DataFrame
            df = DataFrame("mytab")
            df = DataFrame("myview")
            df = DataFrame("myview", False)
            df = DataFrame("mytab", True, "Col1, Col2")

        RAISES:
            TeradataMlException - TDMLDF_CREATE_FAIL
        """
        self.__geom_column = None
        # Call super(), to process the inputs.
        super().__init__(table_name=table_name, index=index,
                         index_label=index_label, query=query,
                         materialize=materialize)

    def _check_geom_column(self, metaexpr=None):
        """
        DESCRIPTION:
            Internal function to whether the metaexpr contains a geospatial
            type column or not.

        PARAMETERS:
            metaexpr:
                Required Argument.
                Specifies the teradataml DataFrame/teradataml GeoDataFrame
                metaexpr to validate for geospatial content.
                Types: _MetaExpression

        RETURNS:
            boolean.
            True if Geospatial data type column exists, False otherwise.

        RAISES:
            None.

        EXAMPLES:
            self._check_geom_column(metaexpr)
        """
        if metaexpr is None:
            metaexpr = self._metaexpr.c
        for col in metaexpr.c:
            if isinstance(col.type, (GEOMETRY, MBR, MBB)):
                return True
        return False

    def plot(self, x=None, y=None, kind="geometry", **kwargs):
        """
        DESCRIPTION:
            Generate plots on teradataml GeoDataFrame. Following type of plots
            are supported, which can be specified using argument "kind":
                * geometry plot
                * bar plot
                * corr plot
                * line plot
                * mesh plot
                * scatter plot
                * wiggle plot
            Notes:
                * Geometry plot is generated based on geometry column in teradataml GeoDataFrame.
                * Only the columns with ST_GEOMETRY type are allowed for generating geometry plot.
                * The maximum size for ST_GEOMETRY must be less than or equal to 64000.
                * The ST_GEOMETRY shape can be POINT, LINESTRING etc. It is POLGYON that allows
                  filling of different colors.

        PARAMETERS:
            x:
                Optional Argument.
                Specifies a GeoDataFrame column to use for the x-axis data.
                Note:
                    "x" is not significant for geometry plots. For other plots
                    it is mandatory argument.
                Types: teradataml GeoDataFrame Column

            y:
                Required Argument.
                Specifies GeoDataFrame column(s) to use for the y-axis data.
                Notes:
                     * Geometry plot always requires geometry column and corresponding 'weight'
                       column. 'weight' column represents the weight of a shape mentioned in
                       geometry column.
                     * If user does not specify geometry column, the default geometry column
                       is considered for plotting.
                Types: teradataml GeoDataFrame Column OR tuple of GeoDataFrame Column OR list of teradataml GeoDataFrame Columns.

            scale:
                Optional Argument.
                Specifies GeoDataFrame column(s) to use for scale data to
                wiggle and mesh plots.
                Note:
                    "scale" is significant for wiggle and mesh plots. Ignored for other
                    type of plots.
                Types: teradataml GeoDataFrame Column OR list of teradataml GeoDataFrame Columns.

            kind:
                Optional Argument.
                Specifies the kind of plot.
                Permitted Values:
                    * 'geometry'
                    * 'line'
                    * 'bar'
                    * 'scatter'
                    * 'corr'
                    * 'wiggle'
                    * 'mesh'
                Default Value: geometry
                Types: str

            ax:
                Optional Argument.
                Specifies the axis for the plot.
                Types: Axis

            cmap:
                Optional Argument.
                Specifies the name of the colormap to be used for plotting.
                Notes:
                     * Significant only when corresponding type of plot is mesh or geometry.
                     * Ignored for other type of plots.
                Permitted Values:
                    * All the colormaps mentioned in below URLs are supported.
                        * https://matplotlib.org/stable/tutorials/colors/colormaps.html
                        * https://matplotlib.org/cmocean/
                Types: str

            figure:
                Optional Argument.
                Specifies the figure for the plot.
                Types: Figure

            figsize:
                Optional Argument.
                Specifies the size of the figure in a tuple of 2 elements. First
                element represents width of plot image in pixels and second
                element represents height of plot image in pixels.
                Default Value: (640, 480)
                Types: tuple

            figtype:
                Optional Argument.
                Specifies the type of the image to generate.
                Permitted Values:
                    * 'png'
                    * 'jpg'
                    * 'svg'
                Default Value: png
                Types: str

            figdpi:
                Optional Argument.
                Specifies the dots per inch for the plot image.
                Note:
                    * Valid range for "dpi" is: 72 <= width <= 300.
                Default Value: 100 for PNG and JPG Type image.
                Types: int

            grid_color:
                Optional Argument.
                Specifies the color of the grid.
                Note:
                    Hexadecimal color codes are not supported.
                Permitted Values:
                    * 'blue'
                    * 'orange'
                    * 'green'
                    * 'red'
                    * 'purple'
                    * 'brown'
                    * 'pink'
                    * 'gray'
                    * 'olive'
                    * 'cyan'
                    * Apart from above mentioned colors, the colors mentioned in
                      https://xkcd.com/color/rgb are also supported.
                Default Value: gray
                Types: str

            grid_format:
                Optional Argument.
                Specifies the format for the grid.
                Types: str

            grid_linestyle:
                Optional Argument.
                Specifies the line style of the grid.
                Permitted Values:
                    * -
                    * --
                    * -.
                Default Value: -
                Types: str

            grid_linewidth:
                Optional Argument.
                Specifies the line width of the grid.
                Note:
                    Valid range for "grid_linewidth" is: 0.5 <= grid_linewidth <= 10.
                Default Value: 0.8
                Types: int OR float

            heading:
                Optional Argument.
                Specifies the heading for the plot.
                Types: str

            legend:
                Optional Argument.
                Specifies the legend(s) for the Plot.
                Types: str OR list of str

            legend_style:
                Optional Argument.
                Specifies the location for legend to display on Plot image. By default,
                legend is displayed at upper right corner.
                Permitted Values:
                    * 'upper right'
                    * 'upper left'
                    * 'lower right'
                    * 'lower left'
                    * 'right'
                    * 'center left'
                    * 'center right'
                    * 'lower center'
                    * 'upper center'
                    * 'center'
                Default Value: 'upper right'
                Types: str

            linestyle:
                Optional Argument.
                Specifies the line style for the plot.
                Permitted Values:
                    * -
                    * --
                    * -.
                    * :
                Default Value: -
                Types: str

            linewidth:
                Optional Argument.
                Specifies the line width for the plot.
                Note:
                    Valid range for "linewidth" is: 0.5 <= linewidth <= 10.
                Default Value: 0.8
                Types: int OR float

            marker:
                Optional Argument.
                Specifies the type of the marker to be used.
                Permitted Values:
                    All the markers mentioned in https://matplotlib.org/stable/api/markers_api.html
                    are supported.
                Types: str

            markersize:
                Optional Argument.
                Specifies the size of the marker.
                Note:
                    Valid range for "markersize" is: 1 <= markersize <= 20.
                Default Value: 6
                Types: int OR float

            position:
                Optional Argument.
                Specifies the position of the axis in the figure. Accepts a tuple
                of two elements where first element represents the row and second
                element represents column.
                Default Value: (1, 1)
                Types: tuple

            span:
                Optional Argument.
                Specifies the span of the axis in the figure. Accepts a tuple
                of two elements where first element represents the row and second
                element represents column.
                For Example,
                    Span of (2, 1) specifies the Axis occupies 2 rows and 1 column
                    in Figure.
                Default Value: (1, 1)
                Types: tuple

            reverse_xaxis:
                Optional Argument.
                Specifies whether to reverse tick values on x-axis or not.
                Default Value: False
                Types: bool

            reverse_yaxis:
                Optional Argument.
                Specifies whether to reverse tick values on y-axis or not.
                Default Value: False
                Types: bool

            series_identifier:
                Optional Argument.
                Specifies the teradataml GeoDataFrame Column which represents the
                identifier for the data. As many plots as distinct "series_identifier"
                are generated in a single Axis.
                For example:
                    consider the below data in teradataml GeoDataFrame.
                           ID   x   y
                        0  1    1   1
                        1  1    2   2
                        2  2   10  10
                        3  2   20  20
                    If "series_identifier" is not specified, simple plot is
                    generated where every 'y' is plotted against 'x' in a
                    single plot. However, specifying "series_identifier" as 'ID'
                    generates two plots in a single axis. One plot is for ID 1
                    and another plot is for ID 2.
                Types: teradataml GeoDataFrame Column.

            style:
                Optional Argument.
                Specifies the color for the plot.
                Note:
                    Hexadecimal color codes are not supported.
                Permitted Values:
                    * 'blue'
                    * 'orange'
                    * 'green'
                    * 'red'
                    * 'purple'
                    * 'brown'
                    * 'pink'
                    * 'gray'
                    * 'olive'
                    * 'cyan'
                    * Apart from above mentioned colors, the colors mentioned in
                      https://xkcd.com/color/rgb are also supported.
                Default Value: 'blue'
                Types: str

            title:
                Optional Argument.
                Specifies the title for the Axis.
                Types: str

            xlabel:
                Optional Argument.
                Specifies the label for x-axis.
                Notes:
                     * When set to empty string, label is not displayed for x-axis.
                     * When set to None, name of the x-axis column is displayed as
                       label.
                Types: str

            xlim:
                Optional Argument.
                Specifies the range for xtick values.
                Types: tuple

            xtick_format:
                Optional Argument.
                Specifies whether to format tick values for x-axis or not.
                Types: str

            ylabel:
                Optional Argument.
                Specifies the label for y-axis.
                Notes:
                     * When set to empty string, label is not displayed for y-axis.
                     * When set to None, name of the y-axis column(s) is displayed as
                       label.
                Types: str

            ylim:
                Optional Argument.
                Specifies the range for ytick values.
                Types: tuple

            ytick_format:
                Optional Argument.
                Specifies whether to format tick values for y-axis or not.
                Types: str

            vmin:
                Optional Argument.
                Specifies the lower range of the color map. By default, the range
                is derived from data and color codes are assigned accordingly.
                Note:
                    "vmin" Significant only for Geometry Plot.
                Types: int OR float

            vmax:
                Optional Argument.
                Specifies the upper range of the color map. By default, the range is
                derived from data and color codes are assigned accordingly.
                Note:
                    "vmax" Significant only for Geometry Plot.
                For example:
                    Assuming user wants to use colormap 'matter' and derive the colors for
                    values which are in between 1 and 100.
                    Note:
                        colormap 'matter' starts with Pale Yellow and ends with Violet.
                    * If "colormap_range" is not specified, then range is derived from
                      existing values. Thus, colors are represented as below in the whole range:
                      * 1 as Pale Yellow.
                      * 100 as Violet.
                    * If "colormap_range" is specified as -100 and 100, the value 1 is at middle of
                      the specified range. Thus, colors are represented as below in the whole range:
                      * -100 as Pale Yellow.
                      * 1 as Orange.
                      * 100 as Violet.
                Types: int OR float

            wiggle_fill:
                Optional Argument.
                Specifies whether to fill the wiggle area or not. By default, the right
                positive half of the wiggle is not filled. If specified as True, wiggle
                area is filled.
                Note:
                    Applicable only for the wiggle plot.
                Default Value: False
                Types: bool

            wiggle_scale:
                Optional Argument.
                Specifies the scale of the wiggle. By default, the amplitude of wiggle is scaled
                relative to RMS of the first payload.  In certain cases, it can lead to excessively
                large wiggles. Use "wiggle_scale" to adjust the relative size of the wiggle.
                Note:
                    Applicable only for the wiggle and mesh plots.
                Types: bool

        RAISES:
            TeradataMlException

        EXAMPLES:
            # TODO: To be done with ELE-5842.
        """
        if kind == "geometry":
            # x is not really required for geometry plot. So, users can pass a None here.
            # However, UAF needs all the records to be a Non NULL value. So, construct x with
            # a dummy value.
            x = x if x is not None else 1
            y = UtilFuncs._as_list(y)

            # For geometry plot, x axis is not significant really.
            # They do not mean any thing.
            kwargs["xlabel"] = ""
            kwargs["xtick_values_format"] = ""

            # Geometry plot always need a tuple. Second
            # element should be a Geometry column. If user does not
            # specify a tuple, convert it to tuple by using default geometry column.
            # use "geometry" API.
            _get_y_axis = lambda x: x if isinstance(x, tuple) else (x, self.geometry)
            y = [_get_y_axis(arg) for arg in y]

        plot = _Plot(x=x, y=y, kind=kind, **kwargs)
        return plot

    def __getattr__(self, name):
        """
        Returns an attribute of the GeoDataFrame.

        PARAMETERS:
            name:
                Required Argument.
                Specifies the name of the attribute.
                Types: str

        RETURNS:
            Return the value of the named attribute of object (if found).

        EXAMPLES:
            df = GeoDataFrame('table')

            # You can access a column from the teradataml GeoDataFrame.
            df.c1

        RAISES:
            Attribute Error when the named attribute is not found.
        """

        # Look in the underlying _MetaExpression for columns
        for col in self._metaexpr.c:
            if col.name == name:
                col._parent_df = self
                return col

        # If "name" is present in any of the following 'GeospatialConstants'
        #   1. GeospatialConstants.PROPERTY_TO_NO_ARG_SQL_FUNCTION_NAME
        #   2. GeospatialConstants.METHOD_TO_ARG_ACCEPTING_SQL_FUNCTION_NAME
        #   3. GeospatialConstants.METHOD_TO_NO_ARG_SQL_FUNCTION_NAME
        # that means, it's a function that operates on Geometry Data.
        #
        # Look for such function names.
        if name in GeospatialConstants.PROPERTY_TO_NO_ARG_SQL_FUNCTION_NAME.value:
            # Geospatial functions which are exposed as property of teradataml
            # GeoDataFrame.
            return self.__process_geometry(func_name=name, all_geom=False,
                                           property=True)

        if name in GeospatialConstants.METHOD_TO_ARG_ACCEPTING_SQL_FUNCTION_NAME.value \
                or name in GeospatialConstants.METHOD_TO_NO_ARG_SQL_FUNCTION_NAME.value:
            # Geospatial functions which are exposed as method of teradataml
            # GeoDataFrame.
            return lambda *args, **kwargs: \
                self.__process_geometry(name, *args, **kwargs)

        # TODO - Raise error or Keep it open ended to accept SQL Function names.
        raise AttributeError("'GeoDataFrame' object has no attribute %s" % name)

    def __process_geometry(self, func_name, *args, **kwargs):
        """
        Function helps to execute the Geospatial function on the column(s)
        containing geometry data.

        PARAMETERS:
            func_name:
                Required Argument.
                Specifies the name of the function to execute.
                Types: string

            all_geom:
                Optional Argument.
                Specifies whether to execute the function on all geometry
                columns in the GeoDataFrame or not.
                When set to 'True', geospatial function specified in
                "func_name", is executed on all the columns containing
                geometry data, i.e., geospatial data.
                When set to 'False', geospatial function specified in
                "func_name", is executed only on the column represented
                by the 'GeoDataFrame.geometry' property.
                Default Value: False
                Types: bool

            property:
                Optional Argument.
                Specifies whether the function being executed should be treated
                as GeoDataFrame property or not.
                When set to 'True', geospatial function specified in
                "func_name", is treated as property, otherwise treated as
                method.
                Default Value: False
                Types: bool

            *args:
                Positional arguments passed to the method, i.e., geospatial
                function.

            **kwargs:
                Keyword arguments passed to the method, i.e., geospatial
                function.

        RETURNS:
            DataFrame or GeoDataFrame

        RAISES:
            None.

        EXAMPLES:
            self.__process_geometry(fname, all_geom, False, *c, **kwargs)
        """
        property = kwargs.pop("property", False)
        all_geom = kwargs.pop("all_geom", False)
        assign_args = {}
        if not all_geom:
            # Function will be run only on column represented by
            # 'GeoDataFrame.geometry' property.
            new_col = "{}_{}_geom".format(func_name, self.geometry.name)
            if property:
                # If property is set to True, then no need to pass **kwargs and
                # no need to invoke the call with parenthesis '()'.
                assign_args[new_col] = self.geometry[func_name]
            else:
                # Pass *args and **kwargs as function accepts arguments.
                assign_args[new_col] = self.geometry[func_name](*args, **kwargs)
        else:
            # Function will be run on all column(s) containing geometry data.
            # Columns containing geometry data can be following types:
            #   1. ST_GEOMETRY
            #   2. MBR
            #   3. MBB
            for col in self._metaexpr.c:
                if col.type in [GEOMETRY, MBR, MBB]:
                    new_col = "{}_{}".format(func_name, col.name)
                    if property:
                        # If property is set to True, then no need to pass
                        # **kwargs and no need to invoke the call with
                        # parenthesis '()'.
                        assign_args[new_col] = self[col.name][func_name]
                    else:
                        # Pass *args and **kwargs as function accepts arguments.
                        assign_args[new_col] = self[col.name][func_name](*args,
                                                                         **kwargs)

        return self.assign(**assign_args)

    @property
    def geometry(self):
        """
        DESCRIPTION:
            Returns a GeoColumnExpression for a column containing geometry data.
            If GeoDataFrame contains, multiple columns containing geometry data,
            then it returns reference to only one of them.
            Columns containing geometry data can be of following types:
                1. ST_GEOMETRY
                2. MBB
                3. MBR
            Refer 'GeoDataFrame.tdtypes' to view the Teradata column data types.

            Note:
                This property is used to execute any geospatial operation on
                GeoDataFrame, i.e., any geospatial function executed on
                GeoDataFrame, is executed on the geomtry column referenced by
                this property.

        RETURNS:
            GeoDataFrameColumn

        EXAMPLES:
            >>> load_example_data("geodataframe", ["sample_cities", "sample_streets"])
            >>> cities = GeoDataFrame("sample_cities")
            >>> streets = GeoDataFrame("sample_streets")
            >>> city_streets = cities.join(streets, how="cross", lsuffix="l", rsuffix="r")
            >>> city_streets
               l_skey  r_skey   city_name                                 city_shape  street_name              street_shape
            0       0       1  Oceanville            POLYGON ((1 1,1 3,6 3,6 0,1 1))  Main Street  LINESTRING (2 2,3 2,4 1)
            1       0       1  Oceanville            POLYGON ((1 1,1 3,6 3,6 0,1 1))   Coast Blvd  LINESTRING (12 12,18 17)
            2       1       1     Seaside  POLYGON ((10 10,10 20,20 20,20 15,10 10))   Coast Blvd  LINESTRING (12 12,18 17)
            3       1       1     Seaside  POLYGON ((10 10,10 20,20 20,20 15,10 10))  Main Street  LINESTRING (2 2,3 2,4 1)
            >>>

            # Check the name of the column containing geometry data, where
            # 'geometry' property references.
            >>> city_streets.geometry.name
            'city_shape'
            >>>

            # Check all the column types.
            >>> city_streets.tdtypes
            l_skey                                    INTEGER()
            r_skey                                    INTEGER()
            city_name       VARCHAR(length=40, charset='LATIN')
            city_shape                               GEOMETRY()
            street_name     VARCHAR(length=40, charset='LATIN')
            street_shape                             GEOMETRY()
            >>>
            >>>

            # Set the 'geometry' property to refer 'street_shape' column.
            >>> city_streets.geometry = city_streets.street_shape
            >>> city_streets.geometry.name
            'street_shape'
            >>>

            # Check whether the geometry referenced by 'geometry' property are 3D
            # or not.
            >>> city_streets.is_3D
               l_skey  r_skey   city_name                                 city_shape  street_name              street_shape  is_3D_street_shape_geom
            0       1       1     Seaside  POLYGON ((10 10,10 20,20 20,20 15,10 10))  Main Street  LINESTRING (2 2,3 2,4 1)                        0
            1       1       1     Seaside  POLYGON ((10 10,10 20,20 20,20 15,10 10))   Coast Blvd  LINESTRING (12 12,18 17)                        0
            2       0       1  Oceanville            POLYGON ((1 1,1 3,6 3,6 0,1 1))   Coast Blvd  LINESTRING (12 12,18 17)                        0
            3       0       1  Oceanville            POLYGON ((1 1,1 3,6 3,6 0,1 1))  Main Street  LINESTRING (2 2,3 2,4 1)                        0
            >>>

            # Use the geometry property to execute multiple geospatial functions
            # in conjunctions with GeoDataFrame.assign()
            # Get the geometry type.
            >>> geom_type = city_streets.geometry.geom_type
            # Check if geometry is simple or not.
            >>> is_simple = city_streets.geometry.is_simple
            # Check if geometry is valid or not.
            >>> is_valid = city_streets.geometry.is_valid
            >>>
            # Call GeoDataFrame.assign() and pass the above GeoDataFrameColumn, i.e.,
            # ColumnExpressions as input.
            >>> city_streets.assign(geom_type = geom_type,
            ...                     is_simple = is_simple,
            ...                     is_valid = is_valid
            ...                     )
               l_skey  r_skey   city_name                                 city_shape  street_name              street_shape      geom_type  is_simple  is_valid
            0       0       1  Oceanville            POLYGON ((1 1,1 3,6 3,6 0,1 1))  Main Street  LINESTRING (2 2,3 2,4 1)  ST_LineString          1         1
            1       0       1  Oceanville            POLYGON ((1 1,1 3,6 3,6 0,1 1))   Coast Blvd  LINESTRING (12 12,18 17)  ST_LineString          1         1
            2       1       1     Seaside  POLYGON ((10 10,10 20,20 20,20 15,10 10))   Coast Blvd  LINESTRING (12 12,18 17)  ST_LineString          1         1
            3       1       1     Seaside  POLYGON ((10 10,10 20,20 20,20 15,10 10))  Main Street  LINESTRING (2 2,3 2,4 1)  ST_LineString          1         1
            >>>
        """
        # Check if attribute __geom_column is already set or not.
        if self.__geom_column is not None:
            return self.__geom_column
        else:
            # No geom column identified, iterate over the columns
            # and set the attribute and return the same.
            for col in self._metaexpr.c:
                if isinstance(col.type, (GEOMETRY, MBR, MBB)):
                    self.__geom_column = col
                    return col

    @geometry.setter
    def geometry(self, column):
        """
        DESCRIPTION:
            Sets the geometry property to new geometry column.

        PARAMETERS:
            column:
                Required Argument.
                Specifies the column used for setting the 'geometry'
                property. Column passed to the function must contain the
                geometry data, i.e., column should be of type GEOMETRY, MBR,
                or MBB.
                Types: str or GeoDataFrameColumn

        RAISES:
            TeradataMlException

        EXAMPLES:
            # Set the property by passing the column name.
            df.geometry = "geom_column"

            # Set the property by passing the GeoDataFrameColumn.
            df.geometry = df.geom_column
        """
        awu_matrix = []
        awu_matrix.append(["column", column, False, (str, GeoDataFrameColumn),
                           True])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        if isinstance(column, str):
            column = getattr(self, column)

        supported_types = (GEOMETRY, MBR, MBB)
        if not isinstance(column.type, supported_types):
            err_fmt = Messages.get_message(MessageCodes.INVALID_COLUMN_DATATYPE)
            err_ = err_fmt.format(column.name, "column", "Supported",
                                  supported_types)
            raise TeradataMlException(err_, MessageCodes.INVALID_COLUMN_DATATYPE)

        self.__geom_column = column

    def _create_dataframe_from_node(self, nodeid, metaexpr, index_label, undropped_columns=None):
        """
        DESCRIPTION:
            This function overrides the parent method, that creates the
            dataframe from node, i.e., using '_Parent_from_node' function.

            Parent class always returns a teradataml DataFrame, but for
            GeoDataFrame, we will return teradataml DataFrame or teradataml
            GeoDataFrame, based on whether the resultant DataFrame contains
            geometry column or not.

        PARAMETERS:
            nodeid:
                Required Argument.
                Specifies the nodeid for the DataFrame or GeoDataFrame.
                Types: str

            metaexpr:
                Required Argument.
                Specifies the metadata for the resultant object.
                Types: _MetaExpression

            index_label:
                Required Argument.
                Specifies list specifying index column(s) for the DataFrame.
                Types: str OR list of Strings (str)

            undropped_columns:
                Optional Argument.
                Specifies list of index column(s) to be retained as columns for printing.
                Types: list

        RETURNS:
            teradataml DataFrame or teradataml GeoDataFrame

        RAISES:
            None

        EXAMPLES:
            self._create_dataframe_from_node(new_nodeid, new_meta,
                                             self._index_label, undropped_columns)
        """
        # TODO: <DEPENDENT_ON_GEOMETRY_DATATYPES_SUPPORT_IN_teradatasqlalchemy>
        #   1. Add the test cases.
        #       a. Run teradataml DataFrame functions, that will result in
        #           dropping the geometry datatype columns.
        #       b. Run GeoDataFrame.assign() with "drop_columns=True" and
        #           run geospatial function on a column, a function that will
        #           not return the Geometry data type column.
        #       All other cases, this should return the object of this class.
        if not self._check_geom_column(metaexpr):
            # If generated metaexpr does not contain a geometry column
            # then we should return the teradataml DataFrame.
            return DataFrame._from_node(nodeid, metaexpr, index_label, undropped_columns)
        else:
            # Return the teradataml GeoDataFrame.
            return self._from_node(nodeid, metaexpr, index_label, undropped_columns)

    def _get_metadata_from_metaexpr(self, metaexpr):
        """
        Private method for setting _metaexpr and retrieving column names and types.

        PARAMETERS:
            metaexpr - Parent meta data (_MetaExpression object).

        RETURNS:
            None

        RAISES:
            None

        EXAMPLE:
            self._get_metadata_from_metaexpr(metaexpr)
        """
        self._metaexpr = self._generate_child_metaexpr(metaexpr)
        self._column_names_and_types = []
        self._td_column_names_and_types = []
        self._td_column_names_and_sqlalchemy_types = {}
        for col in self._metaexpr.c:
            if isinstance(col.type, sqlalchemy.sql.sqltypes.NullType):
                tdtype = TeradataTypes.TD_NULL_TYPE.value
            else:
                tdtype = "{}".format(col.type)

            self._column_names_and_types.append((str(col.name), UtilFuncs._teradata_type_to_python_type(col.type)))
            self._td_column_names_and_types.append((str(col.name), tdtype))
            self._td_column_names_and_sqlalchemy_types[(str(col.name)).lower()] = col.type

            # Set the Geometry column, which will be used as "geometry"
            # property.
            if self.__geom_column is None and \
                    isinstance(col.type, (GEOMETRY, MBR, MBB)):
                self.__geom_column = col

        if self.__geom_column is None:
            error_code = MessageCodes.NO_GEOM_COLUMN_EXIST
            raise TeradataMlException(Messages.get_message(error_code), error_code)


    def _generate_child_metaexpr(self, metaexpr):
        """
        Internal function that generates the metaexpression by converting
        _SQLColumnExpression to GeoDataFrameColumn.

        PARAMETERS:
            metaexpr:
                Required Arguments.
                Specifies the metaexpression to update.
                Types: _MetaExpression

        RETURNS:
            _MetaExpression

        RAISES:
            None.

        EXAMPLES:
            self._metaexpr = self._generate_child_metaexpr(metaexpr)
        """
        metaexpr.c = [GeoDataFrameColumn(col.expression)
                      if not isinstance(col, GeoDataFrameColumn) else col
                      for col in metaexpr.c]
        return metaexpr


