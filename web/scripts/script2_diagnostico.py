import pandas as pd

# Mapeo de recomendaciones por código ENS
RECOMMENDATIONS = {
    'Op.acc.5': 'Implementar autenticación de múltiples factores para accesos externos',
    # ... aquí añadimos más entradas según tu catálogo
}

def generate_diagnostic(respuestas):
    """
    respuestas: lista de dicts {'id': <código>, 'respuesta': 'sí'|'no'}
    Devuelve un DataFrame con columnas [Código ENS, Estado, Recomendación].
    """
    rows = []
    for item in respuestas:
        cid = item['id']
        estado = 'Cumple' if item['respuesta'] == 'sí' else 'No cumple'
        # Si no hay recomendación específica, usamos un genérico
        rec = RECOMMENDATIONS.get(cid,
             'Revisar y aplicar buenas prácticas para este control')
        rows.append({
            'Código ENS': cid,
            'Estado': estado,
            'Recomendación': rec
        })
    df = pd.DataFrame(rows)
    return df
