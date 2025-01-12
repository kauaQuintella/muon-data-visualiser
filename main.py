#python -m pip install --proxy="http://proxy.uefs.br:3128" -U matplotlib julian / python -m pip install --proxy="http://proxy.uefs.br:3128" -upgrade pip

from Data import ExperimentData
from DashApp import Dashboard
from dash import dash, html, dcc
import plotly.express as px
import plotly.io as pio
import pandas as pd
#from Crud import Crud
#import matplotlib.pyplot as plt
#import numpy as np

# Criando objetos
data = ExperimentData()
#settings = SettingsData(crud)
dashboard = Dashboard()

# Processamento de dados de arquivo LABENSOL (.lbsl)
data.processData()


pio.templates.default = "plotly_dark"
stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=stylesheets)
server = app.server

lenEvents = len(data.acqTimeGreg)
listQntEvents = [[1] for i in range(lenEvents)]


# DATAFRAMES
histogramaPkPk = pd.DataFrame ({
    "Tempo": data.acqTimeGreg,
    "pkPk": data.pkPk,
    })

histogramaNegWidht = pd.DataFrame ({
    "Tempo": data.acqTimeGreg,
    "negWidht": data.negWidht,
    })

scatter = pd.DataFrame ({
    "riseTime": data.riseTime,
    "pkPk": data.pkPk,
    })

contagem_x_tempo = pd.DataFrame({
    "Data": data.acqTimeGreg,
    "Eventos": listQntEvents
    })
contagem_x_tempo["Intervalo"] = contagem_x_tempo["Data"].dt.floor("9min")  # Ajustar para 1 hora
contagem_x_tempo_agrupado = contagem_x_tempo.groupby("Intervalo").size().reset_index(name="Contagem")


# FIGs
figPkPk = px.histogram(
    histogramaPkPk,
    title="Histograma de Pico a Pico",
    labels={"Tempo": "Tempo", "pkPk": "Pico a Pico"},
    x = "Tempo",
    y="pkPk",
    )

figNegWidht = px.histogram(
    histogramaNegWidht,
    title="Histograma de Largura de Pulso",
    labels={"Tempo": "Tempo", "negWidht": "Largura Negativa de Pulso"},
    x = "Tempo",
    y="negWidht",
    )

figScatter = px.scatter(
    scatter,
    title="Pico a Pico por Tempo de Subida",
    labels={"pkPk": "Pico à Pico", "riseTime": "Tempo de Subida"},
    x="pkPk",
    y="riseTime"
    )

# Criar o gráfico de contagem x tempo
figContagem_x_tempo = px.line(
    contagem_x_tempo_agrupado,
    title="Contagem de Eventos por Intervalo de Tempo",
    labels={"Intervalo": "Tempo", "Contagem": "Número de Eventos"},
    x="Intervalo",
    y="Contagem"
)

# App Layout
app.layout = html.Div(id="div1",
    children=[
        html.H1("LABENSOL Dash", id="h1"),
        html.Div(
"""
\tO Laboratório de Instrumentação Nuclear e Energia Solar (LABENSOL) desenvolveu um
protótipo de detector que tem como técnica de detecção a medida da radiação Cherenkov gerada
pela passagem das partículas na parte sensível do detector central, que é preenchido com água
filtrada. Esta radiação luminosa gerada é captada por fotomultiplicadores ou PMTs (do inglês
Photo-Multiplier Tube). Para filtrar apenas as partículas incidentes verticalmente, utilizamos um
par de cintiladores orgânicos acoplados em PMTs alinhados verticalmente com o detector central, o
qual fica situado entre os cintiladores. Esta configuração é conhecida como Telescópio de Múons,
pois pode ser direcionado para qualquer direção na qual se deseja medir a incidência de partículas.
"""
        ),
        dcc.Graph(figure=figPkPk, id="graph1"),
        dcc.Graph(figure=figNegWidht, id="graph2"),
        dcc.Graph(figure=figScatter, id="scatter"),
        dcc.Graph(figure=figContagem_x_tempo, id="barFig")
    ]
)

if __name__ == '__main__':

    # Set de dados em dashboard e sua criação
    #app = dashboard.mainDash(data)

    # Execução
    app.run_server(debug=True)


"""
time = np.linspace(0, 5, 10)

#x = [1,2,3,5]
y = np.cos(time)
#plt.plot(time,y)
plt.subplots(nrows = 2, ncols = 2)
plt.show()
"""

    
    








