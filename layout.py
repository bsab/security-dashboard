# -*- coding: utf-8 -*-
import dash_html_components as html
import dash_core_components as dcc


def get_domain_classification_info(domain_info=None):
    """  """
    if not domain_info:
        domain_info = {}
        domain_info['Sticker'] = ""
        domain_info['HTTPS'] = ""
        domain_info['Performance'] = ""
        domain_info['Trust'] = ""


    return [html.Div([
        # html.Div([
        #    html.Iframe(id="domain-preview",
        #                src="http://www." + domain_info['Domain'],
        #                sandbox="allow-same-origin",
        #                style={'border': 'none', 'width': '100%', 'height': 500})
        # ], className="eight columns"),

        html.Img(id='chem_img', src=domain_info['Sticker'],
                 style={'margin': '0 auto', 'display': 'block', 'width': '100'}),

        html.Label('HTTPS:'),
            dcc.Slider(
                id='https_slider',
                min=0,
                max=15,
                value=domain_info['HTTPS'],
            ),
        ]),
        html.Div([
            html.Label('Performance:'),
            dcc.Slider(
                id='performance_slider',
                min=0,
                max=10,
                value=domain_info['Performance'],
            )
        ]),
        html.Div([
            html.Label('Trust:'),
            dcc.Slider(
                id='trust_slider',
                min=0,
                max=10,
                value=domain_info['Trust'],
            )
        ])]


def get_domain_preview(domain_url):
    print ("*******", domain_url, "************")
    return [html.Div([
        # html.Iframe(src="www." + domain_info['Domain']),
        html.Div([
            html.Iframe(src=domain_url,
                        sandbox="allow-same-origin",
                        style={'border': 'none', 'width': '90%', 'height': 500, 'allowfullscreen': '',
                               'frameborder': '0'})
        ], className="eight columns")
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
            html.Div([
                html.Div([
                    html.Label('Cerca:'),
                    dcc.Dropdown(id='chem_dropdown',
                                 value=[starting_domain],
                                 options=[{'label': i, 'value': i} for i in df['Domain'].tolist()]),
                    html.Div(get_domain_classification_info(),
                             id='domain-info-element',
                             className='four columns'
                             ),
                ],
                    className='four columns',
                ),
                html.Div(get_domain_preview(starting_domain),
                         id="domain-preview"),
            ],
                className='row',
                style={'margin-bottom': '10'}
            ),
        ],
            className='row'
        )
    ]),


    # Row 2: Hover Panel and Graph
    html.Hr(style={'margin': '0', 'margin-bottom': '5'}),
    html.Div([
        html.Div([
            dcc.RadioItems(
                id='charts_radio',
                options=[
                    dict(label='Visualizzazione 2D', value='scatter'),
                    dict(label='Visualizzazione 3D', value='scatter3d'),
                    # dict( label='Istogramma', value='histogram2d' ),
                ],
                labelStyle = dict(display='inline'),
                value='scatter'
            ),

            dcc.Graph(id='clickable-graph',
                      style=dict(width='90%'),
                      hoverData=dict( points=[dict(pointNumber=0)] ),
                      figure=FIGURE ),

        ], style=dict(textAlign='center')),
    ], className='row' ),
], className='container')

