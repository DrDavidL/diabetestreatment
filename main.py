import streamlit as st
import numpy as np
from numpy import log as ln, mean, true_divide

st.title("Type 2 Diabetes Care")

st.write('*DRAFT - NOT FOR CLINICAL USE - Not validated across input ranges*')
# Set page two three columns. First for inputs, 2nd for spacing, and 3rd for outputs and explanation.

col1, col2, col3 = st.columns([6,1,4])

with col1:
    
    # Pick a goal first!
    
    # Set A1c goals!
    
    st.markdown('### First, define your goals!')
    goalhba1c = st.radio(
        "Please select a target HbA1c.",
        ('</= 6', '</= 6.5', '</= 7', '</= 7.5', '</= 8', '</= 8.5'))
    
    if goalhba1c == '</= 6':
        goalhba1c = 6.0
    elif goalhba1c == '</= 6.5':
        goalhba1c = 6.5
    elif goalhba1c == '</= 7':
        goalhba1c = 7.0
    elif goalhba1c == '</= 7.5':
        goalhba1c = 7.5
    elif goalhba1c == '</= 8':
        goalhba1c = 8.0
    elif goalhba1c == '</= 8.5':
        goalhba1c = 8.5

    
    st.markdown('### Next, enter details about your patient!')
    
    lasthba1c = st.slider("Select the most recent HbA1c", min_value= 3.0, max_value = 15.0, value = 7.0)
    
       
    

    age = st.slider("Age:", min_value=18, max_value=100, value =50)

    # weight = st.number_input('Enter weight in pounds', min_value=75.0, max_value=400.0, value = 160., step = 1.)

    weight = st.slider("Weight (pounds)", min_value=70, max_value=500, value =150)

    height = st.slider("Height (inches)", min_value=36, max_value=96, value =65)

    # Standard formula for BMI in pounds/inches. Height/weight are more often known than BMI by a patient.

    bmi = 703 * weight / height**2
    
    # Blocking out creatinine for now and just using egfr. Will add back if needed
    # creatinine = st.slider("Last Creatinine", min_value=0.0, max_value = 15.0, value = 1.0)
    
    # Set the egfr variable
    
    egfr = st.slider("Last eGFR", min_value= 0.0, max_value = 120.0, value = 59.0)
    
    # Determine if metformin is contra-indicated to continue based on egfr
    
    if egfr < 30:
        metforminuse = False
    else:
        metforminuse = True
        
    # Determine if it's OK to dose escalate metformin
    
    if egfr < 45:
        metforminescalate = False
    else: 
        metforminescalate = True
 
        

    # Record whether the patient has HTN, smokes and has DM below. Sets to True. 
    
    is_cad = st.checkbox('CAD: Select if the patient has CAD.')
    
    is_cva = st.checkbox('CVA: Select if the patient had a stroke.')
    
    is_ckd = st.checkbox('CKD: Select if the patient has chronic kidney disease.')
    
    is_pad = st.checkbox('PAD: Select if the patient has peripheral arterial disease.')
    
    is_hf = st.checkbox('Heart Failure: Select if the patient has a hstory of heart failure.')

    is_htn = st.checkbox('HTN: Select if treated for hypertension.')

    is_proteinuria = st.checkbox('Proteinuria: Select if at least over microalbuminuria threshold.')

    is_retinopathy = st.checkbox('Retinopathy: Select if the patient has diabetic retinopathy.')


    
    

    # Set sex and race according to algorithm options available. 

    sex = st.radio(
        "Please select sex assigned at birth.",
        ('female', 'male'))


    # Enter other values required by algorithm. Use strealit sliders where possible. 


    ldl = st.slider("LDL cholesterol in mg/dL.", min_value=20, max_value=300, value =110)

    hdl = st.slider("HDL in mg/dL.", min_value=15, max_value=100, value =40)
    
    tg = st.slider("HDL in mg/dL.", min_value=30, max_value=1000, value =200)
    
    st.markdown('### Please enter existing treatments.')
    
    is_insulin = st.checkbox('Insulin: Select if patient is taking insulin.')
    
    metformindose = st.radio(
        "Metformin:",
        ('Contraindicated or intolerant', 'Not taking', 'Below max dose', 'Max dose'))
    
    sulfonylureadose = st.radio(
        "Sulfonylurea:",
        ('Contraindicated or intolerant', 'Not taking', 'Below max dose', 'Max dose'))
        
    meglitinidedose = st.radio(
        "Meglitinide:",
        ('Contraindicated or intolerant', 'Not taking', 'Below max dose', 'Max dose'))
            
    thiazolidinedionedose = st.radio(
        "Thiazolidinedione:",
        ('Contraindicated or intolerant', 'Not taking', 'Below max dose', 'Max dose'))
                
    aglucosidaseinhdose = st.radio(
        "Alpha glucosidase inhibitor:",
        ('Contraindicated or intolerant', 'Not taking', 'Below max dose', 'Max dose'))
                    
    dpp4inhdose = st.radio(
        "Dipeptidyl Peptidase-4 Inhibitor:",
        ('Contraindicated or intolerant', 'Not taking', 'Below max dose', 'Max dose'))
    
    sgl2inhdose = st.radio(
        "SGLT2 inhibitor:",
        ('Contraindicated or intolerant', 'Not taking', 'Below max dose', 'Max dose'))
    
    glp1agonistdose = st.radio(
        "GLP-1 agonist:",
        ('Contraindicated or intolerant', 'Not taking', 'Below max dose', 'Max dose'))
    
    
    acearbdose = st.radio(
        "ACEI or ARB:",
        ('Contraindicated or intolerant', 'Not taking', 'Below max dose', 'Max dose'))
        
    statindose = st.radio(
        "Statin:",
        ('Contraindicated or intolerant', 'Not taking', 'Below max dose', 'Max dose'))
        
    aspirindose = st.radio(
        "Aspirin",
        ('Contraindicated or intolerant', 'Not taking daily', 'Taking daily'))
        
        



 


