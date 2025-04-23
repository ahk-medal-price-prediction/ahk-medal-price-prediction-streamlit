import streamlit as st
import requests
import json
import time
import warnings
warnings.filterwarnings('ignore')


st.set_page_config(page_title='Medal Prediction App', layout="centered")

st.markdown("<h1 style='text-align: center;'>Medal Unit Price Prediction App</h1>",
            unsafe_allow_html=True)

st.divider()

st.markdown(
    """
    <h6 style='text-align: center; font-family: Arial, sans-serif; color: #b967ff; 
    font-style: italic;'>Design custom medals and get price estimate, powered by Machine Learning.</h6>
    """,
    unsafe_allow_html=True
)

st.subheader('Please enter your inputs:')

# Inputs
# Medal dimensions
medal_width_col, medal_height_col, medal_thickness_col = st.columns(3)

with medal_width_col:
    medal_width = st.slider(
        "Medal Width (mm)", min_value=20, max_value=120, value=20, step=5)

with medal_height_col:
    medal_height = st.slider(
        "Medal Height (mm)", min_value=20, max_value=120, value=5, step=5)

with medal_thickness_col:
    medal_thickness = st.slider(
        "Medal Thickness (mm)", min_value=2, max_value=10, value=2)


# Front and Back type
front_type_col, back_type_col = st.columns(2)

with front_type_col:
    front_type = st.radio("Front Type", ('2D', '3D'))

with back_type_col:
    back_type = st.radio("Back Type", ('2D', '3D'))


# Personalisation
front_personalisation_col, back_personalisation_col = st.columns(2)

with front_personalisation_col:
    front_personalisation = st.selectbox(
        "Front Finish",(            
            'Select','Black Laser', 'Digital Printing', 'Enamel', 'Engraving', 
            'Laser Engraving', 'Offset Printing', 'Openwork', 'Smooth', 'Screen Printing', 
            'Unglazed', 'UV Printing'))
    
    if front_personalisation == "Select":
        front_personalisation = "Unenamel"  
    else:
        front_personalisation = front_personalisation

with back_personalisation_col:
    back_personalisation = st.selectbox(
        "Back Finish",(
            'Select', '3M Adhesive', 'Black Laser', 'Enamel', 'Engraving','Epoxy', 
            'Grained', 'Laser Engraving', 'Molded Base', 'Non-Slip Felt', 'Offset Printing',
            'Openwork',  'Smooth', 'Unglazed', 'UV Printing', 'Wooden plaque'))
    
    if back_personalisation == "Select":
        back_personalisation = "Unenamel"  
    else:
        back_personalisation = back_personalisation


# Number of Colors
front_no_of_colors_col, back_no_of_colors_col = st.columns(2)

with front_no_of_colors_col:
    if front_personalisation == "Enamel":
        front_no_of_colors = st.select_slider(
            "No of Front Enamel Colors", (1,2,3,4,5,6,7,8,9,10,11,12))
    else:
        st.select_slider(
            "No of Front Enamel Colors", (1,2,3,4,5,6,7,8,9,10,11,12),
            value=1, disabled=True)  
        front_no_of_colors = 0

with back_no_of_colors_col:
    if back_personalisation == "Enamel":
        back_no_of_colors = st.select_slider(
            "No of Back Enamel Colors", (1,2,3,4,5,6,7,8))
    else:
        st.select_slider(
            "No of Back Enamel Colors", (1,2,3,4,5,6,7,8),
            value=1, disabled=True)  
        back_no_of_colors = 0



# Finishes
finish_col, second_finish_col, double_finish_col = st.columns(3)

# Finish selection
with finish_col:
    finish = st.selectbox("Medal Finish", (
        'Select','Aluminum', 'Antique Bronze', 'Antique Copper', 'Antique Gold', 
        'Antique Nickel', 'Antique Pewter', 'Antique Silver', 'Antique Tin', 'Black Nickel', 'Brass', 
        'Copper', 'Gun Metal', 'Iron', 'Matt Nickel', 'Matte Black', 'Patinated Bronze', 
        'Patinated Pewter', 'Patinated Silver', 'Patinated Tin', 'Real Gold', 
        'Satin Gold', 'Satin Metal', 'Satin Nickel', 'Shiny Gold', 'Shiny Gun', 
        'Shiny Metal','Shiny Nickel', 'Shiny Silver'

    ))

    if finish == "Select":
        finish = "'Shiny Nickel'" 

# Define allowed finishes for Double Finish
allowed_double_finish = ['Antique Gold', 'Satin Gold', 'Satin Metal', 'Shiny Gold']


# Double Finish logic
with double_finish_col:
    if finish in allowed_double_finish:
        double_finish = st.checkbox(
            "Double Finish",
            value=False,
            help="Double Finish is applicable to 'Antique Gold', 'Satin Gold', 'Satin Metal', 'Shiny Gold' only",
            disabled=False
        )
        double_finish = 'Yes' if double_finish else 'No'
    else:
        double_finish = st.checkbox(
            "Double Finish",
            value=False,
            help="Double Finish is only applicable to 'Antique Gold', 'Satin Gold', 'Satin Metal', 'Shiny Gold'.",
            disabled=True
        )
        double_finish = 'No'


