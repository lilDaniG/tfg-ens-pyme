from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask import jsonify
import os
from scripts.script1_evaluador import load_questions, calculate_stats

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
    # POST: procesa respuestas
    if request.method == 'POST':
        respuestas = []
        for code in request.form:
            resp = request.form.get(code)
            respuestas.append({'id': code, 'respuesta': resp})
        stats = calculate_stats(respuestas)
        return render_template('resultado.html', respuestas=respuestas, stats=stats)
    # GET: muestra el cuestionario
    controles = load_questions(path)  # lista de tuplas (id, pregunta)
    return render_template('preguntas.html', controles=controles)

@app.route('/diagnostico', methods=['GET'])
def diagnostico():
    return "Generador de diagnóstico (placeholder)"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
