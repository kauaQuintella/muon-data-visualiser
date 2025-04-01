from datetime import datetime, timedelta
import requests
import gdown

FIRST_STRING = 'Acquisition time\tNeg Width   \tFall time   \tRise time   \tPk-Pk'

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

    def verifyLink (self, url, file_id):

        try:
            # Extrair o ID do arquivo do link compartilhado
            #file_id = url.split('/d/')[1].split('/')[0]
            metadata_url = f"https://drive.google.com/uc?export=download&id={file_id}"

            # Realizar uma requisição para obter as informações do arquivo
            response = requests.get(metadata_url, stream=True)

            # Verificar se a resposta está correta
            if "text/html" in response.headers.get("Content-Type", ""):
                print("Erro: O arquivo não está acessível ou o link está incorreto.")
                return None
            
            # Pegar o nome do arquivo dos cabeçalhos
            content_disposition = response.headers.get("Content-Disposition", "")
            if "filename=" in content_disposition:
                filename = content_disposition.split("filename=")[1].strip('"')
                print(f"Nome do arquivo: {filename}")
                
                # Verificar extensão .lbsl
                if filename.lower().endswith(".lbsl"):
                    print("O arquivo é do tipo .lbsl.")
                    return filename
                else:
                    print("O arquivo não é do tipo .lbsl.")
                    return None
            else:
                print("Não foi possível obter o nome do arquivo.")
                return None

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return None

        #url = "https://drive.google.com/drive/folders/1D80XAHGkujFCqzpMmobuVD-3S9bDS6IV?usp=sharing"
        response = requests.get(url)

        if (FIRST_STRING in response.content):
            with open("data.lbsl", "wb") as file:
                file.write(response.content)
            return True
        else:
            return False

        

    def processData (self, url):
        FILE_PATH = "data.lbsl"
        confirm = False
        #url = "https://drive.google.com/uc?id=1fgm_zJTyqmJ5bi1XGLnPVjLpCt_eeMjU&export=download"
        #response = requests.get(url)
        #url = "https://drive.google.com/file/d/1lQNHwqzCv706MYDySggn9Vn6J1wiA-om/view?usp=drive_link"
        url = "https://docs.google.com/spreadsheets/d/0B7N1fAzIqCLHT2FZTU1zWkdLNE0/edit?usp=drive_link&ouid=102395208117010915304&resourcekey=0-Jgwv5mx8hAM1ZTxAFeva9w&rtpof=true&sd=true"
        
        if ('/d/' in url and self.verifyLink (url, file_id)):
            file_id = url.split('/d/')[1].split('/')[0]
            #confirm = self.verifyLink (url)
             
            gdown.download(f"https://drive.google.com/uc?id={file_id}", FILE_PATH, quiet=False)
            #with open("data.lbsl", "wb") as file:
            #    file.write(response.content)
        
            with open(FILE_PATH, 'r') as file:
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
            confirm = True

        return confirm