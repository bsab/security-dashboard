import dash_html_components as html
import dash_core_components as dcc

def make_dash_table( selection, df ):
    """ Return a dash defintion of an HTML table for a Pandas dataframe """

    df_subset = df.loc[df['Domain'].isin(selection)]
    table = []
    for index, row in df_subset.iterrows():
        html_row = []
        for i in range(len(row)):
            if i == 0 or i == 6:
                html_row.append( html.Td([ row[i] ]) )
            elif i == 1:
                html_row.append( html.Td([ html.A( href=row[i], children='Datasheet' )]))
            elif i == 5:
                html_row.append( html.Td([ html.Img( src=row[i] )]))
            elif i == 4:
                html_row.append( html.Td([ row[i] ]))
        table.append( html.Tr( html_row ) )
    return table


def get_html_layout(starting_domain,
                    score_sticker,
                    domain_info,
                    FIGURE,
                    df):
    return html.Div([
    # Row 1: Header and Intro text

    html.Div([
        html.Img(src="https://avatars1.githubusercontent.com/u/15377824?v=4&s=200",
                style={
                    'height': '100px',
                    'float': 'right',
                    'position': 'relative',
                    'bottom': '40px',
                    'left': '50px',
                    'top': '0px'
                },
                ),
        html.H2('Security Dashboard',
                style={
                    'position': 'relative',
                    'top': '0px',
                    'left': '27px',
                    'font-family': 'Dosis',
                    'display': 'inline',
                    'font-size': '6.0rem',
                    'color': '#4D637F'
                }),
    ], className='row twelve columns', style={'position': 'relative', 'right': '15px'}),

    html.Div([
        html.Div([
            html.Div([
                html.P('HOVER over a domain in the graph to the right to see its structure to the left.'),
                html.P('SELECT a domain in the dropdown to add it to the domain candidates at the bottom.')
            ], style={'margin-left': '10px'}),
            dcc.Dropdown(id='chem_dropdown',
                         multi=True,
                         value=[starting_domain],
                         options=[{'label': i, 'value': i} for i in df['Domain'].tolist()]),
            ], className='twelve columns' )

    ], className='row' ),

    # Row 2: Hover Panel and Graph

    html.Div([
        html.Div([
            html.P("GRADO DI SICUREZZA", style={'text-align': 'center', 'fontSize': '20px', 'margin-top': '10px'}),
            html.Img(id='chem_img', src=score_sticker, style={'margin': '0 auto', 'display': 'block', 'width': '100'}),
            html.A(starting_domain,
                   id='chem_name',
                   href="https://www.gov.it",
                   target="_blank",
                   style={'text-align': 'center', 'display': 'block'}),

            html.P(domain_info,
                   id='chem_desc',
                   style=dict( maxHeight='400px', fontSize='12px' )),

        ], className='three columns', style=dict(height='300px') ),

        html.Div([

            dcc.RadioItems(
                id = 'charts_radio',
                options=[
                    dict( label='Grafico 3D', value='scatter3d' ),
                    dict( label='Grafico 2D', value='scatter' ),
                    dict( label='Istogramma', value='histogram2d' ),
                ],
                labelStyle = dict(display='inline'),
                value='scatter3d'
            ),

            dcc.Graph(id='clickable-graph',
                      style=dict(width='700px'),
                      hoverData=dict( points=[dict(pointNumber=0)] ),
                      figure=FIGURE ),

        ], className='nine columns', style=dict(textAlign='center')),
    ], className='row' ),

    html.Div([
        html.Table(make_dash_table([starting_domain], df), id='table-element')
    ])

], className='container')

