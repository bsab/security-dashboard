# -*- coding: utf-8 -*-
import os
import flask
import pandas as pd
from dash import Dash
from flask import Flask

import dash_core_components as dcc
from dash.dependencies import Input, Output

from classifier import perform_classification
from plot import get_explore_domain_plot, create_bar_plot
from domains import get_domain_dict, get_domain_image_preview
from layout import render_html_layout, get_domain_classification_layout, render_tab_page


dcc._js_dist[0]['external_url'] = (
    'https://cdn.plot.ly/plotly-basic-1.31.0.min.js'
)

server = Flask(__name__, static_url_path='/static', static_folder='./static')
server.secret_key = os.environ.get('secret_key', 'secret')
app = Dash(__name__, server=server, url_base_pathname='/security-dashboard/', csrf_protect=False)

app.config.supress_callback_exceptions = True
app.title = 'security-dashboard'


# Rendering del plot sulla pagina Html
dict_data = {
    'HTTPS':'data/csv/pshtt.csv',
    'PERFORMANCE':'data/csv/pageload.csv',
    'TRUST':'data/csv/trustymail.csv'
}

# calcolo :
# - il dataframe dei risultati totali(df_result),
# - la lista dei domini sui quali effettuare la ricerca
# - i dataframe dettagliati per https, trust e performance
data_results = perform_classification(dict_data)
df_https = data_results['dataframe_https']
df_perf = data_results['dataframe_perf']
df_trust = data_results['dataframe_trust']
search_domain_list = data_results['search_domain_list']

# creo il grafico per l'esploraione di tutti i dati
df_result = data_results['dataframe_all_result']
search_domain_graph = get_explore_domain_plot(df_result)

#..ed infine procedo con il rendering
app.layout = render_html_layout()


def dfRowFromHover(hoverData):
    """ Ritorna il dominio in hover """
    if hoverData is not None:
        if 'points' in hoverData:
            firstPoint = hoverData['points'][0]
            if 'pointNumber' in firstPoint:
                point_number = firstPoint['pointNumber']
                domain_name = str(search_domain_graph['data'][0]['text'][point_number]).strip()
                return df_result.loc[df_result['Domain'] == domain_name]
    return pd.Series()

#
# Lista delle callback associate al grafico ed al box di ricerca
#

@app.callback(
    Output('tab-output', 'children'),
    [Input('tabs', 'value')])
def display_tab_content(value):
    return render_tab_page(value,
                           search_domain_graph,
                           search_domain_list)

@app.callback(
    Output('domain-info-element', 'children'),
    [Input('search_dropdown', 'value')])
def update_domain_info_classification(search_dropdown_value):
    """ Aggiorna le informazione riguardo la classificazione
     del dominio selezionato """

    domain_info = get_domain_dict(df_result, search_dropdown_value)
    return get_domain_classification_layout(domain_info)

@app.callback(
    Output('https_graph', 'figure'),
    [Input('search_dropdown', 'value')])
def update_https_plot(search_dropdown_value):
    """ Aggiorna il grafico relativo alla sicurezza http
     selezionando solo la riga relativa al dominio selezionato"""
    if search_dropdown_value:
        # costruisco il grafico per i dettagli Https
        try:
            df_https_selected = df_https.loc[df_https['Domain'].isin(search_dropdown_value)]
        except:
            tmp = []
            tmp.append(str(search_dropdown_value))
            df_https_selected = df_https.loc[df_https['Domain'].isin(tmp)]

        # seleziono solo le colonne interessanti per il calcolo
        columns = ['Domain Supports HTTPS',
                   'Domain Enforces HTTPS',
                   'Domain Uses Strong HSTS']
        if df_https_selected.empty:
            print('DataFrame HTTPS is empty!')
            return create_bar_plot('Sicurezza', [0, 0, 0], columns)

        values = pd.DataFrame(df_https_selected, columns=columns).values[0]

        return create_bar_plot('Sicurezza', values.astype('O'), columns)

@app.callback(
    Output('perf_graph', 'figure'),
    [Input('search_dropdown', 'value')])
