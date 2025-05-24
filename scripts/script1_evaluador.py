import pandas as pd

def run(input_excel_path):
    # Leer el Excel con preguntas
    df = pd.read_excel(input_excel_path)
    # Supón que hay columna 'Pregunta'
    respuestas = []
    for idx, row in df.iterrows():
        # Aquí podrías console input o lógica distinta
        # Pero por ahora sólo simulamos respuestas 'sí'
        respuestas.append({'id': row['Código ENS'], 'respuesta': 'sí'})
    # Devolver un dict con el resultado
    return respuestas
