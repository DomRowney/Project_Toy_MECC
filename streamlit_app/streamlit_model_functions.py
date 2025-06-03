## streamlit_model_functions.py
import pandas as pd
#import numpy as np
import streamlit as st
from model_two_types_mecc import MECC_Model,SmokeModel_MECC_Model
from alcohol_agents import Alcohol_MECC_Model
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#import time

##################################
### Model Functions
##################################

## Function to create a model
def create_MECC_model(model_parameters
                      ,model_type = 'Generic'
                      ,mecc_trained = False):
    ## for checking
    if model_type == 'Generic':
        model = MECC_Model(
            seed=model_parameters["model_seed"],
            N_people=model_parameters["N_people"],
            N_service=model_parameters["N_service"],
            base_make_intervention_prob=model_parameters["base_make_intervention_prob"],
            visit_prob=model_parameters["visit_prob"],
            mecc_effect=model_parameters["mecc_effect"],            
            mecc_trained=mecc_trained)

    if model_type == 'Alcohol':
        ## for checking
        #st.write(f'mecc_trained: {mecc_trained}')
        ## For the trained version only those with ticks are mecc trained
        if mecc_trained:
            model_parameters["mecc_trained"] = model_parameters["mecc_trained"]
            ## for checking
            #st.write(f'MECC PARAMETERS\n\n{model_parameters}\n\n'
            #         '-----')
        ## For the untrained version no service is mecc trained
        else:
            for service in model_parameters["mecc_trained"]:
                model_parameters["mecc_trained"][service] = False
            ## for checking                
            #st.write(f'NO MECC PARAMETERS\n\n{model_parameters}\n\n'
            #         '-----')

        model = Alcohol_MECC_Model(
            N_people = model_parameters["N_people"]
            #, N_service
            , seed = model_parameters["model_seed"]

            ## dictionaries of intervention chance
            #, contemplation_intervention = model_parameters["contemplation_intervention"]
            #, preparation_intervention = model_parameters["preparation_intervention"]
            #, action_intervention = model_parameters["action_intervention"]

            ## change state probability
            , prob_receptive = model_parameters["prob_receptive"]

            #, change_prob_contemplation = model_parameters[ "change_prob_contemplation"]
            #, change_prob_preparation = model_parameters["change_prob_preparation"]
            #, change_prob_action = model_parameters["change_prob_action"]

            #, lapse_prob_precontemplation = model_parameters["lapse_prob_precontemplation"]
            #, lapse_prob_contemplation = model_parameters["lapse_prob_contemplation"]
            #, lapse_prob_preparation = model_parameters["lapse_prob_preparation"]

            #, golden_window = model_parameters["golden_window"]
            
            ## visit probability
            , visit_prob = model_parameters["visit_prob"]

            ## site properties
            , mecc_effect = model_parameters["mecc_effect"]
            , base_make_intervention_prob = model_parameters["base_make_intervention_prob"]
            , mecc_trained = model_parameters["mecc_trained"]   
            , mecc_training_decay_half_life = model_parameters["mecc_training_decay_half_life"]
            )

    elif model_type == 'Smoke':
        model = SmokeModel_MECC_Model(
            seed=model_parameters["model_seed"],
            N_people=model_parameters["N_people"],
            N_service=model_parameters["N_service"],
            initial_smoking_prob=model_parameters["initial_smoking_prob"],
            base_make_intervention_prob=model_parameters["base_make_intervention_prob"],
            quit_attempt_prob=model_parameters["quit_attempt_prob"],
            visit_prob=model_parameters["visit_prob"],
            base_smoke_relapse_prob = model_parameters["base_smoke_relapse_prob"],
            intervention_effect=model_parameters["intervention_effect"],  
            mecc_effect=model_parameters["mecc_effect"],            
            mecc_trained=mecc_trained)   
    return model

## Function to run simulation steps
def run_simulation_step(model):
    """Run one step of the simulation and return current data"""
    model.step()
    data = model.datacollector.get_model_vars_dataframe()
    return data



##################################
### Output Functions
##################################

# def create_figure(results, step):
#     """Create the figure for single model visualization"""
#     fig = make_subplots(
#         rows=2, 
#         cols=2,
#         subplot_titles=(
#             'Population Changes Over Time',
#             'Interventions and Quit Attempts',
#             'Current Population Distribution',
#             'Success Metrics'
#         ),
#         specs=[[{}, {}], [{}, {}]],
#         row_heights=[0.6, 0.4]
#     )
    