def update_perf_plot(search_dropdown_value):
    """ Aggiorna il grafico relativo alle performance
     selezionando solo la riga relativa al dominio selezionato"""
    if search_dropdown_value:
        # costruisco il grafico per i dettagli Https
        try:
            df_perf_selected = df_perf.loc[df_perf['Domain'].isin(search_dropdown_value)]
        except:
            tmp = []
            tmp.append(str(search_dropdown_value))
            df_perf_selected = df_perf.loc[df_perf['Domain'].isin(tmp)]

        # seleziono solo le colonne interessanti per il calcolo
        columns = ['domContentLoaded',
                   'domComplete']
        if df_perf_selected.empty:
            print('DataFrame is empty!')
            return create_bar_plot('Performance', [0, 0, 0], columns)

        values = pd.DataFrame(df_perf_selected, columns=columns).values[0]

        return create_bar_plot('Performance', values.astype('O'), columns)

@app.callback(
    Output('trust_graph', 'figure'),
    [Input('search_dropdown', 'value')])
def update_trust_plot(search_dropdown_value):
    """ Aggiorna il grafico relativo all'affidabilità
     selezionando solo la riga relativa al dominio selezionato"""
    if search_dropdown_value:
        # costruisco il grafico per i dettagli Https
        try:
            df_trust_selected = df_trust.loc[df_trust['Domain'].isin(search_dropdown_value)]
        except:
            tmp = []
            tmp.append(str(search_dropdown_value))
            df_trust_selected = df_trust.loc[df_trust['Domain'].isin(tmp)]

        # seleziono solo le colonne interessanti per il calcolo
        columns = ['MX Record',
                   'Valid SPF',
                   'Valid DMARC']
        values = pd.DataFrame(df_trust_selected, columns=columns).values[0]

        return create_bar_plot('Affidabilita', values.astype('O'), columns)

@app.callback(
    Output('domain-preview', 'src'),
    [Input('clickable-graph', 'clickData')])
def update_domain_preview(clickData):
    """ Aggiorna le informazione riguardo la classificazione
     del dominio selezionato alla selezione del dominio nella
     combobox oppure cliccando sul grafico"""

    try:
        # seleziono l'url del dominio
        domain_name = clickData['points'][0]['text']
        return get_domain_image_preview(domain_name)
    except:
        return


@app.callback(
    Output('chem_img', 'src'),
    [Input('clickable-graph', 'clickData')])
def display_image(hoverData):
    """ Ritorna l'immagine dello score corrispondente al dominio in hover """
    row = dfRowFromHover(hoverData)
    if row.empty:
        return
    img_src = row['Sticker'].iloc[0]
    return img_src


@app.callback(
    Output('https_slider', 'value'),
    [Input('clickable-graph', 'clickData')])
def over_refresh_https(hoverData):
    row = dfRowFromHover(hoverData)
    if row.empty:
        return
    return row['HTTPS Score'].iloc[0]


@app.callback(
    Output('performance_slider', 'value'),
    [Input('clickable-graph', 'clickData')])
def over_refresh_performance(hoverData):
    row = dfRowFromHover(hoverData)
    if row.empty:
        return
    return row['Performance Score'].iloc[0]


@app.callback(
    Output('trust_slider', 'value'),
    [Input('clickable-graph', 'clickData')])
def over_refresh_trust(hoverData):
    row = dfRowFromHover(hoverData)
    if row.empty:
        return
    return row['Trust Score'].iloc[0]


@app.server.route('/static/<resource>')
def serve_static(resource):
    """ Serve gli statici dalla cartella /static/ """
    return flask.send_static_file(resource)


@app.server.route('/static/<filename>.js')
def serve_script(filename):
    print(('serving {}'.format(filename)))
    if filename not in ['my-event']:
        raise Exception('"{}" is excluded from the allowed static files'.format(filename))
    return flask.send_from_directory(os.getcwd(), '{}.js'.format(filename))

# Aggiunta di file CSS esterni
app.css.append_css({
    'external_url': (
        'https://cdn.rawgit.com/plotly/dash-app-stylesheets/8485c028c19c393e9ab85e1a4fafd78c489609c2/dash-docs-base.css',
        'https://fonts.googleapis.com/css?family=Dosis',
        'https://cdn.rawgit.com/plotly/dash-app-stylesheets/8485c028c19c393e9ab85e1a4fafd78c489609c2/dash-docs-base.css',
        '/static/css/style.css',
    )
})

if __name__ == '__main__':
    app.run_server(debug=True, threaded=True, port=8050)