# Second Finish logic
with second_finish_col:
    second_finish_options = (
        'Select', 'Antique Bronze', 'Antique Gold', 
        'Antique Pewter', 'Antique Silver', 'Antique Tin', 'Patinated Pewter', 
        'Satin Gold', 'Satin Metal', 'Satin Nickel', 'Shiny Gold', 'Shiny Metal','Shiny Nickel'

    )

    if double_finish == 'Yes':
        st.selectbox(
            "Second Finish (auto-selected)",
            second_finish_options,
            index=second_finish_options.index(finish) if finish in second_finish_options else 0,
            disabled=True
        )
        second_finish = finish  # Assign same value as finish
    else:
        second_finish = st.selectbox("Second Finish", second_finish_options)

    if second_finish == "Select":
        second_finish = "No"  

 
# Ribbon section

# Ribbon Needed: Toggle
with st.expander("Ribbon Options", expanded= True):
    
    ribbon_needed_toggle = st.toggle('Ribbon Needed?')

    if ribbon_needed_toggle:
        ribbon_needed = 'Needed'
    else:
        ribbon_needed = 'No'

    # If Ribbon is Needed — show the rest of the inputs
    if ribbon_needed == 'Needed':

        ribbon_width_col, ribbon_height_col = st.columns(2)

        # Ribbon Width and Height (assuming mm)
        with ribbon_width_col:
            ribbon_width = st.slider(
                "Ribbon Width (mm)", min_value=5, max_value=100, value=20, step=1)

        with ribbon_height_col:
            ribbon_height = st.slider(
                "Ribbon Height (mm)", min_value=5, max_value=150, value=50, step=1)
            

        ribbon_no_of_colors_col, ribbon_print_col, no_of_ribbon_print_side_col = st.columns(3)
        
        # Number of Ribbon Colors
        with ribbon_no_of_colors_col:
            ribbon_no_of_colors = st.select_slider(
                "Ribbon No Of Colors",
                options=[1, 2, 3, 4]
            )

        # Ribbon Print Type
        with ribbon_print_col:
            ribbon_print = st.selectbox(
                "Ribbon Print Type",
                ['Custom Print', 'Heat Transfer', 'Offset Print', 
                 'Screen Print', 'Sewn', 'Sublimation', 'Velcro']
            )

        # No Of Ribbon Print Side
        with no_of_ribbon_print_side_col:
            no_of_ribbon_print_side = st.select_slider(
                "Number Of Ribbon Print Sides",
                options=[1, 2]
            )


    else:
        # If ribbon is not needed — set default "empty" values
        ribbon_no_of_colors = 0
        ribbon_print = 'No'
        no_of_ribbon_print_side = 0
        ribbon_width = 0
        ribbon_height = 0


# Attachment, Packaging, Quantity
with st.expander("Packaging & Quantity", expanded=True):
    attachment_col, packaging_col, quantity_col = st.columns(3)

    with attachment_col:
        attachment = st.selectbox("Attachment",(
          
            'Select','ATM-1', 'ATM-16', 'ATM-21', 'ATM-23', 'ATM-5Z', 'ATM-9', 
            'Bail', 'Brass cup', 'Chain', 'Clip', 'Foot Attachment', 'HR502', 
            'Pin Attachment', 'Ribbon attachment', 'Ring', 'Screws', 'Studs', 'Suction Cups'
            ))
        
        if attachment == "Select":
            attachment = "No"  

    with packaging_col:
        packaging = st.selectbox("Packaging",(
            
            'Cellophane', 'Cellophane with AGEC Logo', 'BTC-313', 'BTL-102', 
            'BTL-103', 'BTT-201', 'Cardboard Box',  'Velvet Pouch'
)
        )

    with quantity_col:
        quantity = st.number_input('Quantity', min_value=1, max_value=25000, value=1000, step=100,
                                help='Please enter values from 1 to 25000')


# Input JSON
user_inputs = {
    "front_type": front_type,
    "front_no_of_colors": front_no_of_colors,
    "front_personalisation": front_personalisation,
    "back_type": back_type,
    "back_no_of_colors": back_no_of_colors,
    "back_personalisation": back_personalisation,
    "medal_width": medal_width,
    "medal_height": medal_height,
    "medal_thickness": medal_thickness,
    "finish": finish,
    "second_finish": second_finish,
    "double_finish": double_finish,
    "ribbon_needed": ribbon_needed,
    "ribbon_no_of_colors": ribbon_no_of_colors,
    "ribbon_print": ribbon_print,
    "no_of_ribbon_print_side": no_of_ribbon_print_side,
    "ribbon_width": ribbon_width,
    "ribbon_height": ribbon_height,
    "packaging": packaging,
    "attachment": attachment,
    "quantity": quantity
}

inputs = json.dumps(user_inputs)

if st.button('Predict', type='primary', help='Predict data'):
    with st.spinner('Getting Model Predictions...'):
        time.sleep(1)
        try:
            response = requests.post(
                'https://ahk-medals-price-prediction.onrender.com/model_prediction', data=inputs, headers={'Content-Type': 'application/json'}) 
                # 'http://127.0.0.1:8000/model_prediction', data=inputs, headers={'Content-Type': 'application/json'}) 
            response_data = response.json()

            if 'result' in response_data:
                result = response_data['result'][0]
                formatted_result = '{:,}'.format(int(result))
                st.success(
                    f'**MODEL PREDICTION:** The Unit Price of the Medal is **{formatted_result}€/pc**')
            else:
                st.error('API response is missing the "result" field.')

        except requests.RequestException as e:
            st.error('Failed to fetch prediction result. Status code: ' +
                    str(response.status_code))
            st.warning(f'Persistent Reason: {e}')