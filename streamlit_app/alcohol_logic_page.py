## alcohol_logic_page.py
import streamlit as st
from logic_diagram import create_logic_diagram_Alcohol
from alcohol_parameters import init_parameters

######################################################

# initailise parameter variables for simulation - defaults
init_parameters()

######################################################

st.title("Simulate - Alcohol Advice Model with MECC Training")

# initialise simulation_completed session state
if 'simulation_completed' not in st.session_state:
    st.session_state.simulation_completed = False

######################################################

st.image(create_logic_diagram_Alcohol(number_labels = True)
    , caption="Diagram of Agent Model Logic"
    , use_column_width=False)