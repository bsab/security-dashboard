import time
import six
import os
from datetime import datetime as dt

import dash_html_components as html
import dash_core_components as dcc
import dash_table_experiments as dt
from dash.dependencies import Input, State, Event, Output

from server import app, server

import dashboard

dcc._js_dist[0]['external_url'] = (
    'https://cdn.plot.ly/plotly-basic-1.31.0.min.js'
)


def create_contents(contents):
    h = []
    for i in contents:
        if isinstance(i, list):
            h.append(create_contents(i))
        else:
            h.append(html.Li(i))
    return html.Ul(h)


chapters = {
    'index': {
        'url': '/security/',
        'content': dashboard.app.layout
    },
}

header = html.Div(
    className='header',
    children=html.Div(
        className='container-width',
        style={'height': '100%'},
        children=[
            html.A(html.Img(
                src="https://avatars1.githubusercontent.com/u/15377824?v=4&s=200",
                className="logo"
            ), href='https://plot.ly/products/dash', className="logo-link"),

            html.Div(className="links", children=[
                html.A('pricing', className="link", href="https://plot.ly/products/on-premise"),
                html.A('workshops', className="link", href="https://plotcon.plot.ly/workshops"),
                html.A('user guide', className="link active", href="https://plot.ly/dash/"),
                html.A('plotly', className="link", href="https://plot.ly/")
            ])
        ]
    )
)

app.title = 'security-dashboard'

app.layout = html.Div([
    html.Meta(name='viewport', content='width=device-width, initial-scale=1.0'),
    html.Meta(
        name='description',
        content=('Dash User Guide and Documentation. '
                 'Dash is a Python framework for building '
                 'reactive web apps developed by Plotly.')
    ),
    header,
    html.Div([
        html.Div([
            html.Div(
                html.Div(id="chapter", className="content"),
                className="content-container"
            ),
        ], className="container-width")
    ], className="background"),
    dcc.Location(id='location', refresh=False),
    html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'})
])


@app.callback(Output('chapter', 'children'),
    [Input('location', 'pathname')])
def display_content(pathname):
    if pathname is None:
        return ''
    if pathname.endswith('/') and pathname != '/':
        pathname = pathname[:len(pathname) - 1]
    matched = [c for c in chapters.keys()
               if chapters[c]['url'] == pathname]

    if matched and matched[0] != 'index':
        content = html.Div([
            html.Div(chapters[matched[0]]['content']),
            html.Hr(),
            dcc.Link(html.A('Back to the Table of Contents'), href='/dash/')
        ])
    else:
        content = chapters['index']['content']

    return content

app.css.append_css({
    'external_url': (
        'https://cdn.rawgit.com/plotly/dash-app-stylesheets/8485c028c19c393e9ab85e1a4fafd78c489609c2/dash-docs-base.css',
        '/static/css/style.css',
        'https://fonts.googleapis.com/css?family=Dosis'
    )
})

if 'DYNO' in os.environ:
    app.scripts.config.serve_locally = False
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })
else:
    app.scripts.config.serve_locally = True

if __name__ == '__main__':
    app.run_server(debug=True, threaded=True, port=8050)