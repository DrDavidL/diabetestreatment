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
    ('6.5', '7', '7.5', '8'), index = 1)

if goalhba1c == '6.5':
    goalhba1c = 6.5
elif goalhba1c == '7':
    goalhba1c = 7.0
elif goalhba1c == '7.5':
    goalhba1c = 7.5
elif goalhba1c == '8':
    goalhba1c = 8.0





lasthba1c = st.sidebar.slider("Select the most recent HbA1c", min_value= 3.0, max_value = 15.0, value = 7.5)

# Pooled Cohort ASCVD Risk Calculation Components
    
sex = st.sidebar.radio(
        "Please select a sex assigned at birth.",
        ('female', 'male'))
race = st.sidebar.radio(
    "Please select a race for ASCVD pooled cohort risk equation. (Note - limited to the options available in the published algorithm.) ",
    ('black', 'white', 'other'))

is_asian = st.sidebar.checkbox('Select if the patient is Asian American (bmi threshold differences)')

age = st.sidebar.slider("Age:", min_value=18, max_value=100, value =50)

tchol = st.sidebar.slider("Total cholesterol in mg/dL.", min_value=80, max_value=320, value =160)


ldl = st.sidebar.slider("LDL cholesterol in mg/dL.", min_value=20, max_value=300, value =110)

tg = st.sidebar.slider("Triglycerides in mg/dL.", min_value=30, max_value=1000, value =200)

hdl = st.sidebar.slider("HDL in mg/dL.", min_value=15, max_value=100, value =40)

sbp = st.sidebar.slider("Current systolic blood pressure in mm Hg.", min_value=80, max_value=200, value =120)

is_htn = st.sidebar.checkbox('HTN: Select if treated for hypertension.')

issmoker = st.sidebar.checkbox('Smoking: Select if the patient smokes.')


isdiabetes = st.sidebar.checkbox('DM: Select if the patient has diabetes.', value = True)



features = {1: ln(age), 2: ln(age)**2, 3: ln(tchol), 4: ln(age)*ln(tchol), 5: ln(hdl), 6: ln(age)*ln(hdl), 
            7: (is_htn + 0)*ln(sbp), 8: (is_htn +0)*ln(age)*ln(sbp), 9: ((not is_htn) + 0)*ln(sbp), 10: ((not is_htn) + 0)*ln(age)*ln(sbp), 11: (issmoker+0),
            12: ln(age)*(issmoker+0), 13: (isdiabetes+0) }

coeff = {1: (17.114, -29.799, 2.469, 12.344), 2: (0, 4.884, 0, 0), 3: (0.94, 13.54, 0.302, 11.853), 4: (0, -3.114, 0, -2.664),
5: (-18.92, -13.578,  -0.307, -7.99), 6: (4.475, 3.149, 0, 1.769), 7: (29.291, 2.019, 1.916, 1.797),  8: (-6.432, 0, 0, 0),
9: (27.82, 1.957, 1.809, 1.764), 10: (-6.087, 0, 0, 0), 11: (0.691, 7.574, 0.549, 7.837), 12: (0,  -1.665, 0, -1.795),
13: (0.874, 0.661,  0.645,  0.658)}

MeanTerms = [86.61, -29.18, 19.54, 61.18]

s10 = [0.9533, 0.9665, 0.8954, 0.9144]

if sex == 'female' and race == 'black':
    flex = 0
elif sex == 'female' and race != 'black':
    flex = 1
elif sex == 'male' and race == 'black':
    flex = 2
else:
    flex = 3

sex_race_coeff = {}

templist = []
for key in coeff:
    templist = coeff[key]
    sex_race_coeff[key] = templist[flex]
    
coefxvalue = {}
for key in features:
    coefxvalue[key] = features[key] * sex_race_coeff[key]
    
sum_coefxvalue = sum(coefxvalue.values())

s10_value = s10[flex]

MeanTerms_value = MeanTerms[flex]

ten_yr_risk = 100* (1- (s10_value)**(2.7182818**(sum_coefxvalue-MeanTerms_value)))

if 19 < age < 80 and 89 < sbp < 201 and 129 < tchol < 321 and 19 < hdl < 101:
    st.sidebar.write('Calculated 10 year ASCVD risk is: ', round(ten_yr_risk,1))
