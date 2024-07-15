import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import Dash, html, dcc, callback
import pandas as pd
import plotly.express as px


#Load and Process data
df = pd.read_csv('hies_district.csv')

def plot_income_district(df, state):
    Extract_1 = df[df['state'] == state][['district', 'income_mean']]
    figure = px.bar(
        Extract_1,
        x='district',
        y='income_mean',
        color='district',
        title=f'Income Mean vs {state} Districts'
    )
    figure.update_layout(title_x=0.5)
    return figure

def plot_poverty_income(df, state):
    Extract_2 = df[df['state'] == state][['income_mean', 'poverty']].sort_values(by='poverty')
    figure = px.line(
        Extract_2,
        x='poverty',
        y='income_mean',
        color_discrete_sequence=['red'],
        title=f'Poverty Rate vs Income Mean for {state}'
    )
    figure.update_layout(title_x=0.5)
    return figure

def plot_expenditure_district(df, state):
    Extract_3 = df[df['state'] == state][['district', 'expenditure_mean']]
    figure = px.bar(
        Extract_3,
        x='district',
        y='expenditure_mean',
        color='district',
        color_discrete_sequence=px.colors.qualitative.Set2,
        title=f'Expenditure Mean vs {state} Districts'
    )
    figure.update_layout(title_x=0.5)
    return figure

def plot_poverty_expenditure(df, state):
    Extract_4 = df[df['state'] == state][['expenditure_mean', 'poverty']].sort_values(by='poverty')
    figure = px.line(
        Extract_4,
        x='poverty',
        y='expenditure_mean',
        color_discrete_sequence=['green'],
        title=f'Poverty Rate vs Expenditure Mean for {state}'
    )
    figure.update_layout(title_x=0.5)
    return figure

#Initialize dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#App Layout
app.layout = html.Div(
    [
        html.H4("Household Income Statistics in Different States of Malaysia",
                style={'textAlign': 'center', 'fontSize': '40px', 'fontWeight': 'bold'}),
        html.P("Select a state...", style={'fontWeight': 'bold', 'fontSize': '150%'}),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id = 'state',
                    options = [{'label': state, 'value': state} for state in ['Johor', 'Kedah', 'Kelantan', 'Melaka',
                                'Negeri Sembilan', 'Pahang', 'Pulau Pinang',
                               'Perak', 'Perlis', 'Selangor', 'Terengganu',
                               'Sabah', 'Sarawak', 'W.P. Kuala Lumpur',
                               'W.P. Labuan', 'W.P. Putrajaya']],
                    style = {'border': '1.5px solid Black', 'align-items': 'left', 'fontSize': '120%',
                             'position': 'static'},
                    value = 'Johor',
                    clearable = False,
                ),
            ], width=2),

            dbc.Col([
                dcc.Dropdown(
                    id = 'data',
                    options = [{'label': 'Average Statistics per State', 'value': 'Avg'},
                               {'label': 'Gini & Poverty Rate per State', 'value': 'Gvp'}],
                    placeholder = 'Select the data to view...',
                    style = {'border': '1.5px solid Black', 'align-items': 'left', 'fontSize': '120%',
                             'position': 'static'},
                    value='',
                    clearable = False,
                ),
            ], width=3),
        ]),

        html.Div(dcc.Graph(id='Avg_Bar_Chart')),

        dbc.Row([
            dbc.Col([
                html.P('Income Mean vs Districts', style={'fontWeight': 'bold', 'border': '1.5px solid Black',
                       'fontSize': '120%', 'textAlign': 'center', 'padding': '5px 0px'}),
            ], width=1, style={'margin-left': '10px', 'margin-top': '200px'}),

            dbc.Col([
                dcc.Graph(id='GVIM'),
            ], width=4),

            dbc.Col([
                html.P('Poverty Rate vs Income Mean', style={'fontWeight': 'bold', 'border': '1.5px solid Black',
                       'fontSize': '120%', 'textAlign': 'center', 'padding': '5px 0px'}),
            ], width=1, style={'margin-left': '10px', 'margin-top': '200px'}),

            dbc.Col([
                dcc.Graph(id='line'),
            ], width=4),
        ], className='g-0'),

        dbc.Row([
            dbc.Col([
                html.P('Expenditure vs Districts', style={'fontWeight': 'bold', 'border': '1.5px solid Black',
                       'fontSize': '120%', 'textAlign': 'center', 'padding': '5px 0px'}),
            ], width=1, style={'margin-left': '10px', 'margin-top': '200px'}),

            dbc.Col([
                dcc.Graph(id='Exp'),
            ], width=4),

            dbc.Col([
                html.P('Poverty Rate vs Expenditure', style={'fontWeight': 'bold', 'border': '1.5px solid Black',
                       'fontSize': '120%', 'textAlign': 'center', 'padding': '5px 0px'}),
            ], width=1, style={'margin-left': '10px', 'margin-top': '200px'}),

            dbc.Col([
                dcc.Graph(id='Evp'),
            ], width=4),
        ], className='g-0'),

    ]
)