with col2:

    # Provide some spacing through use of an empty column.

    st.write(' ')
    
    # Here is the metformin logic.
    # Based on eGFR and history variables: Don't start or escalate if < 45. Stop if already on and < 30.


    if lasthba1c > goalhba1c and metformindose != 'Contraindicated or intolerant' and metformindose != 'Max dose' and metforminescalate == True:
        if metformindose == 'Not taking yet' and metforminuse == True:
            nextstep1 = 'Start metformin!'
        else:
            if metforminescalate == True:
                nextstep1 = 'Increase metformin dose!'
    else: 
        nextstep1 = "Nothing with metformin, at least!"          
        
    if metforminuse == False:
        if metformindose == 'Max dose' or metformindose == 'Below max dose':
            nextstep1 = "STOP METFORMIN -- check the eGFR value"
    
with col3:

    # Provide diabetes care considerations!


    st.markdown('## *Diabetes Management Considerations:*')
    
    st.write('Your selected goal HbA1c: ', + goalhba1c)
    
    st.write('Your next steps: ')
    
    st.write('1. ' + str(nextstep1))
    
    
    

    

    st.markdown('### Summary of inputs:')
    
    st.write('Goal A1c is: ', + goalhba1c)

    st.write('Age is: ' + str(age))
  
    sex
    
   #  st.write('Cr: ' + str(creatinine) + ' mg/dL')
    
    st.write('eGFR: ' + str(egfr) + ' mL/min/m^2')
    
    st.write('The BMI calculates to: ', round(bmi,1))
    
    if is_insulin:
        st.write("Taking Insulin")
    else:
        st.write("Not taking insulin")
    
    if is_cad:
        st.write("With CAD")
    else:
        st.write("Without CAD")

    if is_cva:
        st.write("With stroke history")
    else:
        st.write("Without stroke hstory")
        
    if is_ckd:
        st.write("With chronic kidney disease")
    else:
        st.write("Without CKD")
        
    if is_pad:
        st.write("With periperal arterial disease")
    else:
        st.write("Without PAD")
        
    if is_hf:
        st.write("With heart failure history")
    else:
        st.write("Without heart failure history")
        
    if is_htn:
        st.write("With HTN")
    else:
        st.write("Without HTN")
    
    
    if is_proteinuria:
        st.write("With proteinuria")
    else:
        st.write("Without proteinuria")          
        
    if is_retinopathy:
        st.write("With diabetic retinopathy")
    else:
        st.write("Without diabetic retinopathy")          
    
    st.write('BMI is: ' + str(round(bmi,1)))

    # if issmoker:
    #     st.write('Is a smoker')
    # else:
    #     st.write('Is a non-smoker')
    

    st.write('LDL cholesterol: ' + str(ldl) + ' mg/dL')
    st.write('HDL: ' + str(hdl) + ' mg/dL')
    

    