elif 20 > age or 80 < age:
    st.sidebar.write('Age is outside 20-80 range for ASCVD risk calculation.')
elif 90 > sbp or 200 < sbp:
    st.sidebar.write('SBP is outside 90-200 mmHg range for ASCVD risk calculation.')
elif 130 > tchol or 320 < tchol:
    st.sidebar.write('Total cholesterol is outside 130-320 mg/dL range for ASCVD risk calculation.')
elif 20 > hdl or 100 < hdl:
    st.sidebar.write('HDL cholesterol is outside 20-100 mg/dL range for ASCVD risk calculation.')

# st.sidebar.write('Calculated 10 year ASCVD risk is: ', round(ten_yr_risk,1))

# weight = st.number_input('Enter weight in pounds', min_value=75.0, max_value=400.0, value = 160., step = 1.)

weight = st.sidebar.slider("Weight (pounds)", min_value=70, max_value=500, value =180)

height = st.sidebar.slider("Height (inches)", min_value=36, max_value=96, value =67)

# Standard formula for BMI in pounds/inches. Height/weight are more often known than BMI by a patient.

bmi = 703 * weight / height**2

st.sidebar.write('Calculated BMI is: ', round(bmi,1), 'If only BMI known, adjust values as needed to match current BMI.')

# Blocking out creatinine for now and just using egfr. Will add back if needed
# creatinine = st.slider("Last Creatinine", min_value=0.0, max_value = 15.0, value = 1.0)

# Set the egfr variable

egfr = st.sidebar.slider("Last eGFR", min_value= 0.0, max_value = 120.0, value = 59.0)

high_hypoglyc_risk = st.sidebar.radio(
    "High Hypoglycemia Risk",
    ('no', 'yes', 'unknown'), index = 2)

high_insulin_resistance = st.sidebar.radio(
    "High Level of Insulin Resistance",
    ('no', 'yes', 'unknown'), index = 2)

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

is_cad = st.sidebar.checkbox('CAD: Select if the patient had a prior cardiovascular event.')

is_cva = st.sidebar.checkbox('CVA: Select if the patient had a prior cerebrovascular event.')

is_ckd = st.sidebar.checkbox('CKD: Select if the patient has chronic kidney disease.')

is_pad = st.sidebar.checkbox('PAD: Select if the patient has symptomatic peripheral arterial disease.')

is_hf = st.sidebar.checkbox('Heart Failure: Select if the patient has a hstory of heart failure.')

is_proteinuria = st.sidebar.checkbox('Proteinuria: Select if at least over microalbuminuria threshold.')

is_retinopathy = st.sidebar.checkbox('Retinopathy: Select if the patient has diabetic retinopathy.')

is_osteoporosis = st.sidebar.checkbox('Osteoporosis: Select if the patient has osteoporosis.')






# Enter other values required by algorithm. Use streamlit sliders where possible. 





is_insulin = st.sidebar.checkbox('Insulin: Select if patient is taking insulin.')

metformindose = st.sidebar.radio(
    "Metformin:",
    ('Not taking', 'Below max dose', 'Max dose', 'Contraindicated or intolerant'))

sulfonylureadose = st.sidebar.radio(
    "Sulfonylurea:",
    ('Not taking', 'Below max dose', 'Max dose', 'Contraindicated or intolerant'))
    
meglitinidedose = st.sidebar.radio(
    "Meglitinide:",
    ('Not taking', 'Below max dose', 'Max dose', 'Contraindicated or intolerant'))
        
thiazolidinedionedose = st.sidebar.radio(
    "Thiazolidinedione:",
    ('Not taking', 'Below max dose', 'Max dose', 'Contraindicated or intolerant'))
            
aglucosidaseinhdose = st.sidebar.radio(
    "Alpha glucosidase inhibitor:",
    ('Not taking', 'Below max dose', 'Max dose', 'Contraindicated or intolerant'))
                
dpp4idose = st.sidebar.radio(
    "Dipeptidyl Peptidase-4 Inhibitor:",
    ('Not taking', 'Below max dose', 'Max dose', 'Contraindicated or intolerant'))

