# Dataset Card — Cinema: orçamento, bilheteria e recepção

Modelo conforme **Apêndice A** do enunciado (Trabalho 1 — Aquisição de Dados).  
Checklist dos entregáveis: [`ENTREGAVEIS.md`](ENTREGAVEIS.md) · Setup do repo: [`../README.md`](../README.md).

## A.1 Identificação

| Campo | Conteúdo |
|-------|----------|
| **Nome da base** | `cinema_orcamento_recepcao` |
| **Grupo / integrantes** | Lucas Eduardo Siqueira dos Santos (22251137); Luna Veiga Horta Braga (22551154); Samuel Davi Silva de Lima Chagas (22352935); Karen Juliana Báez González (22551695) |
| **Tema e pergunta motivadora** | Impacto do orçamento e do faturamento de filmes na recepção de crítica e público. **Pergunta:** existe correlação positiva entre alto orçamento e aclamação (público/crítica), ou grandes investimentos impactam sobretudo a bilheteria? |
| **Data da coleta** | 12/09/2026 a 13/09/2026 (UTC); integração em 13/09/2026 |

## A.2 Fontes e proveniência

### Fonte 1 — TMDB (The Movie Database)

| Campo | Conteúdo |
|-------|----------|
| **Nome e URL** | TMDB — https://www.themoviedb.org / API https://api.themoviedb.org/3 |
| **Método** | **API REST.** (1) `GET /discover/movie` com `sort_by=revenue.desc`, `include_adult=false`, páginas **1–50** (~1000 IDs). (2) `GET /movie/{id}` por filme para detalhes financeiros e `imdb_id`. `sleep` ~0.25 s; API key via `.env` (`TMDB_API_KEY`). Bruto: `dados_brutos/tmdb_raw.csv`. |
| **Licença / termos** | Uso sob [TMDB API Terms of Use](https://www.themoviedb.org/documentation/api/terms-of-use); atribuição à TMDB; chave pessoal; uso acadêmico/não comercial deste trabalho. |

### Fonte 2 — OMDb (Open Movie Database)

| Campo | Conteúdo |
|-------|----------|
| **Nome e URL** | OMDb — https://www.omdbapi.com |
| **Método** | **API REST.** `GET /?i={imdb_id}&apikey=…` para cada `imdb_id` presente no TMDB. Extrai `imdbRating`, `imdbVotes`, `Metascore`. Plano free (~1000 req/dia). Bruto: `dados_brutos/omdb_raw.csv`. **Substitui** o scraping HTML do IMDb (bloqueado — ver A.6 e `robots_verificacao.md`). |
| **Licença / termos** | [OMDb API](https://www.omdbapi.com/) — plano free para uso pessoal/educacional com chave; redistribuição comercial sujeita aos termos do provedor. |

### Fonte 3 — Letterboxd

| Campo | Conteúdo |
|-------|----------|
| **Nome e URL** | Letterboxd — https://letterboxd.com |
| **Método** | **Web scraping HTML.** URL `https://letterboxd.com/tmdb/{tmdb_id}/`; parse de JSON-LD (`aggregateRating`) e fallback `twitter:data2`; User-Agent acadêmico identificável; `time.sleep(2)` entre requisições; checkpoint a cada 50. Bruto: `dados_brutos/letterboxd_raw.csv`. |
| **Licença / termos** | Dados públicos de páginas de filme; coleta pontual para fins acadêmicos, com rate limit e respeito a `robots.txt` (ver A.6). Redistribuição massiva dos dados Letterboxd pode conflitar com os termos do site — uso restrito ao contexto da disciplina. |

### Chave de integração

1. Base âncora: **TMDB** (`tmdb_id`).
2. **Left join** TMDB ⟕ OMDb em **`imdb_id`**.
3. **Left join** resultado ⟕ Letterboxd em **`tmdb_id`**.
4. Sem casamento por título (evita ambiguidade de strings).

Log completo: `docs/proveniencia.jsonl` (timestamp, fonte, URL mascarando API keys, método, status HTTP, observação).

## A.3 Dicionário de variáveis

Base tratada: `dados_tratados/base_tratada.parquet` (e espelho CSV).

| Variável | Tipo | Descrição | Unidade |
|----------|------|-----------|---------|
| `tmdb_id` | numérica discreta | Identificador do filme no TMDB | id |
| `imdb_id` | texto | Identificador IMDb (`tt…`); pode estar ausente | id |
| `title` | texto | Título (TMDB) | — |
| `release_date` | data/hora | Data de lançamento | data |
| `budget` | numérica contínua | Orçamento de produção (0 na TMDB tratado como ausente) | USD |
| `revenue` | numérica contínua | Faturamento reportado na TMDB | USD |
| `genres` | categórica (texto) | Gêneros concatenados com `\|` | — |
| `runtime` | numérica discreta | Duração | minutos |
| `original_language` | categórica | Código de idioma original (ISO 639-1) | — |
| `tmdb_vote_average` | numérica contínua | Nota média TMDB | escala ~0–10 |
| `tmdb_vote_count` | numérica discreta | Número de votos TMDB | votos |
| `imdb_rating` | numérica contínua | Nota IMDb via OMDb | escala 0–10 |
| `imdb_votes` | numérica discreta | Contagem de votos IMDb via OMDb | votos |
| `metascore` | numérica contínua | Metascore (crítica agregada) via OMDb | escala 0–100 |
| `letterboxd_rating` | numérica contínua | Nota média Letterboxd | escala ~0–5 |
| `letterboxd_rating_count` | numérica discreta | Contagem de ratings Letterboxd | votos |
| `letterboxd_title` | texto | Título na página Letterboxd | — |
| `matched_omdb` | booleana | `True` se houve match no join OMDb | — |
| `matched_letterboxd` | booleana | `True` se houve match no join Letterboxd | — |
| `omdb_response` | categórica / booleana | Flag de sucesso da resposta OMDb | — |
| `omdb_error` | texto | Mensagem de erro OMDb, se houver | — |
| `url_final` | texto | URL final após redirect no Letterboxd | URL |
| `http_status` | numérica discreta | Status HTTP da página Letterboxd | código HTTP |

## A.4 Volume e granularidade

| Campo | Conteúdo |
|-------|----------|
| **Linhas / colunas** | **1000** linhas × **23** colunas |
| **O que representa uma linha** | Um filme (identificado por `tmdb_id`) |
| **Cobertura** | Amostra dos ~1000 filmes com maior `revenue` na TMDB (`revenue.desc`, páginas 1–50), sem filtro geográfico. Datas de lançamento na base: de **1939** a **2026**. Não é uma amostra aleatória do catálogo mundial. |

### Cobertura dos joins (após limpeza)

| Métrica | Valor |
|---------|-------|
| Match OMDb (`matched_omdb`) | 991 / 1000 |
| Match Letterboxd | 1000 / 1000 |
| Com `imdb_rating` | 987 |
| Com `metascore` | 945 |
| Com `letterboxd_rating` | 989 |
| `budget` ausente (incl. zeros convertidos) | 34 |
| `revenue` ausente | 0 |

## A.5 Limitações e decisões

**Dados descartados**

- Nenhum filme da lista TMDB foi removido na integração (left joins).
- Scraping HTML do IMDb **não** foi realizado (proibido por `robots.txt`/termos); notas IMDb/Metascore vêm da OMDb.
- Duplicatas por `tmdb_id`: 0 removidas (não havia).

**Lacunas conhecidas**

- 9 filmes TMDB **sem** `imdb_id` → sem OMDb.
- Alguns `imdb_id` com resposta OMDb sem rating/Metascore.
- 11 filmes Letterboxd sem `letterboxd_rating` (página OK, mas sem aggregate no HTML).
- **Viés de seleção:** só blockbusters por bilheteria (`revenue.desc`) — pouca contraste com filmes de baixo orçamento; limita a pergunta motivadora.
- Orçamento/faturamento TMDB podem estar incompletos ou desatualizados; Letterboxd usa escala distinta (≈0–5) da IMDb/TMDB (≈0–10).

**Decisões de limpeza relevantes**

- Tipos: datas → datetime; ratings/orçamento → numérico; `imdb_votes` sem vírgulas milhar.
- `budget == 0` ou `revenue == 0` → ausente (`NA`), pois zero na TMDB costuma significar “não informado”.
- Deduplicação por `tmdb_id` (keep first).
- Brutos em `dados_brutos/` **inalterados**; limpeza só em `dados_tratados/`.

## A.6 Considerações éticas

| Campo | Conteúdo |
|-------|----------|
| **Contém dados pessoais?** | **Não.** Metadados e agregados públicos sobre filmes (notas médias, contagens). Não há CPF, e-mail, nomes de usuários individuais etc. LGPD: tratamento de dados pessoais **não se aplica** a esta base no sentido de titulares identificáveis. |
| **Restrições de uso / redistribuição** | Uso acadêmico na disciplina. Respeitar termos TMDB, OMDb e Letterboxd; não republicar como produto comercial nem sobrecarregar os serviços. API keys **não** entram no repositório (`.gitignore` + `.env.example`). |
| **robots.txt verificado?** | **Sim.** Detalhes em `docs/robots_verificacao.md`: IMDb (`User-agent: *` → `Disallow: /`) → sem scrape HTML; Letterboxd permite `/tmdb/{id}/` com rate limit. |

## Arquivos associados

| Artefato | Caminho |
|----------|---------|
| Notebook | `coleta_cinema.ipynb` |
| Brutos | `dados_brutos/tmdb_raw.csv`, `omdb_raw.csv`, `letterboxd_raw.csv` |
| Tratado | `dados_tratados/base_tratada.parquet` (+ `.csv`) |
| Proveniência | `docs/proveniencia.jsonl` |
| robots | `docs/robots_verificacao.md` |
| Repositório | https://github.com/Lucased22/trabalho01-aquisicao-cinema |
