## alcohol_parameters.py
import pandas as pd
import streamlit as st

#########

def init_parameters():
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

init_parameters()

########


st.title("Parameters")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Population")

    if 'N_people' not in st.session_state:
        st.session_state.N_people = 50
    st.session_state.N_people = st.slider("Number of People", 10, 1000, st.session_state.N_people, step=10)

with col2:
    st.markdown("#### Simulation")

    if 'model_seed' not in st.session_state:
        st.session_state.model_seed = 42
    st.session_state.model_seed = st.number_input("Random Seed", min_value=0, max_value=None, value=st.session_state.model_seed, step=1)

    if 'num_steps' not in st.session_state:
        st.session_state.num_steps = 24
    st.session_state.num_steps = st.slider("Number of Months to Simulate", 1, 120, st.session_state.num_steps)

    if 'animation_speed' not in st.session_state:
        st.session_state.animation_speed = 0.1
    st.session_state.animation_speed = st.slider("Animation Speed (seconds)", 0)

st.markdown("#### Stages of Change")
colA, colB = st.columns(2)
with colA:
    @st.fragment()
    def population_parameters_alcohol_A():
        
        ##################
        # alcohol_prob_receptive
        #################
        
        if 'alcohol_prob_receptive' not in st.session_state:
            st.session_state.alcohol_prob_receptive = 0.75

        alcohol_prob_receptive =  st.slider(
            "Chance that a pre-Contemplation person not in a golden window is receptive to an intervention"
            , 0.0, 1.0
            , st.session_state.alcohol_prob_receptive
            , on_change=lambda: setattr(st.session_state,
                        'alcohol_prob_receptive',
                        st.session_state['alcohol probability receptive'])
            ,key='alcohol probability receptive')

        st.markdown("**Base Positive Change Chance**")

        ##################
        # alcohol_change_prob_contemplation
        #################
        if 'alcohol_change_prob_contemplation' not in st.session_state:
            st.session_state.alcohol_change_prob_contemplation = 0.01

        alcohol_change_prob_contemplation =  st.slider(
            "Base Pre-Contemplation to Contemplation chance"
            , 0.0, 1.0
            , st.session_state.alcohol_change_prob_contemplation
            , on_change=lambda: setattr(st.session_state,
                                        'alcohol_change_prob_contemplation',
                                        st.session_state['alcohol Contemplation'])
            ,key='alcohol Contemplation')

        ##################
        # alcohol_change_prob_preparation
        #################

        if 'alcohol_change_prob_preparation' not in st.session_state:
            st.session_state.alcohol_change_prob_preparation = 0.01

        alcohol_change_prob_preparation =  st.slider(
            "Base Contemplation to Preparation chance"
            , 0.0, 1.0
            , st.session_state.alcohol_change_prob_preparation
            , on_change=lambda: setattr(st.session_state,
                                        'alcohol_change_prob_preparation',
                                        st.session_state['alcohol Preparation'])
            ,key='alcohol Preparation')

        ##################
        # alcohol_change_prob_action
        #################

        if 'alcohol_change_prob_action' not in st.session_state:
            st.session_state.alcohol_change_prob_action = 0.01

        alcohol_change_prob_action =  st.slider(
            "Base Preparation to Action chance"
            , 0.0, 1.0
            , st.session_state.alcohol_change_prob_action
            , on_change=lambda: setattr(st.session_state,
                                        'alcohol_change_prob_action',
                                        st.session_state['alcohol Action'])
            ,key='alcohol Action')

    population_parameters_alcohol_A()

