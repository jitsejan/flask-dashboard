from flask import Flask, render_template

import json
import plotly

import pandas as pd
import numpy as np

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    df = pd.read_csv('../../notebooks/data/tankbonnen.csv', sep=',')


    graphs = [
        dict(
            data=[
                dict(
                    x=df['date'],
                    y=df['price'],
                    type='bar'
                ),
            ],
            layout=dict(
                title='Price per liter'
            )
        ),
        dict(
            data=[
                dict(
                    x=df['date'],
                    y=df['kilometers'],
                    type='scatter'
                ),
            ],
            layout=dict(
                title='Amount of kilometers'
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
                showlegend = False, 
                geo = dict(
                    resolution=50,
                    scope='europe',
                    projection=dict(
                        type="azimuthal equidistant",
                    ),
                    showland = True,
                    showcoastlines = True,
                    showframe = True,
                    showocean = True,
                    showlakes = True,
                    showrivers = False,
                    showcountries = True,
                    landcolor = 'rgb(243, 243, 243)',
                    countrycolor = 'rgb(204, 204, 204)',
                ),
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
