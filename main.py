import streamlit as st
import numpy as np
from numpy import log as ln, mean, true_divide

# streamlit_app.py


# def check_password():
#     """Returns `True` if the user had the correct password."""

#     def password_entered():
#         """Checks whether a password entered by the user is correct."""
#         if st.session_state["password"] == st.secrets["password"]:
#             st.session_state["password_correct"] = True
#             del st.session_state["password"]  # don't store password
#         else:
#             st.session_state["password_correct"] = False

#     if "password_correct" not in st.session_state:
#         # First run, show input for password.
#         st.text_input(
#             "Password", type="password", on_change=password_entered, key="password"
#         )
#         return False
#     elif not st.session_state["password_correct"]:
#         # Password not correct, show input + error.
#         st.text_input(
#             "Password", type="password", on_change=password_entered, key="password"
#         )
#         st.error("😕 Password incorrect")
#         return False
#     else:
#         # Password correct.
#         return True

# if check_password():
#     st.write("Launching after correct password.")
#     st.button("Click me")



st.title("Type 2 Diabetes Scenario Tool")

st.write('***IN PROGRESS DRAFT - NOT FOR CLINICAL USE***')

  
    # Pick a goal first!
    
    # Set A1c goals!
    
st.sidebar.markdown('### Please enter parameters!')
    
is_possible_pregnant = st.sidebar.checkbox('Select if pregnant, possibly pregnant, or considering pregnancy.')



goalhba1c = st.sidebar.radio(
    "Please select a target HbA1c.",
    ('6.5', '7', '7.5', '8'))

if goalhba1c == '6.5':
    goalhba1c = 6.5
elif goalhba1c == '7':
    goalhba1c = 7.0
elif goalhba1c == '7.5':
    goalhba1c = 7.5
elif goalhba1c == '8':
    goalhba1c = 8.0





lasthba1c = st.sidebar.slider("Select the most recent HbA1c", min_value= 3.0, max_value = 15.0, value = 7.0)

    


age = st.sidebar.slider("Age:", min_value=18, max_value=100, value =50)

# weight = st.number_input('Enter weight in pounds', min_value=75.0, max_value=400.0, value = 160., step = 1.)

weight = st.sidebar.slider("Weight (pounds)", min_value=70, max_value=500, value =150)

height = st.sidebar.slider("Height (inches)", min_value=36, max_value=96, value =65)

# Standard formula for BMI in pounds/inches. Height/weight are more often known than BMI by a patient.

bmi = 703 * weight / height**2

# Blocking out creatinine for now and just using egfr. Will add back if needed
# creatinine = st.slider("Last Creatinine", min_value=0.0, max_value = 15.0, value = 1.0)

# Set the egfr variable

egfr = st.sidebar.slider("Last eGFR", min_value= 0.0, max_value = 120.0, value = 59.0)

# Contraindications Section

# Determine if metformin is contra-indicated to continue based on egfr

if egfr < 30:
    metformin_ok = False
else:
    metformin_ok = True
    
if egfr < 30:
    sglt2i_ok = False
else:
    sglt2i_ok = True
    
# Determine if it's OK to dose escalate metformin

if egfr < 45:
    metforminescalate = False
else: 
    metforminescalate = True

    

# Record whether the patient has HTN, smokes and has DM below. Sets to True. 

is_cad = st.sidebar.checkbox('CAD: Select if the patient has CAD.')

is_cva = st.sidebar.checkbox('CVA: Select if the patient had a stroke.')

is_ckd = st.sidebar.checkbox('CKD: Select if the patient has chronic kidney disease.')

is_pad = st.sidebar.checkbox('PAD: Select if the patient has peripheral arterial disease.')

is_hf = st.sidebar.checkbox('Heart Failure: Select if the patient has a hstory of heart failure.')

is_htn = st.sidebar.checkbox('HTN: Select if treated for hypertension.')

is_proteinuria = st.sidebar.checkbox('Proteinuria: Select if at least over microalbuminuria threshold.')

is_retinopathy = st.sidebar.checkbox('Retinopathy: Select if the patient has diabetic retinopathy.')

is_asian = st.sidebar.checkbox('Select if the patient is Asian American (bmi threshold differences)')





# Set sex and race according to algorithm options available. 

sex = st.sidebar.radio(
    "Please select sex assigned at birth.",
    ('female', 'male'))


# Enter other values required by algorithm. Use strealit sliders where possible. 


ldl = st.sidebar.slider("LDL cholesterol in mg/dL.", min_value=20, max_value=300, value =110)

hdl = st.sidebar.slider("HDL in mg/dL.", min_value=15, max_value=100, value =40)

tg = st.sidebar.slider("HDL in mg/dL.", min_value=30, max_value=1000, value =200)