#     # Population changes over time
#     fig.add_trace(
#         go.Scatter(
#             x=results.index[:step+1], 
#             y=results['Total Smoking'][:step+1], 
#             name="Smoking", 
#             line=dict(color="red")
#         ),
#         row=1, col=1
#     )
#     fig.add_trace(
#         go.Scatter(
#             x=results.index[:step+1], 
#             y=results['Total Not Smoking'][:step+1], 
#             name="Not Smoking", 
#             line=dict(color="green")
#         ),
#         row=1, col=1
#     )
    
#     # Interventions and Quit Attempts over time
#     fig.add_trace(
#         go.Scatter(
#             x=results.index[:step+1], 
#             y=results['Total Interventions'][:step+1], 
#             name="Interventions", 
#             line=dict(color="blue")
#         ),
#         row=1, col=2
#     )
#     fig.add_trace(
#         go.Scatter(
#             x=results.index[:step+1], 
#             y=results['Total Quit Attempts'][:step+1], 
#             name="Quit Attempts", 
#             line=dict(color="purple")
#         ),
#         row=1, col=2
#     )
    
#     # Current Population Distribution (Bar Chart)
#     current_smoking = results['Total Smoking'].iloc[step]
#     current_not_smoking = results['Total Not Smoking'].iloc[step]
    
#     fig.add_trace(
#         go.Bar(
#             x=['Current Distribution'],
#             y=[current_smoking],
#             name='Smoking',
#             marker_color='red'
#         ),
#         row=2, col=1
#     )
#     fig.add_trace(
#         go.Bar(
#             x=['Current Distribution'],
#             y=[current_not_smoking],
#             name='Not Smoking',
#             marker_color='green'
#         ),
#         row=2, col=1
#     )
    
#     # Success Metrics
#     current_quit_attempts = results['Total Quit Attempts'].iloc[step]
#     current_interventions = results['Total Interventions'].iloc[step]
#     current_quits = results['Total Quit Smoking'].iloc[step]
#     avg_months_smoke_free = results['Average Months Smoke Free'].iloc[step]
    
#     fig.add_trace(
#         go.Bar(
#             x=[ 'Interventions','Quit Attempts','Current Quits', 'Avg Months Smoke Free'],
#             y=[current_interventions, current_quit_attempts, current_quits ,avg_months_smoke_free],
#             marker_color=['purple', 'blue', 'orange' ,'black']
#         ),
#         row=2, col=2
#     )
    
#     # Update layout
#     fig.update_layout(
#         height=800,
#         showlegend=True,
#         barmode='group'
#     )
    
#     # Update axes labels
#     fig.update_xaxes(title_text="Time Step", row=1, col=1)
#     fig.update_xaxes(title_text="Time Step", row=1, col=2)
#     fig.update_yaxes(title_text="Number of Agents", row=1, col=1)
#     fig.update_yaxes(title_text="Number of Events", row=1, col=2)
#     fig.update_yaxes(title_text="Number of Agents", row=2, col=1)
#     fig.update_yaxes(title_text="Count", row=2, col=2)
    
#     return fig


