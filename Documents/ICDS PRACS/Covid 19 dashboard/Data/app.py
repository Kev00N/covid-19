import pandas as pd  
import plotly          
import plotly.express as px

import dash             
from dash import dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])


#---------------------------------------------------------------

df = pd.read_excel("C:/Users/Administrator/Documents/ICDS PRACS/Covid 19 dashboard/Data/coviddata.xlsx")


dff = df.groupby('countriesAndTerritories', as_index=False)[['deaths','cases']].sum()
print (dff[:5])
#---------------------------------------------------------------
app.layout = html.Div([
    html.H1("COVID-19 Cases and Deaths Dashboard", style={'textAlign': 'center'}),  # Title centered
    # Data Table
    html.Div([
        dash_table.DataTable(
            id='datatable_id',
            data=dff.to_dict('records'),
            columns=[{"name": i, "id": i, "deletable": False, "selectable": False} for i in dff.columns],
            editable=False,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            row_selectable="multi",
            row_deletable=False,
            selected_rows=[],
            page_action="native",
            page_current=0,
            page_size=6,
            style_cell_conditional=[
                {'if': {'column_id': 'countriesAndTerritories'}, 'width': '40%', 'textAlign': 'left'},
                {'if': {'column_id': 'deaths'}, 'width': '30%', 'textAlign': 'left'},
                {'if': {'column_id': 'cases'}, 'width': '30%', 'textAlign': 'left'},
            ],
        ),
    ], className='row'),

    # Dropdowns for Line and Pie Charts
    html.Div([
        html.Div([
            dcc.Dropdown(id='linedropdown',
                         options=[{'label': 'Deaths', 'value': 'deaths'}, {'label': 'Cases', 'value': 'cases'}],
                         value='deaths',
                         multi=False,
                         clearable=False),
        ], className='six columns'),

        html.Div([
            dcc.Dropdown(id='piedropdown',
                         options=[{'label': 'Deaths', 'value': 'deaths'}, {'label': 'Cases', 'value': 'cases'}],
                         value='cases',
                         multi=False,
                         clearable=False),
        ], className='six columns'),
    ], className='row'),

    # Manually style to place Line and Pie chart side by side
    html.Div([

        html.Div([
            dcc.Graph(id='linechart'),
        ], style={'display': 'inline-block', 'width': '49%'}),  # Use inline-block and width for side-by-side layout

        html.Div([
            dcc.Graph(id='piechart'),
        ], style={'display': 'inline-block', 'width': '49%'})  # Use inline-block and width for side-by-side layout
    ]),

])


#------------------------------------------------------------------
@app.callback(
    [Output('piechart', 'figure'),
     Output('linechart', 'figure')],
    [Input('datatable_id', 'selected_rows'),
     Input('piedropdown', 'value'),
     Input('linedropdown', 'value')]
)
def update_data(chosen_rows, piedropval, linedropval):
    if len(chosen_rows) == 0:
        df_filterd = dff[dff['countriesAndTerritories'].isin(['China', 'Iran', 'Spain', 'Italy'])]
    else:
        df_filterd = dff[dff.index.isin(chosen_rows)]

    # Pie chart
    pie_chart = px.pie(
        data_frame=df_filterd,
        names='countriesAndTerritories',
        values=piedropval,
        hole=.3,
        labels={'countriesAndTerritories': 'Countries'}
    )

    # Add title to pie chart
    pie_chart.update_layout(
        title=f'Total {piedropval.capitalize()} by Country',
        title_x=0.5  # Center the title
    )

    # Extract list of chosen countries
    list_chosen_countries = df_filterd['countriesAndTerritories'].tolist()

    # Filter original df according to chosen countries for the line chart
    df_line = df[df['countriesAndTerritories'].isin(list_chosen_countries)]

    # Line chart
    line_chart = px.line(
        data_frame=df_line,
        x='dateRep',
        y=linedropval,
        color='countriesAndTerritories',
        labels={'countriesAndTerritories': 'Countries', 'dateRep': 'Date'}
    )

    # Add title to line chart
    line_chart.update_layout(
        title=f'Daily {linedropval.capitalize()} Over Time',
        title_x=0.5,  # Center the title
        uirevision='foo'  # Keep UI interactions like zooming consistent
    )

    return pie_chart, line_chart


#------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)