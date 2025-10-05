# -*- coding: utf-8 -*-
"""
Script Definitivo para Classificação de Exoplanetas.

Este script treina (ou carrega) um modelo XGBoost para analisar um novo
arquivo CSV de candidatos, adicionando predições e scores de confiança.
"""
import pandas as pd
import io
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
import joblib

MODEL_PATH = "modelo_exoplanetas.joblib"
SCALER_PATH = "scaler_exoplanetas.joblib"
FEATURES_PATH = "features_exoplanetas.joblib"

# ===================================================================
# FASE 1: TREINAMENTO OU CARREGAMENTO DO MODELO
# ===================================================================
def treinar_modelo_final(caminho_arquivo_treino):
    """
    Treina o modelo XGBoost com o dataset base ou carrega de disco.
    """
    # Se já existir modelo salvo, carrega direto
    if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH) and os.path.exists(FEATURES_PATH):
        print("🧠 Modelo e scaler encontrados. Carregando do disco...")
        modelo = joblib.load(MODEL_PATH)
        escalonador = joblib.load(SCALER_PATH)
        features = joblib.load(FEATURES_PATH)
        print("✅ Modelo carregado com sucesso!")
        return modelo, escalonador, features

    print("=" * 50)
    print("FASE 1: TREINAMENTO DO MODELO FINAL (XGBOOST)")
    print("=" * 50)
    
    try:
        df = pd.read_csv(caminho_arquivo_treino, comment='#')
    except FileNotFoundError:
        print(f"ERRO: O arquivo '{caminho_arquivo_treino}' não foi encontrado.")
        return None, None, None

    df_model = df[df['koi_disposition'].isin(['CONFIRMED', 'FALSE POSITIVE'])].copy()

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
    
    print(f"Dados prontos para treino: {X.shape[0]} amostras e {X.shape[1]} features.")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    print("\nTreinando o modelo XGBoost...")
    model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    model.fit(X_train_scaled, y_train)
    print("✅ Modelo treinado com sucesso!")
    
    accuracy = model.score(scaler.transform(X_test), y_test)
    print(f"ACURÁCIA FINAL DO MODELO: {accuracy * 100:.2f}%")

    # Salvar os arquivos
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(features, FEATURES_PATH)
    print("💾 Modelo, scaler e features salvos em disco.")

    return model, scaler, features

# ===================================================================
# FASE 2: FUNÇÃO DE ANÁLISE DE NOVOS ARQUIVOS
# ===================================================================
def analisar_novo_csv(caminho_arquivo_analise, modelo, escalonador, features):
    """
    Analisa um novo CSV com o modelo treinado e retorna DataFrame.
    """
    print("\n" + "=" * 50)
    print(f"FASE 2: ANALISANDO O ARQUIVO '{caminho_arquivo_analise}'")
    print("=" * 50)

    try:
        # Se for caminho, carrega; se for string, trata como conteúdo CSV
        if isinstance(caminho_arquivo_analise, str) and '.csv' in caminho_arquivo_analise:
            df_analise = pd.read_csv(caminho_arquivo_analise)
        else:
            df_analise = pd.read_csv(io.StringIO(caminho_arquivo_analise))
        print(f"Arquivo carregado com {df_analise.shape[0]} candidatos para análise.")
    except FileNotFoundError:
        print(f"ERRO: O arquivo '{caminho_arquivo_analise}' não foi encontrado.")
        return None
        
    # Valida se contém a coluna de identificação
    if 'kepoi_name' not in df_analise.columns:
        print("ERRO: O arquivo CSV precisa conter a coluna 'kepoi_name'.")
        return None
    ids = df_analise['kepoi_name']
    
    # Preenche valores ausentes
    X_analise = df_analise.copy()
    for col in features:
        if X_analise[col].isnull().any():
            median_val = X_analise[col].median()
            X_analise.loc[:, col] = X_analise[col].fillna(median_val)
            
    X_analise_features = X_analise[features]
    X_analise_scaled = escalonador.transform(X_analise_features)
    
    # Predição
    print("Calculando a probabilidade de ser um exoplaneta...")
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
    
    print("✅ Análise concluída com sucesso!")
    return df_resultados

# ===================================================================
# EXPORTAÇÃO DE FUNÇÕES
# ===================================================================
__all__ = ["treinar_modelo_final", "analisar_novo_csv"]
