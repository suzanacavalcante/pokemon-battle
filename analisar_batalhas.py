import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import json
import itertools # Para gerar combinações de Pokémon
import ast # Para ast.literal_eval

# --- Configurações ---
# Nomes dos arquivos CSV
POKEMON_CSV_FILE = 'final_pokemon.csv'
COMBATS_CSV_FILE = 'final_combats.csv'

# --- Script Principal ---
def main():
    try:
        # 1. Carregar os dados dos Pokémon
        df_pokemon = pd.read_csv(POKEMON_CSV_FILE)
        print(f"Dados de Pokémon carregados de '{POKEMON_CSV_FILE}'.")
        print("Primeiras 5 linhas do df_pokemon:")
        print(df_pokemon.head())
        print("\n" + "="*50 + "\n")

        # 2. Carregar os dados das batalhas
        df_combats = pd.read_csv(COMBATS_CSV_FILE)
        print(f"Dados de batalhas carregados de '{COMBATS_CSV_FILE}'.")
        print("Primeiras 5 linhas do df_combats:")
        print(df_combats.head())
        print("\n" + "="*50 + "\n")

        # 3. Preparar df_pokemon para merges: renomear '#' para 'id'
        if '#' in df_pokemon.columns:
            df_pokemon_renamed = df_pokemon.rename(columns={'#': 'id'})
        else:
            df_pokemon_renamed = df_pokemon.copy()

        # 4. Combinar os dados das batalhas com as características dos Pokémon
        df_merged = pd.merge(df_combats, df_pokemon_renamed,
                             left_on='First_pokemon', right_on='id',
                             how='left', suffixes=('_combat', '_pokemon1'))
        df_merged = df_merged.drop(columns=['id'])
        df_merged.columns = [col.replace('_pokemon1', '_First_pokemon') for col in df_merged.columns]

        df_final = pd.merge(df_merged, df_pokemon_renamed,
                            left_on='Second_pokemon', right_on='id',
                            how='left', suffixes=('_First_pokemon', '_Second_pokemon'))
        df_final = df_final.drop(columns=['id'])

        print("DataFrame final combinado (primeiras 5 linhas):")
        print(df_final.head())
        print("\n" + "="*50 + "\n")

        # --- Engenharia de Features ---
        numeric_stats = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']

        for stat in numeric_stats:
            df_final[f'{stat}_Diff'] = df_final[f'{stat}_First_pokemon'] - df_final[f'{stat}_Second_pokemon']
            epsilon = 1e-6 # Pequeno valor para evitar divisão por zero
            df_final[f'{stat}_Ratio'] = df_final[f'{stat}_First_pokemon'] / (df_final[f'{stat}_Second_pokemon'] + epsilon)

        df_final['Legendary_Diff'] = df_final['Legendary_First_pokemon'].astype(int) - df_final['Legendary_Second_pokemon'].astype(int)

        # 5. Preparação para Machine Learning
        # A variável alvo é se o First_pokemon venceu (1) ou não (0)
        df_final['First_pokemon_Wins'] = (df_final['Winner'] == df_final['First_pokemon']).astype(int)

        # Seleção de features
        features = [f'{stat}_Diff' for stat in numeric_stats] + \
                   [f'{stat}_Ratio' for stat in numeric_stats] + \
                   ['Legendary_Diff'] + \
                   ['Type 1_First_pokemon', 'Type 2_First_pokemon', 'Type 1_Second_pokemon', 'Type 2_Second_pokemon']

        X = df_final[features]
        y = df_final['First_pokemon_Wins']

        # Codificar Variáveis Categóricas (One-Hot Encoding)
        # Isso cria novas colunas para cada categoria de tipo de Pokémon
        X = pd.get_dummies(X, columns=['Type 1_First_pokemon', 'Type 2_First_pokemon', 'Type 1_Second_pokemon', 'Type 2_Second_pokemon'], drop_first=True)

        # Dividir os Dados em Conjuntos de Treino e Teste
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        print(f"Shape dos dados de treino (X_train, y_train): {X_train.shape}, {y_train.shape}")
        print(f"Shape dos dados de teste (X_test, y_test): {X_test.shape}, {y_test.shape}")
        print("\n" + "="*50 + "\n")

        # 6. Treinar o Modelo de Classificação
        # Usando Regressão Logística, um modelo simples e eficaz para classificação binária
        model = LogisticRegression(max_iter=2000, random_state=42, solver='liblinear') # Aumentar max_iter para convergência
        model.fit(X_train, y_train)
        print("Modelo de Regressão Logística treinado com sucesso.")
        print("\n" + "="*50 + "\n")

        # 7. Avaliar o Modelo
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Acurácia do Modelo (Regressão Logística): {accuracy:.4f}")
        print("\n" + "="*50 + "\n")

    except FileNotFoundError as e:
        print(f"Erro: Um dos arquivos CSV não foi encontrado: {e.filename}. Certifique-se de que 'final_pokemon.csv' e 'final_combats.csv' estão na mesma pasta do script.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        import traceback
        traceback.print_exc() # Imprime o stack trace completo para depuração

if __name__ == "__main__":
    main()
