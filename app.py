from flask import Flask, render_template

import json
import plotly
import os

import pandas as pd
import numpy as np

app = Flask(__name__)
app.debug = True
app._static_folder = os.path.abspath("static/")

@app.route('/')
@app.route('/tankbonnen')
def tankbonnen():
    df = pd.read_csv('../../notebooks/data/tankbonnen.csv', sep=',')
    graphs = [
        dict(
            data=[
                dict(
                    x=df['date'],
                    y=df['price'],
                    marker=dict(
                      color='rgb(102,153,255)',
                        line=dict(
                                color='rgb(8,48,107)',
                                width=.5),
                        ),
                    type='bar'
                ),
            ],
            layout=dict(
                xaxis=dict(                 
                    title="Date"
                ),
                yaxis=dict(                 
                    title="Price [EUR]",
                    ticks="",
                    showticklabels=False
                ),
                annotations=[
                    dict(x=xi,y=yi,
                         text=str(yi),
                         xanchor='center',
                         yanchor='bottom',
                         showarrow=False,
                    ) for xi, yi in zip(df['date'], df['price'])],
                title='Price of diesel in EUR',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
        ),
        dict(
            data=[
                dict(
                    x=df['date'],
                    y=df['kilometers'],
                    marker=dict(
                        color='rgb(102,153,255)',
                        line=dict(
                            color='rgb(8,48,107)',
                            width=.5),
                    )
                ),
            ],
            layout=dict(
                xaxis=dict(                 
                    title="Date"
                ),
                yaxis=dict(                 
                    title="Kilometers",
                    
                ),
                title='Amount of kilometers',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
        ),
        dict(
            data=[
                dict(
                    type = 'scattergeo',
                    locationmode = 'europe',
                    lon = df['longitude'],
                    lat = df['latitude'],
                    hoverinfo = 'text',
                    text = df['location'],
                    mode = 'markers',
                    marker = dict( 
                        size=df['amount']*2,
                        color='rgb(255, 0, 0)',
                        line = dict(
                            width=3,
                            color='rgba(102, 153, 255, 0)'
                        )
                    )),
            ],
            layout=dict(
                title = 'Locations of gas stations',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend = False, 
                geo = dict(
                    resolution=50,
                    scope='europe',
                    projection=dict(
                        type="azimuthal equidistant",
                    ),
                    showland = True,
                    showcoastlines = True,
                    showframe = False,
                    showocean = True,
                    showlakes = True,
                    showrivers = False,
                    showcountries = True,
                    landcolor = 'rgb(243, 243, 243)',
                    countrycolor = 'rgb(204, 204, 204)',
                ),
            )
        ),
        dict(
            data=[
                dict(
                    x=df['date'],
                    y=df['distance'],
                    marker=dict(
                      color='rgb(102,153,255)',
                        line=dict(
                                color='rgb(8,48,107)',
                                width=.5),
                        ),
                    type='bar'
                ),
            ],
            layout=dict(
                xaxis=dict(                 
                    title="Date"
                ),
                yaxis=dict(                 
                    title="Distance",
                    showticklabels=True
                ),
                title='Distance travelled',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
        ),
    ]

    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('layouts/index.html',
                           ids=ids,
                           graphJSON=graphJSON)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
