import streamlit as st
import os
import subprocess
import platform

@st.cache_data
def get_quarto(quarto_version="1.5.57"):
    print(f"Output of platform.processor(): {platform.processor()}")
    print(f"type:  {type(platform.processor())}")
    print("Attempting to download Quarto")
    # Download Quarto
    os.system(f"wget https://github.com/quarto-dev/quarto-cli/releases/download/v{quarto_version}/quarto-{quarto_version}-linux-amd64.tar.gz")

    # Create directory and extract Quarto
    os.system(f"tar -xvzf quarto-{quarto_version}-linux-amd64.tar.gz")
    # Check the contents of the folder we are in
    os.system("pwd")

    # # Ensure PATH is updated in the current Python process
    # # os.environ['QUARTO_PATH'] = f"{f'/mount/src/project_toy_mecc/quarto-{quarto_version}/bin/quarto'}"
    # quarto_dir = f'/mount/src/project_toy_mecc/quarto-{quarto_version}/bin/quarto'
    # os.environ['PATH'] = f"{quarto_dir}:{os.environ['PATH']}"

    # print("Trying to run 'quarto check' command")
    # try:
    #     result = subprocess.run(['quarto', 'check'], capture_output=True, text=True, shell=True)
    #     print(result.stdout)
    #     print(result.stderr)
    #     print("Quarto check run")
    # except PermissionError:
    #     print("Permission error encountered when running 'quarto check'")

st.set_page_config(layout="wide")

# If running on community cloud, output of this is an empty string
# If this is the case, we'll try to install quarto
if platform.processor() == '':
    get_quarto()

pg = st.navigation(

    [st.Page("homepage.py",
             title="Hackathon Details",
             icon=":material/cottage:"),
    st.Page("parameters.py",
             title="Parameters for Simulation",
             icon=":material/settings:"),
    st.Page("mesa_abs_two_types_mecc.py",
             title="Smoking cessation with MECC",
             icon=":material/people:")
     ]
     )

pg.run()
