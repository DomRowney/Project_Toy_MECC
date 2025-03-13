## alcohol_outputs.py
import pandas as pd
#import numpy as np
#import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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