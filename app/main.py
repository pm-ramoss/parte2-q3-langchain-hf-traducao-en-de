"""Parte 2 - Questão 3: tradução EN -> DE com Helsinki-NLP/opus-mt-en-de via LangChain + FastAPI."""
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.schemas import TranslateRequest, TranslateResponse
from app.translator import MODEL_NAME, build_chain

resources: dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    resources["chain"] = build_chain()
    yield
    resources.clear()


app = FastAPI(
    title="API de Tradução EN → DE (LangChain + HuggingFace)",
    description="Traduz inglês para alemão usando opus-mt-en-de gerenciado pelo LangChain.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/", tags=["health"])
def health():
    return {"status": "ok", "model": MODEL_NAME}


@app.post("/translate", response_model=TranslateResponse, tags=["translation"])
def translate(payload: TranslateRequest):
    chain = resources.get("chain")
    if chain is None:
        raise HTTPException(status_code=503, detail="Modelo ainda não carregado.")
    try:
        translated = chain.invoke({"text": payload.text})
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Erro na tradução: {exc}") from exc
    return TranslateResponse(
        original_text=payload.text, translated_text=translated.strip(), model=MODEL_NAME
    )
