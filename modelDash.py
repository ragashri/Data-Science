import dash
import dash_core_components as dcc
import dash_html_components as html
from sklearn.externals import joblib
import pickle
import gzip
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

playstoreData = pd.read_csv('FinalData.csv')

model = joblib.load('python_dec_tree_model.pkl')


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
	# html.Div('Category: '
	# 	),
    html.H3('Dashboard for GooglePlaystore App rating prediction'),
    html.Br(),
    html.P('Select the category :'),
    html.Br(),
    html.Div([
        dcc.Dropdown(id='dd_cat', options=[
        {'label': i, 'value': i} for i in playstoreData.Category.unique()
    ], placeholder='Category...', style={'height': '30px', 'width': '500px', 'padding': 10}),
    ]),
  # #   html.Div('Content Rating: '
		# # ),
    html.Br(),
    html.P('Select the content rating type:'),
    html.Br(),
    html.Div([
        dcc.Dropdown(id='dd_cont', options=[
        {'label': i, 'value': i} for i in playstoreData['Content Rating'].unique()
    ], placeholder='Content Rating...', style={'height': '30px', 'width': '500px', 'padding': 10})
        # html.Div(id='output-container')

    ]),

    # html.Div([
    #     dcc.Input(id='txt_size',
    # placeholder='Enter a value for Size...',
    # type='text',
    # value='')
    #     ]),
    #  html.Div([
    #     dcc.Input(id='txt_install',
    # placeholder='Enter a value for Installs...',
    # type='text',
    # value='')
    #     ]),
    #   html.Div([
    #     dcc.Input(id='txt_price',
    # placeholder='Enter the price...',
    # type='text',
    # value='')
    #     ])
   html.Br(),
    html.P('Price of the app:'),
    html.Br(),
    # html.Div([
    html.Div([
         dcc.Slider(
        id='sld_price',
        marks={
        # 0: 'Free',
        # 50: '50 $',
        # 100: '100 $',
        # 150: '150 $',
        # 200: '200 $'
        i: '{}'.format(50 * i) for i in range(4)
    },
        min=0,
        max=4,
        step=1,
        value=2,
        updatemode='drag')#,setProps=predict_results)
        ]),
    html.Br(),
    html.P('No. of installs:'),
    html.Br(),
    html.Div([
        dcc.Input(id='inp_inst',type='number')
        ]),
    html.Br(),
    html.P('Size of the app:'),
    html.Br(),
    html.Div([
        dcc.Input(id='inp_size',type='number',min=0,
        max=10000,
        step=20
        )
        ]),
    html.Br(),
   # html.Div([

   #  	html.Button('Submit', id='button'),
    html.H4('Prediction Result::'),
    html.Div(id='op-div')

   #  		])

    	# ])
])


@app.callback(
	Output(component_id='op-div', component_property='children'),
	[Input(component_id='dd_cat', component_property='value'),
	Input(component_id='dd_cont', component_property='value'),
    Input(component_id='sld_price', component_property='value'),
    Input(component_id='inp_inst',component_property='value'),
    Input(component_id='inp_size',component_property='value')])
	# Event('button','click')
    # state=[State(component_id='button',component_property='value')]
# @app.callback(
#     dash.dependencies.Output('output-container', 'children'),
#     [dash.dependencies.Input('dd_cat', 'value')])
# def predict_results(value1,value2):
    # return 'You have selected "{},{}"'.format(value1,value2)
def predict_results(category, contentRating,price,installs,size):
    if((category is  None or category == '') and (contentRating is None or contentRating == '') and (installs==0) and (size==0)):
        return 'Please select the values properly'
    else:
        # return 'You have selected "{},{}"'.format(category,contentRating)
        ###category and content rating encoding
        #find code for category with matching value of input
        print('You have selected "{},{}"'.format(category,contentRating))
        k=playstoreData.loc[:,['Content Rating','Updated_ContentRating']]
        contCode=k.loc[k['Content Rating']==contentRating,'Updated_ContentRating'].unique()[0]
        print(contentRating,contCode)
        l=playstoreData.loc[:,['Category','CategoryUpdated']]
        catCode=l.loc[l['Category']==category,'CategoryUpdated'].unique()[0]
        print(category,catCode)
        print(price)
        print(installs)
        print(size)
        rating=model.predict(np.asarray([catCode,contCode,float(size),installs,price]).reshape(1,-1))[0]
        print(rating)
        return 'Your app may get a rating of : {}'.format(rating)
if(__name__=='__main__'):
    app.run_server(debug=True)
