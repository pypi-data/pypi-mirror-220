from pathlib import Path
from typing import Optional

import streamlit as st
import streamlit.components.v1 as components

# Tell streamlit that there is a component called st_picture_carousel,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component(
    "st_picture_carousel", path=str(frontend_dir)
)

# Create the python function that will be called
def st_picture_carousel(
        n_pics: Optional[int] = 7,
        key: Optional[str] = None,
):
    """
    Add a descriptive docstring
    """
    component_value = _component_func(
        n_pics=n_pics,
        key=key,
    )

    return component_value


def main():
    st.subheader("Example [st.header]")
    value = st_picture_carousel(15)
    value = st_picture_carousel(7)

if __name__ == "__main__":
    main()
