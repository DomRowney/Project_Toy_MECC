# model_two_types_mecc.py

##################################
### Packages
##################################
import mesa
from mesa import Agent, Model
from mesa.time import RandomActivation
#from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
#import random
import streamlit as st

##################################
### Person Agent Class
##################################

## creates a class of person agent
class PersonAgent(Agent):
    def __init__(self
                 , unique_id
                 , model
                 , visit_prob):
        super().__init__(unique_id, model)
        
        ## Visit properties
        self.visit_prob = visit_prob

        ## Reporting variables
        self.interventions_received = 0

    ## Action to make a visit to a service
    def move(self):
        if self.random.uniform(0,1) < self.visit_prob:
            ## randomly selects a service agent
            ServiceAgent_list = [agent for agent in self.model.schedule.agents if isinstance(agent, ServiceAgent)]
            if ServiceAgent_list:
                    visited_service = self.random.choice(ServiceAgent_list)
                    ## runs the chosen service's have contact function
                    visited_service.have_contact(self)

    ## Defines actions at each step
    def step(self):
        self.move()


## creates a subclass of person agent for the smoking model
class SmokeModel_PersonAgent(PersonAgent):
    def __init__(self
                 , unique_id
                 , model
                 , initial_smoking_prob
                 , quit_attempt_prob,visit_prob
                 , base_smoke_relapse_prob):
        super().__init__(unique_id, model, visit_prob)

        ## Smoking properties
        self.smoker = self.random.uniform(0, 1) < initial_smoking_prob ## randomise whether a smoker
        self.never_smoked = not self.smoker ## Track if they've never smoked
        self.base_smoke_relapse_prob = base_smoke_relapse_prob
        self.quit_attempt_prob = quit_attempt_prob

        ## Smoking Reporting variables
        self.quit_attempts = 0
        self.months_smoke_free = 0

    ## Action to have a change of quitting smoking
    def attempt_quit(self):
        if self.smoker and self.random.uniform(0, 1) < self.quit_attempt_prob:
            self.smoker = False
            self.quit_attempts += 1
            self.months_smoke_free = 0
            self.never_smoked = False  ## They've now smoked and quit

    ## Action to update smoking status
    def update_smoking_status(self):
        if not self.smoker and not self.never_smoked:  ## Only ex-smokers can relapse
            self.months_smoke_free += 1
            ## Recidivism rate decreases as months smoke-free increases
            recidivism_prob = self.base_smoke_relapse_prob * (0.95 ** self.months_smoke_free)
            if self.random.uniform(0, 1) < recidivism_prob:
                self.smoker = True
                self.months_smoke_free = 0

    ## Defines actions at each step
    def step(self):
        super().step()
        self.attempt_quit()
        self.update_smoking_status()




##################################
### Service Agent Class
##################################

## creates a class of service agent
class ServiceAgent(Agent):
    def __init__(self
                 , unique_id
                 , model
                 , mecc_effect = 0
                 , base_make_intervention_prob = 0
                 #, intervention_radius
                 , mecc_trained = False):
        super().__init__(unique_id, model)

        ## Intervention 
        self.mecc_effect = mecc_effect
        self.base_make_intervention_prob = base_make_intervention_prob
        self.mecc_trained = mecc_trained ## If service is MECC trained
        #self.intervention_radius = intervention_radius

        ## Reporting variables
        self.contacts_made = 0
        self.interventions_made = 0
    
    ## Property for probability of making an intervention
    @property
    def make_intervention_prob(self):
        if self.mecc_trained:
            return self.mecc_effect
        else:
            return self.base_make_intervention_prob
    
    ## Function that is called by a person when making a visit to this service
    def have_contact(self, PersonAgent):
        ## adds one to the service contact count
        self.contacts_made += 1
        intervention_rand = self.random.uniform(0, 1)
        ## for checking outputs
        #st.write(f'chance intervention: {intervention_rand}\n\n' 
        #         f' mecc_trained: {self.mecc_trained}\n\n'
        #         f' mecc_effect: {self.mecc_effect}\n\n'
        #         f' base_make_intervention_prob: {self.base_make_intervention_prob}\n\n'
        #         f' make_intervention_prob: {self.make_intervention_prob}\n\n'
        #         '-----')
        if intervention_rand < self.make_intervention_prob:
            PersonAgent.interventions_received += 1
            self.perform_intervention(PersonAgent)
            ## adds 1 to the intervention count
            self.interventions_made += 1
    
    # Placeholder for performing an intervention; can be overridden by subclasses
    def perform_intervention(self, PersonAgent):
        pass
    
    ## doesn't do anything at each step
    def step(self):
        pass

## creates a subclass of service agent for smoking model
class SmokeModel_ServiceAgent(ServiceAgent):
    def __init__(self
                 , unique_id
                 , model
                 , mecc_effect
                 , base_make_intervention_prob
                 , mecc_trained
                 , intervention_effect):
        super().__init__(unique_id, model
                         , mecc_effect
                         , base_make_intervention_prob
                         , mecc_trained)

        ## Smoking Intervention Effect
        self.intervention_effect = intervention_effect

    # Override to perform smoking-specific interventions
    def perform_intervention(self, PersonAgent):
        PersonAgent.quit_attempt_prob *= self.intervention_effect
    
    ## doesn't do anything at each step
    def step(self):
        pass



##################################
### Model Class
##################################

