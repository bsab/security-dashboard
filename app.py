import os
import flask
import dash
import pandas as pd

from dash.dependencies import Input, Output
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

#1) import del csv relativo al test HTTPS (pshtt scanner)
df_score_https = evalute_https_score("csv/pshtt.csv")

#2) import del csv relativo al test sulle performance (pageload scanner)
df_score_performance = evalute_performance_score("csv/pageload.csv")

#3) import del csv relativo al test sull'affidabilita' (trustymail scanner)
df_trust_performance = evalute_trust_score("csv/trustymail.csv")

#4)
df_result = merge_df_results(df_score_https, df_score_performance, df_trust_performance)

df = df_result

def add_markers( figure_data, domains, plot_type = 'scatter3d' ):
    indices = []
    domain_data = figure_data[0]
    for m in domains:
        hover_text = domain_data['text']
        for i in range(len(hover_text)):
            if m == hover_text[i]:
                indices.append(i)

    if plot_type == 'histogram2d':
        plot_type = 'scatter'

    traces = []
    for point_number in indices:
        trace = dict(
            x = [ domain_data['x'][point_number] ],
            y = [ domain_data['y'][point_number] ],
            marker = dict(
                color = 'red',
                size = 16,
                opacity = 0.6,
                symbol = 'cross'
            ),
            type = plot_type
        )

        if plot_type == 'scatter3d':
            trace['z'] = [ domain_data['z'][point_number] ]

        traces.append(trace)

    return traces


BACKGROUND = 'rgb(230, 230, 230)'
COLORSCALE = [[0, "F44336"], [0.25, "#E29A3E"],
               [0.5, "#C9D144"], [0.75, "#7FC049"], [1, "#4CAF50"] ]

def create_scatter_plot(
        x=df['HTTPS Score'],
        y=df['Performance Score'],
        z=df['Trust Score'],
        size=df['Tot Score'],
        color=df['Tot Score'],
        xlabel = 'Sicurezza',
        ylabel = 'Performance',
        zlabel = 'Trust mail',
        plot_type = 'scatter3d',
        markers = [] ):

    def axis_template_3d( title, type='linear' ):
        return dict(
            showbackground = True,
            backgroundcolor = BACKGROUND,
            gridcolor = 'rgb(255, 255, 255)',
            title = title,
            type = type,
            zerolinecolor = 'rgb(255, 255, 255)'
        )

    def axis_template_2d(title):
        return dict(
            xgap = 10, ygap = 10,
            backgroundcolor = BACKGROUND,
            gridcolor = 'rgb(255, 255, 255)',
            title = title,
            zerolinecolor = 'rgb(255, 255, 255)',
            color = '#444'
        )

    def blackout_axis( axis ):
        axis['showgrid'] = False
        axis['zeroline'] = False
        axis['color']  = 'white'
        return axis

    data = [ dict(
        x = x,
        y = y,
        z = z,
        mode = 'markers',
        marker = dict(
            colorscale = COLORSCALE,
            colorbar = dict( title = "Grado di<br>Sicurezza" ),
            line = dict( color = '#444' ),
            reversescale = True,
            sizeref = 45,
            sizemode = 'diameter',
            opacity = 0.7,
            size = size,
            color = color,
        ),
        text = df['Domain'],
        type = plot_type,
    ) ]

    layout = dict(
        font = dict( family = 'Raleway' ),
        hovermode = 'closest',
        margin = dict( r=20, t=0, l=0, b=0 ),
        showlegend = False,
        scene = dict(
            xaxis = axis_template_3d( xlabel ),
            yaxis = axis_template_3d( ylabel ),
            zaxis = axis_template_3d( zlabel, 'log' ),
            camera = dict(
                up=dict(x=0, y=0, z=1),
                center=dict(x=0, y=0, z=0),
                eye=dict(x=0.08, y=2.2, z=0.08)
            )
        )
    )

    if plot_type in ['histogram2d', 'scatter']:
        layout['xaxis'] = axis_template_2d(xlabel)
        layout['yaxis'] = axis_template_2d(ylabel)
        layout['plot_bgcolor'] = BACKGROUND
        layout['paper_bgcolor'] = BACKGROUND
        del layout['scene']
        del data[0]['z']

    if plot_type == 'histogram2d':
        # Scatter plot overlay on 2d Histogram
        data[0]['type'] = 'scatter'
        data.append( dict(
            x = x,
            y = y,
            type = 'histogram2d',
            colorscale = 'Greys',
            showscale = False
        ) )
        layout['plot_bgcolor'] = 'black'
        layout['paper_bgcolor'] = 'black'
        layout['xaxis'] = blackout_axis(layout['xaxis'])
        layout['yaxis'] = blackout_axis(layout['yaxis'])
        layout['font']['color'] = 'white'

    if len(markers) > 0:
        data = data + add_markers( data, markers, plot_type = plot_type )

    return dict( data=data, layout=layout )



