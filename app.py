import pymysql
import pandas as pd
import configparser

from pandas_highcharts.core import serialize

from flask import Flask, render_template, request

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

@app.route('/graph')
def graph_Example(chartID = 'chart_ID', chart_type = 'line', chart_height = 500):

    sql = "select load_dtm, nickname, damage_dealt, frags from battle_stats where nickname = 'explore45' order by load_dtm"

    connection = pymysql.connect(host=config['DATABASE']['HOST'],
                                 user=config['DATABASE']['USER'],
                                 password=config['DATABASE']['PASSWORD'],
                                 database=config['DATABASE']['DATABASE'],
                                 cursorclass=pymysql.cursors.DictCursor)

    df = pd.read_sql(sql, connection, index_col='load_dtm')

    dataset = serialize(df, render_to='my-chart', secondary_y='frags', output_type='json')

    connection.close()

    return render_template('graph.html', chart=dataset)

@app.route('/')
def main():
	return """
    <h1>Pandas with Highcharts</h1>
    <a href='graph'>Click here for graph</a>
    """

# app.run(debug=True)
