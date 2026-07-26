import sqlite3
import os
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

# Usamos la carpeta /tmp porque Render sí permite escribir archivos ahí gratis
DB_PATH = '/tmp/barberia.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS citas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            fecha TEXT NOT NULL,
            hora TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

PLANTILLA_WEB = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reserva tu Cita - Barbería Pro</title>
    <link href="https://jsdelivr.net" rel="stylesheet">
    <style>
        body { background-color: #121212; color: #ffffff; font-family: 'Segoe UI', sans-serif; }
        .card { background-color: #1e1e1e; border: 1px solid #333; border-radius: 15px; }
        .btn-gold { background-color: #d4af37; color: #000; font-weight: bold; }
        .btn-gold:hover { background-color: #b5942b; color: #000; }
        .table { color: #fff; }
    </style>
</head>
<body>
    <div class="container py-5">
        <header class="text-center mb-5">
            <h1 class="display-4 fw-bold text-warning">💈 BARBERÍA PREMIUM 💈</h1>
            <p class="lead text-muted">Agenda tu corte de cabello en segundos, fácil y rápido.</p>
        </header>

        <div class="row g-4">
            <div class="col-md-6">
                <div class="card p-4 shadow">
                    <h3 class="mb-4 text-warning">Reserva tu Turno</h3>
                    <form action="/reservar" method="POST">
                        <div class="mb-3">
                            <label class="form-label">Nombre Completo</label>
                            <input type="text" name="nombre" class="form-control bg-dark text-white border-secondary" required placeholder="Ej. Juan Pérez">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Teléfono / WhatsApp</label>
                            <input type="tel" name="telefono" class="form-control bg-dark text-white border-secondary" required placeholder="Ej. +56912345678">
                        </div>
                        <div class="row">
                            <div class="col-6 mb-3">
                                <label class="form-label">Fecha</label>
                                <input type="date" name="fecha" class="form-control bg-dark text-white border-secondary" required>
                            </div>
                            <div class="col-6 mb-3">
                                <label class="form-label">Hora</label>
                                <input type="time" name="hora" class="form-control bg-dark text-white border-secondary" required>
                            </div>
                        </div>
                        <button type="submit" class="btn btn-gold w-100 py-2 mt-3">Confirmar Reserva Gratis</button>
                    </form>
                </div>
            </div>

            <div class="col-md-6">
                <div class="card p-4 shadow">
                    <h3 class="mb-4 text-warning">📅 Agenda de Hoy (Panel Barbero)</h3>
                    <div class="table-responsive">
                        <table class="table table-dark table-striped align-middle">
                            <thead>
                                <tr>
                                    <th>Cliente</th>
                                    <th>WhatsApp</th>
                                    <th>Fecha/Hora</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for cita in citas %}
                                <tr>
                                    <td class="fw-bold">{{ cita[1] }}</td>
                                    <td><a href="https://wa.me{{ cita[2] }}" target="_blank" class="text-info">{{ cita[2] }}</a></td>
                                    <td><span class="badge bg-secondary">{{ cita[3] }}</span> <span class="badge bg-warning text-dark">{{ cita[4] }}</span></td>
                                </tr>
                                {% else %}
                                <tr>
                                    <td colspan="3" class="text-center text-muted py-4">No hay citas registradas aún.</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM citas ORDER BY fecha ASC, hora ASC')
    todas_citas = cursor.fetchall()
    conn.close()
    return render_template_string(PLANTILLA_WEB, citas=todas_citas)

@app.route('/reservar', methods=['POST'])
def reservar():
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    fecha = request.form['fecha']
    hora = request.form['hora']
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO citas (nombre, telefono, fecha, hora) VALUES (?, ?, ?, ?)', 
                   (nombre, telefono, fecha, hora))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=8080)
