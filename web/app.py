from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'cambiar_esta_clave'

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    # Menú principal con botones para cada script
    return render_template('index.html')

@app.route('/evaluar', methods=['GET', 'POST'])
def evaluar():
    if request.method == 'POST':
        # Guardar Excel subido
        file = request.files.get('excel')
        if not file:
            flash('Por favor sube un archivo Excel.')
            return redirect(url_for('index'))
        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)
        # Aquí llamarías a script1_evaluador.py
        # resultado = script1.run(path)
        # Por simplicidad, devolvemos un placeholder
        return "Evaluación completada (placeholder)"
    return render_template('evaluar.html')

@app.route('/diagnostico', methods=['GET'])
def diagnostico():
    # placeholder para script2
    return "Generador de diagnóstico (placeholder)"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
