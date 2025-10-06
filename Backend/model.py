# -*- coding: utf-8 -*-
"""
Script Definitivo para Classificação de Exoplanetas.

Este script treina (ou carrega) um modelo XGBoost para analisar um novo
arquivo CSV de candidatos, adicionando predições e scores de confiança.
"""
import pandas as pd
import io
import os
import requests
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
import joblib

# Caminhos dos arquivos
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(SCRIPT_DIR, "modelo_exoplanetas.joblib")
SCALER_PATH = os.path.join(SCRIPT_DIR, "scaler_exoplanetas.joblib")
FEATURES_PATH = os.path.join(SCRIPT_DIR, "features_exoplanetas.joblib")
DATASET_PATH = os.path.join(SCRIPT_DIR, "cumulative_dataset.csv")

# URL do dataset da NASA (Kepler KOI Cumulative Table)
DATASET_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+*+from+cumulative&format=csv"

def baixar_dataset():
    """
    Baixa o dataset de exoplanetas da NASA.
    """
    print("📥 Baixando dataset da NASA Exoplanet Archive...")
    print(f"   URL: {DATASET_URL}")
    
    try:
        response = requests.get(DATASET_URL, timeout=60)
        response.raise_for_status()
        
        with open(DATASET_PATH, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Dataset baixado com sucesso!")
        print(f"   Salvo em: {DATASET_PATH}")
        return DATASET_PATH
    except requests.exceptions.RequestException as e:
        print(f"❌ ERRO ao baixar dataset: {e}")
        print("\n⚠️  SOLUÇÃO ALTERNATIVA:")
        print("   1. Baixe manualmente de: https://exoplanetarchive.ipac.caltech.edu/")
        print("   2. Procure por 'Kepler Objects of Interest'")
        print("   3. Salve como 'cumulative_dataset.csv' na pasta Backend")
        raise

def treinar_modelo_final(caminho_arquivo_treino=None):
    """
    Treina o modelo XGBoost com o dataset base ou carrega de disco.
    """
    # Se já existir modelo salvo, carrega direto
    if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH) and os.path.exists(FEATURES_PATH):
        print(f"🧠 Modelo encontrado em: {MODEL_PATH}")
        print("📂 Carregando modelo do disco...")
        modelo = joblib.load(MODEL_PATH)
        escalonador = joblib.load(SCALER_PATH)
        features = joblib.load(FEATURES_PATH)
        print("✅ Modelo carregado com sucesso!")
        return modelo, escalonador, features

    print("=" * 70)
    print("FASE 1: TREINAMENTO DO MODELO FINAL (XGBOOST)")
    print("=" * 70)
    
    # Se não tiver dataset, baixa automaticamente
    if not os.path.exists(DATASET_PATH):
        print("📂 Dataset não encontrado localmente.")
        baixar_dataset()
    
    csv_path = DATASET_PATH
    
    print(f"\n📖 Carregando dataset de: {csv_path}")
    try:
        df = pd.read_csv(csv_path, comment='#')
        print(f"✅ Dataset carregado: {len(df)} registros")
    except Exception as e:
        print(f"❌ ERRO ao ler CSV: {e}")
        raise

    # Filtra apenas CONFIRMED e FALSE POSITIVE
    df_model = df[df['koi_disposition'].isin(['CONFIRMED', 'FALSE POSITIVE'])].copy()
    print(f"📊 Registros após filtro: {len(df_model)} (CONFIRMED + FALSE POSITIVE)")

    features = [
        'koi_period', 'koi_duration', 'koi_depth', 'koi_prad', 'koi_teq',
        'koi_insol', 'koi_model_snr', 'koi_impact',
        'koi_fpflag_nt', 'koi_fpflag_ss', 'koi_fpflag_co', 'koi_fpflag_ec',
        'koi_steff', 'koi_slogg', 'koi_srad'
    ]
    
    df_model.dropna(subset=features, inplace=True)
    df_model['target'] = df_model['koi_disposition'].apply(lambda x: 1 if x == 'CONFIRMED' else 0)

    X = df_model[features]
    y = df_model['target']
    
    print(f"🎯 Dados prontos para treino: {X.shape[0]} amostras e {X.shape[1]} features")
    print(f"   - Confirmados: {y.sum()}")
    print(f"   - Falsos Positivos: {len(y) - y.sum()}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    print("\n🚀 Treinando o modelo XGBoost...")
    model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    model.fit(X_train_scaled, y_train)
    print("✅ Modelo treinado com sucesso!")
    
    accuracy = model.score(scaler.transform(X_test), y_test)
    print(f"\n📈 ACURÁCIA FINAL DO MODELO: {accuracy * 100:.2f}%")

    # Salvar os arquivos
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(features, FEATURES_PATH)
    print(f"\n💾 Arquivos salvos:")
    print(f"   - Modelo: {MODEL_PATH}")
    print(f"   - Scaler: {SCALER_PATH}")
    print(f"   - Features: {FEATURES_PATH}")

    return model, scaler, features

def analisar_novo_csv(caminho_arquivo_analise, modelo, escalonador, features):
    """
    Analisa um novo CSV com o modelo treinado e retorna DataFrame.
    """
    print("\n" + "=" * 70)
    print(f"FASE 2: ANALISANDO ARQUIVO")
    print("=" * 70)

    try:
        # Se for StringIO ou arquivo, carrega com comment='#' para ignorar linhas de comentário
        if isinstance(caminho_arquivo_analise, str) and '.csv' in caminho_arquivo_analise:
            df_analise = pd.read_csv(
                caminho_arquivo_analise, 
                comment='#',  # Ignora linhas que começam com #
                on_bad_lines='skip'
            )
        else:
            # Para StringIO, lê o conteúdo e remove comentários manualmente
            if hasattr(caminho_arquivo_analise, 'getvalue'):
                text = caminho_arquivo_analise.getvalue()
            elif hasattr(caminho_arquivo_analise, 'read'):
                caminho_arquivo_analise.seek(0)
                text = caminho_arquivo_analise.read()
            else:
                text = str(caminho_arquivo_analise)
            
            # Remove linhas de comentário
            lines = text.split('\n')
            data_lines = [line for line in lines if not line.strip().startswith('#')]
            clean_text = '\n'.join(data_lines)
            
            df_analise = pd.read_csv(
                io.StringIO(clean_text),
                on_bad_lines='skip'
            )
        
        print(f"📊 Arquivo carregado: {df_analise.shape[0]} candidatos, {df_analise.shape[1]} colunas")
        
    except Exception as e:
        print(f"❌ ERRO ao ler arquivo: {e}")
        print(f"   Tipo do erro: {type(e).__name__}")
        return None
        
    # Valida se contém a coluna de identificação
    if 'kepoi_name' not in df_analise.columns:
        print("❌ ERRO: O arquivo CSV precisa conter a coluna 'kepoi_name'")
        return None
    
    ids = df_analise['kepoi_name']
    
    # Preenche valores ausentes
    X_analise = df_analise.copy()
    for col in features:
        if col not in X_analise.columns:
            print(f"⚠️  Coluna '{col}' não encontrada, preenchendo com 0")
            X_analise[col] = 0
        elif X_analise[col].isnull().any():
            median_val = X_analise[col].median()
            X_analise.loc[:, col] = X_analise[col].fillna(median_val)
            
    X_analise_features = X_analise[features]
    X_analise_scaled = escalonador.transform(X_analise_features)
    
    # Predição
    print("🔮 Calculando probabilidades...")
    probabilidades = modelo.predict_proba(X_analise_scaled)
    confianca_exoplaneta = probabilidades[:, 1]
    
    # Monta DataFrame final
    df_resultados = pd.DataFrame({
        'kepoi_name': ids,
        'Confianca_Calculada': confianca_exoplaneta,
        'Veredito_do_Modelo': [
            "Planeta Confirmado" if p > 0.5 else "Falso Positivo"
            for p in confianca_exoplaneta
        ]
    })
    
    print("✅ Análise concluída!")
    return df_resultados

__all__ = ["treinar_modelo_final", "analisar_novo_csv"]