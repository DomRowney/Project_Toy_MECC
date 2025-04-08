## alcohol_homepage.py
import streamlit as st
import pandas as pd
from alcohol_parameters import init_parameters
import json
import os

# st.logo("resources/MECC.jpg")

st.title("Toy MECC :material/smart_toy:")
st.write("## _Making Every Contact Count_")
# st.image("./resources/MECC.jpg", width=250)

st.write("""
A (toy) model for showing the benefit of Making Every Contact Count (MECC) Training.
For the case of using a brief intervention in alcohol harm reduction
        
This app was built as part of the [HSMA](https://hsma-programme.github.io/hsma_site/) 6 Hackday 2024 and 
the source code is available on [GitHub](https://github.com/DomRowney/Project_Toy_MECC.git).
         
It is part of an evaluation of [MECC](https://www.meccgateway.co.uk/nenc).
""")

st.write("#### Explanation")
st.write("""
The model is an Agent based simulation:
+ There is an initial group of people (agents) and an initial group of services.
+ The model is run for a number of repeating periods
+ Each period people can, with a certain probability, have contact with each of the services 
+ People in contact with services have a chance of having a Very Brief Intervention.        
+ Services can have MECC training, which increases the a probability that
          any contact will lead to a Very Brief Intervention.
+ The model compares results for the same simultion with and without MECC training.
""")
         
st.write("""        
People are modelled using the Stages of Change Model, also known as the [Transtheoretical Model](https://doi.org/10.4278/0890-1171-12.1.38):
+ There are four stages modelled: Pre-Contemplation, Contemplation, Preparation, and Action.
+ People have one chance each period of moving between these stages or lapsing back.
+ All people start at Pre-Contemplation.
+ There is a probabilty that people in the Pre-Contemplation stage will be amenable to an Intervention
+ Sucessful Interventions increase the chance that people will improve their stage of change.
""")         

st.write("""
A Golden Window is a period of time after a sucessful intervention:
+ In a Golden Window each subsequent Intervention always succeeds
+ The effect of each Intervention adds to the previous
+ Subsequent interventions do not change the duration of the Golden Window
+ After the Golden Window ends the chances of improvement revert to the original values
""") 

st.write("""**You can change all these probabilites on the:**""") 
st.page_link('./alcohol_parameters.py',label='Parameters for Simulation')



################################################################################

# initailise parameter variables for simulation - defaults
init_parameters()

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

# save to json file to be used later for the quarto report
output_path = os.path.join(os.getcwd(),'streamlit_app','outputs')
json_path = os.path.join(output_path,'session_data.json')

with open(json_path, "w") as f:
    json.dump(model_parameters, f, indent=4)
