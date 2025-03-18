import streamlit as st
import pandas as pd
from logic_diagram import create_logic_diagram
import json
import os

# st.logo("resources/MECC.jpg")

st.title("Toy MECC :material/smart_toy:")
st.write("## _Making Every Contact Count_")
# st.image("./resources/MECC.jpg", width=250)

st.write("""
A (toy) model for showing the benefit of Making Every Contact Count (MECC) Training.
        
This app was built as part of the [HSMA](https://hsma-programme.github.io/hsma_site/) 6 Hackday 2024 and 
the source code is available on [GitHub](https://github.com/DomRowney/Project_Toy_MECC.git)
""")

st.write("#### Explanation")
st.write("""
The model is an Agent based simulation:
+ There is an initial group of people (agents) and an initial group of services.
+ People have contact with government services at random with a certain probability
+ People in contact with services have a chance of having a Very Brief Intervention.        
+ Services can have MECC training, which increases the a probability that
          any contact will lead to a Very Brief Intervention.
+ The model compares results for the same simultion with and without MECC training.

_A specific smoking cessation model has additional rules:_
+ A certain proportion of people have lifestyle factors: smoking.
        People cannot start smoking if they never had to start with.
+ People may have a probability of making a smoking quit attempt each month
+ People have a chance of restarting smoking,
          this chance decreases the longer a person is smoke free.         
+ A Very Brief Intervention increases the probability that a person will make a quit attempt.
         It does not effect the chance that a person will stay smoke free.

There is a [Monte Carlo method](https://en.wikipedia.org/wiki/Monte_Carlo_method) version of the simple model.
The simulations contain randomness so this method reruns the simulation multiple times to get average results.

**You can change all these probabilites on the:**""") 
st.page_link('./parameters.py',label='Parameters for Simulation')

st.write("----") # divider
st.write("#### Diagram of Agent Model Logic")
st.write("This diagram shows how a a person agent moves through the system")

st.image(create_logic_diagram()
         , caption="Diagram of Agent Model Logic"
         , use_column_width=False)

################################################################################

# initailise parameter variables for simulation - defaults
if 'N_people' not in st.session_state:
    st.session_state.N_people = 50

if 'initial_smoking_prob' not in st.session_state:
    st.session_state.initial_smoking_prob = 0.5

if 'visit_prob' not in st.session_state:
    st.session_state.visit_prob = 0.1

if 'quit_attempt_prob' not in st.session_state:
    st.session_state.quit_attempt_prob = 0.01

if 'base_smoke_relapse_prob' not in st.session_state:
    st.session_state.base_smoke_relapse_prob = 0.01

if 'base_make_intervention_prob' not in st.session_state:
    st.session_state.base_make_intervention_prob = 0.1

if 'mecc_effect' not in st.session_state:
    st.session_state.mecc_effect = 0.9

if 'intervention_effect' not in st.session_state:
    st.session_state.intervention_effect = 1.1

if 'model_seed' not in st.session_state:
    st.session_state.model_seed = 42

if 'num_steps' not in st.session_state:
    st.session_state.num_steps = 24

if 'animation_speed' not in st.session_state:
    st.session_state.animation_speed = 0.1

## monte carlo parameters
if 'iterations' not in st.session_state:
    st.session_state.iterations = 100

## alcohol specific parameters
if 'alcohol_prob_receptive' not in st.session_state:
    st.session_state.alcohol_prob_receptive = 0.75

if 'alcohol_change_prob_contemplation' not in st.session_state:
    st.session_state.alcohol_change_prob_contemplation = 0.01

if 'alcohol_change_prob_preparation' not in st.session_state:
    st.session_state.alcohol_change_prob_preparation = 0.01

if 'alcohol_change_prob_action' not in st.session_state:
    st.session_state.alcohol_change_prob_action = 0.01

if 'alcohol_lapse_prob_precontemplation' not in st.session_state:
    st.session_state.alcohol_lapse_prob_precontemplation = 0.01

if 'alcohol_lapse_prob_contemplation' not in st.session_state:
    st.session_state.alcohol_lapse_prob_contemplation = 0.01

if 'alcohol_lapse_prob_preparation' not in st.session_state:
    st.session_state.alcohol_lapse_prob_preparation = 0.01

if 'alcohol_golden_window' not in st.session_state:
    st.session_state.alcohol_golden_window = 3

if 'alcohol_services_table' not in st.session_state:
    ## sets a dataframe up one row for each service type
    alcohol_services = pd.DataFrame(
            {'Service': ['Job Centre','Benefits Office','Housing Officer','Community Hub','Pharmacy','GP Practice']
            ,'Person Visit Probability': [0.20,0.20,0.20,0.20,0.1,0.1]
            ,'Chance a Brief Intervention Made Without MECC Training': [0.01,0.01,0.01,0.01,0.10,0.10]
            ,'MECC Trained': [True,True,True,True,False,False]
            ,'Chance Making a Brief Intervention After MECC Training': [0.90,0.90,0.90,0.90,0.90,0.90]
            ,'Post Intervention Pre-Contemplation to Contemplation chance': [0.50,0.50,0.50,0.50,0.50,0.50]
            ,'Post Intervention Contemplation to Preparation chance': [0.50,0.50,0.50,0.50,0.50,0.50]
            ,'Post Intervention Preparation to Action chance': [0.50,0.50,0.50,0.50,0.50,0.50]}
    )
    ## Sets service as index
    alcohol_services = alcohol_services.set_index('Service')    
    st.session_state.alcohol_services_table = alcohol_services.copy()

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
