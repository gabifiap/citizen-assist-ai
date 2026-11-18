import json
from orientacao import Orientacao

class BaseConhecimento:
    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []

    def carregar(self):
        """Lê o arquivo JSON e cria os objetos Orientacao de forma segura."""
        try:
            with open(self.caminho, 'r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)
                self.orientacoes = []
                for item in dados:
                    orientacao = Orientacao(
                        id=item.get("id"),
                        categoria=item.get("categoria"),
                        titulo=item.get("titulo"),
                        palavras_chave=item.get("palavras_chave", []),
                        resposta=item.get("resposta"),
                        documentos=item.get("documentos", []),
                        onde=item.get("onde"),
                        fonte=item.get("fonte"),
                        verificado_em=item.get("verificado_em")
                    )
                    self.orientacoes.append(orientacao)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Aviso: Arquivo de base de conhecimento não encontrado ou corrompido. Iniciando com lista vazia.")
            self.orientacoes = []

    def categorias(self):
        """Retorna uma lista com todas as categorias únicas cadastradas."""
        cats = []
        for ori in self.orientacoes:
            if ori.categoria not in cats:
                cats.append(ori.categoria)
        return cats

    def por_categoria(self, nome_categoria):
        """Filtra e retorna as orientações pertencentes a uma categoria específica."""
        resultado = []
        for ori in self.orientacoes:
            if ori.categoria.lower() == nome_categoria.lower():
                resultado.append(ori)
        return resultado

    def normalizar(self, texto):
        """Remove acentos, pontuações e converte o texto para minúsculas para padronizar a busca."""
        if not texto:
            return ""
        
        acentos = {
            "á": "a", "à": "a", "ã": "a", "â": "a", "ä": "a",
            "é": "e", "ê": "e", "ë": "e",
            "í": "i", "ï": "i",
            "ó": "o", "ô": "o", "õ": "o", "ö": "o",
            "ú": "u", "ü": "u",
            "ç": "c"
        }
        
        texto = texto.lower().strip()
        for letra, troca in acentos.items():
            texto = texto.replace(letra, troca)
            
        sinais = "?!.,;:()-_/\\"
        for sinal in sinais:
            texto = texto.replace(sinal, " ")
            
        return " ".join(texto.split())

    def buscar(self, pergunta):
        """Compara a pergunta com as orientações, pontua e retorna uma lista de tuplas (pontos, orientacao)."""
        pergunta_norm = self.normalizar(pergunta)
        palavras_pergunta = pergunta_norm.split()
        
        pontuadas = []
        
        for ori in self.orientacoes:
            pontos = 0
            
            # Regra 1: +3 pontos se palavra-chave da orientação aparece na pergunta
            for pc in ori.palavras_chave:
                pc_norm = self.normalizar(pc)
                if pc_norm in pergunta_norm:
                    pontos += 3
                    
            # Regra 2: +1 ponto para cada palavra da pergunta (com 4 ou mais letras) que aparece no título
            titulo_norm = self.normalizar(ori.titulo)
            for palavra in palavras_pergunta:
                if len(palavra) >= 4 and palavra in titulo_norm:
                    pontos += 1
                    
            if pontos > 0:
                pontuadas.append((pontos, ori))
                
        # Ordena da maior pontuação para a menor
        pontuadas.sort(key=lambda x: x[0], reverse=True)
        return pontuadas