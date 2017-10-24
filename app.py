# -*- coding: utf-8 -*-
import os
import flask
import dash
import pandas as pd

import dash_html_components as html

from dash.dependencies import Input, Output
from plot import create_scatter_plot
from score import evalute_https_score, evalute_performance_score, evalute_trust_score, merge_df_results
from layout import get_html_layout, make_dash_table


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

# Rendering del plot sulla pagina Html
app.layout = get_html_layout(starting_domain,
                             DOMAIN_IMG,
                             domain_description,
                             domain_plot,
                             df_result)

@app.callback(
    Output('clickable-graph', 'figure'),
    [Input('chem_dropdown', 'value'),
     Input('charts_radio', 'value')])
def highlight_domain(chem_dropdown_values, plot_type):
    print "**CALLBACK::highlight_domain**"
    return create_scatter_plot(x, y, z, size, color, xlabel, ylabel, zlabel, plot_type, text)

@app.callback(
    Output('table-element', 'children'),
    [Input('chem_dropdown', 'value')])
def update_table(chem_dropdown_value):
    print "**CALLBACK::update_table**"
    """ Modifica la tabella con i domini selezionati """
    table = make_dash_table( chem_dropdown_value, df_result)
    return table


def dfRowFromHover( hoverData ):
    print "**CALLBACK::dfRowFromHover**"
    """ Ritorna il dominio in hover """
    if hoverData is not None:
        if 'points' in hoverData:
            firstPoint = hoverData['points'][0]
            if 'pointNumber' in firstPoint:
                point_number = firstPoint['pointNumber']
                domain_name = str(domain_plot['data'][0]['text'][point_number]).strip()
                return df_result.loc[df_result['Domain'] == domain_name]
    return pd.Series()

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
    Output('chem_desc', 'children'),
    [Input('clickable-graph', 'hoverData')])
def display_domain(hoverData):
    print "**CALLBACK::display_domain** -->", hoverData
    """ Ritorna il layout HTML dei parametri del dominio in hover"""
    row = dfRowFromHover(hoverData)
    if row.empty:
        return
    description = html.Div([
        html.P("HTTPS SCORE: " + str(row['HTTPS Score'].iloc[0])),
        html.P("PERFORMANCE SCORE: " + str(row['Performance Score'].iloc[0])),
        html.P("TRUST SCORE: " + str(row['Trust Score'].iloc[0])),
        html.P("TOT SCORE: " + str(row['Tot Score'].iloc[0])),
    ], style={'margin-top': '15px'}),

    return description

@app.server.route('/static/<resource>')
def serve_static(resource):
    """ Serve gli statici dalla cartella /static/ """
    return flask.send_static_file(resource)

# Aggiunta di file CSS esterni
external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "//fonts.googleapis.com/css?family=Dosis:Medium",
                "/static/css/style.css"]

for css in external_css:
    app.css.append_css({"external_url": css})

if __name__ == '__main__':
    app.title = 'security-dashboard'
    app.run_server()
