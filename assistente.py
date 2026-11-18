import json
import csv
import time
import os
from datetime import datetime

class Assistente:
    def __init__(self, nome, base):
        self.nome = nome
        self.base = base
        self.caminho_historico = "data/historico.json"
        self.caminho_csv = "data/atendimentos.csv"
        self.historico = self._carregar_historico()
        self.notas_facilidade = []

    def _carregar_historico(self):
        """Carrega o histórico existente ou retorna uma lista vazia se não existir/estiver corrompido."""
        if not os.path.exists(self.caminho_historico):
            return []
        try:
            with open(self.caminho_historico, "r", encoding="utf-8") as f:
                dados = json.load(f)
                return dados if isinstance(dados, list) else []
        except (json.JSONDecodeError, IOError):
            return []

    def _salvar_historico(self):
        """Salva a lista de atendimentos no arquivo JSON."""
        os.makedirs("data", exist_ok=True)
        with open(self.caminho_historico, "w", encoding="utf-8") as f:
            json.dump(self.historico, f, ensure_ascii=False, indent=2)

    def _contem_dado_pessoal(self, texto):
        """Bloqueia textos com '@' ou com 8 ou mais dígitos numéricos."""
        if "@" in texto:
            return True
        digitos = sum(1 for c in texto if c.isdigit())
        return digitos >= 8

    def _nivel_confianca(self, pontos):
        """Classifica a confiança conforme a pontuação obtida."""
        if pontos >= 6:
            return "ALTA"
        elif pontos >= 3:
            return "MÉDIA"
        return "BAIXA"

    def _perguntar_sim_nao(self, mensagem):
        """Garante que o usuário responda apenas 's' ou 'n' sem quebrar o programa."""
        while True:
            resp = input(mensagem).strip().lower()
            if resp in ("s", "n"):
                return resp == "s"
            print("Entrada inválida. Digite apenas 's' para sim ou 'n' para não.")

    def registrar(self, origem, pergunta, id_orientacao, encontrou, ajudou, tentativas, tempo_segundos):
        """Registra os dados do atendimento no histórico e atualiza o JSON."""
        registro = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": id_orientacao,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo_segundos": tempo_segundos
        }
        self.historico.append(registro)
        self._salvar_historico()

    def perguntar(self):
        """Gerencia o fluxo de perguntas em texto livre."""
        inicio = time.time()
        tentativas = 0

        while True:
            pergunta = input("\nDigite sua dúvida (0 para voltar): ").strip()

            if pergunta == "0":
                return

            if not pergunta:
                print("A dúvida não pode estar vazia. Tente novamente.")
                continue

            if self._contem_dado_pessoal(pergunta):
                print("Atenção: não digite CPF, telefone ou e-mail. Reescreva.")
                continue

            tentativas += 1
            resultados = self.base.buscar(pergunta)

            # Considera encontrada apenas se a melhor pontuação for >= 3
            if not resultados or resultados[0][0] < 3:
                print("\nNão encontrei uma orientação exata para essa dúvida.")
                print("Tente usar outras palavras-chave ou consulte as categorias disponíveis no menu.")
                cats = self.base.categorias()
                if cats:
                    print("Categorias disponíveis:", ", ".join(cats))

                tentar_novamente = self._perguntar_sim_nao("Deseja reformular sua dúvida? (s/n): ")
                if not tentar_novamente:
                    tempo_total = round(time.time() - inicio, 1)
                    self.registrar("pergunta", pergunta, None, False, False, tentativas, tempo_total)
                    return
                continue

            # Melhor resultado encontrado
            melhor_pontos, melhor_ori = resultados[0]
            confianca = self._nivel_confianca(melhor_pontos)

            print(f"\nConfiança da resposta: {confianca} ({melhor_pontos} pontos)")
            melhor_ori.exibir()

            # Exibe até 2 alternativas caso também tenham pontuação >= 3
            alternativas = [r for r in resultados[1:3] if r[0] >= 3]
            if alternativas:
                print("\nOutras orientações relacionadas:")
                for pts, alt_ori in alternativas:
                    print(f" - [{alt_ori.categoria}] {alt_ori.titulo} ({pts} pts)")

            ajudou = self._perguntar_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
            tempo_total = round(time.time() - inicio, 1)
            self.registrar("pergunta", pergunta, melhor_ori.id, True, ajudou, tentativas, tempo_total)
            return

    def navegar(self):
        """Permite navegar pelas categorias e orientações numeradas."""
        inicio = time.time()
        cats = self.base.categorias()

        if not cats:
            print("\nNenhuma categoria cadastrada na base de conhecimento.")
            return

        while True:
            print("\n--- Categorias Disponíveis ---")
            for idx, cat in enumerate(cats, start=1):
                print(f"{idx}. {cat}")
            print("0. Voltar ao menu principal")

            escolha = input("Escolha o número da categoria: ").strip()
            if escolha == "0":
                return

            if not escolha.isdigit() or not (1 <= int(escolha) <= len(cats)):
                print("Opção inválida. Digite um número da lista.")
                continue

            cat_escolhida = cats[int(escolha) - 1]
            orientacoes_cat = self.base.por_categoria(cat_escolhida)

            while True:
                print(f"\n--- Orientações em: {cat_escolhida} ---")
                for idx, ori in enumerate(orientacoes_cat, start=1):
                    print(f"{idx}. {ori.titulo}")
                print("0. Voltar às categorias")

                escolha_ori = input("Escolha o número da orientação: ").strip()
                if escolha_ori == "0":
                    break

                if not escolha_ori.isdigit() or not (1 <= int(escolha_ori) <= len(orientacoes_cat)):
                    print("Opção inválida. Digite um número da lista.")
                    continue

                ori_selecionada = orientacoes_cat[int(escolha_ori) - 1]
                ori_selecionada.exibir()

                ajudou = self._perguntar_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
                tempo_total = round(time.time() - inicio, 1)
                self.registrar(
                    origem="categoria",
                    pergunta=f"Navegação: {cat_escolhida} > {ori_selecionada.titulo}",
                    id_orientacao=ori_selecionada.id,
                    encontrou=True,
                    ajudou=ajudou,
                    tentativas=1,
                    tempo_segundos=tempo_total
                )
                return

    def indicadores(self):
        """Calcula e exibe os indicadores de desempenho do assistente."""
        print("\n=== INDICADORES DE ATENDIMENTO ===")
        total = len(self.historico)

        if total == 0:
            print("Nenhum atendimento registrado até o momento.")
            return

        encontrados = sum(1 for item in self.historico if item.get("encontrou"))
        ajudaram = sum(1 for item in self.historico if item.get("ajudou"))
        soma_tempo = sum(item.get("tempo_segundos", 0) for item in self.historico)
        soma_tentativas = sum(item.get("tentativas", 1) for item in self.historico)
        sem_solucao = [item.get("pergunta") for item in self.historico if not item.get("encontrou")]

        taxa_encontrada = (encontrados / total) * 100
        taxa_acerto = (ajudaram / total) * 100
        tempo_medio = soma_tempo / total
        media_tentativas = soma_tentativas / total

        if self.notas_facilidade:
            media_facilidade = f"{sum(self.notas_facilidade) / len(self.notas_facilidade):.1f} / 5.0"
        else:
            media_facilidade = "Ainda não avaliada nesta sessão"

        print(f"Total de atendimentos: {total}")
        print(f"Resposta encontrada (%): {taxa_encontrada:.1f}%")
        print(f"Taxa de acerto - ajudou (%): {taxa_acerto:.1f}%")
        print(f"Tempo médio para encontrar: {tempo_medio:.1f}s")
        print(f"Tentativas por atendimento: {media_tentativas:.1f}")
        print(f"Facilidade de uso (1 a 5): {media_facilidade}")

        print("\nLista de dúvidas sem solução:")
        if sem_solucao:
            for duvida in sem_solucao:
                print(f" - {duvida}")
        else:
            print(" - Nenhuma dúvida sem solução registrada.")

    def exportar_csv(self):
        """Exporta o histórico de atendimentos para CSV usando csv.DictWriter."""
        if not self.historico:
            return

        os.makedirs("data", exist_ok=True)
        colunas = [
            "data", "origem", "pergunta", "id_orientacao",
            "encontrou", "ajudou", "tentativas", "tempo_segundos"
        ]

        with open(self.caminho_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=colunas)
            writer.writeheader()
            writer.writerows(self.historico)

    def iniciar(self):
        """Loop principal de interação do assistente no terminal."""
        print(f"\n==========================================")
        print(f" Bem-vindo ao {self.nome}")
        print(f" Orientação Cidadã para Pessoas com Deficiência")
        print(f"==========================================")

        while True:
            print("\nMenu Principal:")
            print("1. Fazer uma pergunta")
            print("2. Navegar por categorias")
            print("3. Ver indicadores de atendimento")
            print("0. Sair")

            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                self.perguntar()
            elif opcao == "2":
                self.navegar()
            elif opcao == "3":
                self.indicadores()
            elif opcao == "0":
                while True:
                    nota = input("\nAntes de sair, dê uma nota de facilidade de uso (1 a 5): ").strip()
                    if nota.isdigit() and 1 <= int(nota) <= 5:
                        self.notas_facilidade.append(int(nota))
                        break
                    print("Entrada inválida. Digite um número inteiro entre 1 e 5.")

                self.indicadores()
                self.exportar_csv()
                print(f"\nDados exportados com sucesso para '{self.caminho_csv}'. Até logo!")
                break
            else:
                print("Opção inválida. Escolha 1, 2, 3 ou 0.")