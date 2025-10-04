from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import io
import csv

app = FastAPI(title="Exoplanet_CSV")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_CONTENT_TYPES = {"text/csv", "application/vnd.ms-excel", "text/plain"}

def detect_separator(sample: str) -> str:
    """Tenta detectar o delimitador do CSV; fallback para vírgula."""
    try:
        dialect = csv.Sniffer().sniff(sample)
        return dialect.delimiter
    except Exception:
        return ","

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Recebe um CSV via upload (campo "file").
    Retorna basic info: filename, rows, columns e uma amostra (primeiras linhas).
    """
    # validação básica
    if not file.filename.lower().endswith(".csv") and file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Arquivo inválido. Envie um CSV (.csv).")

    try:
        content_bytes = await file.read()
        # tenta decodificar com utf-8; se falhar, tenta iso-8859-1
        try:
            text = content_bytes.decode("utf-8")
        except UnicodeDecodeError:
            text = content_bytes.decode("iso-8859-1")

        # detecta separador a partir de uma amostra
        sample = text[:8192]
        sep = detect_separator(sample)

        # carrega em DataFrame
        df = pd.read_csv(io.StringIO(text), sep=sep)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao processar CSV: {e}")
    finally:
        await file.close()

    if df is None or df.shape[0] == 0:
        raise HTTPException(status_code=400, detail="CSV vazio ou sem linhas válidas.")

    # preparar resposta resumida (não enviar todo o arquivo)
    sample_rows = df.head(5).to_dict(orient="records")
    response = {
        "status": "ok",
        "filename": file.filename,
        "rows": int(df.shape[0]),
        "columns": list(df.columns),
        "sample": sample_rows,
    }
    return JSONResponse(content=response)