#def create_comparison_figure(results_no_mecc, results_mecc, step):
#    """Create side-by-side comparison figures"""
#    fig = make_subplots(
#        rows=3, 
#        cols=2,
#        subplot_titles=(
#            'Without MECC Training',
#            'With MECC Training',
#            'Interventions & Quit Attempts (No MECC)',
#            'Interventions & Quit Attempts (With MECC)',
#            'Success Metrics Comparison',
#            'Performance Improvement'
#        ),
#        specs=[[{}, {}], [{}, {}], [{}, {}]],
#        row_heights=[0.4, 0.4, 0.2]
#    )
#    
#    # Population changes over time - Without MECC
#    fig.add_trace(
#        go.Scatter(
#            x=results_no_mecc.index[:step+1], 
#            y=results_no_mecc['Total Smoking'][:step+1], 
#            name="Smoking (No MECC)", 
#            line=dict(color="red", dash='solid')
#        ),
#        row=1, col=1
#    )
#    fig.add_trace(
#        go.Scatter(
#            x=results_no_mecc.index[:step+1], 
#            y=results_no_mecc['Total Not Smoking'][:step+1], 
#            name="Not Smoking (No MECC)", 
#            line=dict(color="green", dash='solid')
#        ),
#        row=1, col=1
#    )
#    
#    # Population changes over time - With MECC
#    fig.add_trace(
#        go.Scatter(
#            x=results_mecc.index[:step+1], 
#            y=results_mecc['Total Smoking'][:step+1], 
#            name="Smoking (MECC)", 
#            line=dict(color="red", dash='dot')
#        ),
#        row=1, col=2
#    )
#    fig.add_trace(
#        go.Scatter(
#            x=results_mecc.index[:step+1], 
#            y=results_mecc['Total Not Smoking'][:step+1], 
#            name="Not Smoking (MECC)", 
#            line=dict(color="green", dash='dot')
#        ),
#        row=1, col=2
#    )
#    
#    # Interventions and Quit Attempts - Without MECC
#    fig.add_trace(
#        go.Scatter(
#            x=results_no_mecc.index[:step+1],
#            y=results_no_mecc['Total Interventions'][:step+1],
#            name="Interventions (No MECC)",
#            line=dict(color="blue", dash='solid')
#        ),
#        row=2, col=1
#    )
#    fig.add_trace(
#        go.Scatter(
#            x=results_no_mecc.index[:step+1],
#            y=results_no_mecc['Total Quit Attempts'][:step+1],
#            name="Quit Attempts (No MECC)",
#            line=dict(color="purple", dash='solid')
#        ),
#        row=2, col=1
#    )
#    
#    # Interventions and Quit Attempts - With MECC
#    fig.add_trace(
#        go.Scatter(
#            x=results_mecc.index[:step+1],
#            y=results_mecc['Total Interventions'][:step+1],
#            name="Interventions (MECC)",
#            line=dict(color="blue", dash='dot')
#        ),
#        row=2, col=2
#    )
#    fig.add_trace(
#        go.Scatter(
#            x=results_mecc.index[:step+1],
#            y=results_mecc['Total Quit Attempts'][:step+1],
#            name="Quit Attempts (MECC)",
#            line=dict(color="purple", dash='dot')
#        ),
#        row=2, col=2
#    )
#    
#    # Comparative metrics
#    current_interventions_no_mecc = results_no_mecc['Total Interventions'].iloc[step]
#    current_interventions_mecc = results_mecc['Total Interventions'].iloc[step]
# 
#    current_quit_attempts_no_mecc = results_no_mecc['Total Quit Attempts'].iloc[step]
#    current_quit_attempts_mecc = results_mecc['Total Quit Attempts'].iloc[step]
#
#    current_quits_no_mecc = results_no_mecc['Total Quit Smoking'].iloc[step]
#    current_quits_mecc = results_mecc['Total Quit Smoking'].iloc[step]
#     
#    #success_rate_no_mecc = (results_no_mecc['Total Quit Smoking'].iloc[step] / 
#    #                       results_no_mecc['Total Quit Attempts'].iloc[step] * 100 
#    #                                if results_no_mecc['Total Quit Attempts'].iloc[step] > 0 else 0)
#    #success_rate_mecc = (results_mecc['Total Quit Smoking'].iloc[step] / 
#    #                    results_mecc['Total Quit Attempts'].iloc[step] * 100
#    #                             if results_mecc['Total Quit Attempts'].iloc[step] > 0 else 0)
#    
#    # Success metrics comparison
#    fig.add_trace(
#        go.Bar(
#            x=['Interventions', 'Quit Attempts','Current Quits'],# 'Success Rate (%)'],
#            y=[current_interventions_no_mecc, current_quit_attempts_no_mecc,current_quits_no_mecc],#, success_rate_no_mecc],
#            name='No MECC',
#            marker_color='rgba(135, 206, 250, 0.8)'
#        ),
#        row=3, col=1
#    )
#    
#    fig.add_trace(
#        go.Bar(
#            x=['Interventions', 'Quit Attempts','Current Quits'],# 'Success Rate (%)'],
#            y=[current_interventions_mecc, current_quit_attempts_mecc,current_quits_mecc],#, success_rate_mecc],
#            name='With MECC',
#            marker_color='rgba(0, 0, 139, 0.8)'
#        ),
#        row=3, col=2
#    )
#    
#    # Update layout
#    fig.update_layout(
#        height=1000,  # Increased height to accommodate new row
#        showlegend=True,
#        barmode='group'
#    )
#    
#    # Update axes labels
#    fig.update_xaxes(title_text="Month", row=1, col=1)
#    fig.update_xaxes(title_text="Month", row=1, col=2)
#    fig.update_xaxes(title_text="Month", row=2, col=1)
#    fig.update_xaxes(title_text="Month", row=2, col=2)
#    fig.update_xaxes(title_text="Metrics", row=3, col=1)
#    fig.update_xaxes(title_text="Metrics", row=3, col=2)
#    
#    # Update y-axes labels
#    fig.update_yaxes(title_text="Number of People", row=1, col=1)
#    fig.update_yaxes(title_text="Number of People", row=1, col=2)
#    fig.update_yaxes(title_text="Count", row=2, col=1)
#    fig.update_yaxes(title_text="Count", row=2, col=2)
#    fig.update_yaxes(title_text="Value", row=3, col=1)
#    fig.update_yaxes(title_text="Value", row=3, col=2)
#    
#    # Link the y-axes for each pair of charts in the same row
#    fig.update_yaxes(matches='y2', row=1)  # Matches y-axis for row 1 charts
#    fig.update_yaxes(matches='y3', row=2)  # Matches y-axis for row 2 charts
#    fig.update_yaxes(matches='y4', row=3)  # Matches y-axis for row 3 charts
#
#    return fig

