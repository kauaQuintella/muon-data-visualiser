#python -m pip install --proxy="http://proxy.uefs.br:3128" -U matplotlib julian / python -m pip install --proxy="http://proxy.uefs.br:3128" -upgrade pip

from Data import ExperimentData, SettingsData
from DashApp import Dashboard
#from Crud import Crud
#import matplotlib.pyplot as plt
#import numpy as np

# Criando objetos
data = ExperimentData()
#settings = SettingsData(crud)
dashboard = Dashboard()

if __name__ == '__main__':

    # Processamento de dados de arquivo LABENSOL (.lbsl)
    data.processData()

    # Set de dados em dashboard e sua criação
    app = dashboard.mainDash(data)

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

    
    