is_insulin = st.sidebar.checkbox('Insulin: Select if patient is taking insulin.')

metformindose = st.sidebar.radio(
    "Metformin:",
    ('Contraindicated or intolerant', 'Not taking', 'Below max dose', 'Max dose'))

sulfonylureadose = st.sidebar.radio(
    "Sulfonylurea:",
    ('Contraindicated or intolerant', 'Not taking', 'Below max dose', 'Max dose'))
    
meglitinidedose = st.sidebar.radio(
    "Meglitinide:",
    ('Contraindicated or intolerant', 'Not taking', 'Below max dose', 'Max dose'))
        
thiazolidinedionedose = st.sidebar.radio(
    "Thiazolidinedione:",
    ('Contraindicated or intolerant', 'Not taking', 'Below max dose', 'Max dose'))
            
aglucosidaseinhdose = st.sidebar.radio(
    "Alpha glucosidase inhibitor:",
    ('Contraindicated or intolerant', 'Not taking', 'Below max dose', 'Max dose'))
                
dpp4idose = st.sidebar.radio(
    "Dipeptidyl Peptidase-4 Inhibitor:",
    ('Contraindicated or intolerant', 'Not taking', 'Below max dose', 'Max dose'))

sglt2idose = st.sidebar.radio(
    "SGLT2 inhibitor:",
    ('Contraindicated or intolerant', 'Not taking', 'Below max dose', 'Max dose'))

glp1agonistdose = st.sidebar.radio(
    "GLP-1 agonist:",
    ('Contraindicated or intolerant', 'Not taking', 'Below max dose', 'Max dose'))


acearbdose = st.sidebar.radio(
    "ACEI or ARB:",
    ('Contraindicated or intolerant', 'Not taking', 'Below max dose', 'Max dose'))
    
statindose = st.sidebar.radio(
    "Statin:",
    ('Contraindicated or intolerant', 'Not taking', 'Below max dose', 'Max dose'))
    
aspirindose = st.sidebar.radio(
    "Aspirin",
    ('Contraindicated or intolerant', 'Not taking daily', 'Taking daily'))
        
        








# Provide some spacing through use of an empty column.

st.write(' ')

#Below is where we calculate all the recommenations.

nextsteps = []
# When to use section.

# Here is the metformin logic.
# Based on eGFR and history variables: Don't start or escalate if < 45. Stop if already on and < 30.

# if lasthba1c > goalhba1c:
#     if metformin_ok == True and metforminescalate == True and metformindose == 'Not taking yet':
        



if lasthba1c > goalhba1c and metformindose != 'Contraindicated or intolerant' and metformindose != 'Max dose' and metforminescalate == True:
    if metformindose == 'Not taking' and metformin_ok == True:
        metformin_rec = 'Consider starting metformin. RATIONALE: Above goal Hba1c, not yet taking it, and no contraindications.' 
        nextsteps.append(metformin_rec)
    else:
        if metforminescalate == True:
            metformin_rec = 'Consider increasing metformin dose. RATIONALE: Above goal Hba1c and submaximal metformin dose.'
            nextsteps.append(metformin_rec)   
    
if metformin_ok == False:
    if metformindose == 'Max dose' or metformindose == 'Below max dose':
        metformin_rec = "STOP METFORMIN -- check the eGFR value!"
        nextsteps.append(metformin_rec)
        
# SGLT2i logic

if lasthba1c > goalhba1c and sglt2idose != 'Contraindicated or intolerant' and sglt2idose != 'Max dose' and sglt2i_ok == True:
    if sglt2idose == 'Not taking':
        sglt2i_rec = 'Consider starting an SGLT2 inhibitor (CHECK specific SGLT2i for eGFR dosing guidance.) RATIONALE: Above goal Hba1c, not yet taking it, and no contraindications.' 
        nextsteps.append(sglt2i_rec)
        if is_ckd == True or egfr < 60:
            sglt2i_rec = "SGLT2 inhibitor also suggested for reason of CKD."
            nextsteps.append(sglt2i_rec)
        if is_hf == True:
            sglt2i_rec = "SGLT2 inhibitor also suggested for reason of heart failure."
            nextsteps.append(sglt2i_rec)
    if sglt2idose == 'Below max dose':
        sglt2i_rec = "Consider increasing SGLT2 inhibitor dose. RATIONALE: Above goal Hba1c, submaximal dose, and no contraindications."
        nextsteps.append(sglt2i_rec)   

if sglt2i_ok == False:
    if sglt2idose == 'Max dose' or sglt2idose == 'Below max dose':
        sglt2i_rec = "Check whether the specific SGLT2i should continue with current eGFR."
        nextsteps.append(sglt2i_rec)

