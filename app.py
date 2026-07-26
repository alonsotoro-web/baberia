import sqlite3
import os
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

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
            hora TEXT NOT NULL,
            servicio TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

PLANTILLA_OK = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Gold Room - Barbería Premium</title>
    <link href="https://jsdelivr.net" rel="stylesheet">
    <link href="https://googleapis.com" rel="stylesheet">
    <style>
        body { background-color: #0a0a0b; color: #ffffff; font-family: 'Plus Jakarta Sans', sans-serif; }
        h1, h2, h3 { font-family: 'Marcellus', serif; letter-spacing: 2px; }
        .premium-card { 
            background: rgba(20, 20, 22, 0.75); 
            border: 1px solid rgba(255, 255, 255, 0.05); 
            border-radius: 24px;
            transition: all 0.3s ease;
        }
        .premium-card:hover { border-color: #d4af37; box-shadow: 0 0 20px rgba(212, 175, 55, 0.2); }
        .btn-gold { 
            background: linear-gradient(135deg, #b5942b 0%, #d4af37 50%, #f3e5ab 100%);
            color: #000; font-weight: 800; border: none; border-radius: 12px; padding: 14px;
        }
        .form-control, .form-select {
            background-color: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px; color: #fff !important; padding: 12px;
        }
        .price-tag { color: #d4af37; font-weight: 800; font-size: 1.25rem; }
        .gallery-img { border-radius: 16px; height: 220px; object-fit: cover; }
        .review-stars { color: #d4af37; }
    </style>
</head>
<body>
    <div class="container py-5 text-center">
        <span class="text-uppercase text-muted small d-block mb-2">— EXPERIENCIA EXCLUSIVA —</span>
        <h1 class="display-3 fw-bold text-white mb-3">THE GOLD ROOM</h1>
        <p class="lead text-muted mx-auto" style="max-width: 600px;">Cortes de autor, barbería clásica y estilo de vanguardia en un entorno de puro lujo urbano.</p>
    </div>

    <div class="container mb-5">
        <div class="row g-5">
            <div class="col-lg-7">
                <h3 class="text-warning mb-4 fw-bold">✂️ Servicios & Tarifas 2026</h3>
                <div class="d-flex flex-column gap-3">
                    <div class="premium-card p-3 d-flex justify-content-between align-items-center">
                        <div><h5 class="mb-1 text-white fw-bold">Corte de Autor Premium</h5><p class="text-muted mb-0 small">Asesoría de visagismo, lavado y peinado.</p></div>
                        <span class="price-tag">\$15.000</span>
                    </div>
                    <div class="premium-card p-3 d-flex justify-content-between align-items-center">
                        <div><h5 class="mb-1 text-white fw-bold">Perfilado de Barba + Toalla Ritual</h5><p class="text-muted mb-0 small">Navaja clásica y aceites esenciales.</p></div>
                        <span class="price-tag">\$10.000</span>
                    </div>
                </div>

                <h3 class="text-warning mt-5 mb-4 fw-bold">🔥 Tendencias Urbanas</h3>
                <div class="row g-3">
                    <div class="col-6"><img src="https://unsplash.com" class="w-100 gallery-img" alt="Fade"></div>
                    <div class="col-6"><img src="https://unsplash.com" class="w-100 gallery-img" alt="Barba"></div>
                </div>
            </div>

            <div class="col-lg-5">
                <div class="premium-card p-4 shadow-lg">
                    <h3 class="mb-2 text-warning fw-bold">📅 Agenda tu Turno VIP</h3>
                    <form action="/reservar" method="POST">
                        <div class="mb-3">
                            <label class="form-label text-white-50 small fw-bold">Nombre Completo</label>
                            <input type="text" name="nombre" class="form-control" required placeholder="Ej. Carlos Silva">
                        </div>
                        <div class="mb-3">
                            <label class="form-label text-white-50 small fw-bold">WhatsApp</label>
                            <input type="tel" name="telefono" class="form-control" required placeholder="Ej. +56912345678">
                        </div>
                        <div class="mb-3">
                            <label class="form-label text-white-50 small fw-bold">Servicio</label>
                            <select name="servicio" class="form-select" required>
                                <option value="Corte Autor Premium">Corte de Autor Premium - \$15.000</option>
                                <option value="Perfilado Barba">Perfilado de Barba - \$10.000</option>
                            </select>
                        </div>
                        <div class="row g-2">
                            <div class="col-6 mb-3"><label class="form-label text-white-50 small fw-bold">Fecha</label><input type="date" name="fecha" class="form-control" required></div>
                            <div class="col-6 mb-3"><label class="form-label text-white-50 small fw-bold">Hora</label><input type="time" name="hora" class="form-control" required></div>
                        </div>
                        <button type="submit" class="btn btn-gold w-100 py-3 mt-2">Confirmar Reserva</button>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <div class="container py-5 border-top border-secondary">
        <h3 class="text-center text-warning mb-5 fw-bold">💬 Opiniones de Clientes</h3>
        <div class="row g-4">
            <div class="col-md-6"><div class="premium-card p-4"><div class="review-stars mb-2">★★★★★</div><p class="small text-white">"La mejor atención y el sistema web para reservar es súper rápido."</p><span class="small text-muted fw-bold">— Matías O.</span></div></div>
            <div class="col-md-6"><div class="premium-card p-4"><div class="review-stars mb-2">★★★★★</div><p class="small text-white">"Excelente servicio, muy puntuales con las horas agendadas."</p><span class="small text-muted fw-bold">— Ignacio R.</span></div></div>
        </div>
    </div>

    <div class="container py-4 mt-5 bg-black rounded-4 border border-secondary">
        <h4 class="text-danger fw-bold mb-3 px-3">🔒 Panel Interno del Barbero</h4>
        <div class="table-responsive">
            <table class="table table-dark table-hover">
                <thead><tr><th>Cliente</th><th>WhatsApp</th><th>Servicio</th><th>Fecha/Hora</th></tr></thead>
                <tbody>
                    {% for cita in citas %}
                    <tr>
                        <td class="fw-bold">{{ cita[1] }}</td>
                        <td><a href="https://wa.me{{ cita[2] }}" target="_blank" class="text-info">{{ cita[2] }}</a></td>
                        <td><span class="badge bg-warning text-dark">{{ cita[5] }}</span></td>
                        <td>{{ cita[3] }} a las {{ cita[4] }} hrs</td>
                    </tr>
                    {% else %}
                    <tr><td colspan="4" class="text-center text-muted py-3">No hay citas registradas.</td></tr>
                    {% endfor %}
                </tbody>
            </table>
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
    return render_template_string(PLANTILLA_OK, citas=todas_citas)

@app.route('/reservar', methods=['POST'])
def reservar():
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    fecha = request.form['fecha']
    hora = request.form['hora']
    servicio = request.form['servicio']
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO citas (nombre, telefono, fecha, hora, servicio) VALUES (?, ?, ?, ?, ?)', 
                   (nombre, telefono, fecha, hora, servicio))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=8080)
