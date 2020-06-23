import pandas as pd
import dash
# import packages
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import base64

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Launch the application
app=dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server # the Flask app

image_filename = '9722_UBDC_logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

df = pd.read_csv('health_boards.csv')


#layout of the app
app.layout = html.Div(children = [
    html.Div([ #header div
        html.Div([
            html.H4(html.B('FIND YOUR HEALTH PROTECTION TEAM IN SCOTLAND'),
                    style=dict(lineHeight='7vh', textAlign='center',
                               verticalAlign='middle', color='#a5b1cd'))
        ], style=dict(backgroundColor='#2f3445', width='50%')),
        html.Div([
            html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                     style={'width':'100%', 'height':'100%',
                            'object-fit': 'contain'})
        ], style=dict(backgroundColor='#2f3445',  width='50%',
                      height='80%', margin='10px 10px')),
    ], style=dict(color='white', display='flex',
                  backgroundColor='#2f3445',
                  #borderBottom='thin lightgrey solid',
                  height='10vh')),
    html.Div([
        html.Div('You can only use this service to find health protection \
                  teams in Scotland.'),
        html.Br(),
        html.Div(html.B('Enter a postcode')),
        html.Div('For example AB15 6RE', style=dict(color='grey')),
        dcc.Input(id='pcode-id', value='AB15 6RE', type='text'),
        html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
        html.Div(html.A('Find a postcode on Royal Mail\'s postcode finder',\
                 href='https://www.royalmail.com/find-a-postcode')),
        html.Br(),
        html.Div(id='a-id'),
        html.Div(id='b-id'),
        html.Div(id='c-id')], style=dict(margin='auto', fontSize=24, 
                 width='60%', height='30vh', padding='2%')),
    html.Div([
        html.Div('Contains OS data © Crown copyright and \
                  database rights 2020'),
        html.Div('Contains Royal Mail data © Royal Mail \
                  copyright and database rights 2020'),
        html.Div('Contains National Statistics data © \
                  Crown copyright and database rights 2020')
    ], style=dict(right='2px', bottom='0px', position='fixed'))
])

# interactivity of the app
@app.callback(
    [Output('a-id', 'children'),
     Output('b-id', 'children'),
     Output('c-id', 'children')],
    [Input('submit-button-state', 'n_clicks')],
    [State('pcode-id', 'value')]
)
def postcode_to_health_board(n_clicks, postcode):
    pcod = postcode
    try:
        postcode = postcode.replace(' ', '')
        postcode = postcode.lower()
        hb= df[df['pcd'] == postcode]['HLTHAUNM'].values[0]
    except:
        return 'The postcode "{}" doesn\'t exist in our \
                records'.format(pcod), 'Check it and enter it again', ''
    else:
        officehphone = df[df['pcd'] == postcode]['Office Hours Phone'].values[0]
        outhphone = df[df['pcd'] == postcode]['Out of Hours Phone'].values[0]
        a = 'The health board for the postcode "{}" is "{}"'.format(pcod, hb)
        b = 'Phone: {} (Office hours)'.format(officehphone)
        c = 'Phone: {} (Out of hours, ask for "Public Health")'.format(outhphone)

        return a,b,c

# server clause
if __name__ == '__main__':
    app.run_server(debug=True)
