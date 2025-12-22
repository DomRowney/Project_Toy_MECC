# Toy MECC

## Summary
+ A toy simulation demonstrating how Very Brief Interventions delivered through services could influence behaviour change of alchohol consumption
+ An agent based simulation model hosted on a Streamlit App that enables the production of Quarto report outputs

### Using the app and models

- Open the [Streamlit app](https://domrowney-project-toy-mecc-streamlit-appapp-n0e5hf.streamlit.app/)
- Change model parameters on the parameters tab and run simulations to explore outputs such as number of people in each behaviour state
- The logic model shows how the simulation works
- Download a report showing the finished results of the simulation

---------

## Background
Making Every Contact Count (MECC) in North East and North Cumbria is used across healthcare, local government, Department of Work & Pensions, charities, etc.

> MECC is an approach to behaviour change that utilises the millions of day-to-day interactions that organisations and people have with other people to encourage changes in behaviour that have a positive effect on the health and wellbeing of individuals, communities and populations. ~ [About MECC](https://www.meccgateway.co.uk/nenc/about)

MECC interventions are difficult to study and the impact difficult to measure so we proposed a simulation approach to allow generation of evidence to support the implementation of MECC training.

The simulation would need to be simple to use and to be flexible for use across the wide range of settings and delivery models MECC has.

The project was initially developed for the HSMA 6 Hackday on 22nd Oct 2024, and further developed as a full [HSMA project](https://hsma.co.uk/previous_projects/hsma_6/H6_6040_benefit_of_MECC_using_ABS/index.html) as part of Cohort 6.

The product is a Streamlit App that shows a proof of concept for the effects of the [Transtheoretical Model](https://www.ncbi.nlm.nih.gov/books/NBK556005/) on behaviour change. No data in existing research could be found on the probablilities of moving between these states. Users must use their expert opinion to determine suitible values.


### Model Overview

+ The model consists of two types of agent: People and Services
  - People have a chance of visiting services
  - Services then have a chance of performing an intervention on people that visit, and can be MECC trained or not
+ With MECC training the interventions can be more frequent and/or more efficacious
+ The model is run twice, simultaneously, once with MECC training and once without. Results can then be compared.
+ Also includes:
  - a period where repeated interventions can have an additive effect
  - decay of efficacy of the MECC training
---------
## Project Structure

### [streamlit_app](https://github.com/DomRowney/Project_Toy_MECC/tree/main/streamlit_app)
Contains the core app. See an output of it running on [Streamlit](https://domrowney-project-toy-mecc-streamlit-appapp-n0e5hf.streamlit.app/)

### [Documents](https://github.com/DomRowney/Project_Toy_MECC/tree/main/Documents)
Contains the presentation delivered as part of the HSMA 6 Cohort Showcase. See the video of the presentation [here](https://youtu.be/U6-_3q_CZtA?feature=shared)

### [environment](https://github.com/DomRowney/Project_Toy_MECC/tree/main/environment)
Contains the YAML file necessary to set up the project in Anaconda

### [Archive](https://github.com/DomRowney/Project_Toy_MECC/tree/main/Archive)
Contains elements of the project that were not used in the final release

### [meta](https://github.com/DomRowney/Project_Toy_MECC/tree/main/meta) and [tests](https://github.com/DomRowney/Project_Toy_MECC/tree/main/tests)
Contain elements used for early testing of the model

---------

## Quick start

1. Create a Python environment and install dependencies (choose one):

	- Conda:

	  ```bash
	  conda env create -f environment/environment.yml -n toy_mecc
	  conda activate toy_mecc
	  pip install -r requirements.txt
	  ```

2. Run the Streamlit app locally:

	```bash
	streamlit run streamlit_app/app.py
	```

3. Run tests:

	```bash
	pytest -q
	```
---------

## License
This project includes a `LICENSE.txt` file at the repository root. See that file for license terms.
