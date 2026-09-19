# Aquisição de Dados sobre Cinema: orçamento, bilheteria e recepção

Trabalho 1 da disciplina de **Ciência de Dados**, que consiste na construção de uma base com **1.000 filmes**, integrando informações de orçamento, bilheteria e recepção do público e da crítica a partir do **TMDB**, **OMDb** e **Letterboxd**.

**Slides da apresentação:** [link do Canva](https://www.canva.com/design/DAHVGqCfhI0/FZPV4twqX9o79GRrggAOWg/edit?utm_content=DAHVGqCfhI0&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

**Pergunta motivadora:** Existe correlação positiva entre orçamento alto e aclamação (público/crítica), ou o investimento impacta sobretudo a bilheteria?

**Grupo:**
- Karen Juliana Báez González (22551695)
- Lucas Eduardo Siqueira dos Santos (22251137)
- Luna Veiga Horta Braga (22551154)
- Samuel Davi Silva de Lima Chagas (22352935)
  
## Fontes

| Fonte | Método | Papel | Chave |
|-------|--------|-------|-------|
| [TMDB](https://www.themoviedb.org) | API | Orçamento, faturamento, metadados; gera IDs | gera `tmdb_id`, `imdb_id` |
| [OMDb](https://www.omdbapi.com) | API | Nota IMDb + Metascore | consome `imdb_id` |
| [Letterboxd](https://letterboxd.com) | Scraping HTML | Rating e contagem de votos | consome `tmdb_id` |

Scraping HTML do **IMDb** não é usado: `robots.txt` com `User-agent: *` → `Disallow: /` e termos que proíbem coleta automatizada. Detalhes em [`docs/robots_verificacao.md`](docs/robots_verificacao.md).

```text
TMDB (API) ──► tmdb_raw.csv ──┐
                              ├── left join (imdb_id / tmdb_id) ──► base_tratada.parquet
OMDb (API) ──► omdb_raw.csv ──┤
Letterboxd ──► letterboxd_raw.csv ─┘
```

## Estrutura do Repositório

```text
trabalho01/
├── dados_brutos/                    # Dados coletados, sem alterações
├── dados_tratados/                  # Base integrada e tratada
├── docs/                            # Documentação complementar
│   ├── dataset_card.md              # Documentação da base de dados
│   ├── proveniencia.jsonl           # Registro de proveniência dos dados
│   └── robots_verificacao.md        # Verificação das políticas de acesso
├── .env.example                     # Modelo para as chaves de API
├── .gitignore                       # Arquivos ignorados pelo Git
├── Dataset_Card.pdf                 # Dataset Card em PDF
├── README.md                        # Documentação principal
├── coleta_cinema.ipynb              # Coleta, integração e tratamento dos dados
├── requirements.txt                 # Dependências do projeto
└── scripts_coleta_letterboxd.py     # Script auxiliar para coleta do Letterboxd
```

## Setup Rápido

```powershell
git clone https://github.com/Lucased22/trabalho01-aquisicao-cinema.git
cd trabalho01-aquisicao-cinema
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Preencha `TMDB_API_KEY` e `OMDB_API_KEY` no `.env`, depois:

```powershell
jupyter notebook coleta_cinema.ipynb
```

Os CSVs brutos e o Parquet já estão no repositório — as chaves só são necessárias para reexecutar a coleta (Letterboxd ~52 min com `sleep(2)`).

## Documentação

| Documento | Conteúdo |
|-----------|----------|
| [`docs/dataset_card.md`](docs/dataset_card.md) | Dataset Card (Apêndice A) |
| [`docs/proveniencia.jsonl`](docs/proveniencia.jsonl) | Proveniência da coleta |
| [`docs/robots_verificacao.md`](docs/robots_verificacao.md) | Decisão ética IMDb vs Letterboxd |

## Licença e Uso

Este repositório foi desenvolvido para **fins exclusivamente acadêmicos**, no contexto da disciplina de Ciência de Dados da **UFAM**.

Os dados utilizados são provenientes do **TMDB**, **OMDb** e **Letterboxd**, e seu uso deve respeitar os respectivos termos e condições de cada fonte. O repositório não tem como objetivo a redistribuição ou comercialização dos dados coletados.

As chaves de API utilizadas no projeto são armazenadas no arquivo `.env`, que **não deve ser versionado ou disponibilizado publicamente**.

*This product uses the TMDB API but is not endorsed or certified by TMDB.*
