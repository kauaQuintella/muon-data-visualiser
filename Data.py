from datetime import datetime, timedelta
import requests

class ExperimentData:

    def __init__ (self):
        self.filePath = ""
        self.acqTimeJul = []
        self.acqTimeGreg = []
        self.negWidht = []
        self.fallTime = []
        self.riseTime = []
        self.pkPk = []
        #crud.createBackup()
        
    
    def julianToGregorian (self, julian_date):
        
        julian_epoch = 2440587.5  # Data juliana correspondente ao Unix Epoch (1970-01-01 00:00:00 UTC)
        # real_julian_date = 2451545 + julian_date #CONVERSÃO PARA DATA REAL, ALTERAÇÃO ESPECÍFICA DO PROGRAMA

        seconds_since_epoch = (julian_date - julian_epoch) * 86400  # Calcula o número de segundos desde o Unix epoch
        date = datetime(1970, 1, 1, 0, 0, 0)  # Ponto inicial do Unix Epoch (UTC)
        date += timedelta(seconds=seconds_since_epoch)  # Adiciona os segundos calculados   

        return date    

    def processData (self):

        url = "https://drive.google.com/uc?id=1fgm_zJTyqmJ5bi1XGLnPVjLpCt_eeMjU&export=download"
        response = requests.get(url)
        with open("dataEDT.lbsl", "wb") as file:
            file.write(response.content)
    
        filepath = "dataEDT.lbsl"

        with open(filepath, 'r') as file:
            # Ignorar a primeira linha
            next(file)
            for line in file:
                
                # Separar os valores na linha por espaço ou tabulação
                values = line.split()
                
                # Adicionar os valores nas listas apropriadas
                if (values [0].find(',') > -1):
                    change = values [0]
                    values[0] = change.replace(",", ".")
                    

                values[0] = float(values[0]) + 2451545 # CONVERSÃO PARA DATA REAL, ALTERAÇÃO ESPECÍFICA DO PROGRAMA
                self.acqTimeJul.append(values[0])
                self.negWidht.append(float(values[1]))
                self.fallTime.append(float(values[2]))
                self.riseTime.append(float(values[3]))
                self.pkPk.append(float(values[4]))

                
                gregorianDate = self.julianToGregorian(float(values[0]))
                self.acqTimeGreg.append(gregorianDate)