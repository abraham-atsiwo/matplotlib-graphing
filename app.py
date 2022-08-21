from tkinter import N
import streamlit as st 
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np 
import matplotlib.markers as mpl 
import os


#importing modules from different folders 
#mathplotlib 
def my_line_plotter(ax, col1, col2, df_data=None, param_dict=None):
    out = ax.plot(col1, col2, data=df_data, **param_dict)
    return out
    
def my_scatter_plotter(ax, col1, col2, df_data=None, param_dict=None):
    out = ax.scatter(col1, col2, data=df_data, **param_dict)
    return out
#sidebar
with st.sidebar:
    #browse data
    file_uploaded = st.file_uploader('Upload a Pandas DataFrame', ('txt', 'csv', 'xlsx'))
    plotting_interface = st.selectbox('Plotting Interface', ('Matplotlib', 'Seaborn'))
    plot_type = st.selectbox('Plot Type', ('Scatter', 'Line Plot'))

    if file_uploaded is not None:
        df = pd.read_csv(file_uploaded)
    else:
        df = sns.load_dataset('iris')
    col_names = df.columns
    x_data = st.selectbox('X-Axis', col_names)
    y_data = st.selectbox('Y-Axis', col_names, index=1)

    #optional parameters
    txt_xlabel = st.text_input('X-Label', value=x_data)
    txt_ylabel = st.text_input('Y-Label', value=y_data)
    # txt_chart_color = st.text_input('Chart Color (rgba or color name)')
    txt_chart_color = st.multiselect('Color(s)', 
                    ['red', 'blue', 'green', 'black', 'violet', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'], 
                    ['blue', 'red', 'green'])
    def get_color(col_list):
        col_list = list(col_list)
        if len(col_list) == 0: return 'black'
        nlist = len(col_list)
        ndata = 150
        tmp_list = list(np.repeat(col_list, (ndata // nlist)))
        nremain = ndata - len(tmp_list)
        tmp_list = tmp_list + col_list[:nremain]
        return tmp_list

   


    txt_chart_title = st.text_input('Chart Title', 
                                    value = 'Plot of ' + txt_ylabel + ' vs ' + txt_xlabel)
    



#defining columns 
col1, col2 = st.columns([3, 1])
#column 2 is the
with col2: 
    st.subheader("Plot Parameters")
    #toogle
    multiselect_toggle_list = st.multiselect(
     'Toogle Optional Boolean Parameters',
     ['Grid', 'Visible'],
     ['Grid', 'Visible'])

    def multiselect_toggle_boolean(item):
        if item in multiselect_toggle_list:
            return True
        return False



    def get_marker_key(val):
        for key, value in mpl.MarkerStyle().markers.items():
            if val == value:
                return key
            elif val == 'custom': 
                return get_marker_key(txt_custom_marker)
        return 'o'

    # st.selectbox('Marker', ('Scatteeer', 'Lineeee Plot'))
    select_marker = st.selectbox('MarkerStyle', ('star', 'circle', 'triangle_down', 'plus', 'custom'))
    
    if select_marker == 'custom':
        txt_custom_marker = st.text_input(label='Enter Name')

    #defining line width and alpha 
    numInput_alpha = st.slider(label='Alpha (0, 1)', 
                                    min_value=0.0, 
                                    max_value=1.0, 
                                    value=1.0, 
                                    step=0.05)
                                    
    def get_alpha(value):
        if isinstance(value, float):
            return value
        elif isinstance(value, int):
            return value
        return 1.0

    numInput_linewidth = st.number_input(label='Linewidth',
                                        min_value=0.1, 
                                        max_value=3.0, 
                                        value=1.5, 
                                        step=0.25)

    def get_linewidth(value):
        if value > 0:
            if isinstance(value, float):
                return value
            if isinstance(value, int):
                return value
        return 1.5

    #point sizes
    txt_point_size = st.multiselect('Point Size', 
                    [5, 8, 10, 12, 13, 15, 18, 20, 40, 50], 
                    [5, 8, 20, 50])

    def get_point_size(value):
        pass


#the body content
with col1:

    # st.header("Displaying the Head and Tail of the Data")

    # st.subheader("The head of the Data.")
    # st.dataframe(df.head())

    #Interactive Dashboard
    st.header("Interactive Plot")
    fig, ax = plt.subplots()
    if plotting_interface == 'Matplotlib':
        if plot_type == 'Scatter':
            my_plot =  my_scatter_plotter(ax, x_data, y_data, df_data=df, 
                                          param_dict={'marker': 'o', 
                                                      's': get_color(txt_point_size), 
                                                      'c': get_color(txt_chart_color), 
                                                      'marker': get_marker_key(select_marker), 
                                                      'alpha': get_alpha(numInput_alpha), 
                                                      'linewidths': get_linewidth(numInput_linewidth)})

        elif plot_type == 'Line Plot':
            my_plot =  my_line_plotter(ax, x_data, y_data, df_data=df, param_dict={'marker': 'o'})

    ax.grid(multiselect_toggle_boolean('Grid'))
    ax.set(visible=multiselect_toggle_boolean('Visible'), 
        title=txt_chart_title, xlabel=txt_xlabel, ylabel=txt_ylabel)

    st.pyplot(fig)
    #if ckb_grid:
    #    print('tmp')

    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv = convert_df(df)

    st.download_button(
        label="Download Plot as PNG",
        data=csv,
        file_name='large_df.csv',
        mime='text/csv',
    )




    #Data 
    st.subheader("The tail of the Data.")
    st.dataframe(df.tail())



# st.write(txt_point_size)