##########################################
## Population Figure
##########################################


def create_population_figure(results_no_mecc, results_mecc, step):
    """Create side-by-side comparison figures"""
    fig = make_subplots(
        rows=1, 
        cols=2,
        subplot_titles=(
            'Smoking Population (Without MECC Training)',
            'Smoking Population (With MECC Training)',
        ),
        specs=[[{}, {}]],
        row_heights=[1]
    )

    # Population changes over time - Without MECC
    fig.add_trace(
        go.Scatter(
            x=results_no_mecc.index[:step+1], 
            y=results_no_mecc['Total Smoking'][:step+1], 
            name="Smoking (No MECC Training)", 
            line=dict(color="red", dash='solid')
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=results_no_mecc.index[:step+1], 
            y=results_no_mecc['Total Not Smoking'][:step+1], 
            name="Not Smoking (No MECC Training)", 
            line=dict(color="green", dash='solid')
        ),
        row=1, col=1
    )
    
    # Population changes over time - With MECC
    fig.add_trace(
        go.Scatter(
            x=results_mecc.index[:step+1], 
            y=results_mecc['Total Smoking'][:step+1], 
            name="Smoking (MECC Trained)", 
            line=dict(color="red", dash='dot')
        ),
        row=1, col=2
    )
    fig.add_trace(
        go.Scatter(
            x=results_mecc.index[:step+1], 
            y=results_mecc['Total Not Smoking'][:step+1], 
            name="Not Smoking (MECC Trained)", 
            line=dict(color="green", dash='dot')
        ),
        row=1, col=2
    )
    
    # Update layout
    fig.update_layout(
        height=400, 
        showlegend=True,
        barmode='group'
    )

    # Update legend
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.1,
        xanchor="center",
        x=0.5
    ))

    # Update axes labels
    fig.update_xaxes(title_text="Month", row=1, col=1)
    fig.update_xaxes(title_text="Month", row=1, col=2)

    # Update y-axes labels
    fig.update_yaxes(title_text="Number of People", row=1, col=1)
    fig.update_yaxes(title_text="Number of People", row=1, col=2)
    
    # Link the axes for each pair of charts in the same row
    fig.update_yaxes(matches='y', row=1)
    fig.update_xaxes(matches='x', row=1)

    return fig

##########################################
## Intervention Figure
##########################################

