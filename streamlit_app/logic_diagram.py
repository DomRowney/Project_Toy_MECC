## logic_diagram.py
import schemdraw
from schemdraw import flow
import streamlit as st

# Set default flowchart box fill colors
flow.Box.defaults['fill'] = '#eeffff'
flow.Start.defaults['fill'] = '#ffeeee'
flow.Decision.defaults['fill'] = '#ffffee'
flow.Circle.defaults['fill'] = '#eeeeee'


#################
## Generic Model
#################
def create_logic_diagram(number_labels = False, session_data = None):

    ## general numberless labels
    lb_N_people = 'Number of\nPeople'
    lb_visit_prob = 'Chance visit\na Service'
    lb_make_intervention =  'Chance Service\nDelivers\nIntervention'                             
    lb_last_month = 'Is Last Month?'

    if number_labels:
        ## for use when session state available, so they update with sliders
        if session_data == None:
            N_people = st.session_state.N_people
            visit_prob = st.session_state.visit_prob
            base_make_intervention_prob = st.session_state.base_make_intervention_prob
            mecc_effect = st.session_state.mecc_effect
            num_steps = st.session_state.num_steps
        ## for use with saved variables in quarto output                                    
        else:
            N_people = session_data['N_people']
            visit_prob = session_data['visit_prob']
            base_make_intervention_prob = session_data['base_make_intervention_prob']
            mecc_effect = session_data['mecc_effect']
            num_steps = session_data['num_steps']

        ## general labels with numbers
        lb_N_people = f'{lb_N_people}\n({N_people})'
        lb_visit_prob = f'{lb_visit_prob}\n({(visit_prob*100):.0f}%)'
        lb_make_intervention =  (f'{lb_make_intervention}\n' +
                             f'({(base_make_intervention_prob*100):.0f}%' +
                             ' or ' +
                             f'{(mecc_effect*100):.0f}%)' 
                             )
        lb_last_month = f'{lb_last_month}\n({num_steps})'

    ## create a drawing class
    with schemdraw.Drawing() as d:
        
        ## Population
        person = flow.Circle(r=d.unit/2).label(lb_N_people).drop("S")
        flow.Arrow().at(person.S).down(d.unit/2)

        m_start = flow.Start().label('Month Start').drop("S")
        
        flow.Arrow().down(d.unit/3).at(m_start.S)
        visit = flow.Decision(S='Visit'
                            ,E='Not Visit').label(lb_visit_prob).drop("S")
        
        flow.Arrow().down(d.unit/2).at(visit.S)

        with d.container() as service_box:
            service_box.linestyle(":")
            service_box.label("Service",loc="NW",halign="left",valign="top")
            visit_start = flow.Start().label('Visit Start').anchor('N')
            flow.Arrow().down(d.unit/3).at(visit_start.S)
            interv = flow.Decision(W='No\nIntervention'
                                ,S='Intervention').label(lb_make_intervention)
            flow.Arrow().down(d.unit/3).at(interv.S)
            interv_result = flow.Box().anchor('N').label('Person has an\nintervention')
            flow.Arrow().down(d.unit/3).at(interv_result.S)
            visit_end = flow.Start().label('Visit End').anchor('N')
            flow.Wire('c',k=-d.unit/3 ,arrow ='->').at(interv.W).to(visit_end.W)

        flow.Wire('c',arrow ='->').at(visit.E).to(visit_end.E)
        flow.Arrow().down(d.unit/2).at(visit_end.S)

        m_end = flow.Start().label('Month End').drop("E")
        flow.Arrow().right(d.unit/3).at(m_end.E)
        last_m = flow.Decision(E='No'
                            ,S='Yes').label(lb_last_month).drop("S")
        flow.Arrow().down(d.unit/3).at(last_m.S)
        model_end = flow.Circle(r=d.unit/2).label('Model End')
        flow.Wire('c',k=d.unit/3,arrow ='->').at(last_m.E).to(m_start.E)

    ## Save the drawing to a temporary file
    img_path = "logic_diagram.png"
    d.save(img_path)
    return img_path



