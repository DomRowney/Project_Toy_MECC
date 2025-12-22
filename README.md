# Toy MECC


*This is a project for the HSMA 6 Hackday on 22nd Oct 2024*

A (toy) model for showing the benefit of Making Every Contact Count (MECC) Training

Build a steamlit app for an Agent Based Simulation

The pop culture 80's references will all be in the form of toy robots.

There is an inital group of people and an inital group of government services

People can have lifestyle factors smoking/drinking/no exercise

People make have a probability of making a quit attempt smoking/drinking/no exercise with a probability of success

People have contact with government services at random

Services have can have MECC training, and therefore a probability that any contact will lead to a Very Brief Intervention

Services with MECC training increase over time with a training rate

A Very Brief Intervention increases the probability that a patient will make a quit attempt

Outputs will be MECC training numbers, number of quit attempts and number of successful quits over time

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

## References

### General

[gov.uk MECC evaluation guide 2020](https://www.gov.uk/government/publications/making-every-contact-count-mecc-practical-resources/mecc-evaluation-guide-2020#step-2-identify-the-existing-evidence-base)


[Comparison of brief interventions in primary care on smoking and excessive alcohol consumption: a population survey in England](https://bjgp.org/content/66/642/e1.short)


### Smoking

[Cochrane Review: Physician advice for smoking cessation](https://pmc.ncbi.nlm.nih.gov/articles/PMC7064045/)

*If an unassisted quit rate of 2% at 12 months in a population of primary care attenders is assumed, we can use the confidence intervals for the minimal intervention subgroup, 1.42 to 1.94, to estimate a number needed to treat for an additional beneficial outcome (NNTB) of 50 ‐ 120. If the background rate of quitting was expected to be 3%, then the same effect size estimate would translate to an NNTB of 35‐80. Using the pooled estimate from combining both intensity subgroups in the primary comparison would raise the lower confidence interval and reduce the upper estimate of the NNTBs.*

*Based on the results of a meta‐analysis incorporating 28 trials and over 20,000 participants, a brief advice intervention is **likely to increase the quit rate by 1 to 3 percentage** points. The quit rate in the control groups in the included studies was very variable, ranging from 1% to 14% across the trials in the primary comparison. However the relative effect of the intervention was much less variable, because trials with low control group quit rates generally had low rates with intervention, and vice versa.*

[Prevalence and correlates of receipt by smokers of general practitioner advice on smoking cessation in England: a cross-sectional survey of adults](https://pmc.ncbi.nlm.nih.gov/articles/PMC8432152/pdf/ADD-116-358.pdf)

[Brief opportunistic smoking cessation interventions:a systematic review and meta-analysis to compareadvice to quit and offer of assistance](https://onlinelibrary.wiley.com/doi/full/10.1111/j.1360-0443.2011.03770.x?casa_token=KzcJE3JQ0cwAAAAA%3A-AKlcnickLE7jbewMjqR7N8z-uKBlEhcVtQV5Md000R_x-dHakikMEqaQUSrP1SW0N9TGGxOhTTDdMkc_A)

*Three trials show strong statistical evidence that offering support for cessation motivates an additional **40–60%** of people to attempt cessation compared to being advised to stop smoking on medical grounds. In all three trials, cessation support was offered without screening for willingness to quit.*


[ONS - Adult smoking habits in the UK: 2023](https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthandlifeexpectancies/bulletins/adultsmokinghabitsingreatbritain/2023)

*Around 6.0 million people aged 18 years and over **(11.9%) smoked cigarettes** in the UK in 2023; this is the lowest proportion of current smokers since records began in 2011, based on our estimates from the Annual Population Survey (APS).*

### Alcohol

[Cochrane - Brief interventions for heavy alcohol users admitted to general hospital wards](https://www.cochranelibrary.com/cdsr/doi/10.1002/14651858.CD005191.pub3/full)



Progress: 
simple mesa simulation
simple streamlit app
integration of mesa and streamlit

TODO:
add MECC details