sglt2idose = st.sidebar.radio(
    "SGLT2 inhibitor:",
    ('Not taking', 'Below max dose', 'Max dose', 'Contraindicated or intolerant'))

glp1agonistdose = st.sidebar.radio(
    "GLP-1 agonist:",
    ('Not taking', 'Below max dose', 'Max dose', 'Contraindicated or intolerant'))


acearbdose = st.sidebar.radio(
    "ACEI or ARB:",
    ('Not taking', 'Below max dose', 'Max dose', 'Contraindicated or intolerant'))
    
statindose = st.sidebar.radio(
    "Statin:",
    ('Not taking', 'Below max dose', 'Max dose', 'Contraindicated or intolerant'))
    
anti_platelet_therapydose = st.sidebar.radio(
    "Anti-platelet therapy",
    ('Not taking daily', 'Taking daily', 'Contraindicated or intolerant'))
        









# Provide some spacing through use of an empty column.

st.write(' ')

#Below is where we calculate all the recommenations.

nextsteps = []
# When to use section.

# Insulin - listed only if A1c > 11.

if lasthba1c > 11 and is_insulin == False:    
    insulin_rec = 'Last A1c value is > 11. Consider adding insulin with close clinical follow-up.'
    nextsteps.append(insulin_rec)

# Here is the metformin logic.
# Based on eGFR and history variables: Don't start or escalate if < 45. Stop if already on and < 30.

# if lasthba1c > goalhba1c:
#     if metformin_ok == True and metforminescalate == True and metformindose == 'Not taking yet':

if lasthba1c > goalhba1c and metformindose != 'Contraindicated or intolerant' and metformindose != 'Max dose' and metforminescalate == True:
    if metformindose == 'Not taking' and metformin_ok == True:
        metformin_rec = 'Metformin: Consider starting. RATIONALE: Above goal Hba1c, not yet taking it, and no contraindications.' 
        nextsteps.append(metformin_rec)
    else:
        if metforminescalate == True:
            metformin_rec = 'Metformin: Consider increasing dose. RATIONALE: Above goal Hba1c and submaximal metformin dose.'
            nextsteps.append(metformin_rec)   
    
if metformin_ok == False:
    if metformindose == 'Max dose' or metformindose == 'Below max dose':
        metformin_rec = "Metformin: STOP the metformin -- check the eGFR value."
        nextsteps.append(metformin_rec)
        
# GLP1 Logic

if lasthba1c > goalhba1c and glp1agonistdose != 'Contraindicated or intolerant' and glp1agonistdose != 'Max dose':
    if glp1agonistdose == 'Not taking' and metformindose =='Max dose' and dpp4idose == 'Not taking':
        glp1agonist_rec = 'GLP-1 agonist: Consider starting. RATIONALE: Above goal Hba1c, metformin is at maximal dose, and no use of DPP-4 inhibitor.' 
        nextsteps.append(glp1agonist_rec)
        if is_ckd == True or egfr < 60:
            glp1agonist_rec = "GLP-1 agonist: Consider for reason of CKD."
            nextsteps.append(glp1agonist_rec)
    if glp1agonistdose == 'Below max dose':
        glp1agonist_rec = "GLP-1 agonist: Consider increasing GLP-1 agonist dose. RATIONALE: Above goal Hba1c, submaximal dose, and no contraindications."
        nextsteps.append(glp1agonist_rec)   
if bmi >= 30:
    glp1agonist_rec = "GLP-1 agonist: Consider for obesity for BMI > 30."
    nextsteps.append(glp1agonist_rec)

if bmi >= 27 and bmi < 30 and isdiabetes == True:
    glp1agonist_rec = "GLP-1 agonist: Consider adding since BMI >= 27 and diabetes is present."
    nextsteps.append(glp1agonist_rec)
        
# SGLT2i logic

