# Verificação de `robots.txt`

**Data da verificação:** 2026-09-12  
**URLs consultadas:**

- https://www.imdb.com/robots.txt
- https://letterboxd.com/robots.txt

## IMDb — scraping HTML não permitido

Trechos relevantes do `robots.txt` (consulta ao vivo):

- Cabeçalho: uso de ferramentas de data mining / scrape automatizado é **proibido** sem permissão escrita; licensing em https://www.imdb.com/licensing/
- Regra para crawlers genéricos:

```
User-agent: *
Disallow: /
```

Isso bloqueia **todo** o site (incluindo `/title/{imdb_id}/`) para user-agents que não estejam na lista explícita de bots (Googlebot, bingbot, etc.).

As [Conditions of Use](https://www.imdb.com/conditions/) reforçam a proibição de robots/screen scraping sem consentimento escrito. Para uso não comercial, a IMDb indica os [datasets oficiais](https://developer.imdb.com/non-commercial-datasets/), não o HTML.

**Decisão:** não raspar o IMDb. Notas de público IMDb e Metascore serão obtidas via **OMDb API**.

## Letterboxd — scraping de página de filme permitido pelo robots

- Não há `Disallow: /` para `User-agent: *`.
- Bloqueios pontuais: listagens/filtros (`/*/genre/*`, `/*/country/*`, `/films/year/*`, `/*/by/*`, `/*/friends/*`, etc.) e bloqueio total para bots de IA nomeados (GPTBot, ClaudeBot, …).
- A URL `https://letterboxd.com/tmdb/{tmdb_id}/` **não** está nos `Disallow` listados.

**Decisão:** usar Letterboxd como fonte de **web scraping HTML**, com User-Agent identificável, `time.sleep(2)` entre requisições e volume limitado (~400 filmes), para uso acadêmico.

## Resumo

| Fonte | robots.txt | Método adotado |
|-------|------------|----------------|
| IMDb | Bloqueia `*` em `/` | OMDb API (sem scrape HTML) |
| Letterboxd | Permite `/tmdb/{id}/` | BeautifulSoup + requests |
