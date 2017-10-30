# -*- coding: utf-8 -*-
import dash_html_components as html
import dash_core_components as dcc


def header_layout():
    """ Rendering header"""
    return html.Div(
        className='header',
        children=html.Div(
            className='container-width',
            style={'height': '100%'},
            children=[
                html.A(html.Img(
                    src="https://avatars1.githubusercontent.com/u/15377824?v=4&s=200",
                    className="logo"
                ), href='#', className="logo-link"),
                html.Div(className="", children=[
                    html.H1('Security Dashboard', className="header-title"),
                ])
            ]
        )
    )


def tab_introduction():
    """ Rendering della pagina linkata dal tab Introduzione"""
    return [html.Div(
        html.Div([
            html.H1('Security Dashboard'),
            html.Hr(),
            html.P("Il calcolo del punteggio viene effettuato sulla base di 3 caratteristiche:"),
            html.Ul([
                html.Li([html.Strong('Sicurezza'), html.Span(': garantita dall\'uso del protocollo HTTPS o HTS.')]),
                html.Li([html.Strong('Performance'),
                         html.Span(': analizzando i tempi di caricamento delle pagine e degli assets.')]),
                html.Li(
                    [html.Strong('Affidabilita'), html.Span(': verificando l\'utilizzo dei record MX, SPF e DMARC.')]),
            ]),
            html.P(
                "Considerando questi fattori, ad ogni dominio viene attribuito un punteggio da A a F."),
            html.Img(src='/static/img/classifica.png',
                     style={'margin': '0 auto',
                            'display': 'block'}),
            html.P(
                "Il dominio che ottiene il valore più alto in tutte tre queste caratteristiche puo essere considerato un dominio altamente sicuro."),
            html.Hr(),
        ])
    )]


def get_domain_classification_layout(domain_info=None):
    """Creazione del layout relativo alla classificazione
      che ha ottenuto il dominio"""
    if domain_info:
        return [html.Div([
            html.Div([
                html.Br(),
                html.Img(id='chem_img', src=domain_info['Sticker'],
                         style={'margin': '0 auto',
                                'display': 'block',
                                'width': '100'}),
                html.Div([
                    html.H3(domain_info['Domain'],
                            style={'text-align': 'center'})
                ]),
            ]),
            html.Div([
                html.Div(
                    [
                        html.Label('Sicurezza:'),
                        dcc.Slider(
                            id='https_slider',
                            min=0,
                            max=15,
                            value=domain_info['HTTPS'],
                            disabled=True,
                        ),
                    ]
                ),
                html.Div([
                    html.Label('Performance:'),
                    dcc.Slider(
                        id='performance_slider',
                        min=0,
                        max=10,
                        value=domain_info['Performance'],
                        disabled=True,
                    )
                ]),
                html.Div([
                    html.Label('Affidabilità:'),
                    dcc.Slider(
                        id='trust_slider',
                        min=0,
                        max=10,
                        value=domain_info['Trust'],
                        disabled=True,
                    )
                ]),
            ],style={'margin':'10px 50px 10px 50px'}),
            html.Br(),
        ],className='eight columns content-container',
            style={
                'padding-bottom': '15px'
            }
        ),
            html.Div(
                [
                    html.Img(src=domain_info['Preview'],
                             id='domain-preview',
                             style={
                                 'width': '100%'
                             })
                ], className='browser-mockup with-url four columns')
        ]


def render_html_layout():
    """ Rendering della pagina completa"""
    return html.Div([
        html.Meta(name='viewport', content='width=device-width, initial-scale=1.0'),
        html.Meta(
            name='description',
            content=('Security Dashboard '
                     'A dashboard that shows the status of security features on .gov.it websites')
        ),
        header_layout(),
        html.Div([
            html.Div(
                dcc.Tabs(
                    tabs=[
                        {'label': 'Introduzione', 'value': 1},
                        {'label': 'Cerca', 'value': 2},
                        {'label': 'Esplora', 'value': 3},
                    ],
                    value=1,
                    id='tabs',
                    vertical=True,
                    style={
                        'height': '100vh',
                        'borderRight': 'thin lightgrey solid',
                        'textAlign': 'left'
                    }
                ),
                style={'width': '20%', 'float': 'left'}
            ),
            html.Div(
                html.Div(id='tab-output'),
                style={'width': '80%', 'float': 'right'}
            )
        ], style={
            'fontFamily': 'Sans-Serif',
            'margin-left': 'auto',
            'margin-right': 'auto',
        })
    ])


def render_tab_page(tab_index,
                    search_domain_graph,
                    search_domain_list):
    """ Rendering del singolo tab selezionato"""
    if tab_index == 1:
        return \
            html.Div([
                html.Div([
                    html.Div([

                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(tab_introduction(),
                                                 id='domain-info-element'
                                                 )
                                    ],
                                    className='twelve columns',
                                    style={'margin-top': '20'}
                                ),
                            ],
                            className='row'
                        )
                    ],
                        className='ten columns offset-by-one'
                    )
                ])
            ], className='container')
    elif tab_index == 2:
        return html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                html.H2('Cerca un dominio'),
                                html.Hr()]),
                            html.P(
                                "Seleziona un dominio dalla barra di ricerca per scoprirne il grado di affidabilità"),
                        ]),
                    ]),
                    html.Div(
                        [
                            html.Div(
                                [
                                    dcc.Dropdown(id='search_dropdown',
                                                 options=search_domain_list),
                                ],
                                className='six columns'
                            )
                        ],
                        className='row'
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(get_domain_classification_layout(),
                                             id='domain-info-element'
                                             )
                                ],
                                className='twelve columns',
                                style={'margin-top': '20'}
                            ),
                        ],
                        className='row'
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    dcc.Graph(id='https_graph')
                                ],
                                className='four columns',
                            ),
                            html.Div(
                                [
                                    dcc.Graph(id='perf_graph')
                                ],
                                className='four columns',
                            ),
                            html.Div(
                                [
                                    dcc.Graph(id='trust_graph')
                                ],
                                className='four columns',
                            ),
                        ],
                        className='row'
                    ),
                ],
                    className='ten columns offset-by-one'
                )
            ])
        ], className='container',
            style={'margin-bottom': '20'})
    else:
        return html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                html.H2('Esplora i domini'),
                                html.Hr()]),
                            html.P(
                                "Passa il mouse sul grafico per esplorare le caratteristiche dei domini"),
                        ]),
                    ]),
                    html.Div(
                        [
                            html.Div(
                                [
                                    dcc.Graph(id='clickable-graph',
                                              style=dict(width='100%'),
                                              hoverData=dict(points=[dict(pointNumber=0)]),
                                              figure=search_domain_graph),
                                    dcc.RadioItems(
                                        id='charts_radio',
                                        options=[
                                            dict(label='Visualizzazione 2D', value='scatter'),
                                            dict(label='Visualizzazione 3D', value='scatter3d')
                                        ],
                                        labelStyle=dict(display='inline'),
                                        value='scatter'
                                    )
                                ],
                                className='twelve columns',
                            ),
                        ],
                        className='row'
                    ),
                ],
                    className='ten columns offset-by-one'
                )
            ])
        ], className='container')
