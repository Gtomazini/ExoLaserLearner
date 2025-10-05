# -*- coding: utf-8 -*-
"""
Script Definitivo para Classificação de Exoplanetas.

Este script treina um modelo de alta performance (XGBoost) e o utiliza
para analisar um novo arquivo CSV de candidatos, adicionando predições
e scores de confiança a cada um.
"""
import pandas as pd
import io
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler

# ===================================================================
# FASE 1: FUNÇÃO DE TREINAMENTO (Nenhuma alteração aqui)
# ===================================================================
def treinar_modelo_final(caminho_arquivo_treino):
    """
    Treina o modelo XGBoost com o dataset base.
    """
    print("="*50)
    print("FASE 1: TREINAMENTO DO MODELO FINAL (XGBOOST)")
    print("="*50)
    
    try:
        df = pd.read_csv(caminho_arquivo_treino, comment='#')
    except FileNotFoundError:
        print(f"ERRO: O arquivo de treinamento '{caminho_arquivo_treino}' não foi encontrado.")
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

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    print("\nTreinando o modelo XGBoost...")
    model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    model.fit(X_train_scaled, y_train)
    print("Modelo treinado com sucesso!")
    
    accuracy = model.score(scaler.transform(X_test), y_test)
    print(f"ACURÁCIA FINAL DO MODELO: {accuracy * 100:.2f}%")
    
    return model, scaler, features

# ===================================================================
# FASE 2: FUNÇÃO DE ANÁLISE DE NOVOS ARQUIVOS
# ===================================================================
def analisar_novo_csv(caminho_arquivo_analise, modelo, escalonador, features):
    """
    Carrega um novo CSV, analisa cada linha com o modelo treinado e retorna os resultados.
    
    Args:
        caminho_arquivo_analise (str): O caminho do CSV a ser analisado.
        modelo: O modelo XGBoost treinado.
        escalonador: O escalonador ajustado aos dados de treino.
        features (list): A lista de features que o modelo espera.
        
    Returns:
        DataFrame: Um DataFrame do Pandas com os resultados da análise.
    """
    print("\n" + "="*50)
    print(f"FASE 2: ANALISANDO O ARQUIVO '{caminho_arquivo_analise}'")
    print("="*50)

    try:
        # Se o arquivo for um caminho, carrega o arquivo. Se for uma string, trata como CSV.
        if isinstance(caminho_arquivo_analise, str) and '.csv' in caminho_arquivo_analise:
             df_analise = pd.read_csv(caminho_arquivo_analise)
        else:
             df_analise = pd.read_csv(io.StringIO(caminho_arquivo_analise))
        print(f"Arquivo carregado com {df_analise.shape[0]} candidatos para análise.")
    except FileNotFoundError:
        print(f"ERRO: O arquivo para análise '{caminho_arquivo_analise}' não foi encontrado.")
        return None
        
    # Salvar os nomes para o relatório final (assumindo que a coluna de nome existe)
    if 'kepoi_name' not in df_analise.columns:
        print("ERRO: O arquivo CSV de análise precisa conter uma coluna de identificação chamada 'kepoi_name'.")
        return None
    ids = df_analise['kepoi_name']
    
    # Preparar os dados para o modelo
    X_analise = df_analise.copy()
    for col in features:
        if X_analise[col].isnull().any():
            median_val = X_analise[col].median()
            X_analise.loc[:, col] = X_analise[col].fillna(median_val)
            
    X_analise_features = X_analise[features]
    X_analise_scaled = escalonador.transform(X_analise_features)
    
    # Fazer as predições de probabilidade
    print("Calculando a probabilidade de ser um exoplaneta para cada candidato...")
    probabilidades = modelo.predict_proba(X_analise_scaled)
    confianca_exoplaneta = probabilidades[:, 1]
    
    # Criar o DataFrame de resultados
    df_resultados = pd.DataFrame({
        'kepoi_name': ids,
        'Confianca_Calculada': confianca_exoplaneta,
        'Veredito_do_Modelo': ["Planeta Confirmado" if p > 0.5 else "Falso Positivo" for p in confianca_exoplaneta]
    })
    
    print("Análise concluída com sucesso!")
    return df_resultados

# ===================================================================
# EXECUÇÃO PRINCIPAL
# ===================================================================
if __name__ == '__main__':
    # 1. TREINE O MODELO
    arquivo_de_treino = 'cumulative_2025.10.04_10.14.38.csv'
    modelo_final, escalonador_final, features_usadas = treinar_modelo_final(arquivo_de_treino)
    
    # 2. ANALISE UM NOVO ARQUIVO CSV
    if modelo_final:
        # --- PREPARE SEU ARQUIVO CSV AQUI ---
        # Para demonstração, estou criando um CSV de exemplo em formato de string.
        # No seu uso real, você substituirá todo este bloco por:
        # arquivo_para_analisar = 'meus_candidatos.csv'
        
        csv_de_exemplo = """kepoi_name,koi_period,koi_duration,koi_depth,koi_prad,koi_teq,koi_insol,koi_model_snr,koi_impact,koi_fpflag_nt,koi_fpflag_ss,koi_fpflag_co,koi_fpflag_ec,koi_steff,koi_slogg,koi_srad
K99999.01,10.5,3.0,800.0,2.5,750,80.0,40.0,0.5,0,0,0,0,5800,4.4,1.0
K99999.02,150.2,10.0,20000.0,45.0,1000,20.0,15.0,0.9,0,1,0,0,5800,4.4,1.0
K00001.01,2.47,1.74,14231,13.04,1339,761.46,4304.3,0.818,0,0,0,0,5820,4.457,0.964
"""
        arquivo_para_analisar = csv_de_exemplo
        
        # Chama a função de análise
        resultados_da_analise = analisar_novo_csv(arquivo_para_analisar, modelo_final, escalonador_final, features_usadas)
        
        # 3. EXIBA OS RESULTADOS
        if resultados_da_analise is not None:
            # Formatar a coluna de chance para porcentagem
            resultados_da_analise['Confianca_Calculada'] = resultados_da_analise['Confianca_Calculada'].map('{:.2%}'.format)
            
            print("\n--- RESULTADO DA ANÁLISE ---")
            print(resultados_da_analise)