## creates a class of model
class MECC_Model(Model): 
    def __init__(self
                , N_people = 0
                , N_service = 0
                , mecc_effect = 0
                , base_make_intervention_prob  = 0
                , visit_prob = 0
                , mecc_trained = False
                , seed = None):
        super().__init__()  # Properly initialize the Model class

        ## Set the seed for reproducibility
        #if seed_value is not None:
        #    random.seed(seed_value)  

        ## numbers of agents
        self.N_people = N_people
        self.N_service = N_service

        ## other features for person agents
        self.visit_prob = visit_prob
        
        ## intervention features for service agents
        self.base_make_intervention_prob = base_make_intervention_prob
        self.mecc_effect = mecc_effect
        
        ## Flag for whether model includes MECC training
        self.mecc_trained = mecc_trained
        
        ## Schedule
        self.schedule = RandomActivation(self)
        #self.grid = MultiGrid(self.width, self.height, True)
        
        ## Data collector for metrics
        self.datacollector = DataCollector(
            model_reporters={
                "Total Contacts": calculate_total_contacts,
                "Total Interventions": calculate_total_interventions
            },
            agent_reporters={}
        )
        
        ## Create person agents
        for i in range(self.N_people):
            a = PersonAgent(unique_id = i
                            , model = self
                            , visit_prob = self.visit_prob)
            self.schedule.add(a)
            
        ## Create service agents
        for i in range(self.N_service):
            a = ServiceAgent(unique_id = i + self.N_people
                             , model = self
                             , base_make_intervention_prob = self.base_make_intervention_prob
                             , mecc_effect = self.mecc_effect
                             , mecc_trained = self.mecc_trained)
            self.schedule.add(a)

    ## Define actions at each step
    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()


## creates a subclass of model for smoking
class SmokeModel_MECC_Model(MECC_Model): 
    def __init__(self
                , N_people
                , N_service
                , mecc_effect
                , base_make_intervention_prob 
                , visit_prob
                , mecc_trained     
                , seed
                , intervention_effect
                , initial_smoking_prob 
                , quit_attempt_prob
                , base_smoke_relapse_prob):
        super().__init__( N_people
                , N_service
                , mecc_effect
                , base_make_intervention_prob 
                , visit_prob
                , mecc_trained     
                , seed )  # Properly initialize the MECC_Model class

        ## smoking features for person agents
        ## Convert dictionary values if they're dictionaries
        self.initial_smoking_prob = initial_smoking_prob['value'] if isinstance(initial_smoking_prob, dict) else initial_smoking_prob
        self.quit_attempt_prob = quit_attempt_prob['value'] if isinstance(quit_attempt_prob, dict) else quit_attempt_prob
        self.base_smoke_relapse_prob = base_smoke_relapse_prob['value'] if isinstance(base_smoke_relapse_prob, dict) else base_smoke_relapse_prob
        self.intervention_effect = intervention_effect['value'] if isinstance(intervention_effect, dict) else intervention_effect

        
        ## Overwrite Data collector for metrics
        self.datacollector = DataCollector(
            model_reporters={
                "Total Smoking": calculate_number_smoking,
                "Total Not Smoking": calculate_number_not_smoking,
                "Total Quit Attempts": calculate_total_quit_attempts,
                "Total Quit Smoking": calculate_total_quit_smoking,
                "Total Contacts": calculate_total_contacts,
                "Total Interventions": calculate_total_interventions,
                "Smokers With an Intervention": calculate_smoker_with_interventions,
                "Average Months Smoke Free": calculate_average_months_smoke_free
            },
            agent_reporters={}
        )
        
        ## Reset Schedule to overwrite for agents
        self.schedule = RandomActivation(self)

        ## Create person agents
        for i in range(self.N_people):
            a = SmokeModel_PersonAgent(unique_id = i
                            , model = self
                            , initial_smoking_prob = self.initial_smoking_prob
                            , quit_attempt_prob  = self.quit_attempt_prob
                            , base_smoke_relapse_prob = self.base_smoke_relapse_prob
                            , visit_prob = self.visit_prob)
            self.schedule.add(a)
            
        ## Create service agents
        for i in range(self.N_service):
            a = SmokeModel_ServiceAgent(unique_id = i + self.N_people
                             , model = self
                             , base_make_intervention_prob = self.base_make_intervention_prob
                             , mecc_effect = self.mecc_effect
                             , intervention_effect = self.intervention_effect
                             , mecc_trained = self.mecc_trained)
            self.schedule.add(a)

##################################
### Metric Outputs
##################################

## creates metrics used by model to report stats
def calculate_number_smoking(model):
    return sum(1 for agent in model.schedule.agents 
              if isinstance(agent, PersonAgent) and agent.smoker)

def calculate_number_not_smoking(model):
    return sum(1 for agent in model.schedule.agents 
              if isinstance(agent, PersonAgent) and not agent.smoker)

def calculate_total_quit_attempts(model):
    return sum(agent.quit_attempts for agent in model.schedule.agents 
              if isinstance(agent, PersonAgent))

def calculate_total_quit_smoking(model):
    return sum(agent.quit_attempts for agent in model.schedule.agents 
              if isinstance(agent, PersonAgent)
                and not agent.never_smoked
                and not agent.smoker )

def calculate_total_contacts(model):
    return sum(agent.contacts_made for agent in model.schedule.agents 
              if isinstance(agent, ServiceAgent))

def calculate_total_interventions(model):
    return sum(agent.interventions_made for agent in model.schedule.agents 
              if isinstance(agent, ServiceAgent))

def calculate_smoker_with_interventions(model):
    return sum(1 for agent in model.schedule.agents 
              if isinstance(agent, PersonAgent)
                and not agent.never_smoked
                and agent.interventions_received > 0)

def calculate_average_months_smoke_free(model):
    smoke_free_months = [agent.months_smoke_free for agent in model.schedule.agents 
                      if isinstance(agent, PersonAgent) and not agent.smoker]
    return sum(smoke_free_months) / len(smoke_free_months) if smoke_free_months else 0