# Here is DPP4 logic
# If taking GLP-1 agonist and DPP4inh, the DPP4 should be stopped.

if dpp4idose == "Below max dose" or dpp4idose == 'Max dose':
    if glp1agonistdose == "Below max dose" or glp1agonistdose == 'Max dose':
        dpp4i_rec = "Stop DPP-4 inhibitor: The patient is on a GLP-1 agonist so there is no added benefit from the DPP-4 inhibitor."
        nextsteps.append(dpp4i_rec)
            
if dpp4idose == "Not taking" or dpp4idose == 'Below max dose':
    if lasthba1c > goalhba1c and sglt2idose == 'Max dose' and metformindose == 'Max dose' and glp1agonistdose == 'Contraindicated or intolerant':
        if dpp4idose == 'Not taking':
            dpp4i_rec = "Consider starting a DPP-4 inhibitor. RATIONALE: Metformin dose is max, SGLT2i dose is max and adding a GLP-1 agonist is not possible."
            nextsteps.append(dpp4i_rec)
        if dpp4i_rec == 'Below max dose':
            dpp4i_rec = "Consider increasing the DPP-4 inhibitor dose. RATIONALE: Metformin dose is max, SGLT2i dose is max and adding a GLP-1 agonist is not possible."
            nextsteps.append(dpp4i_rec)
        

# Here is weight loss surgery discussion with different cutoff for Asian American.

considersurgery = False

if bmi >= 40:
    considersurgery = True
else:
    if bmi >= 37.5 and is_asian == True:
        considersurgery = True

if considersurgery == True:
    surgery_rec = 'Consider evaluation for weight loss surgery: BMI above race-based cutoff for consideration.' 
    nextsteps.append(surgery_rec)
    
# ACEI and ARB 
# Still needs proteinuria and other renal ranges covered.

if is_htn == True:
    if acearbdose == "Not taking":
        if egfr > 20 and egfr < 60:
            acearb_rec = 'Consider addition of an ACEI or ARB for HTN management in CKD. Dose adjust for eGFR per individual agent.'
            nextsteps.append(acearb_rec)




# Provide diabetes care considerations!


st.markdown('## *Scenario Considerations:*')

st.write('Your selected target HbA1c: ', + goalhba1c)

st.write('Your most recent HbA1c: ', + lasthba1c)


if is_possible_pregnant == True:
    possible_preg_rec = 'Recommendations through this tool are not yet possible for pregnant or possibly pregnant patients.'
    nextsteps= []
    nextsteps.append(possible_preg_rec)

i = 0
while i < len(nextsteps):
    st.markdown('### ' + str(i+1) + ': ' + nextsteps[i])
    i += 1 

st.write("Always reinforce [diet and exercise guidance.](https://www.niddk.nih.gov/health-information/diabetes/overview/diet-eating-physical-activity)")

st.write("Review evidence [here.](https://professional.diabetes.org/sites/professional.diabetes.org/files/media/soc_2022_evidence_table.pdf)")



# st.markdown('### Summary of inputs:')

# st.write('Goal A1c is: ', + goalhba1c)

# st.write('Age is: ' + str(age))

# sexß

# #  st.write('Cr: ' + str(creatinine) + ' mg/dL')

# st.write('eGFR: ' + str(egfr) + ' mL/min/m^2')

# st.write('The BMI calculates to: ', round(bmi,1))

# if is_insulin:
#     st.write("Taking Insulin")
# else:
#     st.write("Not taking insulin")

# if is_cad:
#     st.write("With CAD")
# else:
#     st.write("Without CAD")

# if is_cva:
#     st.write("With stroke history")
# else:
#     st.write("Without stroke hstory")
    
# if is_ckd:
#     st.write("With chronic kidney disease")
# else:
#     st.write("Without CKD")
    
# if is_pad:
#     st.write("With periperal arterial disease")
# else:
#     st.write("Without PAD")
    
# if is_hf:
#     st.write("With heart failure history")
# else:
#     st.write("Without heart failure history")
    
# if is_htn:
#     st.write("With HTN")
# else:
#     st.write("Without HTN")


# if is_proteinuria:
#     st.write("With proteinuria")
# else:
#     st.write("Without proteinuria")          
    
# if is_retinopathy:
#     st.write("With diabetic retinopathy")
# else:
#     st.write("Without diabetic retinopathy")          

# st.write('BMI is: ' + str(round(bmi,1)))

# # if issmoker:
# #     st.write('Is a smoker')
# # else:
# #     st.write('Is a non-smoker')


# st.write('LDL cholesterol: ' + str(ldl) + ' mg/dL')
# st.write('HDL: ' + str(hdl) + ' mg/dL')
    

    


