# Documentação dos entregáveis — Trabalho 1 (Aquisição de Dados)

Este documento descreve **o que o enunciado pede**, **onde está cada artefato** neste pacote e **como entregar no ColabWeb**.  
Para visão geral do projeto e setup técnico, use o [README do repositório](../README.md).  
A ficha formal da base (Apêndice A) está em [`dataset_card.md`](dataset_card.md).

**Disciplina:** Ciência de Dados — UFAM  
**Forma de entrega:** ColabWeb (pacote único: repositório ou zip)  
**Repo:** https://github.com/Lucased22/trabalho01-aquisicao-cinema  

**Grupo:**

| Nome | Matrícula |
|------|-----------|
| Lucas Eduardo Siqueira dos Santos | 22251137 |
| Luna Veiga Horta Braga | 22551154 |
| Samuel Davi Silva de Lima Chagas | 22352935 |
| Karen Juliana Báez González | 22551695 |

---

## 1. Requisitos do enunciado × artefatos

| Exigência | Como foi atendida | Artefato |
|-----------|-------------------|----------|
| Tema próprio + pergunta | Orçamento/faturamento × recepção crítica/público | [`dataset_card.md`](dataset_card.md) § A.1 |
| Pelo menos 1 API | TMDB + OMDb | `coleta_cinema.ipynb` §§ 2–3; brutos TMDB/OMDb |
| Pelo menos 1 scraping HTML | Letterboxd (`/tmdb/{id}/`) | `coleta_cinema.ipynb` § 4; `letterboxd_raw.csv` |
| Integração real (não tabelas soltas) | Left join `imdb_id` + `tmdb_id` | `coleta_cinema.ipynb` § 5; `base_tratada.parquet` |
| Guardar bruto antes da limpeza | CSVs crus intactos | `dados_brutos/` |
| Base tratada | Parquet (+ CSV de apoio) | `dados_tratados/` |
| Proveniência | Log JSONL por requisição | [`proveniencia.jsonl`](proveniencia.jsonl) |
| Dataset Card | Apêndice A preenchido | [`dataset_card.md`](dataset_card.md) |
| Ética / robots.txt | IMDb bloqueado → OMDb; Letterboxd com sleep | [`robots_verificacao.md`](robots_verificacao.md) |

---

## 2. Checklist de entrega (ColabWeb)

Marque antes de enviar:

- [x] Notebook reprodutível com coleta, integração e limpeza — `coleta_cinema.ipynb`
- [x] Dados brutos de cada fonte — `dados_brutos/tmdb_raw.csv`, `omdb_raw.csv`, `letterboxd_raw.csv`
- [x] Base tratada — `dados_tratados/base_tratada.parquet` (e `base_tratada.csv`)
- [x] Registro de proveniência — `docs/proveniencia.jsonl`
- [x] Dataset Card — `docs/dataset_card.md`
- [x] Verificação robots / ética — `docs/robots_verificacao.md`
- [x] Dependências e exemplo de env — `requirements.txt`, `.env.example`
- [x] Nomes e matrículas do grupo em `docs/dataset_card.md` § A.1
- [ ] Zip **sem** `.venv` e **sem** `.env` (regenerar se a documentação mudar)

Zip de referência gerado localmente: `../trabalho01_colabweb.zip` (pasta pai `CD/`).

---

## 3. Descrição de cada entregável

### 3.1 Notebook — `coleta_cinema.ipynb`

Código comentado, seções:

| Seção | Conteúdo |
|-------|----------|
| 0 | Setup, pastas, `.env`, `log_proveniencia`, `get_com_retry` |
| 1 | Teste das API keys |
| 2 | Coleta TMDB (`discover` + details) → `tmdb_raw.csv` |
| 3 | Coleta OMDb por `imdb_id` → `omdb_raw.csv` |
| 4 | Scraping Letterboxd → `letterboxd_raw.csv` |
| 5 | Joins, tipagem, `budget`/`revenue` 0→NA, dedupe → Parquet |
| 6 | Ponteiros para esta documentação |