@app.callback(
    Output('Avg_Bar_Chart', 'figure'),
    [Input('data', 'value')]
)
def update_main_chart(dropdown_2_value):
    if dropdown_2_value == '':
        return {}

    elif dropdown_2_value == 'Avg':
        Meandf = df.groupby(['state'])['income_mean'].mean().round(0).reset_index()
        Mediandf = df.groupby(['state'])['income_median'].mean().round(0).reset_index()
        Expdf = df.groupby(['state'])['expenditure_mean'].mean().round(0).reset_index()
        Combined_Avg_df = Meandf.merge(Mediandf, on=['state']).merge(Expdf, on=['state'])
        Melted_Avg_df = pd.melt(Combined_Avg_df, id_vars=['state'],
                                value_vars=['income_mean', 'income_median', 'expenditure_mean'],
                                var_name='Stats', value_name='Value')
        figure = px.bar(
            Melted_Avg_df,
            x='state',
            y='Value',
            color='Stats',
            barmode='group',
            title='Income & Expenditure Statistics for Different States in Malaysia',
        )
        figure.update_layout(title_x=0.5)
        return figure

    elif dropdown_2_value == 'Gvp':
        Gdf = df.groupby(['state'])['gini'].mean().round(3).reset_index()
        Pdf = df.groupby(['state'])['poverty'].mean().round(3).reset_index()
        Combined_Gdf_Pdf = pd.merge(Gdf, Pdf, on=['state'])
        Melted_Gdf_Pdf = pd.melt(Combined_Gdf_Pdf, id_vars=['state'],
                                 value_vars=['gini', 'poverty'], var_name='Stats', value_name='Value')

        figure = px.bar(
            Melted_Gdf_Pdf,
            x='state',
            y='Value',
            color='Stats',
            barmode='group',
            color_discrete_sequence=px.colors.qualitative.Set1,
            title='Gini Coefficient vs Poverty Rate Comparison for Different States in Malaysia'
        )
        figure.update_layout(title_x=0.5)
        return figure

