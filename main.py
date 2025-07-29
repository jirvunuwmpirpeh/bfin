from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/info_azione/{ticker}")
def info_azione(ticker: str):
    try:
        t = yf.Ticker(ticker)
        info = t.info
    except Exception:
        raise HTTPException(status_code=404, detail="Ticker non valido")

    # Proviamo prima con currentPrice da .info
    price = info.get("currentPrice")

    # Se non c'è, usiamo il prezzo di chiusura più recente
    if price is None:
        hist = t.history(period="1d")
        if not hist.empty:
            price = hist["Close"].iloc[-1]
        else:
            price = "N/A"

    return {
        "longName": info.get("longName", info.get("shortName", "N/A")),
        "ticker": info.get("symbol", ticker),
        "currency": info.get("currency", "N/A"),
        "currentPrice": price,
        "exchange": info.get("exchange", "N/A"),
        "market": info.get("country", "N/A"),
    }
