
BACKGROUND = 'rgb(230, 230, 230)'

COLORSCALE = [[0, "#4CAF50"],
              [0.25, "#7FC049"],
              [0.5, "#C9D144"],
              [0.75, "#E29A3E"],
              [1, "#F44336"]]


def add_markers(figure_data,
                domains,
                plot_type='scatter3d'):
    """

    :param figure_data:
    :param domains:
    :param plot_type:
    :return:
    """
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


def create_scatter_plot(x, y, z, size, color, xlabel, ylabel, zlabel, plot_type, text, markers=[] ):
    """

    :param x: dataset asse X
    :param y: dataset asse Y
    :param z: dataset asse Z
    :param size: dataset
    :param color: gradiente di colori
    :param xlabel: Label asse X
    :param ylabel: Label asse Y
    :param zlabel: Label asse Z
    :param plot_type: tipo di grafico
    :param text:
    :param markers:
    :return:
    """
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
        text = text,
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

    '''
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
    '''

    if len(markers) > 0:
        data = data + add_markers(data, markers, plot_type=plot_type)

    return dict( data=data, layout=layout )