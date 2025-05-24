import pandas as pd

def load_questions(path_excel):
    df = pd.read_excel(path_excel)
    # Devuelve lista de (id, pregunta)
    return list(zip(df['Código ENS'], df['Pregunta']))

def calculate_stats(respuestas):
    total = len(respuestas)
    cumplidos = sum(1 for r in respuestas if r['respuesta'] == 'sí')
    porcentaje = round(cumplidos / total * 100, 2) if total else 0
    return {'total': total, 'cumplidos': cumplidos, 'porcentaje': porcentaje}

# Función CLI (opcional)
def run_cli(path_excel):
    df = pd.read_excel(path_excel)
    resultados = []
    total = len(df)
    cumplidos = 0
    for _, row in df.iterrows():
        pregunta = row['Pregunta']
        resp = input(f"{pregunta} (sí/no): ").strip().lower()
        ok = resp in ('sí','si','s','y','yes')
        resultados.append({'id': row['Código ENS'], 'respuesta': 'sí' if ok else 'no'})
        if ok:
            cumplidos += 1
    porcentaje = round(cumplidos/total*100,2) if total else 0
    print(f"\nCumplimiento: {cumplidos}/{total} controles ({porcentaje}%)")
    return resultados