#################
## Smoking Model
#################
def create_logic_diagram_SmokeModel(number_labels = False, session_data = None):
    
    ## general numberless labels
    lb_N_people = 'Number of\nPeople'
    lb_visit_prob = 'Chance visit\na Service'
    lb_make_intervention =  'Chance Service\nDelivers\nIntervention'                             
    lb_last_month = 'Is Last Month?'

    ## smoking numberless labels
    lb_smoking_prob ='Proportion\nof Population\nSmokers'
    lb_quit_attempt_prob = 'Chance Person\nMakes a\nQuit Attempt'
    lb_smoke_relapse_prob = 'Chance Person\nRestarts Smoking'
    lb_intervention_effect = 'Person increases chance\nof making a quit attempt'
    lb_months_smoke_free = ''
    lb_interventions = ''

    if number_labels:
        ## for use when session state available, so they update with sliders
        if session_data == None:
            ## general
            N_people = st.session_state.N_people
            visit_prob = st.session_state.visit_prob
            base_make_intervention_prob = st.session_state.base_make_intervention_prob
            mecc_effect = st.session_state.mecc_effect
            num_steps = st.session_state.num_steps
            ## smoking specific
            initial_smoking_prob = st.session_state.initial_smoking_prob
            intervention_effect = st.session_state.intervention_effect  
            quit_attempt_prob = st.session_state.quit_attempt_prob
            base_smoke_relapse_prob = st.session_state.base_smoke_relapse_prob

        ## for use with saved variables in quarto output                                    
        else:
            ## general
            N_people = session_data['N_people']
            visit_prob = session_data['visit_prob']
            base_make_intervention_prob = session_data['base_make_intervention_prob']
            mecc_effect = session_data['mecc_effect']
            num_steps = session_data['num_steps']
            ## smoking specific
            initial_smoking_prob = session_data['initial_smoking_prob']
            intervention_effect = session_data['intervention_effect']
            quit_attempt_prob = session_data['quit_attempt_prob']
            base_smoke_relapse_prob = session_data['base_smoke_relapse_prob']

        ## general labels with numbers
        lb_N_people = f'{lb_N_people}\n({N_people})'
        lb_visit_prob = f'{lb_visit_prob}\n({(visit_prob*100):.0f}%)'
        lb_make_intervention =  (f'{lb_make_intervention}\n' +
                             f'({(base_make_intervention_prob*100):.0f}%' +
                             ' or ' +
                             f'{(mecc_effect*100):.0f}%)' 
                             )
        lb_last_month = f'{lb_last_month}\n({num_steps})'

        ## smoking labels with numbers
        lb_smoking_prob =f'{lb_smoking_prob}\n({(initial_smoking_prob*100):.0f}%)'
        lb_intervention_effect = (f'{lb_intervention_effect}\n' 
                                  #+ f'({(quit_attempt_prob*100):.0f}%'
                                  + '($\\times$ '
                                  + f'{intervention_effect}$^i$)'
                                    )
        lb_quit_attempt_prob = (f'{lb_quit_attempt_prob}\n'
                                  + f'({(quit_attempt_prob*100):.0f}%'
                                  + ' $\\times$ '
                                  + f'{intervention_effect}$^i$)'
                                    )
        lb_smoke_relapse_prob = (f'{lb_smoke_relapse_prob}\n'
                                 + f'({(base_smoke_relapse_prob*100):.0f}% '
                                 + '$\\times$ 0.95$^m$)'                                 
                                )
        lb_months_smoke_free = '$m$=Months\nSmoke Free' 
        lb_interventions = '$i$=Number\nInterventions'         

    ## create a drawing class
    with schemdraw.Drawing() as d:
        
        ## Population
        person = flow.Circle(r=d.unit/2).label(lb_N_people).drop("S")
        flow.Arrow().at(person.S).down(d.unit/2)

        ## Smokers
        smoke = flow.Decision(E='Not\nSmoker'
                        , W='Smoker').label(lb_smoking_prob).drop("S")
        d.push() ## remembers current location
        flow.Arrow().down(d.unit/2).at(smoke.W)
        is_smoke = flow.Box().label('Smoking Status:\nSmoker').drop("S")
        flow.Arrow().down(d.unit/2).at(smoke.E)

        no_smoke = flow.Box().label('Smoking Status:\nNever Smoked')
        d.pop() ## returns previous remembered location
        d.move(dx=0,dy=-d.unit)

        m_start = flow.Start().label('Month Start').drop("S")
        flow.Wire('n',k=-d.unit/6,arrow ='->').at(is_smoke.S).to(m_start.N)
        flow.Wire('n',k=-d.unit/6,arrow ='->').at(no_smoke.S).to(m_start.N)
        
        flow.Arrow().down(d.unit/3).at(m_start.S)
        visit = flow.Decision(S='Visit'
                            ,E='Not Visit').label(lb_visit_prob).drop("S")
        
        flow.Arrow().down(d.unit/2).at(visit.S)

        with d.container() as service_box:
            service_box.linestyle(":")
            service_box.label("Service",loc="NW",halign="left",valign="top")
            visit_start = flow.Start().label('Visit Start').anchor('N')
            flow.Arrow().down(d.unit/3).at(visit_start.S)
            interv = flow.Decision(W='No\nIntervention'
                                ,S='Intervention').label(lb_make_intervention)
            flow.Arrow().down(d.unit/3).at(interv.S)
            interv_result = (flow.Box().anchor('N').label(lb_intervention_effect)
                                                .label(lb_interventions
                                        , loc='S'
                                        , halign='right',valign='top'
                                        , fontsize=10
                                        , ofst=(-0.2,-0.1)))
            flow.Arrow().down(d.unit/3).at(interv_result.S)
            visit_end = flow.Start().label('Visit End').anchor('N')
            flow.Wire('c',k=-d.unit/3 ,arrow ='->').at(interv.W).to(visit_end.W)

        flow.Wire('c',arrow ='->').at(visit.E).to(visit_end.E)
        flow.Arrow().down(d.unit/2).at(visit_end.S)

        smoke_start = flow.Start().label('Smoking Update Start').anchor('N')
        flow.Arrow().down(d.unit/3).at(smoke_start.S)

        check_smoke = flow.Decision(W='Never\nSmoked'
                                    ,E='Ex-Smoker'
                            ,S='Smoker').label('Is smoker?')
        flow.Arrow().down(d.unit/3).at(check_smoke.S)
        
        quit_attp = (flow.Decision(S='No Quit\nAttempt'
                                    ,E='Quit\nAttempt')
                                    .label(lb_quit_attempt_prob)
                                    .label(lb_interventions
                                        , loc='SW'
                                        , halign='right',valign='top'
                                        , fontsize=10
                                        , ofst=(-0.1,-0.1)))
        flow.Arrow().right(d.unit/1.25).at(quit_attp.E)
        quit_result = flow.Box().anchor('W').label('Smoking Status:\nEx-Smoker')
        flow.Arrow().down(d.unit/3).at(quit_result.S)
        restart_smoke = (flow.Decision(W='No\nRestart'
                            ,S='Restart\nSmoking').label(lb_smoke_relapse_prob)
                                                  .label(lb_months_smoke_free
                                                         , loc='SE'
                                                         , halign='left',valign='top'
                                                         , fontsize=10
                                                         , ofst=(0.1,-0.1)))
        flow.Arrow().down(d.unit/3).at(restart_smoke.S)
        restart_result = flow.Box().anchor('N').label('Smoking Status:\nSmoker')
        flow.Arrow().down(d.unit/3).at(restart_result.S)

        smoke_end = flow.Start().label('Smoking Update End').anchor('N')
        flow.Arrow().down(d.unit/3).at(smoke_end.S)
        d.push() ## remembers current location
        flow.Wire('c',k=d.unit*3,arrow ='->').at(check_smoke.E).to(restart_smoke.E) 
        flow.Wire('c',k=-d.unit*1.25,arrow ='->').at(check_smoke.W).to(smoke_end.W)
        flow.Wire('|-',arrow ='->').at(quit_attp.S).to(smoke_end.W)
        flow.Wire('c',k=-d.unit/3,arrow ='->').at(restart_smoke.W).to(smoke_end.W)

        d.pop() ## returns previous remembered location
        m_end = flow.Start().label('Month End').drop("E")
        flow.Arrow().right(d.unit/3).at(m_end.E)
        last_m = flow.Decision(E='No'
                            ,S='Yes').label(lb_last_month).drop("S")
        flow.Arrow().down(d.unit/3).at(last_m.S)
        model_end = flow.Circle(r=d.unit/2).label('Model End')
        flow.Wire('c',k=d.unit/3,arrow ='->').at(last_m.E).to(m_start.E)

    ## Save the drawing to a temporary file
    img_path = "smoke_logic_diagram.png"
    d.save(img_path)
    return img_path


