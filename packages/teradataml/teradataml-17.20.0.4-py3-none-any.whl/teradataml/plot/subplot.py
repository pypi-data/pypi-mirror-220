# ##################################################################
#
# Copyright 2023 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
#
# Primary Owner: Pradeep Garre (pradeep.garre@teradata.com)
# Secondary Owner:
#
# This file implements subplots function, which is used for sub-plotting.
#
# ##################################################################
from teradataml.plot.figure import Figure
from teradataml.plot.axis import AxesSubplot

def subplots(nrows=None, ncols=None, grid=None):
    """
    DESCRIPTION:
        Function to create a figure and a set of subplots. The function
        makes it convenient to create common layouts of subplots, including
        the enclosing figure object.

    PARAMETERS:
        nrows:
            Required when "grid" is not used, optional otherwise.
            Specifies the number of rows of the subplot grid.
            Notes:
                 * Provide either "grid" argument or "nrows" and "ncols" arguments.
                 * "nrows" and "ncols" are mutually inclusive.
            Types: int

        ncols:
            Optional Argument.
            Specifies the number of columns of the subplot grid.
            Notes:
                 * Provide either "grid" argument or "nrows" and "ncols" arguments.
                 * "nrows" and "ncols" are mutually inclusive.
            Types: int

        grid:
            Required when "nrows" and "ncols" are not used, optional otherwise.
            Specifies grid for subplotting. The argument is useful when one or more
            subplot occupies more than one unit of space in figure.
            For example:
                "grid" {(1,1): (1, 1), (1,2): (1,1), (2, 1): (1, 2)} makes 3 subplots
                in a figure.
                * The first subplot which is positioned at first row and first column
                  occupies one row and one column in the figure.
                * The second subplot which is positioned at first row and second column
                  occupies one row and one column in the figure.
                * The third subplot which is positioned at second row and first column
                  occupies one row and two columns in the figure. Thus, the third subplot
                  occupies the entire second row of subplot.
            Notes:
                 * Provide either "grid" argument or "nrows" and "ncols" arguments.
                 * "nrows" and "ncols" are mutually inclusive.
            Types: dict, both keys and values are tuples.

    RETURNS:
        tuple, with two elements. First element represents the object of Figure and
        second element represents list of objects of AxesSubplot.
        Note:
            The default width and height in figure object is 640 and 480 pixels
            respectively. However, incase of subplotting, the default width of
            width and height is 1920 and 1080 respectively.

    EXAMPLES:
        # TODO: To be added with ELE-5842.

    RAISES:
        TeradataMlException
    """
    # TODO: Either grid or nrows/ncols is mandatory. One can not pass both.
    #  Add validation.
    #  To be added with ELE-5804.

    _sub_axis = []
    # Since it is a subplot, make sure to provide a figure with larger size.
    figure = Figure(width=1920, height=1080)
    # grid is a dictionary, with keys as position and values as span. Both
    # represents tuples.
    if grid is not None:
        _min, _max = 1, 1
        for position, span in grid.items():
            _axis = AxesSubplot(position=position, span=span)
            figure._add_axis(_axis)
            _sub_axis.append(_axis)

            # Layout should be mix/max of position and span elements.
            _min = max(_min, position[0], span[0])
            _max = max(_max, position[1], span[1])

        _layout = (_min, _max)

    else:
        _layout = (nrows, ncols)
        for row in range(1, nrows+1):
            for col in range(1, ncols+1):
                position = (row, col)
                _axis = AxesSubplot(position=(row, col))
                figure._add_axis(_axis)
                _sub_axis.append(_axis)
    figure.layout = _layout
    return figure, _sub_axis