@app.callback(
    Output('GVIM', 'figure'),
    [Input('state', 'value')]
)
def update_side_charts(dropdown_1_value):
    if dropdown_1_value == 'Johor':
        figure = plot_income_district(df,'Johor')
        return figure

    elif dropdown_1_value == 'Kedah':
        figure = plot_income_district(df, 'Kedah')
        return figure

    elif dropdown_1_value == 'Kelantan':
        figure = plot_income_district(df, 'Kelantan')
        return figure

    elif dropdown_1_value == 'Melaka':
        figure = plot_income_district(df, 'Melaka')
        return figure

    elif dropdown_1_value == 'Negeri Sembilan':
        figure = plot_income_district(df, 'Negeri Sembilan')
        return figure

    elif dropdown_1_value == 'Pahang':
        figure = plot_income_district(df, 'Pahang')
        return figure

    elif dropdown_1_value == 'Pulau Pinang':
        figure = plot_income_district(df, 'Pulau Pinang')
        return figure

    elif dropdown_1_value == 'Perak':
        figure = plot_income_district(df, 'Perak')
        return figure

    elif dropdown_1_value == 'Perlis':
        figure = plot_income_district(df, 'Perlis')
        return figure

    elif dropdown_1_value == 'Selangor':
        figure = plot_income_district(df, 'Selangor')
        return figure

    elif dropdown_1_value == 'Terengganu':
        figure = plot_income_district(df, 'Terengganu')
        return figure

    elif dropdown_1_value == 'Sabah':
        figure = plot_income_district(df, 'Sabah')
        return figure

    elif dropdown_1_value == 'Sarawak':
        figure = plot_income_district(df, 'Sarawak')
        return figure

    elif dropdown_1_value == 'W.P. Kuala Lumpur':
        figure = plot_income_district(df, 'W.P. Kuala Lumpur')
        return figure

    elif dropdown_1_value == 'W.P. Labuan':
        figure = plot_income_district(df, 'W.P. Labuan')
        return figure

    elif dropdown_1_value == 'W.P. Putrajaya':
        figure = plot_income_district(df, 'W.P. Putrajaya')
        return figure

@app.callback(
    Output('line', 'figure'),
    [Input('state', 'value')]
)
def update_side_charts(dropdown_1_value):
    if dropdown_1_value == 'Johor':
        figure = plot_poverty_income(df,'Johor')
        return figure

    elif dropdown_1_value == 'Kedah':
        figure = plot_poverty_income(df, 'Kedah')
        return figure

    elif dropdown_1_value == 'Kelantan':
        figure = plot_poverty_income(df, 'Kelantan')
        return figure

    elif dropdown_1_value == 'Melaka':
        figure = plot_poverty_income(df, 'Melaka')
        return figure

    elif dropdown_1_value == 'Negeri Sembilan':
        figure = plot_poverty_income(df, 'Negeri Sembilan')
        return figure

    elif dropdown_1_value == 'Pahang':
        figure = plot_poverty_income(df, 'Pahang')
        return figure

    elif dropdown_1_value == 'Pulau Pinang':
        figure = plot_poverty_income(df, 'Pulau Pinang')
        return figure

    elif dropdown_1_value == 'Perak':
        figure = plot_poverty_income(df, 'Perak')
        return figure

    elif dropdown_1_value == 'Perlis':
        figure = plot_poverty_income(df, 'Perlis')
        return figure

    elif dropdown_1_value == 'Selangor':
        figure = plot_poverty_income(df, 'Selangor')
        return figure

    elif dropdown_1_value == 'Terengganu':
        figure = plot_poverty_income(df, 'Terengganu')
        return figure

    elif dropdown_1_value == 'Sabah':
        figure = plot_poverty_income(df, 'Sabah')
        return figure

    elif dropdown_1_value == 'Sarawak':
        figure = plot_poverty_income(df, 'Sarawak')
        return figure

    elif dropdown_1_value == 'W.P. Kuala Lumpur':
        figure = plot_poverty_income(df, 'W.P. Kuala Lumpur')
        return figure

    elif dropdown_1_value == 'W.P. Labuan':
        figure = plot_poverty_income(df, 'W.P. Labuan')
        return figure

    elif dropdown_1_value == 'W.P. Putrajaya':
        figure = plot_poverty_income(df, 'W.P. Putrajaya')
        return figure

