# Added mould price which is now extracted from SEPARATE ENDPOINT
# thus version has only cellopane with agec and default quantity value is 100
# and it is the next iteration of "with material"

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
medal_material_col,medal_diameter_col, medal_thickness_col = st.columns(3)

with medal_material_col:
    medal_material = st.selectbox(
        "Medal Material",('Zamac', 'Iron', 'Aluminium', 'Brass'))

with medal_diameter_col:
    medal_diameter = st.slider(
        "Medal Diameter (mm)", min_value=50, max_value=100, value=50, step=5)

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

        # "Front Personalization",(            
        # 'Select','Smooth', 'Engraving','Laser Engraving','Black Laser','Enamel', 
        # 'UV Printing','Offset Printing'))

        "Front Personalization",(            
        'Select','Smooth', 'Engraving','Laser Engraving','Black Laser','Enamel', 
        'UV Printing'))
    
    if front_personalisation == "Select":
        front_personalisation = "Unenamel"  
    else:
        front_personalisation = front_personalisation

with back_personalisation_col:
    back_personalisation = st.selectbox(

        # "Back Personalization",(
        #     'Select','Smooth', 'Engraving', 'Laser Engraving', 
        #     'Black Laser', 'Enamel', 'UV Printing', '3M Adhesive',
        #     'Epoxy', 'Grained','Molded Base', 'Non-Slip Felt', 'Offset Printing', 'Wooden plaque'))

        "Back Personalization",(
        'Select','Smooth', 'Engraving','Laser Engraving','Black Laser','Enamel', 
        'UV Printing'))
    
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
   

    finish = st.selectbox("Medal Plating", (
        'Select', 'Shiny Nickel', 'Satin Nickel', 'Shiny Gold', 'Antique Tin', 'Antique Bronze',
        'Antique Gold', 'Antique Silver'
    ))

    if finish == "Select":
        finish = "'Shiny Nickel'" 

# Define allowed finishes for Double Finish
# allowed_double_finish = ['Antique Gold', 'Satin Gold', 'Satin Metal', 'Shiny Gold']


# Double Finish logic
with double_finish_col:
    # if finish in allowed_double_finish:
        double_finish = st.checkbox(
            "Double Plating",
            value=False,
            # help="Double Finish is applicable to 'Antique Gold', 'Satin Gold', 'Satin Metal', 'Shiny Gold' only",
            disabled=False
        )
        double_finish = 'Yes' if double_finish else 'No'
    # else:
    #     double_finish = st.checkbox(
    #         "Double Finish",
    #         value=False,
    #         help="Double Finish is only applicable to 'Antique Gold', 'Satin Gold', 'Satin Metal', 'Shiny Gold'.",
    #         disabled=True
    #     )
    #     double_finish = 'No'


# Second Finish logic
with second_finish_col:
    second_finish_options = (
        # 'Select', 'Antique Bronze', 'Antique Gold', 
        # 'Antique Pewter', 'Antique Silver', 'Antique Tin', 'Patinated Pewter', 
        # 'Satin Gold', 'Satin Metal', 'Satin Nickel', 'Shiny Gold', 'Shiny Metal','Shiny Nickel'

        'Select', 'Shiny Nickel', 'Satin Nickel', 'Shiny Gold', 'Antique Tin', 'Antique Bronze',
        'Antique Gold', 'Antique Silver'

    )

    if double_finish == 'Yes':
        st.selectbox(
            # "Second Finish (auto-selected)",
            "Second Medal Plating",
            second_finish_options,
            index=second_finish_options.index(finish) if finish in second_finish_options else 0,
            disabled=False
        )
        second_finish = finish  # Assign same value as finish
    else:
        second_finish = st.selectbox("Second Medal Plating", second_finish_options, disabled=True)

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
                # "Ribbon Width (mm)", min_value=5, max_value=100, value=20, step=1)
                "Ribbon Width (mm)", min_value=5, max_value=100, value=20, step=5)

        with ribbon_height_col:
            ribbon_height = st.slider(
                # "Ribbon Height (mm)", min_value=5, max_value=150, value=50, step=1)
                "Ribbon Height (mm)", min_value=5, max_value=900, value=50, step=5)
            

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
    packaging_col, quantity_col = st.columns(2)

    with packaging_col:
        packaging = st.selectbox("Packaging",(
            
            'Cellophane with AGEC Logo', 'BTC-313', 'BTL-102', 
            'BTL-103', 'BTT-201', 'Cardboard Box',  'Velvet Pouch'
)
        )

    with quantity_col:
        quantity = st.number_input('Quantity', min_value=30, max_value=10000, value=100, step=100,
                                help='Please enter values from 30 to 10,000')
        

