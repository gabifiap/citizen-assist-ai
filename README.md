# Citizen Assist AI - Guia de Orientação Cidadã para PcD (InclusivAI)

Projeto Integrador (Global Solution) desenvolvido para a disciplina de Pensamento Computacional e Automação com Python (PCP).

---

## Integrantes
* Gabriela Batista - RM: 573583
* Samara Carvalho - RM: 573666

---

## 1. Público-Alvo e Problema
* Público-Alvo: Pessoas com Deficiência (PcD), seus familiares e responsáveis legais.
* Problema Resolvido: A grande descentralização e complexidade burocrática para encontrar informações confiáveis sobre direitos, isenções fiscais, benefícios assistenciais (como o BPC/LOAS) e serviços de saúde e transporte gratuitos garantidos por lei. O assistente centraliza essas orientações de forma ágil, humanizada e baseada estritamente em fontes oficiais governamentais (.gov.br).

---

## 2. Alinhamento com os ODS (Objetivos de Desenvolvimento Sustentável)
O projeto está alinhado diretamente com os seguintes ODS da ONU:
* ODS 10 - Redução das Desigualdades: Promove a inclusão social e o acesso igualitário a direitos fundamentais para cidadãos com deficiência.
* ODS 16 - Paz, Justiça e Instituições Eficazes: Facilita a transparência pública e o acesso à informação governamental de forma acessível e desburocratizada.

---

## 3. Estrutura do Projeto
O repositório está organizado seguindo rigorosamente os padrões de Programação Orientada a Objetos (POO) e composição:

```text
citizen-assist-ai/
│
├── data/
│   ├── base_conhecimento.json   # Base com 10 orientações detalhadas
│   ├── historico.json           # Histórico de atendimentos gerado automaticamente
│   └── atendimentos.csv         # Exportação final em formato CSV
│
├── orientacao.py                # Classe Orientacao (atributos e exibição)
├── base_conhecimento.py         # Classe BaseConhecimento (leitura JSON, normalização e busca)
├── assistente.py                # Classe Assistente (interação, validações, histórico e indicadores)
├── main.py                      # Arquivo principal de execução
└── README.md                    # Documentação do projeto
```

---

## 4. Como Executar o Projeto

### Pré-requisitos
Certifique-se de ter o Python 3.x instalado no seu computador.

### Passo a Passo
1. Clone ou baixe este repositório para o seu computador:
   ```bash
   git clone [https://github.com/seu-usuario/citizen-assist-ai.git](https://github.com/seu-usuario/citizen-assist-ai.git)
   ```
2. Abra a pasta do projeto no VS Code.
3. No terminal integrado, execute o arquivo principal:
   ```bash
   python main.py
   ```
4. Navegue pelo menu interativo escolhendo as opções para fazer perguntas em texto livre, navegar por categorias ou visualizar os indicadores de desempenho.

---

## 5. Regra de Pontuação e Busca
O mecanismo de busca inteligente (`base_conhecimento.py`) aplica as seguintes regras matemáticas de pontuação:
1. Palavras-chave: Cada palavra-chave da orientação que aparece na pergunta do usuário soma 3 pontos.
2. Título: Cada palavra da pergunta (com 4 ou mais letras) que aparece no título da orientação soma 1 ponto.
3. Classificação de Confiança:
   * ALTA: Pontuação >= 6 pontos.
   * MÉDIA: Pontuação entre 3 e 5 pontos (exibe até duas alternativas relacionadas).
   * BAIXA: Menor que 3 pontos (sugere reformulação ou consulta às categorias).

---

## 6. Fontes de Dados Utilizadas
Todas as orientações cadastradas na base de conhecimento (`data/base_conhecimento.json`) foram extraídas de canais oficiais do Governo Federal, tais como:
* Ministério da Saúde e SUS (`https://www.gov.br/saude`)
* Instituto Nacional do Seguro Social - INSS (`https://www.gov.br/inss`)
* Ministério dos Direitos Humanos e da Cidadania (`https://www.gov.br/direitos-humanos`)
* Secretaria da Receita Federal e portais de trânsito estaduais/federais.

---

## 7. Resultados dos Testes com Usuários (Validação)

* Total de atendimentos realizados nos testes: **12**
* Taxa de respostas encontradas (%): **83.3%**
* Taxa de acerto / utilidade (%): **75.0%**
* Tempo médio por busca: **21.4s**
* Média de facilidade de uso (Nota de 1 a 5): **4.7 / 5.0**
---

## 8. Limitações Conhecidas
* O assistente depende estritamente das palavras-chave e registros cadastrados no arquivo JSON, não utilizando modelos de IA generativa complexos (LLMs) remotos.
* Consultas com termos muito genéricos podem exigir refinamento pelo usuário através do menu de categorias.

---

## 9. Link do Vídeo Técnico
Assista à demonstração técnica completa do código e do projeto no YouTube:
https://youtu.be/OaAYKluk5Jk