if lasthba1c > goalhba1c and sglt2idose != 'Contraindicated or intolerant' and sglt2idose != 'Max dose' and sglt2i_ok == True:
    if sglt2idose == 'Not taking' and egfr > 29:
        sglt2i_rec = 'SGLT2i: Consider starting an SGLT2 inhibitor (CHECK specific SGLT2i for eGFR dosing guidance.) RATIONALE: Above goal Hba1c, not yet taking it, and no contraindications.' 
        nextsteps.append(sglt2i_rec)
        if is_ckd == True or 30 < egfr < 60:
            sglt2i_rec = "SGLT2i: SGLT2 inhibitor also suggested for reason of CKD."
            nextsteps.append(sglt2i_rec)
        if is_hf == True:
            sglt2i_rec = "SGLT2i: SGLT2 inhibitor also suggested for reason of heart failure."
            nextsteps.append(sglt2i_rec)
    if sglt2idose == 'Below max dose':
        sglt2i_rec = "SGLT2i: Consider increasing SGLT2 inhibitor dose. RATIONALE: Above goal Hba1c, submaximal dose, and no contraindications."
        nextsteps.append(sglt2i_rec)   

if sglt2idose == 'Not taking' and egfr > 29 and is_hf == True:
    sglt2i_rec = 'SGLT2i: Consider starting an SGLT2 inhibitor for heart failure independent of diabetes control. (CHECK specific SGLT2i for eGFR dosing guidance.) RATIONALE: Improved heart failure outcomes.' 
    nextsteps.append(sglt2i_rec)    


if sglt2i_ok == False:
    if sglt2idose == 'Max dose' or sglt2idose == 'Below max dose':
        sglt2i_rec = "SGLT2i: Check whether the specific SGLT2i should continue with current eGFR."
        nextsteps.append(sglt2i_rec)
        

# Here is DPP4 logic
# If taking GLP-1 agonist and DPP4inh, the DPP4 should be stopped.

if dpp4idose == "Below max dose" or dpp4idose == 'Max dose':
    if glp1agonistdose == "Below max dose" or glp1agonistdose == 'Max dose':
        dpp4i_rec = "DPP-4 inhibitor: Consider stopping. The patient is on a GLP-1 agonist so there is no added benefit from the DPP-4 inhibitor."
        nextsteps.append(dpp4i_rec)
    elif egfr < 59:
        dpp4i_rec = "DPP-4i: Renal function is abnormal. Ensure dpp4i dosing is appropriate for agent used."



# Needs intolerant logic for metformin and SGLT2i.
            
if dpp4idose == "Not taking" or dpp4idose == 'Below max dose':
    if lasthba1c > goalhba1c and sglt2idose == 'Max dose' and metformindose == 'Max dose' and glp1agonistdose == 'Contraindicated or intolerant':
        if dpp4idose == 'Not taking':
            dpp4i_rec = "DPP-4i: Consider starting a DPP-4 inhibitor. RATIONALE: Metformin dose is max, SGLT2i dose is max and adding a GLP-1 agonist is not possible."
            nextsteps.append(dpp4i_rec)
        if dpp4i_rec == 'Below max dose':
            dpp4i_rec = "DPP-4i: Consider increasing the DPP-4 inhibitor dose. RATIONALE: Metformin dose is max, SGLT2i dose is max and adding a GLP-1 agonist is not possible."
            nextsteps.append(dpp4i_rec)

# Suflonylurea logic:

if sulfonylureadose == 'Below max dose' or sulfonylureadose == 'Max dose':
    if egfr < 60:
        sulfonylurea_rec = "Sulfonylurea: Renal function is abnormal. Ensure sulfonylurea dosing is appropriate. Consider maximizing alternative agents better associated with improved outcomes." 
        nextsteps.append(sulfonylurea_rec)
    else:
        sulfonylurea_rec = "Sulfonylurea: Assess continued use of sulfonylurea in context of alternative agents better associated with improved outcomes." 
        nextsteps.append(sulfonylurea_rec)

# Meglitinide logic:

if meglitinidedose == 'Below max dose' or meglitinidedose == 'Max dose':
    if egfr < 60:
        meglitinide_rec = "Meglitinide: Renal function is abnormal. Ensure meglitinide dosing is appropriate. Consider maximizing alternative agents better associated with improved outcomes." 
        nextsteps.append(meglitinide_rec)
    else:
        meglitinide_rec = "Meglitinide: Assess continued use of meglitinide in context of alternative agents better associated with improved outcomes." 
        nextsteps.append(meglitinide_rec)


# Thiazolidinedione logic