def create_intervention_figure(results_no_mecc, results_mecc, step):
    """Create side-by-side comparison figures"""

    no_mecc_quit = (True if 'Total Quit Attempts' 
                    in results_no_mecc.columns else False)
    mecc_quit = (True if 'Total Quit Attempts' 
                    in results_mecc.columns else False)
    
    no_mecc_subtitle = ('Interventions' +
                         (' & Quit Attempts' if no_mecc_quit else '') +
                           ' (No MECC Training)')
    mecc_subtitle = ('Interventions' +
                      (' & Quit Attempts' if mecc_quit else '') +
                        ' (MECC Trained)')

    fig = make_subplots(
        rows=1, 
        cols=2,
        subplot_titles=(
            no_mecc_subtitle,
            mecc_subtitle,
        ),
        specs=[[{}, {}]],
        row_heights=[1]
    )

        
    # Interventions and Quit Attempts - Without MECC
    fig.add_trace(
        go.Scatter(
            x=results_no_mecc.index[:step+1],
            y=results_no_mecc['Total Contacts'][:step+1],
            name="Contacts (No MECC Training)",
            line=dict(color="grey", dash='solid')
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=results_no_mecc.index[:step+1],
            y=results_no_mecc['Total Interventions'][:step+1],
            name="Interventions (No MECC Training)",
            line=dict(color="blue", dash='solid')
        ),
        row=1, col=1
    )
    if no_mecc_quit:
        fig.add_trace(
            go.Scatter(
                x=results_no_mecc.index[:step+1],
                y=results_no_mecc['Total Quit Attempts'][:step+1],
                name="Quit Attempts (No MECC Training)",
                line=dict(color="purple", dash='solid')
            ),
            row=1, col=1
            )
    
    # Interventions and Quit Attempts - With MECC
    fig.add_trace(
        go.Scatter(
            x=results_mecc.index[:step+1],
            y=results_mecc['Total Contacts'][:step+1],
            name="Contacts (MECC Trained)",
            line=dict(color="grey", dash='dot')
        ),
        row=1, col=2
        )
        
    fig.add_trace(
        go.Scatter(
            x=results_mecc.index[:step+1],
            y=results_mecc['Total Interventions'][:step+1],
            name="Interventions (MECC Trained)",
            line=dict(color="blue", dash='dot')
        ),
        row=1, col=2
        )
    if mecc_quit:
        fig.add_trace(
            go.Scatter(
                x=results_mecc.index[:step+1],
                y=results_mecc['Total Quit Attempts'][:step+1],
                name="Quit Attempts (MECC Trained)",
                line=dict(color="purple", dash='dot')
            ),
            row=1, col=2
            )
    
    # Update layout
    fig.update_layout(
        height=400,  
        showlegend=True,
        barmode='group'
    )

    # Update legend
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.1,
        xanchor="center",
        x=0.5
    ))

    # Update axes labels
    fig.update_xaxes(title_text="Month", row=1, col=1)
    fig.update_xaxes(title_text="Month", row=1, col=2)
    
    # Update y-axes labels
    fig.update_yaxes(title_text="Count", row=1, col=1)
    fig.update_yaxes(title_text="Count", row=1, col=2)
    
    # Link the axes for each pair of charts in the same row
    fig.update_yaxes(matches='y', row=1)
    fig.update_xaxes(matches='x', row=1)

    return fig


##########################################
## Multi-model Intervention Figure
##########################################

def create_multi_intervention_figure(results_no_mecc, results_mecc):
    """
    Create side-by-side aggregate comparison figures for multiple models
    with mean and standard deviation.
    """
    def compute_aggregates(data):
        """
        Compute mean and standard deviation for each column except 'month' and 'seed'.
        """
        grouped = data.groupby('month').agg(['mean', 'std','min','max']).reset_index()
        mean_cols = grouped.xs('mean', axis=1, level=1)
        std_cols = grouped.xs('std', axis=1, level=1)
        min_cols = grouped.xs('min', axis=1, level=1)
        max_cols = grouped.xs('max', axis=1, level=1)

        mean_cols['month'] = grouped['month']
        std_cols['month'] = grouped['month']
        min_cols['month'] = grouped['month']
        max_cols['month'] = grouped['month']

        return mean_cols, std_cols, min_cols, max_cols

    no_mecc_mean, no_mecc_std, no_mecc_min, no_mecc_max = compute_aggregates(results_no_mecc)
    mecc_mean, mecc_std, mecc_min, mecc_max = compute_aggregates(results_mecc)

    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=("Interventions (No MECC Training)", "Interventions (MECC Trained)"),
        specs=[[{}, {}]],
        row_heights=[1]
    )

    # Helper function to add traces
    def add_traces(fig, mean_data, std_data,min_data,max_data, col, label_suffix, dash):
        metric_colors = zip(['Total Contacts'
                                  , 'Total Interventions'
                                  , 'Total Quit Attempts'],
                                 ['grey', 'blue', 'purple'])
        for metric, color in metric_colors:
            if metric in mean_data.columns:
                # Add shaded area for minmax
                fig.add_trace(
                    go.Scatter(
                        x=pd.concat([mean_data['month'], mean_data['month'][::-1]]),
                        y=pd.concat([
                            max_data[metric],
                            (min_data[metric])[::-1]
                        ]),
                        name=f"{metric.replace('Total', 'Range')} {metric} ({label_suffix})",
                        fill='toself',
                        opacity=0.05,
                        fillcolor=color,
                        line=dict(color=color),
                        showlegend=False
                    ),
                    row=1, col=col
                )          
                # Add shaded area for std dev 
                fig.add_trace(
                    go.Scatter(
                        x=pd.concat([mean_data['month'], mean_data['month'][::-1]]),
                        y=pd.concat([
                            mean_data[metric] + std_data[metric],
                            (mean_data[metric] - std_data[metric])[::-1]
                        ]),
                        name=f"{metric.replace('Total', '±1 StdDev')} {metric} ({label_suffix})",
                        fill='toself',
                        opacity=0.2,
                        fillcolor=color,
                        line=dict(color=color),
                        showlegend=False
                    ),
                    row=1, col=col
                )                               
                # Add mean line      
                fig.add_trace(
                    go.Scatter(
                        x=mean_data['month'],
                        y=mean_data[metric],
                        name=f"{metric.replace('Total', 'Mean')} ({label_suffix})",
                        line=dict(color=color,dash=dash)
                    ),
                    row=1, col=col
                )       



    # Add traces for No MECC and MECC
    add_traces(fig
               , no_mecc_mean
               , no_mecc_std
               , no_mecc_min
               , no_mecc_max               
               , col=1
               , label_suffix="No MECC"
               , dash='solid')
    add_traces(fig
               , mecc_mean
               , mecc_std
               , mecc_min
               , mecc_max                      
               , col=2
               , label_suffix="MECC Trained"
               , dash='dot')

    # Update layout
    fig.update_layout(
        height=400,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.1,
            xanchor="center",
            x=0.5
        ),
        title_text="Aggregate Comparison of Interventions and Quit Attempts"
    )

    # Update axes labels
    fig.update_xaxes(title_text="Month", row=1, col=1)
    fig.update_xaxes(title_text="Month", row=1, col=2)
    
    # Update y-axes labels
    fig.update_yaxes(title_text="Count", row=1, col=1)
    fig.update_yaxes(title_text="Count", row=1, col=2)
    
    # Link the axes for each pair of charts in the same row
    fig.update_yaxes(matches='y', row=1)
    fig.update_xaxes(matches='x', row=1)

    return fig

