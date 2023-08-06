"""Defines the container that takes user inputs for the exploration of variables."""
import pathlib
from typing import Optional, Union

import streamlit as st
from pydantic import BaseModel  # pylint: disable=no-name-in-module


class UserInputs(BaseModel):
    """Class containing the user inputs for the exploration of variables."""

    plot_type: Optional[str] = None
    selected_col: str
    button_activator: bool
    selected_y: Optional[str] = None
    selected_color: Optional[str] = None
    selected_histfunc: Optional[str] = None
    selected_nbins: Optional[int] = None
    selected_marginal: Optional[str] = None
    selected_points: Optional[Union[str, bool]] = None
    selected_log_x: Optional[bool] = None
    selected_log_y: Optional[bool] = None
    selected_orientation: Optional[str] = None


class Plot:
    """Base class for the different plot types, their settings and their corresponding streamlit selectors."""

    def __init__(self, columns: list, key: str):
        """Construct Plot object."""
        self.y_axis = st.selectbox("Select a y-axis", options=[None] + columns, key=f"abscissa_col_{key}")
        self.color = st.selectbox("Select a color field", options=[None] + columns, key=f"color_col_{key}")
        self.log_x = st.selectbox(
            "Activate log scaling for the x-axis",
            options=[False, True],
            key=f"log_x_{key}",
        )
        self.log_y = st.selectbox(
            "Activate log scaling for the y-axis",
            options=[False, True],
            key=f"log_y_{key}",
        )
        self.orientation = st.selectbox(
            "Choose the orientation:",
            options=[None, "h", "v"],
            key=f"orientation_{key}",
        )


class Histogram(Plot):
    """Class containing the settings for the histogram plot."""

    def __init__(self, columns: list, key: str):
        """Construct the histogram plot settings."""
        super().__init__(columns, key)
        self.histfunc = st.selectbox(
            "Select an aggregation function",
            options=["avg", "count", "sum", "min", "max"],
            key=f"histfunc_{key}",
        )
        self.nbins = st.selectbox(
            "Select the number of bins",
            options=[None, 3, 5, 10, 20],
            key=f"nbins_{key}",
        )
        self.marginal = st.selectbox(
            "Select a marginal",
            options=[None, "rug", "box", "violin", "histogram"],
            key=f"marginal_{key}",
        )


def user_input_container(file_path: pathlib.Path, tab_key: str, columns: list[str]) -> UserInputs:
    """Container for user inputs."""
    # pylint: disable=too-many-locals
    dvc_step = file_path.parts[-1]
    selected_histfunc = None
    selected_nbins = None
    selected_marginal = None
    selected_y = None
    selected_color = None
    selected_points = None
    selected_log_x = None
    selected_log_y = None
    selected_orientation = None

    key = f"{tab_key}_{dvc_step}"
    selected_col = st.selectbox(
        "Select a column to inspect (x-axis)",
        options=sorted(columns),
        key=f"col_inspect_{key}",
    )
    plot_type = st.selectbox(
        "Select the type of plot you want to use",
        options=[None, "histogram", "box"],
        key=f"plot_type_{key}",
    )
    if plot_type:
        plot = Plot(columns=columns, key=key)
        selected_y = plot.y_axis
        selected_color = plot.color
        selected_log_x = plot.log_x
        selected_log_y = plot.log_y
        selected_orientation = plot.orientation
    if plot_type == "box":
        selected_points = st.selectbox(
            "Select how to display outliers",
            options=[
                None,
                "outliers",
                "suspectedoutliers",
                "all",
                False,
            ],
        )
    if plot_type == "histogram":
        selected_histfunc = st.selectbox(
            "Select an aggregation function",
            options=["avg", "count", "sum", "min", "max"],
            key=f"histfunc_{key}",
        )
        selected_nbins = st.selectbox(
            "Select the number of bins",
            options=[None, 3, 5, 10, 20],
            key=f"nbins_{key}",
        )
        selected_marginal = st.selectbox(
            "Select a marginal",
            options=[None, "rug", "box", "violin", "histogram"],
            key=f"marginal_{key}",
        )

    button_activator = st.button(
        "Inspect",
        key=f"button_activator_{key}",
    )
    return UserInputs(
        plot_type=plot_type,
        selected_col=selected_col,
        button_activator=button_activator,
        selected_y=selected_y,
        selected_color=selected_color,
        selected_histfunc=selected_histfunc,
        selected_nbins=selected_nbins,
        selected_marginal=selected_marginal,
        selected_points=selected_points,
        selected_log_x=selected_log_x,
        selected_log_y=selected_log_y,
        selected_orientation=selected_orientation,
    )