with colB:
    @st.fragment()
    def population_parameters_alcohol_B():
        ##################
        # alcohol_golden_window
        #################
        
        if 'alcohol_golden_window' not in st.session_state:
            st.session_state.alcohol_golden_window = 3

        alcohol_golden_window =  st.slider(
            "Periods before chances reset to base (the golden window)"
            , 0, 24
            , st.session_state.alcohol_golden_window
            , on_change=lambda: setattr(st.session_state,
                        'alcohol_golden_window',
                        st.session_state['alcohol golden window'])
            ,key='alcohol golden window')
        
        ##################
        # alcohol_lapse_prob_precontemplation
        #################

        st.markdown("**Lapse Chance**")

        if 'alcohol_lapse_prob_precontemplation' not in st.session_state:
            st.session_state.alcohol_lapse_prob_precontemplation = 0.01

        alcohol_lapse_prob_precontemplation =  st.slider(
            "Base Contemplation to Pre-Contemplation lapse chance"
            , 0.0, 1.0
            , st.session_state.alcohol_lapse_prob_precontemplation
            , on_change=lambda: setattr(st.session_state,
                                        'alcohol_lapse_prob_precontemplation',
                                        st.session_state['alcohol lapse Pre-Contemplation'])
            ,key='alcohol lapse Pre-Contemplation')

        ##################
        # alcohol_lapse_prob_contemplation
        #################

        if 'alcohol_lapse_prob_contemplation' not in st.session_state:
            st.session_state.alcohol_lapse_prob_contemplation = 0.01

        alcohol_lapse_prob_contemplation =  st.slider(
            "Base Preparation to Contemplation lapse chance"
            , 0.0, 1.0
            , st.session_state.alcohol_lapse_prob_contemplation
            , on_change=lambda: setattr(st.session_state,
                        'alcohol_lapse_prob_contemplation',
                        st.session_state['alcohol lapse Contemplation'])
            ,key='alcohol lapse Contemplation')

        ##################
        # alcohol_lapse_prob_preparation
        #################

        if 'alcohol_lapse_prob_preparation' not in st.session_state:
            st.session_state.alcohol_lapse_prob_preparation = 0.01

        alcohol_lapse_prob_preparation =  st.slider(
            "Base Action to Preparation lapse chance"
            , 0.0, 1.0
            , st.session_state.alcohol_lapse_prob_preparation
            , on_change=lambda: setattr(st.session_state,
                        'alcohol_lapse_prob_preparation',
                        st.session_state['alcohol lapse Preparation'])
            ,key='alcohol lapse Preparation')



    population_parameters_alcohol_B()

###################################################

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

## adds to session state if does not exist
if 'alcohol_services_table' not in st.session_state:
    st.session_state.alcohol_services_table = alcohol_services.copy()

@st.fragment
def alcohol_service_input(alcohol_services):
    st.markdown("#### Service")

## creates a data editor of the variables
    alcohol_services_edit = st.data_editor(
        alcohol_services,
        disabled=["Service"],
        key='alcohol_services_editor',
        # on_change = lambda: setattr(st.session_state
        #                             ,'alcohol_services_table'
        #                             , alcohol_services_edit.copy()),
        column_config={
            "Service": "Service",
            "Person Visit Probability": st.column_config.NumberColumn(
                "Person Visit Probability",
                width='medium',
                help="How likely is someone to visit in a month (0.0-1.0)?",
                min_value=0.0,
                max_value=1.0,
                step=0.01,),
            "Chance a Brief Intervention Made Without MECC Training": st.column_config.NumberColumn(
                "Chance a Brief Intervention Made Without MECC Training",
                width='medium',
                help="How likely is an intervention before MECC training (0.0-1.0)?",
                min_value=0.0,
                max_value=1.0,
                step=0.01,),
            "MECC Trained":"MECC Trained",
            "Chance Making a Brief Intervention After MECC Training": st.column_config.NumberColumn(
                "Chance Making a Brief Intervention After MECC Training",
                width='medium',
                help="How likely is an intervention after MECC training (0.0-1.0)?",
                min_value=0.0,
                max_value=1.0,
                step=0.01,),
            "Post Intervention Pre-Contemplation to Contemplation chance": st.column_config.NumberColumn(
                "Post Intervention Pre-Contemplation to Contemplation chance",
                width='medium',
                help="What does a person's chance of changing from" +
                        "Pre-Contemplation to Contemplation become" +
                        "post-intervention (0.0-1.0)?",
                min_value=0.0,
                max_value=1.0,
                step=0.01,),
            "Post Intervention Contemplation to Preparation chance": st.column_config.NumberColumn(
                "Post Intervention Contemplation to Preparation chance",
                width='medium',
                help="What does a person's chance of changing from" +
                        "Contemplation to Preparation become" +
                        "post-intervention (0.0-1.0)?",
                min_value=0.0,
                max_value=1.0,
                step=0.01,),
            "Post Intervention Preparation to Action chance": st.column_config.NumberColumn(
                "Post Intervention Preparation to Action chance",
                width='medium',
                help="What does a person's chance of changing from" +
                        "Preparation to Action become" +
                        "post-intervention (0.0-1.0)?",
                min_value=0.0,
                max_value=1.0,
                step=0.01,),
                },
        )

    st.session_state['alcohol_services_table'] = alcohol_services_edit.copy()

alcohol_service_input(st.session_state.alcohol_services_table)