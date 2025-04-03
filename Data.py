from datetime import datetime, timedelta
import requests
import gdown

class ExperimentData:

    def __init__ (self):
        self.initVariables ()

    def initVariables (self):
        """
        Função para inicializar variáveis, foi feita dessa maneira para reultilização em código

        :param self: Self@ExperimentData
        """

        self.filePath = ""
        self.acqTimeJul = []
        self.acqTimeGreg = []
        self.negWidht = []
        self.fallTime = []
        self.riseTime = []
        self.pkPk = []
        self.listQntEvents = []
        self.lenEvents = 0


    def julianToGregorian (self, julian_date):
        """
        Função para conversão do Juliano alterado para Gregoriano

        :param self: Self@ExperimentData
        :param julian_date: float

        :return date: datetime
        """

        julian_epoch = 2440587.5  # Data juliana correspondente ao Unix Epoch (1970-01-01 00:00:00 UTC)
        # real_julian_date = 2451545 + julian_date #CONVERSÃO PARA DATA REAL, ALTERAÇÃO ESPECÍFICA DO PROGRAMA

        seconds_since_epoch = (julian_date - julian_epoch) * 86400  # Calcula o número de segundos desde o Unix epoch
        date = datetime(1970, 1, 1, 0, 0, 0)  # Ponto inicial do Unix Epoch (UTC)
        date += timedelta(seconds=seconds_since_epoch)  # Adiciona os segundos calculados   

        return date    


    def verifyLink (self, url, file_id):
        """
        Função específica para verificar se o link do usuário é válido ou não. Faz-se necessário o arquivo está acessível, o link estar correto e ser da extensão .lbsl. Ao final da verificação

        :param self: Self@ExperimentData
        :param url: string
        :param file_id: string

        :return Boolean: Boolean
        """

        try:
            metadata_url = f"https://drive.google.com/uc?export=download&id={file_id}"

            # Realizar uma requisição para obter as informações do arquivo
            response = requests.get(metadata_url, stream=True)

            # Verificar se a resposta está correta
            if not("text/html" in response.headers.get("Content-Type", "")):
                
                # Pegar o nome do arquivo dos cabeçalhos
                content_disposition = response.headers.get("Content-Disposition", "") 
                if "filename=" in content_disposition:
                    filename = content_disposition.split("filename=")[1].strip('"')
                    print(f"Nome do arquivo: {filename}")

                    # Verificar se a extensão do arquivo é .lbsl
                    if filename.lower().endswith(".lbsl"):
                        print("Verificação concluida com sucesso!")
                        return True
                    
            print("Erro: O arquivo pode não está acessível ou o link está incorreto ou arquivo não é .lbsl")
            return False
            
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return False
        

    def processData (self, url):
        """
        Função para analise de arquivo enviado pelo usuário e, caso esteja correto, processamento do mesmo. Caso tenha algum problema, retornara um boolean False, para evitar que o Dash faça uma possível alteração.

        :param self: Self@ExperimentData
        :param url: string

        :return confirm: Boolean
        """

        FILE_PATH = "data.lbsl"
        confirm = False

        if ('/d/' in url): # Caso não tenha '\d\' no URL, retornará falso para confirmação
            file_id = url.split('/d/')[1].split('/')[0]
    
            if (self.verifyLink (url, file_id)): # Verificação de link

                self.initVariables()# Reset de variaveis
                gdown.download(f"https://drive.google.com/uc?id={file_id}", FILE_PATH, quiet=False)# Download arquivo
            
                # Abertura arquivo
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

                        
                        gregorianDate = self.julianToGregorian(float(values[0])) #Conversão de Juliano alterado para Gregoriano
                        self.acqTimeGreg.append(gregorianDate)
                
               
                self.lenEvents = len(self.acqTimeGreg) # Quantidade de Eventos
                self.listQntEvents = [[1] for i in range(self.lenEvents)] # Lista que tem o len dos eventos
                
                confirm = True #confirmação de que deu certo!

        return confirm #retorno da confirmação