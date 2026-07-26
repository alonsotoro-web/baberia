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

PLANTILLA_LUJO = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Gold Room - Barbería Premium</title>
    <!-- Bootstrap 5 & Animate.css para efectos visuales modernos -->
    <link href="https://jsdelivr.net" rel="stylesheet">
    <link rel="stylesheet" href="https://cloudflare.com"/>
    <!-- Google Fonts modernas -->
    <link href="https://googleapis.com" rel="stylesheet">
    
    <style>
        :root {
            --bg-dark: #0a0a0b;
            --card-bg: rgba(20, 20, 22, 0.75);
            --gold: #d4af37;
            --gold-glow: rgba(212, 175, 55, 0.2);
            --text-gray: #a0a0ab;
        }

        body { 
            background-color: var(--bg-dark); 
            color: #ffffff; 
            font-family: 'Plus Jakarta Sans', sans-serif;
            overflow-x: hidden;
        }

        h1, h2, h3, .brand-font {
            font-family: 'Marcellus', serif;
            letter-spacing: 2px;
        }

        /* Efecto de fondo abstracto de lujo */
        .bg-glow {
            position: absolute;
            top: -10%;
            left: 50%;
            transform: translateX(-50%);
            width: 600px;
            height: 600px;
            background: radial-gradient(circle, rgba(212,175,55,0.08) 0%, rgba(0,0,0,0) 70%);
            z-index: -1;
            pointer-events: none;
        }

        /* Glassmorphism: Tarjetas modernas con desenfoque de cristal */
        .premium-card { 
            background: var(--card-bg); 
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.05); 
            border-radius: 24px;
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }
        
        .premium-card:hover {
            transform: translateY(-8px);
            border-color: var(--gold);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5), 0 0 20px var(--gold-glow);
        }

        /* Botón de Oro Animado */
        .btn-gold { 
            background: linear-gradient(135deg, #b5942b 0%, #d4af37 50%, #f3e5ab 100%);
            color: #000; 
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 1px;
            border: none;
            border-radius: 12px;
            padding: 14px;
            transition: all 0.3s ease;
        }

        .btn-gold:hover { 
            transform: scale(1.02);
            box-shadow: 0 0 25px rgba(212, 175, 55, 0.6);
            color: #000;
        }

        /* Inputs estilizados oscuros */
        .form-control, .form-select {
            background-color: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px;
            color: #fff !important;
            padding: 12px;
        }

        .form-control:focus, .form-select:focus {
            border-color: var(--gold) !important;
            box-shadow: 0 0 10px var(--gold-glow) !important;
        }

        /* Badges de Precios */
        .price-tag {
            color: var(--gold);
            font-weight: 800;
            font-size: 1.25rem;
        }

        /* Imagenes de cortes con efecto Zoom */
        .gallery-img {
            border-radius: 16px;
            height: 220px;
            object-fit: cover;
            transition: transform 0.5s ease;
        }

        .gallery-wrapper {
            overflow: hidden;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .gallery-wrapper:hover .gallery-img {
            transform: scale(1.1);
        }

        .review-stars {
            color: var(--gold);
        }
    </style>
</head>
<body>
    <div class="bg-glow"></div>

    <!-- HERO SECTION (Presentación de Alto Impacto) -->
    <div class="container py-5 text-center animate__animated animate__fadeIn">
        <span class="text-uppercase text-muted small tracking-widest d-block mb-2">— EXPERIENCIA EXCLUSIVA —</span>
        <h1 class="display-3 fw-bold text-white mb-3">THE GOLD ROOM</h1>
        <p class="lead text-muted mx-auto" style="max-width: 600px;">Cortes de autor, barbería clásica y estilo de vanguardia urbana en un entorno de puro lujo arquitectónico.</p>
        <div class="d-flex justify-content-center gap-3 mt-4">
            <span class="badge bg-dark border border-secondary px-3 py-2">⭐ 4.9/5 Google Reviews</span>
            <span class="badge bg-dark border border-secondary px-3 py-2">📍 Centro de la Ciudad</span>
        </div>
    </div>

    <div class="container mb-5">
        <div class="row g-5">
            
            <!-- LISTA DE PRECIOS Y SERVICIOS -->
            <div class="col-lg-7 animate__animated animate__fadeInLeft">
                <h3 class="text-warning mb-4 fw-bold">✂️ Nuestros Servicios & Tarifas</h3>
                <div class="d-flex flex-column gap-3">
                    
                    <div class="premium-card p-3 d-flex justify-content-between align-items-center">
                        <div>
                            <h5 class="mb-1 text-white fw-bold">Corte de Autor Premium</h5>
                            <p class="text-muted mb-0 small">Incluye asesoría de visagismo, lavado y peinado con cera mate.</p>
                        </div>
                        <span class="price-tag">\$15.000</span>
                    </div>

                    <div class="premium-card p-3 d-flex justify-content-between align-items-center">
                        <div>
                            <h5 class="mb-1 text-white fw-bold">Perfilado de Barba + Toalla Ritual</h5>
                            <p class="text-muted mb-0 small">Navaja clásica, aceites esenciales de hidratación y vapor de ozono.</p>
                        </div>
                        <span class="price-tag">\$10.000</span>
                    </div>

                    <div class="premium-card p-3 d-flex justify-content-between align-items-center">
                        <div>
                            <h5 class="mb-1 text-white fw-bold">Combo Gold Completo</h5>
                            <p class="text-muted mb-0 small">Máxima experiencia: Corte de cabello + Barba ritual completa.</p>
                        </div>
                        <span class="price-tag">\$22.000</span>
                    </div>
                </div>

                <!-- GALERÍA DE TRABAJOS (Fotos Modernas Simuladas con Enlaces Estéticos) -->
                <h3 class="text-warning mt-5 mb-4 fw-bold">🔥 Portafolio de Estilos</h3>
                <div class="row g-3">
                    <div class="col-6 col-sm-4">
                        <div class="gallery-wrapper">
                            <img src="https://unsplash.com" class="w-100 gallery-img" alt="Fade">
                        </div>
                    </div>
                    <div class="col-6 col-sm-4">
                        <div class="gallery-wrapper">
                            <img src="https://unsplash.com" class="w-100 gallery-img" alt="Barba">
                        </div>
                    </div>
                    <div class="col-12 col-sm-4 d-none d-sm-block">
                        <div class="gallery-wrapper">
                            <img src="https://unsplash.com" class="w-100 gallery-img" alt="Clásico">
                        </div>
                    </div>
                </div>
            </div>

            <!-- FORMULARIO DE RESERVA DE CITAS -->
            <div class="col-lg-5 animate__animated animate__fadeInRight">
                <div class="premium-card p-4 shadow-lg sticky-lg-top" style="top: 20px;">
                    <h3 class="mb-2 text-warning fw-bold">📅 Agenda Tu Turno</h3>
                    <p class="text-muted small mb-4">Selecciona tu horario preferido. Recibirás confirmación inmediata.</p>
                    
                    <form action="/reservar" method="POST">
                        <div class="mb-3">
                            <label class="form-label text-white-50 small fw-bold">Nombre Completo</label>
                            <input type="text" name="nombre" class="form-control" required placeholder="Ej. Carlos Silva">
                        </div>
                        <div class="mb-3">
                            <label class="form-label text-white-50 small fw-bold">WhatsApp de Contacto</label>
                            <input type="tel" name="telefono" class="form-control" required placeholder="Ej. +56912345678">
                        </div>
                        <div class="mb-3">
                            <label class="form-label text-white-50 small fw-bold">Servicio Requerido</label>
                            <select name="servicio" class="form-select" required>
                                <option value="Corte Autor Premium">Corte de Autor Premium - \$15.000</option>
