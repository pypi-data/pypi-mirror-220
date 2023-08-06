import os
import streamlit.components.v1 as components
from typing import List, Dict

_RELEASE = False

if not _RELEASE:
    _component_func = components.declare_component(
        "st_selection_header",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("st_selection_header", path=build_dir)


def st_selection_header(date, key=None):
    component_value = _component_func(date=date, key=key, default=0)
    return component_value

if not _RELEASE:
    import streamlit as st
    st.set_page_config(layout="wide")
    date = "2023-07-21 00:00:00"
    data = st_selection_header("2023-07-21 00:00:00", key=date)
    print(type(data), data)
    