##########################################
## Success Metrics Figure
##########################################

def create_metrics_figure(results_no_mecc, results_mecc, step):
    """Create side-by-side comparison figures"""
    fig = make_subplots(
        rows=1, 
        cols=2,
        subplot_titles=(
            'Success Metrics Comparison',
            'Performance Improvement'
        ),
        specs=[[{}, {}]],
        row_heights=[1]
    )
       
    # Comparative metrics
    current_interventions_no_mecc = results_no_mecc['Total Interventions'].iloc[step]
    current_interventions_mecc = results_mecc['Total Interventions'].iloc[step]
 
    current_quit_attempts_no_mecc = results_no_mecc['Total Quit Attempts'].iloc[step]
    current_quit_attempts_mecc = results_mecc['Total Quit Attempts'].iloc[step]

    current_quits_no_mecc = results_no_mecc['Total Quit Smoking'].iloc[step]
    current_quits_mecc = results_mecc['Total Quit Smoking'].iloc[step]
     
    # Success metrics comparison
    fig.add_trace(
        go.Bar(
            x=['Interventions', 'Quit Attempts','Current Quits'],# 'Success Rate (%)'],
            y=[current_interventions_no_mecc, current_quit_attempts_no_mecc,current_quits_no_mecc],#, success_rate_no_mecc],
            name='No MECC Training',
            marker_color='rgba(135, 206, 250, 0.8)'
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(
            x=['Interventions', 'Quit Attempts','Current Quits'],# 'Success Rate (%)'],
            y=[current_interventions_mecc, current_quit_attempts_mecc,current_quits_mecc],#, success_rate_mecc],
            name='MECC Trained',
            marker_color='rgba(0, 0, 139, 0.8)'
        ),
        row=1, col=2
    )
    
    # Update layout
    fig.update_layout(
        height=300,  
        showlegend=True,
        barmode='group'
    )
    
    # Update legend
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.1,
        xanchor="center",
        x=0.5
    ))

    # Update axes labels
    fig.update_xaxes(title_text="Metrics", row=1, col=1)
    fig.update_xaxes(title_text="Metrics", row=1, col=2)
    
    # Update y-axes labels
    fig.update_yaxes(title_text="Value", row=1, col=1)
    fig.update_yaxes(title_text="Value", row=1, col=2)
    
    # Link the axes for each pair of charts in the same row
    fig.update_yaxes(matches='y', row=1)  
    fig.update_xaxes(matches='x', row=1)

    return fig

