# -*- coding: utf-8 -*-
import os
import flask
import dash
import requests
import pandas as pd

import dash_html_components as html

from dash.dependencies import Input, Output
from plot import create_scatter_plot
from score import evalute_https_score, evalute_performance_score, evalute_trust_score, merge_df_results
from layout import get_html_layout, get_domain_classification_info, get_domain_preview


# Configurazione server Flask
STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
server = flask.Flask('security-dashboard')
app = dash.Dash('security-dashboard', server=server, url_base_pathname='/security-dashboard/', csrf_protect=False)

server.secret_key = os.environ.get('secret_key', 'secret')

#
# Import dei csv ottenuti dall'utility domain-scan
#

# 1) Importo il csv relativo al test HTTPS (pshtt scanner)
# e calcolo un punteggio finale associato ad ogni dominio analizzato
# in scala da 0 a 15
df_score_https = evalute_https_score("csv/pshtt.csv")

# 2) Importo il csv relativo al test sulle performance (pageload scanner)
# e calcolo un punteggio finale associato ad ogni dominio analizzato
# in scala da 0 a 15
df_score_performance = evalute_performance_score("csv/pageload.csv")

#3) Importo il csv relativo al test sull'affidabilita' (trustymail scanner)
# e calcolo un punteggio finale associato ad ogni dominio analizzato
# in scala da 0 a 15
df_trust_performance = evalute_trust_score("csv/trustymail.csv")

# 4) Unifico i risultati in unico DataFrame definendo un punteggio finale
# in scala da 0 a 1500
df_result = merge_df_results(df_score_https, df_score_performance, df_trust_performance)

#
# Definisco i parametri per la configurazione del grafico Dash
#
x=df_result['HTTPS Score']
y=df_result['Performance Score']
z=df_result['Trust Score']
size=df_result['Tot Score']
color=df_result['Tot Score']
text = df_result['Domain']

xlabel = 'Sicurezza'
ylabel = 'Performance'
zlabel = 'Affidabilita'
plot_type = 'scatter3d'

# Plotting del grafico relativo alla lista dei domini importati
domain_plot = create_scatter_plot(x, y, z, size, color, xlabel, ylabel, zlabel, plot_type, text)
starting_domain = '1cdbacoli.gov.it'
domain_description = ""
DOMAIN_IMG = ""

NOPAGE_B64 = ''

# Rendering del plot sulla pagina Html
app.layout = get_html_layout(starting_domain,
                             DOMAIN_IMG,
                             domain_description,
                             domain_plot,
                             df_result)



def get_domain_dict(df, selection):
    domain_info = {}

    try:
        df_subset = df.loc[df['Domain'].isin(selection)]
    except:
        tmp = []
        tmp.append(str(selection))
        df_subset = df.loc[df['Domain'].isin(tmp)]

    print "df_subset--------->", df_subset
    for index, row in df_subset.iterrows():
        for i in range(len(row)):
            if i == 0 or i == 6:
                domain_info['Domain'] = row[i]
            elif i == 5:
                domain_info['Sticker'] = row[i]
            elif i == 1:
                domain_info['HTTPS'] = row[i]
            elif i == 2:
                domain_info['Performance'] = row[i]
            elif i == 3:
                domain_info['Trust'] = row[i]

    return domain_info


@app.callback(
    Output('clickable-graph', 'figure'),
    [Input('search_dropdown', 'value'),
     Input('charts_radio', 'value')])
def highlight_domain(search_dropdown_values, plot_type):
    print "**CALLBACK::highlight_domain**"
    return create_scatter_plot(x, y, z, size, color, xlabel, ylabel, zlabel, plot_type, text)

@app.callback(
    Output('domain-info-element', 'children'),
    [Input('search_dropdown', 'value')])
def update_domain_info_classification(search_dropdown_value):
    """ Aggiorna le informazione riguardo la classificazione
     del dominio selezionato """

    domain_info = get_domain_dict(df_result, search_dropdown_value)
    return get_domain_classification_info(domain_info)


