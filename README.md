# Trabalho 1 — Aquisição de Dados (Cinema)

Repositório: https://github.com/Lucased22/trabalho01-aquisicao-cinema

Projeto da disciplina de Ciência de Dados (UFAM): coleta, integração e documentação de uma base sobre orçamento/faturamento de filmes e recepção de crítica/público.

## Fontes

| Fonte | Método | Chave de integração |
|-------|--------|---------------------|
| TMDB | API | gera `tmdb_id`, `imdb_id` |
| OMDb | API | consome `imdb_id` (notas IMDb / Metascore) |
| Letterboxd | Web scraping | consome `tmdb_id` |

O scraping HTML do IMDb **não** é usado: o `robots.txt` do IMDb (`User-agent: *` → `Disallow: /`) e os termos de uso proíbem coleta automatizada. Detalhes em `docs/robots_verificacao.md`.

## Setup

```powershell
cd trabalho01
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Preencha `TMDB_API_KEY` e `OMDB_API_KEY` em `.env` (veja abaixo).

```powershell
jupyter notebook coleta_cinema.ipynb
```

## Como obter as API keys

### TMDB

1. Conta em https://www.themoviedb.org/signup (confirmar e-mail).
2. Conta → **Settings** → **API** → Request an API Key → **Developer**.
3. Aceitar termos e enviar o formulário (uso educacional).
4. Copiar a **API Key (v3)** para `.env` como `TMDB_API_KEY`.

Teste:

```powershell
python -c "import os,requests; from dotenv import load_dotenv; load_dotenv(); r=requests.get('https://api.themoviedb.org/3/movie/550', params={'api_key': os.getenv('TMDB_API_KEY')}); print(r.status_code, r.json().get('title'))"
```

### OMDb

1. https://www.omdbapi.com/apikey.aspx → plano **FREE**.
2. Confirmar e-mail e copiar a chave para `.env` como `OMDB_API_KEY`.

## Estrutura

- `dados_brutos/` — CSVs crus (inalterados após a coleta)
- `dados_tratados/` — base integrada limpa (Parquet + CSV)
- `docs/` — `dataset_card.md`, `proveniencia.jsonl`, `robots_verificacao.md`
- `coleta_cinema.ipynb` — notebook reprodutível (API + scraping + join)

## Entrega (ColabWeb)

Prazo do enunciado: **10/09/2026**.

Checklist:

| Artefato | Caminho |
|----------|---------|
| Notebook | `coleta_cinema.ipynb` |
| Brutos | `dados_brutos/tmdb_raw.csv`, `omdb_raw.csv`, `letterboxd_raw.csv` |
| Base tratada | `dados_tratados/base_tratada.parquet` |
| Proveniência | `docs/proveniencia.jsonl` |
| Dataset Card | `docs/dataset_card.md` |
| robots | `docs/robots_verificacao.md` |

Compactar `trabalho01/` **sem** `.venv` e **sem** `.env` (usar `.env.example`).
