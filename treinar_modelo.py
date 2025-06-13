import pandas as pd
from meuportal import carregar_imoveis_xml
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

# Criar pasta se não existir
os.makedirs("models", exist_ok=True)

# 1. Carregar dados
print("Carregando dados do XML...")
df = carregar_imoveis_xml()

# 2. Preparar dados
print("Preparando dados...")
df = df.dropna(subset=['bairro', 'm2', 'quartos', 'banheiros', 'garagem', 'valor'])
df = df[df['m2'] > 0]

# 3. Selecionar colunas
colunas = ['estado', 'cidade', 'bairro', 'tipo', 'm2', 'quartos', 'banheiros', 'garagem', 'mobilia', 'ano']
X = df[colunas].copy()
y = df['valor']

# 4. Codificar categóricas
print("Codificando variáveis categóricas...")
le_dict = {}
for col in ['estado', 'cidade', 'bairro', 'tipo', 'mobilia']:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    le_dict[col] = le

# 5. Treinar modelo
print("Treinando modelo...")
modelo = RandomForestRegressor(n_estimators=100, random_state=42)
modelo.fit(X, y)

# 6. Salvar modelo e encoders
print("Salvando arquivos...")
joblib.dump(modelo, 'models/modelo_avaliacao.joblib')
joblib.dump(le_dict, 'models/label_encoders.joblib')
joblib.dump(X.columns.tolist(), 'models/colunas_modelo.joblib')

print("Modelo treinado e salvo com sucesso!")
