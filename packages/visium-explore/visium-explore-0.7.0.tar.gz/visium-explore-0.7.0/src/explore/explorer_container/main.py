"""The explorer container allows the user to interact with the chosen data by selecting columns to explore and plot."""
import pathlib

import pandas as pd
import streamlit as st

from src.explore.explorer_container.exploration_container import exploration_container
from src.explore.explorer_container.user_input_container import user_input_container


def explorer_container(file_path: pathlib.Path, tab_key: str, sample_df: pd.DataFrame) -> None:
    """Display the explorer container.

    It allows the user to interact with the chosen data by selecting columns to explore and plot.
    """
    file_path = pathlib.Path(file_path)

    col1, col2 = st.columns([1, 3])
    with col1:
        user_inputs = user_input_container(file_path=file_path, tab_key=tab_key, columns=list(sample_df.columns))

    with col2:
        exploration_container(file_path, user_inputs=user_inputs)