@app.callback(
    Output('domain-preview', 'children'),
    [Input('search_dropdown', 'value')])
def update_domain_preview(search_dropdown_value):
    """ Aggiorna le informazione riguardo la classificazione
     del dominio selezionato """

    # seleziono l'url del dominio
    domain = get_domain_dict(df_result, search_dropdown_value)['Domain']
    domain_url = "http://www." + str(domain)

    try:
        # e lo passo a google pagespeed per ottenere l'anteprima in b64
        # api = "https://www.googleapis.com/pagespeedonline/v1/runPagespeed?screenshot=true&strategy=mobile"
        api = "https://www.googleapis.com/pagespeedonline/v1/runPagespeed?screenshot=true&strategy=desktop"

        r = requests.get(api, [('url', domain_url)])
        site_data = r.json()
        screenshot_encoded = site_data['screenshot']['data']
        screenshot_encoded = screenshot_encoded.replace("_", "/")
        screenshot_encoded = screenshot_encoded.replace("-", "+")

        screenshot_encoded = "data:image/jpeg;base64," + screenshot_encoded
    except:
        screenshot_encoded = NOPAGE_B64

    return get_domain_preview(screenshot_encoded)


def dfRowFromHover(hoverData):
    """ Ritorna il dominio in hover """
    if hoverData is not None:
        if 'points' in hoverData:
            firstPoint = hoverData['points'][0]
            if 'pointNumber' in firstPoint:
                point_number = firstPoint['pointNumber']
                domain_name = str(domain_plot['data'][0]['text'][point_number]).strip()
                return df_result.loc[df_result['Domain'] == domain_name]
    return pd.Series()


'''
@app.callback(
    Output('chem_name', 'children'),
    [Input('clickable-graph', 'hoverData')])
def return_domain_name(hoverData):
    print "**CALLBACK::return_domain_name**"
    """ Ritorna il dominio in hover """
    if hoverData is not None:
        if 'points' in hoverData:
            firstPoint = hoverData['points'][0]
            if 'pointNumber' in firstPoint:
                point_number = firstPoint['pointNumber']
                domain_name = str(domain_plot['data'][0]['text'][point_number]).strip()
                return ""

@app.callback(
    Output('chem_name', 'href'),
    [Input('clickable-graph', 'hoverData')])
def return_href(hoverData):
    print "**CALLBACK::return_href**"
    """ Ritorna il link del dominio in hover """
    row = dfRowFromHover(hoverData)
    if row.empty:
        return
    datasheet_link = "http://" + row['Domain'].iloc[0]
    return datasheet_link
'''

@app.callback(
    Output('chem_img', 'src'),
    [Input('clickable-graph', 'hoverData')])
def display_image(hoverData):
    print "**CALLBACK::display_image**"
    """ Ritorna l'immagine dello score corrispondente al dominio in hover """
    row = dfRowFromHover(hoverData)
    if row.empty:
        return
    img_src = row['Sticker'].iloc[0]
    return img_src


@app.callback(
    Output('https_slider', 'value'),
    [Input('clickable-graph', 'hoverData')])
def over_refresh_https(hoverData):
    row = dfRowFromHover(hoverData)
    print "hover_refresh_https:", row
    if row.empty:
        return
    return row['HTTPS Score'].iloc[0]


@app.callback(
    Output('performance_slider', 'value'),
    [Input('clickable-graph', 'hoverData')])
def over_refresh_performance(hoverData):
    row = dfRowFromHover(hoverData)
    print "hover_refresh_https:", row
    if row.empty:
        return
    return row['Performance Score'].iloc[0]


@app.callback(
    Output('trust_slider', 'value'),
    [Input('clickable-graph', 'hoverData')])
def over_refresh_trust(hoverData):
    row = dfRowFromHover(hoverData)
    print "hover_refresh_https:", row
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
        '/static/css/style.css',
        'https://fonts.googleapis.com/css?family=Dosis'
    )
})