if thiazolidinedionedose == 'Below max dose' or thiazolidinedionedose == 'Max dose':
    if is_osteoporosis == True: 
        thiazolidinedione_rec = 'Thiazolidinedione: Consider stopping thiazolidinediones in presence of osteoporosis.'
        nextsteps.append(thiazolidinedione_rec)
        
# Alpha-glucosidase inhibitors

if aglucosidaseinhdose == 'Below max dose' or aglucosidaseinhdose == 'Max dose':
    if egfr < 60:
        aglucosidaseinh_rec = "Alpha-Glucosidase Inhibitor: Renal function is abnormal. Ensure alpha-glucosidase inhibitor dosing is appropriate. Consider maximizing alternative agents better associated with improved outcomes." 
        nextsteps.append(aglucosidaseinh_rec)
    else:
        aglucosidaseinh_rec = "Alpha-Glucosidase Inhibitor: Assess continued use of alpha-glucosidase inhibitor in context of alternative agents better associated with improved outcomes." 
        nextsteps.append(aglucosidaseinh_rec)
        
# Here is weight loss surgery discussion with different cutoff for Asian American.

considersurgery = False

if bmi >= 40:
    considersurgery = True
else:
    if bmi >= 37.5 and is_asian == True:
        considersurgery = True

if considersurgery == True:
    surgery_rec = 'Surgery: Consider evaluation for weight loss surgery. RATIONALE: BMI above race-based cutoff for consideration.' 
    nextsteps.append(surgery_rec)
    
# ACEI and ARB 
# Still needs proteinuria and other renal ranges covered.

if is_proteinuria == True and isdiabetes == True and is_htn == True:
    if acearbdose == "Not taking":
        if egfr > 20 and egfr < 60:
            acearb_rec = 'ACEI/ARB: Consider addition of an ACEI or ARB given presence of CKD, proteinuria, hypertension, and diabetes. Dose adjust for eGFR per individual agent.'
            nextsteps.append(acearb_rec)
        if egfr <=20:
            acearb_rec = 'ACEI/ARB: Discuss management with nephrologist regarding usage of ACEI/ARB with very low eGFR in context of proteinuria, DM, and HTN.'
            nextsteps.append(acearb_rec)
        if egfr >= 60:
            acearb_rec = 'ACEI/ARB: Consider addition of an ACEI or ARB given presence of proteinuria, hypertension, and diabetes.'
            nextsteps.append(acearb_rec)
 
if is_proteinuria == False and isdiabetes == True and is_htn == True:
    if acearbdose == "Not taking":
        if egfr > 20 and egfr < 60:
            acearb_rec = 'ACEI/ARB: Consider addition of an ACEI or ARB given presence of CKD, hypertension, and diabetes. Dose adjust for eGFR per individual agent.'
            nextsteps.append(acearb_rec)
        if egfr <=20:
            acearb_rec = 'ACEI/ARB: Discuss management with nephrologist regarding usage of ACEI/ARB with very low eGFR in context of DM, and HTN.'
            nextsteps.append(acearb_rec)
        if egfr >= 60:
            acearb_rec = 'ACEI/ARB: Consider addition of an ACEI or ARB given presence of hypertension and diabetes.'
            nextsteps.append(acearb_rec)
 
            

# anti-platelet therapy Recs

if ten_yr_risk > 10 and anti_platelet_therapydose == 'Not taking daily' and is_cad == False and 39 < age < 60 and is_pad == False and is_cva == False:
    anti_platelet_therapy_rec = 'Anti-platelet therapy: Discuss with patient regarding daily anti-platelet therapy for primary ASCVD prevention. The 10 year ASCVD risk is above 10 AND age is 40 - 59.'
    nextsteps.append(anti_platelet_therapy_rec)
    
if anti_platelet_therapydose == 'Not taking daily':
    if is_cad == True:
        anti_platelet_therapy_rec = 'Anti-platelet therapy: Given CAD event history, consider adding anti-platelet therapy for secondary prevention.'
        nextsteps.append(anti_platelet_therapy_rec)
    if is_cva == True:
        anti_platelet_therapy_rec = 'Anti-platelet therapy: Given CVA event history, consider adding anti-platelet therapy for secondary prevention.'
        nextsteps.append(anti_platelet_therapy_rec)
    if is_pad == True:
        anti_platelet_therapy_rec = 'Anti-platelet therapy: Given symptomatic PAD, consider adding anti-platelet therapy for reduced morbidity.'
        nextsteps.append(anti_platelet_therapy_rec)