# show_mould_price = st.toggle("Show Mould Price?",value=True, help="Mould price is calculated using quantity = 1")    
show_mould_price = st.toggle("Show Mould Price?",value=True)



# Input JSON
user_inputs = {
    "front_type": front_type,
    "front_no_of_colors": front_no_of_colors,
    "front_personalisation": front_personalisation,
    "back_type": back_type,
    "back_no_of_colors": back_no_of_colors,
    "back_personalisation": back_personalisation,
    # "medal_width": medal_width,
    # "medal_height": medal_height,
    "medal_width": medal_diameter,
    "medal_height": medal_diameter,
    "medal_thickness": medal_thickness,
    "medal_material": medal_material,
    "finish": finish,
    "second_finish": second_finish,
    # "double_finish": double_finish,
    "ribbon_needed": ribbon_needed,
    "ribbon_no_of_colors": ribbon_no_of_colors,
    "ribbon_print": ribbon_print,
    "no_of_ribbon_print_side": no_of_ribbon_print_side,
    "ribbon_width": ribbon_width,
    "ribbon_height": ribbon_height,
    "packaging": packaging,
    # "attachment": attachment,
    "quantity": quantity
}

inputs = json.dumps(user_inputs)

if st.button('Predict', type='primary', help='Predict data'):
    with st.spinner('Getting Model Predictions...'):
        time.sleep(1)
        try:
            response = requests.post(
                'https://ahk-medals-price-prediction.onrender.com/medal_prediction', data=inputs, headers={'Content-Type': 'application/json'}) 
                # 'http://127.0.0.1:8000/medal_prediction', data=inputs, headers={'Content-Type': 'application/json'}) 
            response_data = response.json()

            if 'cost_per_piece' in response_data and 'total_cost' in response_data:
                cost_per_piece = response_data['cost_per_piece']
                total_cost = response_data['total_cost']

                formatted_cost_per_piece = '{:,.2f}'.format(cost_per_piece)
                formatted_total_cost = '{:,.2f}'.format(total_cost)

                st.success(
                    f'**MODEL PREDICTION:**\n\n'
                    f'**Unit Price of the Medal:** {formatted_cost_per_piece} €/pc\n\n'
                    f'**Total Medal Cost:** {formatted_total_cost} €'
                )

                # Optional mould price prediction
                if show_mould_price:
                    mould_input = user_inputs.copy()
                    mould_input['quantity'] = 1

                    mould_response = requests.post(
                        # 'http://127.0.0.1:8000/medal_prediction',
                        # 'https://ahk-medals-price-prediction.onrender.com/medal_prediction',
                        
                        # 'http://127.0.0.1:8000/mould_prediction',
                        'https://ahk-medals-price-prediction.onrender.com/mould_prediction',
                        data=json.dumps(mould_input),
                        headers={'Content-Type': 'application/json'}
                    )
                    mould_data = mould_response.json()

                    if 'cost_per_piece' in mould_data and 'total_cost' in mould_data:
                        # mould_cost = '{:,.2f}'.format(mould_data['total_cost'])
                        mould_cost_float = mould_data['total_cost']
                        mould_cost = '{:,.2f}'.format(mould_cost_float)

                        combined_total = total_cost + mould_cost_float
                        formatted_combined_total = '{:,.2f}'.format(combined_total)


                        st.info(f'**Mould Price:** {mould_cost} €\n\n'
                                f'**Total Cost with Mould:** {formatted_total_cost} € (medals) + {mould_cost} € (mould) = {formatted_combined_total} €')
                    else:
                        st.warning("Could not retrieve mould price.")
                
            else:
                st.error('API response is missing the "result" field.')

        except requests.RequestException as e:
            st.error('Failed to fetch prediction result. Status code: ' +
                    str(response.status_code))
            st.warning(f'Persistent Reason: {e}')