FIGURE = create_scatter_plot()
STARTING_DOMAIN = '1cdbacoli.gov.it'
DOMAIN_DESCRIPTION = ""
DOMAIN_IMG = "http://www.freepnglogos.com/uploads/a-letter-logo-png-6.png"

app.layout = get_html_layout(STARTING_DOMAIN,
                             DOMAIN_IMG,
                             DOMAIN_DESCRIPTION,
                             FIGURE,
                             df)

@app.callback(
    Output('clickable-graph', 'figure'),
    [Input('chem_dropdown', 'value'),
     Input('charts_radio', 'value')])
def highlight_domain(chem_dropdown_values, plot_type):
    return create_scatter_plot(markers = chem_dropdown_values, plot_type = plot_type)


@app.callback(
    Output('table-element', 'children'),
    [Input('chem_dropdown', 'value')])
def update_table(chem_dropdown_value):
    table = make_dash_table( chem_dropdown_value, df )
    return table


def dfRowFromHover( hoverData ):
    ''' Returns row for hover point as a Pandas Series '''
    if hoverData is not None:
        if 'points' in hoverData:
            firstPoint = hoverData['points'][0]
            if 'pointNumber' in firstPoint:
                point_number = firstPoint['pointNumber']
                domain_name = str(FIGURE['data'][0]['text'][point_number]).strip()
                return df.loc[df['Domain'] == domain_name]
    return pd.Series()


@app.callback(
    Output('chem_name', 'children'),
    [Input('clickable-graph', 'hoverData')])
def return_domain_name(hoverData):
    if hoverData is not None:
        if 'points' in hoverData:
            firstPoint = hoverData['points'][0]
            if 'pointNumber' in firstPoint:
                point_number = firstPoint['pointNumber']
                domain_name = str(FIGURE['data'][0]['text'][point_number]).strip()
                return domain_name


@app.callback(
    dash.dependencies.Output('chem_name', 'href'),
    [dash.dependencies.Input('clickable-graph', 'hoverData')])
def return_href(hoverData):
    row = dfRowFromHover(hoverData)
    if row.empty:
        return
    #datasheet_link = row['PAGE'].iloc[0]
    datasheet_link = "http://" + row['Domain'].iloc[0]
    return datasheet_link


@app.callback(
    Output('chem_img', 'src'),
    [Input('clickable-graph', 'hoverData')])
def display_image(hoverData):
    row = dfRowFromHover(hoverData)
    if row.empty:
        return

    img_src = row['Sticker'].iloc[0]
    return img_src


@app.callback(
    Output('chem_desc', 'children'),
    [Input('clickable-graph', 'hoverData')])

def display_domain(hoverData):
    row = dfRowFromHover(hoverData)
    if row.empty:
        return

    description = row['Domain'].iloc[0]
    return description

@app.server.route('/static/<resource>')
def serve_static(resource):
    return flask.send_from_directory(STATIC_PATH, resource)

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "//fonts.googleapis.com/css?family=Dosis:Medium",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/0e463810ed36927caf20372b6411690692f94819/dash-security-dashboard-demo-stylesheet.css"]


for css in external_css:
    app.css.append_css({"external_url": css})


if __name__ == '__main__':
    app.run_server()
