import streamlit as st

# For data wrangling
import datetime as dt
import pandas as pd
import numpy as np
from datetime import datetime

# For data visualization
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px

#
st.set_page_config(
                   page_title='Stock Market Dashboard',
                   page_icon='📊',
                   layout="wide",
                   initial_sidebar_state="auto",
                   menu_items=
                    {
                      'About': 'dzakyrafliansyah@gmail.com'
                    })


st.title('Stock Market Dashboard: BAC 2004-2015 Case 📊')

uploaded_file = st.file_uploader("Upload your file here",
                                     type="csv",
                                     help="The file will be used as an input for doing dashboard")

if uploaded_file is not None:
  data = pd.read_csv(uploaded_file, parse_dates=['Date'])
  st.write('You can check the data')
  st.write(data)

  st.write('---'*5)

  st.markdown('# Dashboard Section')
  select_date_slider = st.slider('Select the date accordingly', datetime(2004, 1, 1),
                                 datetime(2015, 12, 31), (datetime(2004, 1, 1), datetime(2004, 1, 5)),
                                 format='YY-MM-DD'
                                )
  col1, col2 = st.columns(2)

  with col1:
    st.markdown('### Trend Over Time')

  # Validating the data
    if 'data' in locals():
      selectbox_column = st.selectbox('Select column you might need here', 
                                       data.columns)
      
      # For slider-validated data                                )
      selected_data = data[data['Date'].between(select_date_slider[0], select_date_slider[1])]

      fig1 = px.line(selected_data,
              x='Date',
              y=selectbox_column)

      st.plotly_chart(fig1, use_container_width=True)
    else:
      st.write('Dashboard cannot be loaded, please upload the data first')

  with col2:
      subcol1, subcol2 = st.columns(2)

      with subcol1:
        st.markdown('### Minimum Value')
        st.write(f"**Lowest value of {selectbox_column} in selected date**")
        st.metric(label='Value',
                  value=selected_data[selectbox_column].min().round(2),
                  delta=None
                  )

      with subcol2:
        st.markdown('### Maximum Value')
        st.write(f"**Highest value of {selectbox_column} in selected date**")

        st.metric(label='Value',
                  value=selected_data[selectbox_column].max().round(2),
                  delta=None
                  )

else:
  st.markdown('**Before continue to dashboard, please upload the data set first :D**')
