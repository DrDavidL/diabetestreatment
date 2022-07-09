import streamlit as st
import numpy as np
from numpy import log as ln, mean, true_divide

st.title("Diabetes Care")
st.write('*DRAFT*')
st.write('*DRAFT - NOT FOR CLINICAL USE - Not validated across input ranges*')
# Set page two three columns. First for inputs, 2nd for spacing, and 3rd for outputs and explanation.

col1, col2, col3 = st.columns([2,1,4])

with col1:
    
    # Pick a goal first!
    
    # Set A1c goals!
    
    st.markdown('### First, define your goals!')
    goalhba1c = st.radio(
        "Please select a target HbA1c.",
        ('</= 6', '</= 6.5', '</= 7', '</= 7.5', '</= 8', '</= 8.5', 'Over 8.5'))
    
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
    
    lasthba1c = st.slider("Select the last HbA1c", min_value= 3.0, max_value = 15.0, value = 7.0)
    
       
    metformindose = st.radio(
        "Metformin:",
        ('Contraindicated or intolerant', 'Not taking yet', 'Below max dose', 'Max dose'))

    age = st.slider("Age:", min_value=18, max_value=100, value =50)

    # weight = st.number_input('Enter weight in pounds', min_value=75.0, max_value=400.0, value = 160., step = 1.)

    weight = st.slider("Weight (pounds)", min_value=70, max_value=500, value =150)

    height = st.slider("Height (inches)", min_value=36, max_value=96, value =65)

    # Standard formula for BMI in pounds/inches. Height/weight are more often known than BMI by a patient.

    bmi = 703 * weight / height**2

    st.write('The BMI calculates to ', round(bmi,1))
    
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

    ishtn = st.checkbox('HTN: Select if treated for hypertension.')

    isproteinuria = st.checkbox('Proteinuria: Select if at least over microalbuminuria threshold.')

    isretinopathy = st.checkbox('Retinopathy: Select if the patient has diabetic retinopathy.')


    isCAD = st.checkbox('CAD: Select if the patient has CAD.')
    

    # Set sex and race according to algorithm options available. 

    sex = st.radio(
        "Please select a sex. (Note - limited to the options available in the published algorithm.) ",
        ('female', 'male'))

    race = st.radio(
        "Please select a race. (Note - limited to the options available in the published algorithm.) ",
        ('black', 'white'))

    # Enter other values required by algorithm. Use strealit sliders where possible. 


    sbp = st.slider("Current systolic blood pressure in mm Hg.", min_value=80, max_value=200, value =120)

    glucose = st.slider("Fasting glucose mg/dL.", min_value=60, max_value=300, value =100)

    tchol = st.slider("Total cholesterol in mg/dL.", min_value=80, max_value=300, value =160)

    hdl = st.slider("HDL in mg/dL.", min_value=15, max_value=100, value =40)

    qrs = st.slider("QRS duration in msec.", min_value=55, max_value=200, value =100)

 


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

    # Provide diabetes considerations!


    st.markdown('## *Diabetes Management Considerations:*')
    
    st.write('Your selected goal HbA1c: ' + str(goalhba1c))
    
    st.write('Your next steps: ')
    
    st.write('1. ' + str(nextstep1))
    
    
    st.title(str(round(riskpct,2)) + ' %')

    

    st.markdown('### Summary of inputs:')

    st.write('Age is: ' + str(age))
    race
    sex
    
    st.write('Cr: ' + str(creatinine) + ' mg/dL')
    
    st.write('eGFR: ' + str(egfr) + ' mL/min/m^2')
    
    if isCAD:
        st.write("With CAD")
    else:
        st.write("Without CAD")

    if ishtn:
        st.write("With treated HTN")
    else:
        st.write("Without treated HTN")
    
    st.write('BMI is: ' + str(round(bmi,1)))

    if issmoker:
        st.write('Is a smoker')
    else:
        st.write('Is a non-smoker')
    
    st.write('SBP: ' + str(sbp) + ' mmHg')
    st.write('Total cholesterol: ' + str(tchol) + ' mg/dL')
    st.write('HDL: ' + str(hdl) + ' mg/dL')
    st.write('QRS interval: ' + str(qrs) +' msec')

    st.markdown('### Equation Details:')

    
    st.latex("Risk = 1 - S_{0}^{e^{(IndX - MeanCV)}}")

    st.latex("S_{0} = survival\;(baseline)") 

    st.latex("IndX = sum\;of\;(coefficient\;x\;value)") 

    st.latex("MeanCV = Sex\;and\;race \;specific \;mean \;coefficient \;x \;value") 

    st.markdown('*Reference*:')

    st.markdown('Khan S, Ning H, Shah S, et al. 10-Year Risk Equations for Incident Heart Failure in the General Population. J Am Coll Cardiol. 2019 May, 73 (19) 2388-2397. https://doi.org/10.1016/j.jacc.2019.02.057')

    st.markdown('Github URL: https://github.com/DrDavidL/pcp_hf')
  


