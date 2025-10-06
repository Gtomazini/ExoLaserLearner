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

# Variáveis globais para o modelo
modelo_final = None
escalonador_final = None
features_usadas = None

# --- Treina o modelo uma vez ao iniciar o app ---
@app.on_event("startup")
async def startup_event():
    global modelo_final, escalonador_final, features_usadas
    
    print("\n" + "=" * 70)
    print("🚀 INICIANDO SERVIDOR - EXOPLANET PREDICTION API")
    print("=" * 70)
    
    try:
        print("\n🔄 Carregando/treinando modelo de Machine Learning...")
        modelo_final, escalonador_final, features_usadas = model.treinar_modelo_final()
        print("\n✅ SERVIDOR PRONTO!")
        print("=" * 70)
    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO ao carregar modelo: {e}")
        print("\n⚠️  O servidor vai iniciar, mas o endpoint /predict NÃO funcionará!")
        print("⚠️  Verifique os logs acima para mais detalhes.")
        print("=" * 70)
        modelo_final, escalonador_final, features_usadas = None, None, None

def detect_separator(sample: str) -> str:
    """Detecta o delimitador do CSV; fallback para vírgula."""
    try:
        dialect = csv.Sniffer().sniff(sample)
        return dialect.delimiter
    except Exception:
        return ","

@app.get("/")
async def root():
    """Endpoint raiz para verificar se a API está rodando."""
    status = "✅ Online" if modelo_final is not None else "⚠️  Modelo não carregado"
    return {
        "message": "Exoplanet Prediction API",
        "status": status,
        "version": "1.0.0",
        "endpoints": {
            "predict": "/predict (POST)",
            "health": "/health (GET)"
        }
    }

@app.get("/health")
async def health():
    """Endpoint de health check."""
    return {
        "status": "healthy" if modelo_final is not None else "model_not_loaded",
        "model_loaded": modelo_final is not None,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """Recebe um CSV, roda o modelo e retorna JSON + CSV codificado em Base64."""
    
    # Verifica se o modelo está carregado
    if modelo_final is None:
        raise HTTPException(
            status_code=503, 
            detail="Modelo não está carregado. Verifique os logs do servidor e reinicie."
        )
    
    # Valida o arquivo
    if not file.filename.lower().endswith(".csv") and file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400, 
            detail="Arquivo inválido. Envie um CSV (.csv)."
        )

    try:
        # Lê o conteúdo do CSV
        content_bytes = await file.read()
        try:
            text = content_bytes.decode("utf-8")
        except UnicodeDecodeError:
            try:
                text = content_bytes.decode("iso-8859-1")
            except:
                text = content_bytes.decode("latin-1")

        # Remove linhas de comentário (começam com #)
        lines = text.split('\n')
        data_lines = [line for line in lines if not line.strip().startswith('#')]
        clean_text = '\n'.join(data_lines)
        
        # Detecta o separador no conteúdo limpo
        sep = detect_separator(clean_text[:2048])
        
        # Carrega o CSV
        df = pd.read_csv(
            io.StringIO(clean_text), 
            sep=sep,
            on_bad_lines='skip'
        )
        
        print(f"\n📄 Arquivo recebido: {file.filename}")
        print(f"   Delimitador: '{sep}'")
        print(f"   Linhas: {len(df)}, Colunas: {len(df.columns)}")
        print(f"   Colunas principais: {', '.join(df.columns[:5].tolist())}...")
        
    except Exception as e:
        await file.close()
        raise HTTPException(
            status_code=400, 
            detail=f"Erro ao processar CSV: {str(e)}. Verifique se o arquivo está bem formatado."
        )
    finally:
        await file.close()

    # Roda o modelo de análise
    try:
        resultados = model.analisar_novo_csv(
            io.StringIO(text), 
            modelo_final, 
            escalonador_final, 
            features_usadas
        )
    except Exception as e:
        print(f"❌ Erro durante análise: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao analisar CSV: {e}")
    
    if resultados is None or resultados.empty:
        raise HTTPException(
            status_code=400, 
            detail="Erro ao analisar CSV. Verifique se o formato está correto."
        )

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
    
    print(f"✅ Análise concluída: {len(predictions)} predições geradas")

    return JSONResponse(content=json_response)