Casa Inteligente — ExpoTech 2026

Autores:

|Jean Messias - RA: 276788
|Nicolas Matos - RA: 296473
|José Matheus - RA: 297997
|Gustavo Henrique de Jesus Silva - 281939
|Juan Silva Rodrigues Carlos - RA: 299358
Sobre o Projeto

Projeto acadêmico desenvolvido para a **ExpoTech 2026**, com o objetivo de aplicar conhecimentos de tecnologia, programação e automação no desenvolvimento de soluções digitais.

O repositório contém uma implementação de gerenciamento e análise de tarefas, utilizando Python para processar informações exportadas do Bubble e gerar relatórios sobre atividades pendentes, prazos e níveis de urgência.

Objetivo

Facilitar o acompanhamento e a organização de tarefas por meio da análise automatizada de dados, permitindo identificar atividades atrasadas, próximas do vencimento e suas respectivas prioridades.

Funcionalidades

- Leitura de arquivos CSV exportados do Bubble.
- Identificação de tarefas pendentes.
- Identificação de tarefas atrasadas.
- Contagem de tarefas previstas para a semana.
- Classificação automática de urgência com base nos prazos.
- Organização das tarefas por data de vencimento.
- Geração de relatórios diretamente no terminal.
- Possibilidade de definir uma data personalizada para testes.

Tecnologias Utilizadas

- Python: processamento e análise dos dados.
- Pandas: leitura, organização e manipulação de dados.
- Bubble: plataforma utilizada no desenvolvimento da interface e gerenciamento das informações.
- CSV: formato utilizado para exportação e leitura dos dados.
- Git e GitHub: versionamento e compartilhamento do projeto.

Estrutura do Repositório:

Casa-inteligente-Expotech-2026/
│
├── Lembrete de tarefas.json
├── README.md
├── analise_tarefas.py
├── exemplo_saida.txt
└── tarefas_bubble_export.csv

Como Executar

1. Pré-requisitos

É necessário ter o Python instalado e a biblioteca Pandas.

Instale a dependência com:

pip install pandas

2. Clonar o repositório

git clone https://github.com/gustavosilva06784-sketch/Casa-inteligente-Expotech-2026-.git


3. Acessar a pasta

cd Casa-inteligente-Expotech-2026-

4. Executar o programa


python analise_tarefas.py

O programa utilizará automaticamente o arquivo "tarefas_bubble_export.csv".

Também é possível informar outro arquivo:

python analise_tarefas.py outro_arquivo.csv

Para realizar testes utilizando uma data específica:

python analise_tarefas.py tarefas_bubble_export.csv --hoje 2026-11-09

Classificação de Urgência

O sistema calcula automaticamente a urgência das tarefas considerando a data de vencimento:

| Condição | Classificação |
| Prazo vencido | Crítica (Atrasada) |
| Até 2 dias | Alta |
| Até 7 dias | Média |
| Mais de 7 dias | Baixa |

Tarefas concluídas não entram no relatório de pendências.

Aprendizados e Desenvolvimento

O desenvolvimento deste projeto proporciona a aplicação prática de conceitos importantes da programação, como:

- Manipulação e tratamento de dados.
- Leitura e processamento de arquivos CSV.
- Utilização de bibliotecas Python.
- Organização e estruturação de código.
- Automação de processos.
- Integração entre ferramentas de desenvolvimento.

Projeto Acadêmico

ExpoTech 2026 — Ciência da Computação

Projeto desenvolvido em equipe como parte das atividades acadêmicas, com foco na aplicação prática da tecnologia para solucionar problemas do cotidiano.

---

Desenvolvido como parte da jornada de aprendizado em tecnologia e desenvolvimento de software.
