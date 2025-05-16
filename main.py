from Data import ExperimentData
from dash import dash, html, dcc, Input, Output, State
import plotly.express as px
import plotly.io as pio
import pandas as pd


def dashFigs (data):
    """
    Função para crianção de figuras Dash. Houve-se a modularização para reuso no projeto.

    :param data: ExperimentData

    :return figPkPk: Figure
    :return figNegWidht: Figure
    :return figScatter: Figure
    :return figContagem_x_tempo: Figure
    """

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
        "Eventos": data.listQntEvents
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

    return (figPkPk, figNegWidht, figScatter,figContagem_x_tempo)

#--- INICIO CÓDIGO ---#

# Criando objetos
data = ExperimentData()

# Processamento de dados de arquivo LABENSOL (.lbsl)
url = "https://drive.google.com/file/d/1lQNHwqzCv706MYDySggn9Vn6J1wiA-om/view?usp=drive_link" #dado de teste do experimento
confirm = data.processData(url)

if(not(confirm)):
    print("Arquivo errado amigão!")

else:

    # Configuração e criação de Dash
    pio.templates.default = "plotly_dark"
    stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=stylesheets)
    server = app.server

    #Criação de figuras
    (figPkPk, figNegWidht, figScatter,figContagem_x_tempo) = dashFigs(data)

    #Criação de Layout do Dash
    app.layout = html.Div(id="mainDiv",
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

            \n\nFeito por: Kauã de Quintella Paes Oliveira
            """
            ),

            html.Div(dcc.Input(id='input-on-submit', type='text')),
            html.Button('Submit', id='submit-val', n_clicks=0),
            html.Div(id='container-button-basic',
                    children='Copie e cole o link do .lbsl do experimento'),

            dcc.Graph(figure=figPkPk, id="graph1"),
            dcc.Graph(figure=figNegWidht, id="graph2"),
            dcc.Graph(figure=figScatter, id="scatter"),
            dcc.Graph(figure=figContagem_x_tempo, id="barFig"),

        ]
    )


@app.callback(
    [
        Output('graph1', 'figure'),
        Output('graph2', 'figure'),
        Output('scatter', 'figure'),
        Output('barFig', 'figure'),
        Output('container-button-basic', 'children')
    ],
    Input('submit-val', 'n_clicks'),
    State('input-on-submit', 'value'),
    prevent_initial_call=True
)
def updateFile (n_clicks,value):
    """
    Função com callback de Dash para alterar figuras caso haja alteração de link

    :param n_clicks: Any
    :param value: Any

    :return figPkPk: Figure
    :return figNegWidht: Figure
    :return figScatter: Figure
    :return figContagem_x_tempo: Figure
    """

    confirm = data.processData(value)

    if not confirm:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, "Arquivo errado amigão!"

    (figPkPk, figNegWidht, figScatter,figContagem_x_tempo) = dashFigs(data)

    return figPkPk, figNegWidht, figScatter, figContagem_x_tempo, "Dados atualizados com sucesso!"

if __name__ == '__main__':
    # Execução
    app.run(debug=True)#app.run_server!!!

    
    








