from flask import Flask, render_template, request, redirect, url_for, flash, session
import os

from scripts.script1_evaluador import load_questions, calculate_stats
from scripts.script2_diagnostico import generate_diagnostic
from scripts.script3_politicas import generate_policy


app = Flask(__name__)
app.secret_key = 'cambiar_esta_clave'

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    # Menú principal con enlaces a cada script
    return render_template('index.html')

@app.route('/evaluar', methods=['GET', 'POST'])
def evaluar():
    if request.method == 'POST':
        file = request.files.get('excel')
        if not file:
            flash('Por favor sube un archivo Excel.')
            return redirect(url_for('index'))
        filename = file.filename
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        session['uploaded_file'] = filename
        return redirect(url_for('mostrar_preguntas'))
    return render_template('evaluar.html')

@app.route('/evaluar/preguntas', methods=['GET', 'POST'])
def mostrar_preguntas():
    filename = session.get('uploaded_file')
    if not filename:
        flash('No se ha subido ningún archivo.')
        return redirect(url_for('index'))
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if request.method == 'POST':
        # Recoger y guardar respuestas
        respuestas = []
        for code in request.form:
            resp = request.form.get(code)
            respuestas.append({'id': code, 'respuesta': resp})
        session['last_respuestas'] = respuestas

        # Calcular estadísticas y mostrar resultado
        stats = calculate_stats(respuestas)
        return render_template('resultado.html', respuestas=respuestas, stats=stats)

    # GET: mostrar el cuestionario
    controles = load_questions(path)  # lista de tuplas (id, pregunta)
    return render_template('preguntas.html', controles=controles)

@app.route('/diagnostico', methods=['GET'])
def diagnostico():
    respuestas = session.get('last_respuestas')
    if not respuestas:
        flash('Primero debes completar la evaluación.')
        return redirect(url_for('index'))

    # Generar diagnóstico y mostrarlos
    df = generate_diagnostic(respuestas)
    tabla = df.to_dict(orient='records')
    return render_template('diagnostico.html', tabla=tabla)

@app.route('/politicas', methods=['GET','POST'])
def politicas():
    if request.method == 'POST':
        # Recogemos todos los campos del formulario en un dict
        params = request.form.to_dict(flat=True)
        # Recogemos la lista de políticas marcadas
        selected = request.form.getlist('policies')
        # Generamos cada política
        resultados = [ generate_policy(key, params) for key in selected ]
        return render_template('politicas_resultado.html', resultados=resultados)
    # GET solo muestra el formulario
    return render_template('politicas.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
