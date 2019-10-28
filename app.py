import dash
import dash_core_components as dcc
import dash_html_components as html
import os
import request_data as rd
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

filenames = []
filenames.append(os.getcwd() + "/TRdata_oil.json" )
filenames.append(os.getcwd() + "/TRdata_gas.json" )
#df_dict = rd.load_TRTickdata(filenames, ["CLc1", "NGc1"])

final_df = rd.load_TRHistdata(["CLc1","NGc1"], "2016-11-01", "2018-10-31", os.getcwd() + "/TRHist.json")
final_df["CLc1"] = 0.13*final_df["CLc1"]
final_df.rename(columns={"CLc1": "13% CLc1"}, inplace=True)


app.layout = html.Div([
    html.H3('Dashboard'),
    html.H6('Historical data (2016-11-01 to 2018-10-31) collected from Thomson Reuter Refinitiv'),

    html.Div([
        dcc.Graph(id="oil-gas-plot"
         )],
        style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}
        ),

    # html.Div(children=[html.H4(children='Gas Monthly Summary'), rd.generate_table(monthly_summary)],
    #      style={"width": '49%', 'display': 'inline-block'})
    html.Div([
        dcc.Graph(id="gas-summary"
               )],
        style={'display': 'inline-block', 'width': '49%'}
        ),

    html.Div(dcc.DatePickerRange(
            id = 'date-picker',
            min_date_allowed=datetime(2016, 11, 1),
            max_date_allowed=datetime(2018, 10, 31),
            initial_visible_month=datetime(2017,10,31),
            end_date=datetime(2018,10,31)
    ), #className="six columns")
        style={'width': '49%', 'padding': '0px 20px 20px 20px'}),

    html.H6("Tick Data from 2018-10-01 to 2018-12-31"),
    html.Div([dcc.Graph(id='gas-tick')]),

    html.Div(dcc.DatePickerSingle(
                 id = 'tick-date-picker',
                 min_date_allowed=datetime(2018, 10, 1),
                 max_date_allowed=datetime(2018, 12, 31),
                 initial_visible_month=datetime(2018, 10, 1),
                 date=str(datetime(2018, 10, 1))
             ), #className="six columns")
                 style={'width': '49%', 'padding': '0px 20px 20px 20px'})
    ]
    )


@app.callback(
    (dash.dependencies.Output('oil-gas-plot', 'figure')),
    [dash.dependencies.Input('date-picker', "start_date"),
     dash.dependencies.Input('date-picker', "end_date")])
def update_graph(start_date, end_date):

    if start_date is None:
        start_date=datetime(2016,11,1)
    if end_date is None:
        end_date=datetime(2018,10,31)

    sub_df = final_df.loc[start_date:end_date]

    return {
        'data': [go.Scatter(
            x=sub_df.index,
            y=sub_df[i],
            mode = 'lines+markers',
            opacity=0.7,
            marker={
                'size': 1,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ) for i in sub_df.columns],
        'layout': go.Layout(
            xaxis={'title': 'Date'},
            yaxis={'title': 'Price'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            #legend={'x': 0, 'y': 1},
            hovermode='closest')
    }


@app.callback(
    dash.dependencies.Output('gas-tick', 'figure'),
    [dash.dependencies.Input('tick-date-picker', 'date')])
def update_tick(date):

    if date is None:
        date = datetime(2018, 10, 1)

    tick_df = rd.loadTRtickdata("NGc1", date).resample("1s").mean()

    return {
        'data': [go.Scatter(
            x=tick_df.index,
            y=tick_df["Price"],
            mode = 'lines+markers',
            opacity=0.7,
            marker={
                'size': 1,
                'line': {'width': 0.5, 'color': 'blue'}
            },
            name="Price"
        ), go.Scatter(
            x=tick_df.index,
            y=tick_df["Volume"],
            mode = 'lines+markers',
            yaxis="y2",
            opacity=0.7,
            marker={
                'size': 1,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name="Volume"
        )],
        'layout': go.Layout(
            xaxis={'title': 'Date'},
            yaxis={'title': 'Price'},
            yaxis2={'title': "Volume", 'side':'right', 'overlaying': 'y'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            #legend={'x': 0, 'y': 1},
            hovermode='closest')
    }


@app.callback(
    (dash.dependencies.Output('gas-summary', 'figure')),
    [dash.dependencies.Input('date-picker', "start_date"),
     dash.dependencies.Input('date-picker', "end_date")])
def update_summary(start_date, end_date):

    if start_date is None:
        start_date=datetime(2016,11,1)
    if end_date is None:
        end_date=datetime(2018,10,31)

    sub_df = final_df.loc[start_date:end_date]["NGc1"]
    sub_df = sub_df.resample("1M")

    summary_df = pd.DataFrame({"Mean": sub_df.mean(),
                               "Median": sub_df.median(),
                               "Max":  sub_df.max(),
                               "Min":  sub_df.min()})
    return {
        'data': [go.Scatter(
            x=summary_df.index,
            y=summary_df[i],
            mode = 'lines+markers',
            opacity=0.7,
            marker={
                'size': 1,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ) for i in summary_df.columns],
        'layout': go.Layout(
            xaxis={'title': 'Date'},
            yaxis={'title': 'Price'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            #legend={'x': 0, 'y': 1},
            hovermode='closest')
    }



if __name__ == '__main__':
    app.run_server(debug=True)