"""Coleta Letterboxd — Passo A. Executar a partir de trabalho01/."""
from __future__ import annotations

import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from tqdm import tqdm

ROOT = Path(__file__).resolve().parent
DIR_BRUTOS = ROOT / "dados_brutos"
DIR_DOCS = ROOT / "docs"
LOG_PATH = DIR_DOCS / "proveniencia.jsonl"
LB_RAW_PATH = DIR_BRUTOS / "letterboxd_raw.csv"
LB_SLEEP = 2.0
CHECKPOINT_EVERY = 50

HEADERS = {
    "User-Agent": "UFAM-CD-Trabalho1-Cinema/1.0 (+academic; contato via repositorio do projeto)",
    "Accept-Language": "en-US,en;q=0.9",
}

load_dotenv(ROOT / ".env")


def log_proveniencia(fonte, url, metodo, status, params=None, observacao=""):
    registro = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "fonte": fonte,
        "url": url,
        "metodo": metodo,
        "params": params or {},
        "status": status,
        "observacao": observacao,
    }
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")


def get_com_retry(url, max_tentativas=3, sleep_base=1.0, timeout=40):
    ultimo = None
    for tentativa in range(1, max_tentativas + 1):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
            if resp.status_code in {429, 500, 502, 503, 504}:
                time.sleep(sleep_base * tentativa * 2)
                continue
            return resp
        except requests.RequestException as exc:
            ultimo = exc
            time.sleep(sleep_base * tentativa)
    if ultimo:
        raise ultimo
    raise RuntimeError(url)


def parse_letterboxd_html(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")
    out = {
        "letterboxd_rating": None,
        "letterboxd_rating_count": None,
        "letterboxd_title": None,
    }
    script = soup.select_one('script[type="application/ld+json"]')
    if script:
        raw = script.string or script.get_text() or ""
        m = re.search(r"\{.*\}", raw, re.S)
        if m:
            try:
                data = json.loads(m.group(0))
                out["letterboxd_title"] = data.get("name")
                agg = data.get("aggregateRating") or {}
                out["letterboxd_rating"] = agg.get("ratingValue")
                out["letterboxd_rating_count"] = agg.get("ratingCount")
            except json.JSONDecodeError:
                pass
    if out["letterboxd_rating"] is None:
        tw = soup.select_one('meta[name="twitter:data2"]')
        if tw and tw.get("content"):
            mm = re.search(r"([0-9]+(?:\.[0-9]+)?)", tw["content"])
            if mm:
                out["letterboxd_rating"] = float(mm.group(1))
    return out


def main():
    df_tmdb = pd.read_csv(DIR_BRUTOS / "tmdb_raw.csv")
    tmdb_ids = df_tmdb["tmdb_id"].dropna().astype(int).unique().tolist()
    print("tmdb_id:", len(tmdb_ids))

    done = set()
    rows = []
    if LB_RAW_PATH.exists():
        prev = pd.read_csv(LB_RAW_PATH)
        rows = prev.to_dict(orient="records")
        done = set(prev["tmdb_id"].dropna().astype(int).tolist())
        print("Retomando:", len(done))

    pendentes = [i for i in tmdb_ids if i not in done]
    print("Pendentes:", len(pendentes))
    log_proveniencia(
        "Letterboxd",
        "https://letterboxd.com/tmdb/",
        "COLETA_INICIO",
        None,
        {"pendentes": len(pendentes)},
        "inicio scrape Letterboxd",
    )

    for n, tid in enumerate(tqdm(pendentes, desc="Letterboxd"), start=1):
        url = f"https://letterboxd.com/tmdb/{tid}/"
        try:
            resp = get_com_retry(url)
            status = resp.status_code
            final_url = str(resp.url)
            parsed = parse_letterboxd_html(resp.text) if status == 200 else {}
            log_proveniencia(
                "Letterboxd",
                url,
                "SCRAPE GET",
                status,
                {"tmdb_id": tid, "final_url": final_url},
            )
        except Exception as exc:
            status = None
            final_url = url
            parsed = {}
            log_proveniencia("Letterboxd", url, "SCRAPE GET", None, {"tmdb_id": tid}, str(exc)[:200])

        rows.append(
            {
                "tmdb_id": tid,
                "letterboxd_rating": parsed.get("letterboxd_rating"),
                "letterboxd_rating_count": parsed.get("letterboxd_rating_count"),
                "letterboxd_title": parsed.get("letterboxd_title"),
                "url_final": final_url,
                "http_status": status,
            }
        )
        if n % CHECKPOINT_EVERY == 0:
            pd.DataFrame(rows).to_csv(LB_RAW_PATH, index=False, encoding="utf-8")
        time.sleep(LB_SLEEP)

    df = pd.DataFrame(rows)
    df.to_csv(LB_RAW_PATH, index=False, encoding="utf-8")
    print("Salvo:", LB_RAW_PATH)
    print("Linhas:", len(df))
    print("Com rating:", df["letterboxd_rating"].notna().sum())
    print("HTTP 200:", (df["http_status"] == 200).sum())
    print(df.head(3).to_string())
    log_proveniencia(
        "Letterboxd",
        str(LB_RAW_PATH),
        "COLETA_FIM",
        200,
        {"linhas": len(df), "com_rating": int(df["letterboxd_rating"].notna().sum())},
        "fim scrape Letterboxd",
    )


if __name__ == "__main__":
    main()
