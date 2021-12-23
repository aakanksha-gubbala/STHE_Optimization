import streamlit as st
import numpy as np
import lxml
import ref
# import STHE_BD

np.seterr(divide='ignore', invalid='ignore')

PAGES = {"Home": ref}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Home"])

with st.spinner(f'Loading {selection} ...'):
    PAGES[selection].main()

st.sidebar.title("About")
st.sidebar.info("Heat exchanger design & optimization")
st.sidebar.info("Heat transfer calculations by Bell-Delaware Method")
st.sidebar.info("""Here's the [link](https://github.com/aakanksha-gubbala/) to the source code""")

