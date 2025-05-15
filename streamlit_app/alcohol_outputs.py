## alcohol_outputs.py
import pandas as pd
import numpy as np
#import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import chi2_contingency #, mannwhitneyu
#import time

##########################################
## Population Figure
##########################################

def create_population_figure(results_no_mecc, results_mecc, step):
    """Create side-by-side comparison figures"""
    fig = make_subplots(
        rows=1, 
        cols=2,
        subplot_titles=(
            'Population (Without MECC Training)',
            'Population (With MECC Training)',
        ),
        specs=[[{}, {}]],
        row_heights=[1]
    )
    
    stage_colour_dict = {
                "Pre-contemplation":  "red",
                "Contemplation":  "orange",
                "Preparation":  "blue",
                "Action":  "green",
    }

    for stage in stage_colour_dict:
        # Population changes over time - Without MECC
        fig.add_trace(
            go.Scatter(
                x=results_no_mecc.index[:step+1], 
                y=results_no_mecc[f'Total {stage}'][:step+1], 
                name=f"{stage}",# (No MECC Training)", 
                line=dict(color=stage_colour_dict[stage]
                          , dash='solid')
            ),
            row=1, col=1
        )    
        # Population changes over time - With MECC
        fig.add_trace(
            go.Scatter(
                x=results_mecc.index[:step+1], 
                y=results_mecc[f'Total {stage}'][:step+1], 
                name=f"{stage}",# (MECC Trained)", 
                line=dict(color=stage_colour_dict[stage]
                          , dash='solid'),
                showlegend=False
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
## Site Figure
##########################################

def create_intervention_figure(results_no_mecc, results_mecc, step, figure_type = 'X'):
    """Create side-by-side comparison figures"""

    no_mecc_subtitle = (f'{figure_type}' +
                           ' (No MECC Training)')
    mecc_subtitle = (f'{figure_type}' +
                        ' (MECC Trained)')

    service_colour_dict = { 'Job Centre': "red"
                    ,'Benefits Office': "blue"
                    ,'Housing Officer': "orange"
                    ,'Community Hub': "purple"
                    ,'Pharmacy': "yellow"
                    ,'GP Practice': "green"}
    

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


    for service in service_colour_dict:
        # Interventions and Quit Attempts - Without MECC
        fig.add_trace(
            go.Scatter(
                x=results_no_mecc.index[:step+1],
                y=results_no_mecc[f'{service} {figure_type}'][:step+1],
                name=f"{service}",
                line=dict(color=service_colour_dict[service]
                          , dash='solid')
            ),
            row=1, col=1
        )

        # Interventions and Quit Attempts - With MECC
        fig.add_trace(
            go.Scatter(
                x=results_mecc.index[:step+1],
                y=results_mecc[f'{service} {figure_type}'][:step+1],
                name=f"{service}",
                line=dict(color=service_colour_dict[service]
                          , dash='solid'),
                showlegend=False          
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
## Significance Tests
##########################################

def chi_square_text(chi2, p, dof,N,sig_threshold):
    if p < 0.00001:
        p_txt = 'p<.00001*'
    if p < 0.0001:
        p_txt = 'p<.0001*'        
    elif p < 0.001:
        p_txt = 'p<.001*'
    elif p <= sig_threshold:
        p_txt = f'p={p:.3f}*'.lstrip('0')                
    else:
        p_txt = f'p={p:.3f}'.lstrip('0') 

    return f'χ² ({dof:,.0f}, N={N:,.0f}) = {chi2:,.2f} {p_txt}'


### Perform chi square test
def results_chi(result
                ,model_parameters
                ,sig_threhold = 0.025):


    p_values = []
    p_values_text = []

    ## converts pandas to array
    for i, row in result.iterrows():
        ## check if chi square valid
        if any([(row['No MECC Training'] >= 5), (row['MECC Trained'] >= 5)]) :
            
            ## sample size
            if 'Total' in str(i):
                N = (model_parameters["N_people"] *
                            model_parameters["num_steps"] *
                            len(model_parameters["visit_prob"]) )
            else:    
                N = (model_parameters["N_people"] *
                            model_parameters["num_steps"])
            ## test
            contingency_array = np.array([
                                        [row['No MECC Training']
                                        ,(N-row['No MECC Training'])]
                                        ,[row['MECC Trained']
                                        ,(N-row['MECC Trained'])]
                                            ])
            chi2, p, dof, expected = chi2_contingency(contingency_array)

            ## output
            p_values_text.append(chi_square_text(chi2, p, dof,N,sig_threhold))
            p_values.append(p)
        else:
            p_values_text.append('n/a')
            p_values.append(pd.NA)

    sig_column =('*Significant (p<=' +
                f'{sig_threhold:.3f}'.lstrip('0') +
                ')')
    result['p-value'] = p_values
    result[sig_column] = p_values_text

    return  result


### Perform Chi-Square Test for Independence
def results_stage_chi(result
                      ,model_parameters
                      ,sig_threhold = 0.025
                      ,stages=['Pre-contemplation'
                                        ,'Contemplation'
                                        ,'Preparation'
                                        ,'Action']):
    ## concat stages into single regex
    stages = '|'.join(stages)
       
    ## gets N from params
    N = model_parameters["N_people"]   

    ## Takes only rows with a stage
    result_stages = result.iloc[result.index.str.contains(stages, regex=True)].copy()

    ## Calculates total
    result_stages_1 = result_stages.copy()
    result_stages_1['Total'] = (result_stages_1['No MECC Training'] +
                                result_stages_1['MECC Trained'])

    ## Removes those stages with 0/0
    result_stages_1 = result_stages_1[result_stages_1['Total'] != 0]

    ## creates array to calculate chi square without 0/0 stages
    contingency_array = np.array([result_stages_1['No MECC Training']
                                    ,result_stages_1['MECC Trained'] ])

    ## Other results
    result_other = result.iloc[~result.index.str.contains(stages, regex=True)].copy()

    ## Name of significance column    
    sig_column =('*Significant (p<=' +
        f'{sig_threhold:.3f}'.lstrip('0') +
        ')')

    ## Calculate chi square
    try:
        chi2, p, dof, expected = chi2_contingency(contingency_array)

        ## apply result to all, including 0/0 stages
        result_stages['p-value'] = p
        result_stages[sig_column] = result_stages['p-value'].apply(
                lambda p: chi_square_text(chi2, p, dof,N,sig_threhold))
    ## error handling
    except:
        result_stages['p-value'] = pd.NA
        result_stages[sig_column] = 'n/a'

    ## creates columns for other results if they don't exist
    if 'p-value' in result_other.columns:
        pass
    else:
        result_other[sig_column] = ''
        result_other['p-value'] = ''

    ## combines results
    output_results = pd.concat([result_other, result_stages])
    return  output_results


def create_effectiveness_figure(results_no_mecc, results_mecc, step):
    # print(results_mecc)
    fig = make_subplots(
        rows=1, 
        cols=2,
        subplot_titles=(
            'Without MECC Training', 
            'With MECC Training',    
        ),
        specs=[[{}, {}]],
        row_heights=[1]
    )
    
    service_colors = {
        'Job Centre': 'red',
        'Benefits Office': 'blue',
        'Housing Officer': 'purple',
        'Community Hub': 'orange',
        'Pharmacy': 'yellow',
        'GP Practice': 'green'
    }

    services = [s for s in service_colors 
               if f'{s} Effectiveness' in results_mecc.columns]
    
    for service in services:
        fig.add_trace(
            go.Scatter(
                x=results_no_mecc.index[:step+1],
                y=results_no_mecc[f'{service} Effectiveness'][:step+1],
                name=service,
                line=dict(color=service_colors[service], dash='solid'),
                opacity=0.7
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=results_mecc.index[:step+1],
                y=results_mecc[f'{service} Effectiveness'][:step+1],
                name=service,
                line=dict(color=service_colors[service], dash='solid'),
                showlegend=False,
                opacity=0.7
            ),
            row=1, col=2
        )
    
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
        margin=dict(t=40, b=40)
    )
    
    fig.update_xaxes(title_text="Month", row=1, col=1)
    fig.update_xaxes(title_text="Month", row=1, col=2)
    fig.update_yaxes(
        title_text="Effectiveness (0-1 scale)", 
        range=[0, 1.1],
        row=1, col=1
    )
    fig.update_yaxes(
        title_text="Effectiveness (0-1 scale)", 
        range=[0, 1.1],
        row=1, col=2
    )
    
    fig.update_yaxes(matches='y', row=1)
    fig.update_xaxes(matches='x', row=1)
    
    return fig