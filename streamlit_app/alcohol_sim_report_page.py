import streamlit as st
import pandas as pd
from alcohol_parameters import init_parameters
import json
import os
import subprocess

st.title("Download Alcohol Simulation Results Report")

st.write("""
Download the most recent simulation results as an HTML report.
You can convert the downloaded file to PDF if needed.
""")

if "download_clicked" not in st.session_state:
    st.session_state.download_clicked = False
    
if "simulation_completed" not in st.session_state:
    st.session_state.simulation_completed = False

if not st.session_state.simulation_completed:
    st.info("The generate report button will only appear once a simulation has been successfully run.")

## checkbox options - currently not being utilised.
st.subheader("Select Report Sections:")
incl_charts = st.checkbox("Include Charts Section", value=True)
incl_final_stats = st.checkbox("Include Final Statistics Section", value=True)
incl_sim_param = st.checkbox("Include Simulation Parameters Section", value=True)
incl_ld = st.checkbox("Include Logic Diagram", value=True)
       
        
if st.session_state.simulation_completed:
     if st.button("Generate Report"):
        report_message = st.empty()
        report_message.info(f"Generaing Report for Download...")
        
        model_parameters = {
            "model_seed": st.session_state.model_seed,
            "N_people": st.session_state.N_people,
            "N_service": 1,
            "initial_smoking_prob": st.session_state.initial_smoking_prob,
            "visit_prob": st.session_state.visit_prob,
            "quit_attempt_prob": st.session_state.quit_attempt_prob,
            "base_smoke_relapse_prob": st.session_state.base_smoke_relapse_prob,
            "base_make_intervention_prob": st.session_state.base_make_intervention_prob,
            "mecc_effect": st.session_state.mecc_effect,
            "intervention_effect": st.session_state.intervention_effect,
            "num_steps" : st.session_state.num_steps,
            "animation_speed" : st.session_state.animation_speed,
            "iterations":st.session_state.iterations,
            ## alcohol specific parameters
            "prob_receptive": st.session_state.alcohol_prob_receptive,
            "change_prob_contemplation": st.session_state.alcohol_change_prob_contemplation,
            "change_prob_preparation":st.session_state.alcohol_change_prob_preparation,
            "change_prob_action": st.session_state.alcohol_change_prob_action,
            "lapse_prob_precontemplation": st.session_state.alcohol_lapse_prob_precontemplation,
            "lapse_prob_contemplation": st.session_state.alcohol_lapse_prob_contemplation,
            "lapse_prob_preparation": st.session_state.alcohol_lapse_prob_preparation,
            "golden_window": st.session_state.alcohol_golden_window,
            "contemplation_intervention": st.session_state.alcohol_services_table['Post Intervention Pre-Contemplation to Contemplation chance'].to_dict(),
            "preparation_intervention": st.session_state.alcohol_services_table['Post Intervention Contemplation to Preparation chance'].to_dict(),
            "action_intervention": st.session_state.alcohol_services_table['Post Intervention Preparation to Action chance'].to_dict(),
        }

        ## save to json file to be used later for the quarto report
        output_path = os.path.join(os.getcwd(),'streamlit_app','outputs')
        json_path = os.path.join(output_path,'session_data.json')

        with open(json_path, "w") as f:
            json.dump(model_parameters, f, indent=4)
            
        ## filepaths
        output_dir = os.path.join(os.getcwd(),'streamlit_app','downloads')
        qmd_filename = 'alcohol_sim_report.qmd'
        qmd_path = os.path.join(os.getcwd(),'streamlit_app',qmd_filename)
        html_filename = os.path.basename(qmd_filename).replace('.qmd', '.html')
        dest_html_path = os.path.join(output_dir,html_filename)

        try:
            ## forces result to be html
            result = subprocess.run(["quarto"
                                    , "render"
                                    , qmd_path
                                    , "--to"
                                    , "html"
                                    , "--output-dir"
                                    , output_dir]
                                    , capture_output=True
                                    , text=True)
            if os.path.exists(dest_html_path):
                with open(dest_html_path, "r") as f:
                    html_data = f.read()

                report_message.success("Report ready for download!")
                st.download_button(
                    label="Download Report",
                    data=html_data,
                    file_name=html_filename,
                    mime="text/html",
                    on_click=lambda: st.session_state.update({
                        "download_clicked": False,
                        "simulation_completed": False
                    })
                )
                # st.balloons()
            else:
                report_message.error("Report failed to generate.")
                st.code(result.stderr or "No error message available.")

        except Exception as e:
            report_message.error("Report generation error:")
            st.exception(e)