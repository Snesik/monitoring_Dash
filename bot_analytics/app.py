import datetime
from dash import Dash, html, dcc
import mysql.connector as connection
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from utils import read_yaml
import dash_auth
from users import USERNAME_PASSWORD_PAIRS

app = Dash(__name__)
auth = dash_auth.BasicAuth(
    app,
    USERNAME_PASSWORD_PAIRS
)
config = read_yaml('config/connect_bd.yaml')


def data_base(host, database, user, passwd):
    mydb = connection.connect(host=host,
                              database=database,
                              user=user,
                              passwd=passwd,
                              use_pure=True)
    query = 'select p1.bot, p2.bal, p2.buy, sell, sell_count, status_2, status_2_count, percent_15, sum, p1.maxdata ' \
            'from (' \
            'select bot, max(data) as maxdata from trade_statistick group by bot) as p1 ' \
            'left join trade_statistick p2 ON p1.bot = p2.bot and p2.data = p1.maxdata'

    data = pd.read_sql(query, mydb)
    mydb.close()  # close the connection
    data.bal = data.bal.astype(int)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=data.bot, y=data.bal,
                         marker_color='green',
                         name='bal',
                         ))
    fig.add_trace(go.Bar(x=data.bot, y=data.buy,
                         marker_color='blue',
                         name='buy'))
    fig.add_trace(go.Bar(x=data.bot, y=data.sell,
                         marker_color='red',
                         name='sell'))
    fig.add_trace(go.Bar(x=data.bot, y=data.sell_count,
                         marker_color='orange',
                         name='sell_count'))
    fig.add_trace(go.Bar(x=data.bot, y=data.status_2,
                         marker_color='black',
                         name='status_2'))
    fig.add_trace(go.Bar(x=data.bot, y=data.status_2_count,
                         marker_color='crimson',
                         name='status_2_count'))
    fig.add_trace(go.Bar(x=data.bot, y=data.percent_15,
                         marker_color='crimson',
                         name='percent_15'))
    fig.add_trace(go.Bar(x=data.bot, y=data['sum'],
                         marker_color='turquoise',
                         name='sum'))
    fig.update_layout(title='Информация по каждому боту в отдельности')

    fig.update_traces(texttemplate='%{y:.0f}', textposition='outside', textfont_size=10)

    fig1 = px.bar(data, x="bot", y="bal", color="sum", barmode="group", text_auto='.0f')
    fig1.update_traces(textfont_size=12, textangle=0, textposition="outside")
    fig1.update_layout(title='Тестовый стенд')

    data.mean(numeric_only=True)
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=data.columns, y=data.sum(),
                          marker_color='turquoise',
                          name='sum'))

    fig2.update_traces(texttemplate='%{y:.0f}', textposition='outside', textfont_size=11)
    fig2.update_layout(title='Общие показатели всех ботов')
    return fig1, fig, fig2, data


def serve_layout():
    fig1, fig, fig2, data = data_base(**config)

    data = html.Div(children=[
        html.H1(children='НАШИ УСПЕХИ'),

        html.Div(children=f'''
           {'The time is: ' + str(datetime.datetime.now())}
        '''),

        html.Button('Нажми', id='inp-btn'),
        html.Div(id='out', children='Начальное значение'),
        dcc.Graph(
            id='example-graph1',
            figure=fig1,

        ),
        dcc.Graph(
            id='example-graph2',
            figure=fig

        ),
        dcc.Graph(
            id='example-graph3',
            figure=fig2

        ),
        dcc.Interval(
            id='interval-component',
            interval=1 * 1000,  # in milliseconds
            n_intervals=0
        )

    ])

    return data


app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=False)