# Statin recs
    
if ten_yr_risk > 10 and statindose == 'Not taking':
    if is_cad == False: 
        statin_rec = 'Statin: Consider a statin for primary ASCVD prevention. The 10 year ASCVD risk is above 10.'
        nextsteps.append(statin_rec)
        
if statindose == 'Not taking':
    if is_cad == True:  
        statin_rec = 'Statin: Given CAD event history, consider adding a statin for secondary ASCVD prevention.'
        nextsteps.append(statin_rec)
    if is_cva == True:  
        statin_rec = 'Statin: Given CVA event history, consider adding a statin for secondary ASCVD prevention.'
        nextsteps.append(statin_rec)
    if is_pad == True:  
        statin_rec = 'Statin: Given symptomatic PAD, consider adding a statin for secondary ASCVD prevention.'
        nextsteps.append(statin_rec)


# Provide diabetes care considerations!


st.markdown('## *Care Considerations:*')

if is_possible_pregnant == True:
    possible_preg_rec = """ Specific recommendations through this tool are not possible for pregnant or possibly pregnant patients. \
        Most patients with type 2 diabetes are treated during pregnancy with multiple daily insulin injections. \
        Metformin and possibly glyburide may be continued or utilized when sufficient. Specialist expertise should be sought for management. \
    """
    nextsteps= []
    nextsteps.append(possible_preg_rec)

i = 0
while i < len(nextsteps):
    st.markdown('### ' + str(i+1) + ': ' + nextsteps[i])
    i += 1 

st.write("Always reinforce [diet and exercise guidance.](https://www.niddk.nih.gov/health-information/diabetes/overview/diet-eating-physical-activity)")

st.write("Review evidence [here.](https://professional.diabetes.org/sites/professional.diabetes.org/files/media/soc_2022_evidence_table.pdf)")



st.markdown('## *Input Summary: A1c Goal, ASCVD Risk and Existing Medications Prior to any Changes:*')

st.write('Target HbA1c: ', + goalhba1c)

st.write('Most recent HbA1c: ', + lasthba1c)

if 19 < age < 80 and 89 < sbp < 201 and 129 < tchol < 321 and 19 < hdl < 101:
    st.write('Calculated 10 year ASCVD risk is: ', round(ten_yr_risk,2))
elif 20 > age or 80 < age:
    st.write('Age is outside 20-80 range for ASCVD risk calculation.')
elif 90 > sbp or 200 < sbp:
    st.write('SBP is outside 90-200 mmHg range for ASCVD risk calculation.')
elif 130 > tchol or 320 < tchol:
    st.write('Total cholesterol is outside 130-320 mg/dL range for ASCVD risk calculation.')
elif 20 > hdl or 100 < hdl:
    st.write('HDL cholesterol is outside 20-100 mg/dL range for ASCVD risk calculation.')


st.write('Current DM Medication Class Status:')

if is_insulin == True:
    st.markdown(' - ***Insulin:*** Taking')
else:
    st.markdown(' - ***Insulin:*** Not taking')

st.markdown(' - ***Metformin:***  ' + metformindose)
st.markdown(' - ***SGLT2 inh:***  ' + sglt2idose)
st.markdown(' - ***GLP-1 agonist:***  ' + glp1agonistdose)
st.markdown(' - ***DPP-4 inh:***  ' + dpp4idose)
st.markdown(' - ***Meglitinide:***  ' + meglitinidedose)
st.markdown(' - ***Sulfonylurea:***  ' + sulfonylureadose)
st.markdown(' - ***Alpha-glucosidase inh:***  ' + aglucosidaseinhdose)
st.markdown(' - ***Thiazolidinedione:***  ' + thiazolidinedionedose)

st.write('Additional Medications of Interest:')

st.markdown(' - ***ACEi or ARB:***  ' + acearbdose)
st.markdown(' - ***Statin:***  ' + statindose)
st.markdown(' - ***Anti-platelet therapy:***  ' + anti_platelet_therapydose)


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
    

    