#################
## Alcohol Model
#################
def create_logic_diagram_Alcohol(number_labels = False, session_data = None):

    
    ## general numberless labels
    lb_N_people = 'Number of\nPeople'
    lb_services_list = ('Services:\n' +                      
                        'Job Centre\n' +
                        'Benefits Office\n' +
                        'Housing Officer\n' +
                        'Community Hub\n' +
                        'Pharmacy\n' +
                        'GP Practice')
    lb_random_service = 'Randomise which\norder to interact\nwith Services'
    lb_visit_prob = 'Chance visit\na Service'
    lb_last_service = 'Is last service?'
    lb_make_intervention =  'Chance Service\nDelivers\nIntervention'
    lb_is_receptive = ('Chance person\n' +
                        'is receptive\n' +
                        'to intervention')
    lb_in_window = 'Is person in\n"Golden Window"\nof intervention?'
    lb_start_window = '"Golden Window": True\n and Timer = 0'
    lb_end_window = ('"Golden Window": False\n'+
                    'and reset to base\n' +
                    'chance status improves')

    lb_window_time_up = 'Is "Golden Window"\nTimer > Length?'

    lb_training_effectivness = ('Service\n'+
                                'MECC Training Effectiveness:\n'+
                                'Reduce intervention chance by half-life\n'+
                                'to minimum of base intervention chance')
    lb_last_period = 'Is Last Period?'

    #lb_inital_state = 'Status:\nPre-Contemplation'
    lb_intervention_effect = ('Add intervention effect\n' +
                              'of service to person\n'+
                              'chance status improves')
    lb_status_box = ('Status Update\n\n' +
                      '*$can\/be\/changed$\n'+
                      '$by\/intervention$')
    lb_change_pre_to_con = 'Chance* status\nimproves'
    lb_change_con_to_prp = 'Chance* status\nimproves'
    lb_change_prp_to_act = 'Chance* status\nimproves'
    lb_lapse_act_to_prp = 'Chance status\nlapses'
    lb_lapse_prp_to_con = 'Chance status\nlapses'
    lb_lapse_con_to_pre = 'Chance status\nlapses'

    lb_status_pre = 'Status:\nPre-Contemplation'
    lb_status_con = 'Status:\nContemplation'
    lb_status_prp = 'Status:\nPreparation'
    lb_status_act = 'Status:\nAction'

    if number_labels:
        ## for use when session state available, so they update with sliders
        if session_data == None:
            ## general
            N_people = st.session_state.N_people
            num_steps = st.session_state.num_steps
            golden_window = st.session_state.alcohol_golden_window
            prob_receptive = st.session_state.alcohol_prob_receptive
        ## for use with saved variables in quarto output                                    
        else:
            ## general
            N_people = session_data['N_people']
            num_steps = session_data['num_steps']
            golden_window = session_data['alcohol_golden_window']
            prob_receptive = session_data['alcohol_prob_receptive']

        ## general labels with numbers
        lb_N_people = f'{lb_N_people}\n({N_people})'
        lb_last_period = f'{lb_last_period}\n({num_steps})'
        lb_is_receptive = f'{lb_is_receptive}\n({prob_receptive})'
        #lb_start_window = f'{lb_start_window}\n(length: {golden_window})'
        lb_window_time_up = f'{lb_window_time_up}\n({golden_window})'

    ## create a drawing class
    with schemdraw.Drawing() as d:
        
        default_len = d.unit/5

        ## Population
        d.push() ## remembers current location
        d.move(dx=-d.unit*2,dy=0)
        services = flow.Circle(r=d.unit/2).label('Services').drop("S")
        flow.Arrow().down(default_len).at(services.S)
        services_list = flow.Box().label(lb_services_list).drop("S")
        flow.Arrow().down(default_len).at(services_list.S)
        training_status = flow.Box().label('Service\nMECC Training Effectiveness:\n' +
                                           ' Intervention chance maximum').drop("S")

        d.pop() ## returns previous remembered location
        person = flow.Circle(r=d.unit/2).label(lb_N_people).drop("S")
        flow.Arrow().at(person.S).down(default_len)

        ## Inital State
        inital_state = flow.Box().label(lb_status_pre).drop("S")
        flow.Arrow().down(default_len*7).at(inital_state.S)
        
        period_start = flow.Start().label('Period Start').drop("S")
        flow.Wire('|-',arrow ='->').at(training_status.S).to(period_start.W)            
        flow.Arrow().down(default_len).at(period_start.S)
        

        ## service
        random_service = flow.Decision(S='').label(lb_random_service).drop("S")
    
        d.pop() ## returns previous remembered location
        flow.Arrow().down(default_len).at(random_service.S)
        service_select = flow.Start(S='').label('Select Service').drop("S")
        flow.Arrow().down(default_len).at(service_select.S)

        visit = flow.Decision(S='Visit'
                            ,W='Not Visit').label(lb_visit_prob).drop("S")        
        flow.Arrow().down(d.unit/2).at(visit.S)
        
        with d.container() as service_box:
            service_box.linestyle(":")
            service_box.label("Service",loc="NW",halign="left",valign="top")
            visit_start = flow.Start().label('Visit Start').anchor('N')
            flow.Arrow().down(default_len).at(visit_start.S)
            interv = flow.Decision(W='No\nIntervention'
                                ,S='Intervention').label(lb_make_intervention)
            flow.Arrow().down(default_len).at(interv.S)

            in_window = flow.Decision(W='Yes'
                                ,S='No').label(lb_in_window)
            flow.Arrow().down(default_len).at(in_window.S)

            check_status = flow.Decision(W='No'
                                ,S='Yes').label("Is status:\nPre-Contemplation?")
            #d.push() ## remembers location
            
            #d.pop() ## returns to push location        
            flow.Arrow().down(default_len).at(check_status.S)

            is_receptive = flow.Decision(E='Not\nReceptive'
                                ,S='Receptive').label(lb_is_receptive)
            flow.Arrow().down(default_len).at(is_receptive.S)
                 
            #flow.Wire('-|',arrow ='->').at(check_status.E).to(check_status.E)

            #flow.Arrow().right().at(check_status.E).to(is_receptive.N)

            start_window = flow.Box().anchor('N').label(lb_start_window)
            flow.Wire('c',k=-default_len ,arrow ='->').at(check_status.W).to(start_window.W)
            flow.Arrow().down(default_len).at(start_window.S)

            #flow.Wire('-|',arrow ='->').at(is_receptive.W).to(start_window.N)
            #flow.Wire('-|',arrow ='->').at(is_receptive.E).to(start_window.N)
                    

            interv_result = flow.Box().anchor('N').label(lb_intervention_effect)
            flow.Wire('c',k=-d.unit/2 ,arrow ='->').at(in_window.W).to(interv_result.W)
            flow.Arrow().down(default_len).at(interv_result.S)


            visit_end = flow.Start().label('Visit End').anchor('N')
            flow.Wire('c',k=-d.unit ,arrow ='->').at(interv.W).to(visit_end.W)
            flow.Wire('c',k=default_len ,arrow ='->').at(is_receptive.E).to(visit_end.E)

        flow.Arrow().down(d.unit/2).at(visit_end.S)
        last_service = flow.Decision(E='No'
                                ,S='Yes').label(lb_last_service)
        flow.Wire('c',k=-d.unit*2,arrow ='->').at(visit.W).to(last_service.W)        
        flow.Wire('c',k=d.unit*1.5,arrow ='->').at(last_service.E).to(service_select.E)
        flow.Arrow().down(d.unit/2).at(last_service.S)

        ## Status update
        with d.container() as status_box:
            status_box.linestyle(":")
            status_box.label(lb_status_box
                             ,loc="NW",halign="left",valign="top")

            status_update_start = flow.Start().label('Status Update Start').anchor('N')
            flow.Arrow().down(default_len).at(status_update_start.S)
            
            ## Pre to Con
            status_pre = (flow.Decision(S='Yes'
                                        ,E='No')
                                        .label('Is status:\nPre-Contemplation?')) 
            flow.Arrow().down(default_len).at(status_pre.S)
            change_pre_to_con = (flow.Decision(W='Improves'
                                        ,E='No\nChange')
                                        .label(lb_change_pre_to_con)) 

            d.push() ## remembers current location
            flow.Arrow().down(d.unit/2).at(change_pre_to_con.W)
            pre_to_con = flow.Box().label(lb_status_con).drop("S")
            flow.Arrow().down(d.unit/2).at(change_pre_to_con.E)
            still_pre = flow.Box().label(lb_status_pre)
            d.pop() ## returns previous remembered location
            d.move(dx=0,dy=-d.unit)

            ## Con to Prp
            status_con = (flow.Decision(S='Yes'
                                        ,W='No')
                                        .label('Is status:\nContemplation?'))         
            flow.Wire('n',k=-default_len,arrow ='->').at(pre_to_con.S).to(status_con.N)
            flow.Wire('n',k=-default_len,arrow ='->').at(still_pre.S).to(status_con.N)
            flow.Wire('c',k=d.unit,arrow ='->').at(status_pre.E).to(status_con.E)
            flow.Arrow().down(default_len).at(status_con.S)
            change_con_to_prp = (flow.Decision(W='Improves'
                                        ,E='No\nChange')
                                        .label(lb_change_con_to_prp)) 

            d.push() ## remembers current location
            flow.Arrow().down(d.unit/2).at(change_con_to_prp.W)
            con_to_prp = flow.Box().label(lb_status_prp).drop("S")
            flow.Arrow().down(d.unit/2).at(change_con_to_prp.E)
            still_con = flow.Box().label(lb_status_con)
            d.pop() ## returns previous remembered location
            d.move(dx=0,dy=-d.unit)

            ## Prp to Act
            status_prp = (flow.Decision(S='Yes'
                                        ,E='No')
                                        .label('Is status:\nPreparation?'))         
            flow.Wire('n',k=-default_len,arrow ='->').at(con_to_prp.S).to(status_prp.N)
            flow.Wire('n',k=-default_len,arrow ='->').at(still_con.S).to(status_prp.N)
            flow.Wire('c',k=-d.unit,arrow ='->').at(status_con.W).to(status_prp.W)
            flow.Arrow().down(default_len).at(status_prp.S)
            change_prp_to_act = (flow.Decision(W='Improves'
                                        ,E='No\nChange')
                                        .label(lb_change_prp_to_act)) 

            d.push() ## remembers current location
            flow.Arrow().down(d.unit/2).at(change_prp_to_act.W)
            prp_to_act = flow.Box().label(lb_status_act).drop("S")
            flow.Arrow().down(d.unit/2).at(change_prp_to_act.E)
            still_prp = flow.Box().label(lb_status_prp)
            d.pop() ## returns previous remembered location
            d.move(dx=0,dy=-d.unit)

            ## Lapse Act to Prp 
            status_act = (flow.Decision(S='Yes'
                                        ,W='No')
                                        .label('Is status:\nAction?'))         
            flow.Wire('n',k=-default_len,arrow ='->').at(prp_to_act.S).to(status_act.N)
            flow.Wire('n',k=-default_len,arrow ='->').at(still_prp.S).to(status_act.N)
            flow.Wire('c',k=d.unit,arrow ='->').at(status_prp.E).to(status_act.E)
            flow.Arrow().down(default_len).at(status_act.S)
            lapse_act_to_prp = (flow.Decision(W='Lapse'
                                        ,E='No\nChange')
                                        .label(lb_lapse_act_to_prp)) 

            d.push() ## remembers current location
            flow.Arrow().down(d.unit/2).at(lapse_act_to_prp.W)
            act_to_prp = flow.Box().label(lb_status_prp).drop("S")
            flow.Arrow().down(d.unit/2).at(lapse_act_to_prp.E)
            still_act = flow.Box().label(lb_status_act)
            d.pop() ## returns previous remembered location
            d.move(dx=0,dy=-d.unit)


            ## Lapse Prp to Con
            status_prp2 = (flow.Decision(S='Yes'
                                        ,E='No')
                                        .label('Is status:\nPreparation?'))         
            flow.Wire('n',k=-default_len,arrow ='->').at(act_to_prp.S).to(status_prp2.N)
            flow.Wire('n',k=-default_len,arrow ='->').at(still_act.S).to(status_prp2.N)
            flow.Wire('c',k=-d.unit,arrow ='->').at(status_act.W).to(status_prp2.W)
            flow.Arrow().down(default_len).at(status_prp2.S)
            lapse_prp_to_con = (flow.Decision(W='Lapse'
                                        ,E='No\nChange')
                                        .label(lb_lapse_prp_to_con)) 

            d.push() ## remembers current location
            flow.Arrow().down(d.unit/2).at(lapse_prp_to_con.W)
            act_to_prp = flow.Box().label(lb_status_con).drop("S")
            flow.Arrow().down(d.unit/2).at(lapse_prp_to_con.E)
            still_prp2 = flow.Box().label(lb_status_prp)
            d.pop() ## returns previous remembered location
            d.move(dx=0,dy=-d.unit)

            ## Lapse Con to Pre
            status_con2 = (flow.Decision(S='Yes'
                                        ,W='No')
                                        .label('Is status:\nContemplation?'))         
            flow.Wire('n',k=-default_len,arrow ='->').at(act_to_prp.S).to(status_con2.N)
            flow.Wire('n',k=-default_len,arrow ='->').at(still_prp2.S).to(status_con2.N)
            flow.Wire('c',k=d.unit,arrow ='->').at(status_prp2.E).to(status_con2.E)
            flow.Arrow().down(default_len).at(status_con2.S)
            lapse_con_to_pre = (flow.Decision(W='Lapse'
                                        ,E='No\nChange')
                                        .label(lb_lapse_con_to_pre)) 

            d.push() ## remembers current location
            flow.Arrow().down(d.unit/2).at(lapse_con_to_pre.W)
            con_to_pre = flow.Box().label(lb_status_pre).drop("S")
            flow.Arrow().down(d.unit/2).at(lapse_con_to_pre.E)
            still_con2 = flow.Box().label(lb_status_con)
            d.pop() ## returns previous remembered location
            d.move(dx=0,dy=-d.unit)

            ## End update
            status_update_end = flow.Start().label('Status Update End').anchor('N')
        flow.Wire('n',k=-d.unit/6,arrow ='->').at(con_to_pre.S).to(status_update_end.N)
        flow.Wire('n',k=-d.unit/6,arrow ='->').at(still_con2.S).to(status_update_end.N)        
        flow.Wire('c',k=-d.unit,arrow ='->').at(status_con2.W).to(status_update_end.W)
        flow.Arrow().down(d.unit*0.75).at(status_update_end.S)

        ## Golden Window update
        with d.container() as window_box:
            window_box.linestyle(":")
            window_box.label('"Golden Window"\nUpdate'
                             ,loc="NW",halign="left",valign="top")

            window_update_start = flow.Start().label('"Golden Window"\nUpdate Start').anchor('N')
            flow.Arrow().down(default_len).at(window_update_start.S)
            in_window2 = flow.Decision(S='Yes'
                                ,W='No').label(lb_in_window)
            flow.Arrow().down(default_len).at(in_window2.S)
            window_time_add = flow.Box().label('"Golden Window"\nTimer +1')
            flow.Arrow().down(default_len).at(window_time_add.S)
            window_time_up = flow.Decision(S='Yes'
                                    ,E='No').label(lb_window_time_up)
            flow.Arrow().down(default_len).at(window_time_up.S)
            end_window = flow.Box().label(lb_end_window)
            flow.Arrow().down(default_len).at(end_window.S)

            window_update_end = flow.Start().label('"Golden Window"\nUpdate End').anchor('N')

            flow.Wire('c',k=-d.unit/3 ,arrow ='->').at(in_window2.W).to(window_update_end.W)
            flow.Wire('c',k=d.unit/3 ,arrow ='->').at(window_time_up.E).to(window_update_end.E)
        flow.Arrow().down(d.unit/2).at(window_update_end.S)

        training_effectivness = flow.Box().label(lb_training_effectivness).drop("S")
        flow.Arrow().down(default_len).at(training_effectivness.S)

        ## End period
        period_end = flow.Start().label('Period End').drop("E")
        flow.Arrow().right(d.unit).at(period_end.E)

        last_period = flow.Decision(E='No'
                            ,S='Yes').label(lb_last_period).drop("S")
        flow.Arrow().down(d.unit/3).at(last_period.S)
        model_end = flow.Circle(r=d.unit/2).label('Model End')
        flow.Wire('c',k=d.unit/3,arrow ='->').at(last_period.E).to(period_start.E)


    ## Save the drawing to a temporary file
    img_path = "alcohol_logic_diagram.png"
    d.save(img_path)
    return img_path