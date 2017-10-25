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

NOPAGE_B64 = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAgAAAAIACAYAAAD0eNT6AAAgAElEQVR4Xu3daZAc533f8f/cx+7M3hf2xH0sAIIASVmnLcV2yvFR5Viu8u3YVa5cVXHyJilVJbHzxnmTVCLJiRUddhwnlGTJimJZsmXxMg+RICmCIAEQBHEQ2MUNLLDYXewu9pjUMwQoEMRi5tc925jp/naVinbh3z39fJ5nd37bx/PEjA0BBBBAAAEEIicQi1yLaTACCCCAAAIIGAGAQYAAAggggEAEBQgAEex0mowAAggggAABgDGAAAIIIIBABAUIABHsdJqMAAIIIIAAAYAxgAACCCCAQAQFCAAR7HSajAACCCCAAAGAMYAAAggggEAEBQgAEex0mowAAggggAABgDGAAAIIIIBABAUIABHsdJqMAAIIIIAAAYAxgAACCCCAQAQFCAAR7HSajAACCCCAAAGAMYAAAggggEAEBQgAEex0mowAAggggAABgDGAAAIIIIBABAUIABHsdJqMAAIIIIAAAYAxgAACCCCAQAQFCAAR7HSajAACCCCAAAGAMYAAAggggEAEBQgAEex0mowAAggggAABgDGAAAIIIIBABAUIABHsdJqMAAIIIIAAAYAxgAACCCCAQAQFCAAR7HSajAACCCCAAAGAMYAAAggggEAEBQgAEex0mowAAggggAABgDGAAAIIIIBABAUIABHsdJqMAAIIIIAAAYAxgAACCCCAQAQFCAAR7HSajAACCCCAAAGAMYAAAggggEAEBQgAEex0mowAAggggAABgDGAAAIIIIBABAUIABHsdJqMAAIIIIAAAYAxgAACCCCAQAQFCAAR7HSajAACCCCAAAGAMYAAAggggEAEBQgAEex0mowAAggggAABgDGAAAIIIIBABAUIABHsdJqMAAIIIIAAAYAxgAACCCCAQAQFCAAR7HSajAACCCCAAAGAMYAAAggggEAEBQgAEex0mowAAggggAABgDGAAAIIIIBABAUIABHsdJqMAAIIIIAAAYAxgAACCCCAQAQFCAAR7HSajAACCCCAAAGAMYAAAggggEAEBQgAEex0mowAAggggAABgDGAAAIIIIBABAUIABHsdJqMAAIIIIAAAYAxgAACCCCAQAQFCAAR7HSajAACCCCAAAGAMYAAAggggEAEBQgAEex0mowAAggggAABgDGAAAII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'

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
if __name__ == '__main__':
    app.title = 'security-dashboard'
    app.run_server()
