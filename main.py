from base_conhecimento import BaseConhecimento
from assistente import Assistente

def main():
    # Caminho do arquivo JSON da base de conhecimento
    caminho_json = "data/base_conhecimento.json"
    
    # Instancia a Base de Conhecimento e carrega os dados do JSON
    base = BaseConhecimento(caminho_json)
    base.carregar()
    
    # Cria o assistente com um nome personalizado para o projeto de PcD
    assistente = Assistente("InclusivAI", base)
    
    # Inicia o loop principal de atendimento no terminal
    assistente.iniciar()

if __name__ == "__main__":
    main()