import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import math
import re
import base64
from collections import Counter
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([html.Div([html.Div([html.H3("TEXT SIMILARTIES APP")], className='pretty_container',
                                                              style={'text-align': 'center'}),
                                                     # Column_name field
                                                     html.Div([html.H4("Text1")], className='pretty_container'),
                                                     html.Div(
                                                         [dcc.Textarea(id="text1",
                                                                       placeholder="enter text",
                                                                       style={'width': '100%',
                                                                              'height': '100px',
                                                                              'padding': '12px 20px',
                                                                              'box-sizing': 'border-box',
                                                                              'border': '2px solid #ccc',
                                                                              'border-radius': '4px',
                                                                              'background-color': '#f8f8f8',
                                                                              'font-size': '16px',
                                                                              'resize': 'none'})], className='pretty_container'),

                                                     html.Div([html.H4("OR")], className='pretty_container',style={'text-align': 'center'}),
                                                     html.Div([
                                                        dcc.Upload(
                                                            id='upload-text1',
                                                            children=html.Div([
                                                                'Drag and Drop or ',
                                                                html.A('Select File')
                                                            ]),
                                                            style={
                                                                'width': '100%',
                                                                'height': '60px',
                                                                'lineHeight': '60px',
                                                                'borderWidth': '1px',
                                                                'borderStyle': 'dashed',
                                                                'borderRadius': '5px',
                                                                'textAlign': 'center',
                                                                'margin': '10px',
                                                                'background-color': '#d9e6ad'
                                                            },
                                                            # Allow multiple files to be uploaded
                                                            multiple=False
                                                        )]),
                                                     html.Div([html.H4("Text2")], className='pretty_container'),
                                                     html.Div(
                                                         [dcc.Textarea(id="text2",
                                                                       placeholder="enter text",
                                                                       style={'width': '100%',
                                                                              'height': '100px',
                                                                              'padding': '12px 20px',
                                                                              'box-sizing': 'border-box',
                                                                              'border': '2px solid #ccc',
                                                                              'border-radius': '4px',
                                                                              'background-color': '#f8f8f8',
                                                                              'font-size': '16px',
                                                                              'resize': 'none'})],
                                                         className='pretty_container'),
                                                     html.Div([html.H4("OR")], className='pretty_container',style={'text-align': 'center'}),
                                                     html.Div([
                                                        dcc.Upload(
                                                            id='upload-text2',
                                                            children=html.Div([
                                                                'Drag and Drop or ',
                                                                html.A('Select File')
                                                            ]),
                                                            style={
                                                                'width': '100%',
                                                                'height': '60px',
                                                                'lineHeight': '60px',
                                                                'borderWidth': '1px',
                                                                'borderStyle': 'dashed',
                                                                'borderRadius': '5px',
                                                                'textAlign': 'center',
                                                                'margin': '10px',
                                                                'background-color': '#d9e6ad'
                                                            },
                                                            # Allow multiple files to be uploaded
                                                            multiple=False
                                                        )]),
                                                     html.Div(id="text_compare", className='pretty_container',
                                                              style={'border': '1px solid',
                                                                     'background-color': '#eee2c6',
                                                                     'border-style': 'hidden',
                                                                     'border-radius': '10px',
                                                                     'padding': '10px',
                                                                     'box-shadow': '1px 1px 1px 1px grey'}),
                                                     html.Div([html.Button("RUN(click-here)", id="check-button",
                                                                           style={'font-size': '20px',
                                                                                  'text-align': 'center',
                                                                                  'height': '50px',
                                                                                  'width': '325px',
                                                                                  'margin-top': '50px',
                                                                                  'margin-left': '40%',
                                                                                  'background-color': '#ffffff',
                                                                                  'cursor': 'pointer'
                                                                                  })],
                                                              className='pretty_container')],
                                                    className='pretty_container')],
                                          className='pretty_container',
                                          style={'border': '1px solid', 'border-style': 'hidden',
                                                 'border-radius': '10px', 'background-color': '#adbce6',
                                                 'box-shadow': '1px 1px 1px 1px grey',
                                                 'padding': '28px'})
def text_conv_vector(text):
    words = re.compile(r"\w+") #to find all words in a text
    return Counter([x.lower() for x in words.findall(text)])
def clicked(ctx):
    if not ctx.triggered or not ctx.triggered[0]['value']:
        return None
    else:
        return ctx.triggered[0]['prop_id'].split('.')[0]

@app.callback(
    Output('text1', 'value'),
    [Input('upload-text1', 'contents')]
)
def uploaded_text(list_of_contents_text1):
    content_type1, content_string1 = list_of_contents_text1.split(',')
    decoded = base64.b64decode(content_string1)
    return decoded.decode('utf-8')
@app.callback(
    Output('text2', 'value'),
    [Input('upload-text2', 'contents')]
)
def uploaded_text(list_of_contents_text2):
    content_type1, content_string1 = list_of_contents_text2.split(',')
    decoded = base64.b64decode(content_string1)
    return decoded.decode('utf-8')


@app.callback(
    Output('text_compare', 'children'),
    [Input("check-button", "n_clicks")],
    [State("text1", "value"), State("text2", "value")])
def text_similarities(n, text1, text2):
    user_clicked = clicked(dash.callback_context)
    # print(u'''clicked = {}'''.format(user_clicked))
    if (n is not None) and (user_clicked == "check-button"):
        try:
            vector1 = text_conv_vector(text1)
            vector2 = text_conv_vector(text2)
            intersection = set(vector1.keys()) & set(vector2.keys())
            numerator = sum([vector1[x] * vector2[x] for x in intersection])  # (A . B)

            sum1 = sum([vector1[x] ** 2 for x in list(vector1.keys())])
            sum2 = sum([vector2[x] ** 2 for x in list(vector2.keys())])
            denominator = math.sqrt(sum1) * math.sqrt(sum2)  # (||A|| ||B||)
            resultText = "The two texts are "
            if not denominator:
                return resultText+str(0.0*100)+" % similar" 
            else:
                return resultText+str(round((float(numerator) / denominator)*100, 2))+" % similar"   # cosine similarity
        except Exception as e:
                value = e.args
                return value


application = app.server
if __name__ == "__main__":
    app.server.run()