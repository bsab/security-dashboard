# -*- coding: utf-8 -*-
import dash_html_components as html
import dash_core_components as dcc

def make_dash_table( selection, df ):
    print "make_dash_table--->", selection
    """ Return a dash defintion of an HTML table for a Pandas dataframe """

    try:
        df_subset = df.loc[df['Domain'].isin(selection)]
    except:
        tmp = []
        tmp.append(str(selection))
        df_subset = df.loc[df['Domain'].isin(tmp)]

    table = []
    table.append(html.Tr([html.Th('Dominio'), html.Th("HTTPS Score"), html.Th("Performance Score"), html.Th("Trust Score"), html.Th("Grado")]))
    for index, row in df_subset.iterrows():
        html_row = []
        for i in range(len(row)):
            if i == 0 or i == 6:
                html_row.append( html.Td([ row[i] ]) )
            elif i == 5:
                html_row.append( html.Td([ html.Img( src=row[i], style={'margin': '0 auto', 'display': 'block', 'width': '50'} )]))
            elif i == 1:
                html_row.append( html.Td([ row[i] ]))
            elif i == 2:
                html_row.append( html.Td([ row[i] ]))
            elif i == 3:
                html_row.append( html.Td([ row[i] ]))
        table.append( html.Tr( html_row ) )

    print table
    return table

def get_domain_classification_info( selection, df ):
    print "get_domain_classification_info--->", df
    """  """

    try:
        df_subset = df.loc[df['Domain'].isin(selection)]
    except:
        tmp = []
        tmp.append(str(selection))
        df_subset = df.loc[df['Domain'].isin(tmp)]

    print "df_subset['Domain']--->", df_subset['Domain']

    return [html.Div([
            html.Label('HTTPS:'),
            dcc.Slider(
                id='price_slider',
                min=0,
                max=15,
                value=5,
            ),
        ]),
        html.Div([
            html.Label('Performance:'),
            dcc.Slider(
                id='volume_slider',
                min=0,
                max=10,
                value=1,
            )
        ]),
        html.Div([
            html.Label('Trust:'),
            dcc.Slider(
                id='trust_slider',
                min=0,
                max=10,
                value=1,
            )
        ])]

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
                html.Div([

                    html.P("Seleziona un dominio dalla barra di ricerca o direttamente cliccando sul grafico. Ad ogni dominio è stato associato un punteggio da A a F."),
                    html.P("Il calcolo del punteggio viene effettuato sulla base di 3 caratteristiche:"),
                    html.P("- Sicurezza: garantita dall'uso del protocollo HTTPS o HTS.", style={'margin-top':'-20px'}),
                    html.P("- Performance: analizzando i tempi di caricamento delle pagine e degli assets.", style={'margin-top':'-20px'}),
                    html.P("- Affidabilita: verificando l'utilizzo dei record MX, SPF e DMARC.", style={'margin-top':'-20px'}),
                    html.P("Il dominio che ottiene il valore più alto in tutte tre queste caratteristiche puo essere considerato un dominio altamente sicuro."),

                ]),
            ], style={'margin-left': '10px'}),
        ], className='row'),

        html.Hr(style={'margin': '0', 'margin-bottom': '5'}),

        html.Div(
            [
            html.Hr(style={'margin': '0', 'margin-bottom': '5'}),
            html.Div([
                html.Div([
                    html.Label('Cerca:'),
                    dcc.Dropdown(id='chem_dropdown',
                                 # multi=True,
                                 value=[starting_domain],
                                 options=[{'label': i, 'value': i} for i in df['Domain'].tolist()]),
                ],
                    className='six columns',
                ),
                html.Div([
                    html.Img(id='chem_img', src=score_sticker,
                             style={'margin': '0 auto', 'display': 'block', 'width': '100'}),
                    html.A(starting_domain,
                           id='chem_name',
                           href="https://www.gov.it",
                           target="_blank",
                           style={'text-align': 'center', 'display': 'block'}),
                    html.P(domain_info,
                           id='chem_desc',
                           style=dict(maxHeight='400px', fontSize='12px')),

                ],
                    className='two columns',
                ),

                html.Div(get_domain_classification_info([starting_domain], df),
                    id='domain-info-element',
                    className='four columns'
                ),
            ],
                className='row',
                style={'margin-bottom': '10'}
            ),
            html.Div([
                dcc.Graph(id='iv_surface', style={'max-height': '600', 'height': '60vh'}),
            ],
                className='row',
                style={'margin-bottom': '20'}
            ),
            html.Div([
                html.Div([
                    dcc.Graph(id='iv_heatmap', style={'max-height': '350', 'height': '35vh'}),
                ],
                    className='five columns'
                ),
                html.Div([
                    dcc.Graph(id='iv_scatter', style={'max-height': '350', 'height': '35vh'}),
                ],
                    className='seven columns'
                )
            ],
                className='row'
            ),
            # Temporary hack for live dataframe caching
            # 'hidden' set to 'loaded' triggers next callback
            html.P(
                hidden='',
                id='raw_container',
                style={'display': 'none'}
            ),
            html.P(
                hidden='',
                id='filtered_container',
                style={'display': 'none'}
            )
        ],
         className='container'
    ),
        html.Div([
            html.Table(make_dash_table([starting_domain], df), id='table-element'),
        ]
        ),
    ]),


    # Row 2: Hover Panel and Graph
    html.Hr(style={'margin': '0', 'margin-bottom': '5'}),
    html.Div([
        html.Div([
            html.P("GRADO DI SICUREZZA", style={'text-align': 'center', 'fontSize': '20px', 'margin-top': '10px'}),
            #html.Img(id='chem_img', src=score_sticker, style={'margin': '0 auto', 'display': 'block', 'width': '100'}),
            #html.A(starting_domain,
            #       id='chem_name',
            #       href="https://www.gov.it",
            #       target="_blank",
            #       style={'text-align': 'center', 'display': 'block'}),

            #html.P(domain_info,
            #       id='chem_desc',
            #       style=dict( maxHeight='400px', fontSize='12px' )),

        ], className='three columns', style=dict(height='300px') ),

        html.Div([

            dcc.RadioItems(
                id = 'charts_radio',
                options=[
                    dict(label='Visualizzazione 3D', value='scatter3d'),
                    dict(label='Visualizzazione 2D', value='scatter'),
                    # dict( label='Istogramma', value='histogram2d' ),
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
], className='container')

