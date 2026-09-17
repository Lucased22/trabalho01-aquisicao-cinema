# Aquisição de Dados — Cinema (orçamento, bilheteria e recepção)

Trabalho 1 da disciplina de **Ciência de Dados (UFAM)**: construção de uma base própria a partir de **API** e **web scraping**, com integração por chaves estáveis, preservação do bruto e documentação completa.

**Pergunta motivadora:** orçamento alto correlaciona com aclamação (público/crítica), ou o investimento impacta sobretudo a bilheteria?

**Grupo:** Lucas Eduardo Siqueira dos Santos (22251137) · Luna Veiga Horta Braga (22551154) · Samuel Davi Silva de Lima Chagas (22352935) · Karen Juliana Báez González (22551695)

> Pacote acadêmico para o ColabWeb: veja a [documentação dos entregáveis](docs/ENTREGAVEIS.md).

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

## Estrutura do repositório

```text
trabalho01/
├── coleta_cinema.ipynb          # coleta + join + limpeza
├── scripts_coleta_letterboxd.py # helper opcional do scrape
├── requirements.txt
├── .env.example                 # chaves (nunca commitar .env)
├── dados_brutos/                # CSVs crus, inalterados
├── dados_tratados/              # base integrada (Parquet + CSV)
└── docs/
    ├── ENTREGAVEIS.md           # documentação dos entregáveis
    ├── dataset_card.md          # Apêndice A
    ├── proveniencia.jsonl       # log URL / timestamp / status
    └── robots_verificacao.md
```

## Setup rápido

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
| [`docs/ENTREGAVEIS.md`](docs/ENTREGAVEIS.md) | Checklist do enunciado, o que cada arquivo entrega, como empacotar no ColabWeb |
| [`docs/dataset_card.md`](docs/dataset_card.md) | Dataset Card (Apêndice A) |
| [`docs/proveniencia.jsonl`](docs/proveniencia.jsonl) | Proveniência da coleta |
| [`docs/robots_verificacao.md`](docs/robots_verificacao.md) | Decisão ética IMDb vs Letterboxd |

## Licença e uso

Uso acadêmico. Respeitar termos da TMDB, OMDb e Letterboxd. Não commitar `.env`. Redistribuição comercial dos dados rasgados/agregados não é o objetivo deste repositório.