@app.callback(
    Output('Exp', 'figure'),
    [Input('state', 'value')]
)
def update_side_charts(dropdown_1_value):
    if dropdown_1_value == 'Johor':
        figure = plot_expenditure_district(df,'Johor')
        return figure

    elif dropdown_1_value == 'Kedah':
        figure = plot_expenditure_district(df, 'Kedah')
        return figure

    elif dropdown_1_value == 'Kelantan':
        figure = plot_expenditure_district(df, 'Kelantan')
        return figure

    elif dropdown_1_value == 'Melaka':
        figure = plot_expenditure_district(df, 'Melaka')
        return figure

    elif dropdown_1_value == 'Negeri Sembilan':
        figure = plot_expenditure_district(df, 'Negeri Sembilan')
        return figure

    elif dropdown_1_value == 'Pahang':
        figure = plot_expenditure_district(df, 'Pahang')
        return figure

    elif dropdown_1_value == 'Pulau Pinang':
        figure = plot_expenditure_district(df, 'Pulau Pinang')
        return figure

    elif dropdown_1_value == 'Perak':
        figure = plot_expenditure_district(df, 'Perak')
        return figure

    elif dropdown_1_value == 'Perlis':
        figure = plot_expenditure_district(df, 'Perlis')
        return figure

    elif dropdown_1_value == 'Selangor':
        figure = plot_expenditure_district(df, 'Selangor')
        return figure

    elif dropdown_1_value == 'Terengganu':
        figure = plot_expenditure_district(df, 'Terengganu')
        return figure

    elif dropdown_1_value == 'Sabah':
        figure = plot_expenditure_district(df, 'Sabah')
        return figure

    elif dropdown_1_value == 'Sarawak':
        figure = plot_expenditure_district(df, 'Sarawak')
        return figure

    elif dropdown_1_value == 'W.P. Kuala Lumpur':
        figure = plot_expenditure_district(df, 'W.P. Kuala Lumpur')
        return figure

    elif dropdown_1_value == 'W.P. Labuan':
        figure = plot_expenditure_district(df, 'W.P. Labuan')
        return figure

    elif dropdown_1_value == 'W.P. Putrajaya':
        figure = plot_expenditure_district(df, 'W.P. Putrajaya')
        return figure

@app.callback(
    Output('Evp', 'figure'),
    [Input('state', 'value')]
)
def update_side_charts(dropdown_1_value):
    if dropdown_1_value == 'Johor':
        figure = plot_poverty_expenditure(df,'Johor')
        return figure

    elif dropdown_1_value == 'Kedah':
        figure = plot_poverty_expenditure(df, 'Kedah')
        return figure

    elif dropdown_1_value == 'Kelantan':
        figure = plot_poverty_expenditure(df, 'Kelantan')
        return figure

    elif dropdown_1_value == 'Melaka':
        figure = plot_poverty_expenditure(df, 'Melaka')
        return figure

    elif dropdown_1_value == 'Negeri Sembilan':
        figure = plot_poverty_expenditure(df, 'Negeri Sembilan')
        return figure

    elif dropdown_1_value == 'Pahang':
        figure = plot_poverty_expenditure(df, 'Pahang')
        return figure

    elif dropdown_1_value == 'Pulau Pinang':
        figure = plot_poverty_expenditure(df, 'Pulau Pinang')
        return figure

    elif dropdown_1_value == 'Perak':
        figure = plot_poverty_expenditure(df, 'Perak')
        return figure

    elif dropdown_1_value == 'Perlis':
        figure = plot_poverty_expenditure(df, 'Perlis')
        return figure

    elif dropdown_1_value == 'Selangor':
        figure = plot_poverty_expenditure(df, 'Selangor')
        return figure

    elif dropdown_1_value == 'Terengganu':
        figure = plot_poverty_expenditure(df, 'Terengganu')
        return figure

    elif dropdown_1_value == 'Sabah':
        figure = plot_poverty_expenditure(df, 'Sabah')
        return figure

    elif dropdown_1_value == 'Sarawak':
        figure = plot_poverty_expenditure(df, 'Sarawak')
        return figure

    elif dropdown_1_value == 'W.P. Kuala Lumpur':
        figure = plot_poverty_expenditure(df, 'W.P. Kuala Lumpur')
        return figure

    elif dropdown_1_value == 'W.P. Labuan':
        figure = plot_poverty_expenditure(df, 'W.P. Labuan')
        return figure

    elif dropdown_1_value == 'W.P. Putrajaya':
        figure = plot_poverty_expenditure(df, 'W.P. Putrajaya')
        return figure

if __name__ == '__main__':
    app.run_server(debug=True)