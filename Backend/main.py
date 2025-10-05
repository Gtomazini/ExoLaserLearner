from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import io
import csv
import base64
from datetime import datetime
import model

app = FastAPI(title="Exoplanet Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_CONTENT_TYPES = {"text/csv", "application/vnd.ms-excel", "text/plain"}

# --- Treina o modelo uma vez ao iniciar o app ---
print("🔄 Treinando modelo base...")
modelo_final, escalonador_final, features_usadas = model.treinar_modelo_final("cumulative_2025.10.04_10.14.38.csv")
print("✅ Modelo carregado com sucesso!")

def detect_separator(sample: str) -> str:
    """Detecta o delimitador do CSV; fallback para vírgula."""
    try:
        dialect = csv.Sniffer().sniff(sample)
        return dialect.delimiter
    except Exception:
        return ","

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """Recebe um CSV, roda o modelo e retorna JSON + CSV codificado em Base64."""
    if not file.filename.lower().endswith(".csv") and file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Arquivo inválido. Envie um CSV (.csv).")

    try:
        # Lê o conteúdo do CSV
        content_bytes = await file.read()
        try:
            text = content_bytes.decode("utf-8")
        except UnicodeDecodeError:
            text = content_bytes.decode("iso-8859-1")

        # Detecta separador e carrega em DataFrame
        sep = detect_separator(text[:8192])
        df = pd.read_csv(io.StringIO(text), sep=sep)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao processar CSV: {e}")
    finally:
        await file.close()

    if modelo_final is None:
        raise HTTPException(status_code=500, detail="Modelo não carregado.")

    # Roda o modelo de análise
    resultados = model.analisar_novo_csv(io.StringIO(text), modelo_final, escalonador_final, features_usadas)
    if resultados is None or resultados.empty:
        raise HTTPException(status_code=400, detail="Erro ao analisar CSV com o modelo.")

    # Cria o CSV de saída com predições
    csv_output = io.StringIO()
    resultados.to_csv(csv_output, index=False)
    csv_bytes = csv_output.getvalue().encode("utf-8")

    # Codifica o CSV em base64
    csv_base64 = base64.b64encode(csv_bytes).decode("utf-8")

    # Cria o JSON de resposta
    predictions = []
    for idx, row in resultados.iterrows():
        try:
            percent = float(row["Confianca_Calculada"]) * 100 if isinstance(row["Confianca_Calculada"], (float, int)) else None
        except Exception:
            percent = None
        predictions.append({
            "id": idx + 1,
            "name": row.get("kepoi_name", f"ID_{idx+1}"),
            "percent": round(percent, 2) if percent else None,
            "status": row.get("Veredito_do_Modelo", "Desconhecido")
        })

    json_response = {
        "predictions": predictions,
        "metadata": {
            "totalSamples": len(predictions),
            "processedAt": datetime.utcnow().isoformat() + "Z",
            "modelVersion": "v1.0.0",
            "accuracy": 0.85
        },
        "csv_base64": csv_base64,
        "filename": f"predicoes_{file.filename}"
    }

    return JSONResponse(content=json_response)