Helper opcional (mesmo parse do scrape): `scripts_coleta_letterboxd.py`.

### 3.2 Dados brutos — `dados_brutos/`

Arquivos **exatamente como coletados** (não editar):

| Arquivo | Linhas (aprox.) | Conteúdo principal |
|---------|-----------------|--------------------|
| `tmdb_raw.csv` | 1000 | `tmdb_id`, `imdb_id`, título, data, budget, revenue, gêneros, votos TMDB |
| `omdb_raw.csv` | 991 | `imdb_id`, `imdb_rating`, `imdb_votes`, `metascore`, status OMDb |
| `letterboxd_raw.csv` | 1000 | `tmdb_id`, rating, count, título LB, URL final, HTTP status |

### 3.3 Base tratada — `dados_tratados/`

| Arquivo | Descrição |
|---------|-----------|
| `base_tratada.parquet` | Base final preferencial (enunciado) |
| `base_tratada.csv` | Espelho legível / backup |

- **1000** linhas × **23** colunas  
- Unidade de observação: **um filme** (`tmdb_id`)  
- Dicionário completo: [`dataset_card.md`](dataset_card.md) § A.3  

Resumo da integração:

| Join | Resultado |
|------|-----------|
| TMDB ⟕ OMDb (`imdb_id`) | 991 both · 9 left_only (sem `imdb_id`) |
| ⟕ Letterboxd (`tmdb_id`) | 1000 both |
| Limpeza | `budget==0` → NA (34); sem duplicatas `tmdb_id` |

### 3.4 Proveniência — `docs/proveniencia.jsonl`

Uma linha JSON por evento de coleta/integração, com:

- `timestamp` (UTC)
- `fonte` (`TMDB`, `OMDb`, `Letterboxd`, `integracao`)
- `url` (API keys mascaradas como `***`)
- `metodo`, `status`, `params`, `observacao`

Serve para auditar **onde / quando / como** cada dado foi obtido.

### 3.5 Dataset Card — `docs/dataset_card.md`

Ficha do Apêndice A: identificação, fontes, dicionário, volume, limitações (incl. viés `revenue.desc`), ética/LGPD/robots.

### 3.6 robots.txt — `docs/robots_verificacao.md`

Registro da verificação e da decisão de arquitetura (IMDb → OMDb API; Letterboxd → scrape com rate limit).

---

## 4. Como empacotar para o ColabWeb

1. Confirme o checklist da seção 2.
2. Compacte a pasta do projeto **excluindo**:
   - `.venv/`
   - `.env` (envie só `.env.example`)
   - opcional: `.git/` (se o professor pedir só o zip de arquivos)
3. Envie o zip (ou o link do repositório, se aceito) no **ColabWeb**.

Exemplo (PowerShell, a partir da pasta pai):

```powershell
# Preferir o zip já gerado: trabalho01_colabweb.zip
# Ou regenerar sem .venv / .env / .git
```

---

## 5. Limitações relevantes para a correção

- Amostra = top bilheteria TMDB (`sort_by=revenue.desc`) — viés para blockbusters; pouco contraste de baixo orçamento.
- Escalas de nota diferentes (IMDb/TMDB ≈ 0–10; Letterboxd ≈ 0–5; Metascore 0–100).
- Brutos preservados; qualquer reexecução da coleta pode alterar valores se as fontes mudarem online.

---

## 6. Mapa rápido de pastas no pacote

```text
coleta_cinema.ipynb
requirements.txt
.env.example
dados_brutos/          ← brutos
dados_tratados/        ← base final
docs/
  ENTREGAVEIS.md       ← este arquivo
  dataset_card.md
  proveniencia.jsonl
  robots_verificacao.md
README.md              ← visão GitHub / setup
```
