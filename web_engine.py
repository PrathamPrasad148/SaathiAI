"""God-Level Website Engine for Saathi AI.
Integrates UI/UX Pro Max standards & 21st.dev interactive components:
- Extreme Color Palettes (Cyberpunk, Obsidian Gold, Tricolor Neon, Emerald Aurora, Tech Nebula)
- 21st.dev Spotlight Mouse-Tracking Cards
- Interactive HTML5 Particle Constellation Canvas
- Zero-dependency Web Audio API Sound Effects Synthesizer (Hover blips, click chimes, fanfare chords)
- Physics Confetti Canon Celebration
- 3D Card Tilt & Responsive Bento Grid
- Scroll-triggered reveals via IntersectionObserver
- Guaranteed automatic browser launching
"""
from __future__ import annotations

import html
import re
from pathlib import Path


def generate_independence_day_html() -> str:
    """Returns a production-ready, god-level animated Independence Day website."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>78th Independence Day 🇮🇳 | Bharat Gaurav</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;900&family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --saffron: #ff6f00;
            --saffron-glow: rgba(255, 111, 0, 0.45);
            --white: #ffffff;
            --white-glow: rgba(255, 255, 255, 0.4);
            --green: #00c853;
            --green-glow: rgba(0, 200, 83, 0.45);
            --navy: #0033aa;
            --navy-glow: rgba(0, 51, 170, 0.6);
            --bg: #04040a;
            --bg-card: rgba(18, 18, 30, 0.7);
            --border-card: rgba(255, 255, 255, 0.08);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent-rgb: 255, 111, 0;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Outfit', sans-serif;
            -webkit-font-smoothing: antialiased;
        }

        body {
            background: var(--bg);
            color: var(--text-main);
            overflow-x: hidden;
            min-height: 100vh;
            position: relative;
        }

        /* Particle Canvas */
        #particleCanvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 0;
            pointer-events: none;
        }

        /* Ambient Glow Blobs */
        .ambient-glow {
            position: fixed;
            width: 550px;
            height: 550px;
            border-radius: 50%;
            filter: blur(140px);
            opacity: 0.18;
            z-index: 0;
            pointer-events: none;
            animation: floatGlow 14s ease-in-out infinite alternate;
        }
        .glow-saffron { top: -10%; left: -10%; background: var(--saffron); }
        .glow-green { bottom: -10%; right: -10%; background: var(--green); }
        .glow-navy { top: 40%; left: 50%; transform: translate(-50%, -50%); background: var(--navy); }

        @keyframes floatGlow {
            0% { transform: scale(1) translate(0, 0); }
            100% { transform: scale(1.2) translate(40px, -30px); }
        }

        /* Content Container */
        .page-content {
            position: relative;
            z-index: 10;
        }

        /* Tricolor Top Bar */
        .tricolor-stripe {
            height: 6px;
            width: 100%;
            background: linear-gradient(90deg, #ff6f00 0%, #ff6f00 33.3%, #ffffff 33.3%, #ffffff 66.6%, #00c853 66.6%, #00c853 100%);
            box-shadow: 0 0 25px rgba(255, 111, 0, 0.5);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        /* Floating Glass Navbar */
        .navbar {
            max-width: 1100px;
            margin: 20px auto 0;
            padding: 12px 28px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: rgba(14, 14, 24, 0.65);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-card);
            border-radius: 100px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        }

        .nav-brand {
            display: flex;
            align-items: center;
            gap: 10px;
            font-family: 'Cinzel', serif;
            font-weight: 900;
            font-size: 1.25rem;
            letter-spacing: 1.5px;
            color: #fff;
        }

        .nav-brand span {
            background: linear-gradient(135deg, var(--saffron), #fff, var(--green));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .nav-links {
            display: flex;
            gap: 24px;
            align-items: center;
        }

        .nav-links a {
            color: var(--text-muted);
            text-decoration: none;
            font-size: 0.95rem;
            font-weight: 500;
            transition: color 0.2s, transform 0.2s;
        }

        .nav-links a:hover {
            color: #fff;
            transform: translateY(-1px);
        }

        .sound-toggle {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 6px 14px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-card);
            border-radius: 50px;
            font-size: 0.85rem;
            color: var(--text-muted);
            cursor: pointer;
            transition: all 0.2s;
        }
        .sound-toggle:hover {
            background: rgba(255, 255, 255, 0.1);
            color: #fff;
        }

        /* Hero Section */
        .hero {
            max-width: 1000px;
            margin: 60px auto 40px;
            text-align: center;
            padding: 0 24px;
        }

        .pill-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 22px;
            border-radius: 50px;
            background: rgba(255, 111, 0, 0.08);
            border: 1px solid rgba(255, 111, 0, 0.35);
            color: #ff9d42;
            font-weight: 600;
            font-size: 0.85rem;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 24px;
            box-shadow: 0 0 20px rgba(255, 111, 0, 0.15);
            animation: pulseGlow 2.5s infinite;
        }

        @keyframes pulseGlow {
            0%, 100% { box-shadow: 0 0 15px rgba(255, 111, 0, 0.15); }
            50% { box-shadow: 0 0 30px rgba(255, 111, 0, 0.4); transform: scale(1.02); }
        }

        .hero h1 {
            font-family: 'Cinzel', serif;
            font-size: clamp(2.8rem, 7vw, 5.2rem);
            font-weight: 900;
            line-height: 1.12;
            letter-spacing: -0.5px;
            margin-bottom: 24px;
            background: linear-gradient(135deg, #ff8800 0%, #ffffff 50%, #00d95a 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 50px rgba(255, 255, 255, 0.12);
        }

        .hero p.tagline {
            font-size: clamp(1.1rem, 2.4vw, 1.35rem);
            color: var(--text-muted);
            max-width: 720px;
            margin: 0 auto 40px;
            line-height: 1.65;
            font-weight: 400;
        }

        /* 3D Animated Ashok Chakra */
        .chakra-stage {
            position: relative;
            width: 170px;
            height: 170px;
            margin: 20px auto 45px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .chakra-aura {
            position: absolute;
            inset: -15px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(0, 80, 255, 0.35) 0%, transparent 70%);
            animation: pulseAura 3s ease-in-out infinite alternate;
        }

        @keyframes pulseAura {
            0% { transform: scale(0.9); opacity: 0.4; }
            100% { transform: scale(1.2); opacity: 0.8; }
        }

        .ashok-chakra {
            width: 100%;
            height: 100%;
            border-radius: 50%;
            border: 7px solid #1a53ff;
            background: radial-gradient(circle, #ffffff 30%, #e0e9ff 100%);
            position: relative;
            box-shadow: 0 0 45px rgba(26, 83, 255, 0.7), inset 0 0 20px rgba(0, 40, 160, 0.4);
            animation: spinChakra 20s linear infinite;
        }

        @keyframes spinChakra {
            100% { transform: rotate(360deg); }
        }

        .chakra-hub {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 22px;
            height: 22px;
            background: #1a53ff;
            border: 3px solid #ffffff;
            border-radius: 50%;
            z-index: 5;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
        }

        .spoke {
            position: absolute;
            top: 50%;
            left: 50%;
            width: 100%;
            height: 2.2px;
            background: #1a53ff;
            transform-origin: center;
        }

        /* Action Controls & Salute Station */
        .action-row {
            display: flex;
            gap: 16px;
            justify-content: center;
            flex-wrap: wrap;
            margin-bottom: 50px;
        }

        .btn-salute {
            position: relative;
            padding: 18px 42px;
            font-size: 1.15rem;
            font-weight: 700;
            color: #fff;
            background: linear-gradient(135deg, #ff6f00, #e65100);
            border: none;
            border-radius: 100px;
            cursor: pointer;
            box-shadow: 0 12px 35px rgba(255, 111, 0, 0.4);
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
            display: flex;
            align-items: center;
            gap: 10px;
            overflow: hidden;
        }

        .btn-salute:hover {
            transform: scale(1.05) translateY(-2px);
            box-shadow: 0 18px 45px rgba(255, 111, 0, 0.6);
        }

        .btn-salute:active {
            transform: scale(0.98);
        }

        .btn-anthem {
            padding: 18px 36px;
            font-size: 1.1rem;
            font-weight: 600;
            color: #fff;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-card);
            border-radius: 100px;
            cursor: pointer;
            backdrop-filter: blur(12px);
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .btn-anthem:hover {
            background: rgba(255, 255, 255, 0.12);
            border-color: rgba(255, 255, 255, 0.25);
            transform: translateY(-2px);
        }

        .salute-counter {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 0.95rem;
            color: var(--text-muted);
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border-card);
            padding: 8px 18px;
            border-radius: 50px;
            margin-top: 10px;
        }

        .salute-counter strong {
            color: var(--green);
            font-size: 1.15rem;
            font-weight: 800;
        }

        /* 21st.dev Bento Grid Section */
        .section-title {
            text-align: center;
            font-family: 'Cinzel', serif;
            font-size: 2.2rem;
            font-weight: 800;
            margin: 60px 0 15px;
            color: #fff;
        }
        .section-sub {
            text-align: center;
            color: var(--text-muted);
            max-width: 600px;
            margin: 0 auto 40px;
            font-size: 1rem;
        }

        .bento-grid {
            max-width: 1100px;
            margin: 0 auto 80px;
            padding: 0 24px;
            display: grid;
            grid-template-columns: repeat(12, 1fr);
            gap: 24px;
        }

        /* 21st.dev Spotlight Card */
        .bento-card {
            position: relative;
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 28px;
            padding: 34px;
            overflow: hidden;
            backdrop-filter: blur(14px);
            transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.3s, box-shadow 0.3s;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .bento-card::before {
            content: '';
            position: absolute;
            inset: 0;
            border-radius: inherit;
            background: radial-gradient(450px circle at var(--mouse-x, 50%) var(--mouse-y, 50%), rgba(var(--accent-rgb), 0.18), transparent 70%);
            opacity: 0;
            transition: opacity 0.4s ease;
            pointer-events: none;
            z-index: 1;
        }

        .bento-card:hover::before {
            opacity: 1;
        }

        .bento-card:hover {
            transform: translateY(-6px);
            border-color: rgba(255, 111, 0, 0.4);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
        }

        .col-8 { grid-column: span 8; }
        .col-4 { grid-column: span 4; }
        .col-6 { grid-column: span 6; }
        .col-12 { grid-column: span 12; }

        @media (max-width: 900px) {
            .col-8, .col-4, .col-6 { grid-column: span 12; }
        }

        .card-tag {
            display: inline-block;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            padding: 5px 12px;
            border-radius: 50px;
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--saffron);
            margin-bottom: 18px;
            width: fit-content;
        }

        .card-tag.green { color: var(--green); border-color: rgba(0, 200, 83, 0.3); }
        .card-tag.navy { color: #60a5fa; border-color: rgba(96, 165, 250, 0.3); }

        .bento-card h3 {
            font-size: 1.55rem;
            font-weight: 800;
            margin-bottom: 12px;
            color: #fff;
            position: relative;
            z-index: 2;
        }

        .bento-card p {
            color: var(--text-muted);
            line-height: 1.6;
            font-size: 0.98rem;
            position: relative;
            z-index: 2;
        }

        .stat-highlight {
            font-size: 2.6rem;
            font-weight: 900;
            font-family: 'Cinzel', serif;
            color: #fff;
            margin-top: 24px;
            position: relative;
            z-index: 2;
        }
        .stat-highlight span {
            background: linear-gradient(135deg, var(--saffron), #fff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Freedom Quotes Carousel */
        .quote-box {
            max-width: 900px;
            margin: 0 auto 80px;
            padding: 40px;
            background: rgba(255, 255, 255, 0.025);
            border: 1px solid var(--border-card);
            border-radius: 28px;
            text-align: center;
            position: relative;
        }

        .quote-icon {
            font-size: 2.8rem;
            color: var(--saffron);
            margin-bottom: 15px;
            opacity: 0.8;
        }

        .quote-text {
            font-size: 1.4rem;
            font-style: italic;
            font-weight: 500;
            line-height: 1.6;
            color: #e2e8f0;
            margin-bottom: 18px;
            min-height: 70px;
        }

        .quote-author {
            font-size: 1rem;
            font-weight: 700;
            color: var(--saffron);
            letter-spacing: 1px;
        }

        /* Footer */
        footer {
            border-top: 1px solid var(--border-card);
            padding: 45px 24px;
            text-align: center;
            color: var(--text-muted);
            font-size: 0.95rem;
            background: rgba(4, 4, 10, 0.8);
        }

        footer strong {
            color: #fff;
        }

        .tricolor-text {
            background: linear-gradient(90deg, #ff6f00, #ffffff, #00c853);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }
    </style>
</head>
<body>
    <canvas id="particleCanvas"></canvas>
    <div class="ambient-glow glow-saffron"></div>
    <div class="ambient-glow glow-green"></div>
    <div class="ambient-glow glow-navy"></div>

    <div class="tricolor-stripe"></div>

    <div class="page-content">
        <!-- Floating Navbar -->
        <nav class="navbar">
            <div class="nav-brand">
                <span>BHARAT</span> GAURAV 🇮🇳
            </div>
            <div class="nav-links">
                <a href="#achievements" onclick="AudioFX.playClick()">Pillars</a>
                <a href="#quotes" onclick="AudioFX.playClick()">Freedom Voice</a>
                <button class="sound-toggle" id="soundBtn" onclick="toggleSound()">
                    🔊 Sound ON
                </button>
            </div>
        </nav>

        <!-- Hero -->
        <section class="hero">
            <div class="pill-badge">
                ★ AZADI KA AMRIT KAAL ★ 1947–2026
            </div>
            <h1>HAPPY 78th INDEPENDENCE DAY</h1>
            <p class="tagline">
                Saluting the immortal valor of our freedom heroes, celebrating our vibrant democracy, and marching proudly towards a global superpower future.
            </p>

            <!-- 3D Ashok Chakra -->
            <div class="chakra-stage">
                <div class="chakra-aura"></div>
                <div class="ashok-chakra" id="chakra">
                    <div class="chakra-hub"></div>
                </div>
            </div>

            <!-- Action Controls -->
            <div class="action-row">
                <button class="btn-salute" onclick="saluteTiranga()">
                    <span>🫡 Salute the Tiranga</span>
                </button>
                <button class="btn-anthem" onclick="playVandeMataramChimes()">
                    <span>🎵 Play Victory Fanfare</span>
                </button>
            </div>

            <div>
                <div class="salute-counter">
                    National Salutes Recorded: <strong id="saluteNum">1,947,078</strong>
                </div>
            </div>
        </section>

        <!-- 21st.dev Bento Grid -->
        <section id="achievements">
            <h2 class="section-title">PILLARS OF MODERN BHARAT</h2>
            <p class="section-sub">From our rich heritage to boundless space exploration — India shines on the global stage.</p>

            <div class="bento-grid">
                <div class="bento-card col-8 spotlight-card">
                    <div>
                        <span class="card-tag">Space & Innovation</span>
                        <h3>Chandrayaan & Beyond</h3>
                        <p>The first nation to conquer the Moon's South Pole. Pioneering affordable interplanetary exploration with Gaganyaan, Aditya-L1, and the world's most trusted satellite launch systems.</p>
                    </div>
                    <div class="stat-highlight">
                        <span>#1 Lunar South Pole</span>
                    </div>
                </div>

                <div class="bento-card col-4 spotlight-card">
                    <div>
                        <span class="card-tag green">Fintech Revolution</span>
                        <h3>Digital Superpower</h3>
                        <p>UPI processes over 13 Billion instant real-time transactions every month — transforming the everyday life of 1.4 Billion citizens seamlessly.</p>
                    </div>
                    <div class="stat-highlight">
                        <span>100B+ <span style="font-size:1.1rem; color:var(--green)">Annually</span></span>
                    </div>
                </div>

                <div class="bento-card col-4 spotlight-card">
                    <div>
                        <span class="card-tag navy">Armed Forces</span>
                        <h3>Indomitable Valor</h3>
                        <p>Guardians of our skies, seas, and borders. Unwavering dedication protecting 3.28 million square kilometers of sovereign territory with indigenous defence pride.</p>
                    </div>
                    <div class="stat-highlight">
                        <span style="font-size:1.6rem">1.4M+ Bravehearts</span>
                    </div>
                </div>

                <div class="bento-card col-8 spotlight-card">
                    <div>
                        <span class="card-tag">Culture & Unity</span>
                        <h3>5,000 Years of Timeless Soul</h3>
                        <p>The birthplace of Yoga, Ayurveda, Zero, and profound philosophy. A tapestry of 22 official languages, thousands of festivals, and infinite harmony under one tricolor flag.</p>
                    </div>
                    <div class="stat-highlight">
                        <span>Unity in Diversity</span>
                    </div>
                </div>
            </div>
        </section>

        <!-- Quotes Section -->
        <section id="quotes" class="hero" style="margin-top:20px;">
            <div class="quote-box">
                <div class="quote-icon">❝</div>
                <div class="quote-text" id="quoteDisplay">
                    "Swaraj is my birthright, and I shall have it!"
                </div>
                <div class="quote-author" id="authorDisplay">— Bal Gangadhar Tilak</div>
            </div>
        </section>

        <!-- Footer -->
        <footer>
            Crafted with passion by <strong>Saathi AI</strong> • <span class="tricolor-text">VANDE MATARAM • JAI HIND! 🇮🇳</span>
        </footer>
    </div>

    <!-- Scripts: 21st.dev Spotlight, Audio Synthesizer, Confetti & Canvas -->
    <script>
        // 1. Build Ashok Chakra 24 Spokes
        const chakra = document.getElementById('chakra');
        for (let i = 0; i < 12; i++) {
            const spoke = document.createElement('div');
            spoke.className = 'spoke';
            spoke.style.transform = `translate(-50%, -50%) rotate(${i * 15}deg)`;
            chakra.appendChild(spoke);
        }

        // 2. Web Audio API Sound Synthesizer (Zero external dependencies)
        const AudioFX = {
            ctx: null,
            enabled: true,
            init() {
                if (!this.ctx) {
                    const AudioContext = window.AudioContext || window.webkitAudioContext;
                    if (AudioContext) this.ctx = new AudioContext();
                }
            },
            playHover() {
                if (!this.enabled) return;
                this.init();
                if (!this.ctx) return;
                const osc = this.ctx.createOscillator();
                const gain = this.ctx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(480, this.ctx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(720, this.ctx.currentTime + 0.05);
                gain.gain.setValueAtTime(0.04, this.ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.05);
                osc.connect(gain); gain.connect(this.ctx.destination);
                osc.start(); osc.stop(this.ctx.currentTime + 0.05);
            },
            playClick() {
                if (!this.enabled) return;
                this.init();
                if (!this.ctx) return;
                const osc = this.ctx.createOscillator();
                const gain = this.ctx.createGain();
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(340, this.ctx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(120, this.ctx.currentTime + 0.08);
                gain.gain.setValueAtTime(0.12, this.ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.08);
                osc.connect(gain); gain.connect(this.ctx.destination);
                osc.start(); osc.stop(this.ctx.currentTime + 0.08);
            },
            playFanfare() {
                if (!this.enabled) return;
                this.init();
                if (!this.ctx) return;
                // C5, E5, G5, C6 triumphant chord
                const notes = [523.25, 659.25, 783.99, 1046.50];
                notes.forEach((freq, idx) => {
                    const osc = this.ctx.createOscillator();
                    const gain = this.ctx.createGain();
                    osc.type = 'sine';
                    const startTime = this.ctx.currentTime + idx * 0.08;
                    osc.frequency.setValueAtTime(freq, startTime);
                    gain.gain.setValueAtTime(0.12, startTime);
                    gain.gain.exponentialRampToValueAtTime(0.001, startTime + 0.5);
                    osc.connect(gain); gain.connect(this.ctx.destination);
                    osc.start(startTime); osc.stop(startTime + 0.55);
                });
            }
        };

        function toggleSound() {
            AudioFX.enabled = !AudioFX.enabled;
            const btn = document.getElementById('soundBtn');
            btn.innerHTML = AudioFX.enabled ? "🔊 Sound ON" : "🔇 Sound OFF";
            if (AudioFX.enabled) AudioFX.playClick();
        }

        // 3. 21st.dev Spotlight Mouse Tracking Effect
        document.querySelectorAll('.spotlight-card').forEach(card => {
            card.addEventListener('mousemove', e => {
                const rect = card.getBoundingClientRect();
                card.style.setProperty('--mouse-x', `${e.clientX - rect.left}px`);
                card.style.setProperty('--mouse-y', `${e.clientY - rect.top}px`);
            });
            card.addEventListener('mouseenter', () => AudioFX.playHover());
        });

        // 4. Interactive Salute Counter & Fanfare
        let count = 1947078;
        function saluteTiranga() {
            count++;
            document.getElementById('saluteNum').innerText = count.toLocaleString('en-IN');
            AudioFX.playFanfare();
            launchTricolorConfetti();
        }

        function playVandeMataramChimes() {
            AudioFX.playFanfare();
            launchTricolorConfetti();
        }

        // 5. Physics Confetti Engine (Saffron, White, Green, Navy)
        function launchTricolorConfetti() {
            const colors = ['#ff6f00', '#ffffff', '#00c853', '#1a53ff', '#ffa726'];
            for (let i = 0; i < 90; i++) {
                const conf = document.createElement('div');
                conf.style.position = 'fixed';
                conf.style.left = Math.random() * window.innerWidth + 'px';
                conf.style.top = '-15px';
                const size = Math.random() * 9 + 6;
                conf.style.width = size + 'px';
                conf.style.height = (size * (Math.random() > 0.5 ? 1 : 1.6)) + 'px';
                conf.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                conf.style.borderRadius = Math.random() > 0.4 ? '2px' : '50%';
                conf.style.zIndex = '9999';
                conf.style.pointerEvents = 'none';
                conf.style.boxShadow = '0 0 10px rgba(255,255,255,0.4)';
                document.body.appendChild(conf);

                const drift = (Math.random() - 0.5) * 160;
                const duration = Math.random() * 2000 + 1800;
                const rotate = Math.random() * 720 - 360;

                conf.animate([
                    { transform: `translate(0, 0) rotate(0deg)`, opacity: 1 },
                    { transform: `translate(${drift}px, ${window.innerHeight + 30}px) rotate(${rotate}deg)`, opacity: 0 }
                ], {
                    duration: duration,
                    easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'
                }).onfinish = () => conf.remove();
            }
        }

        // 6. Freedom Quotes Rotator
        const quotes = [
            { text: '"Swaraj is my birthright, and I shall have it!"', author: '— Bal Gangadhar Tilak' },
            { text: '"Give me blood, and I shall give you freedom!"', author: '— Netaji Subhash Chandra Bose' },
            { text: '"Inquilab Zindabad!"', author: '— Bhagat Singh' },
            { text: '"A nation\'s culture resides in the hearts and in the soul of its people."', author: '— Mahatma Gandhi' },
            { text: '"At the stroke of the midnight hour, when the world sleeps, India will awake to life and freedom."', author: '— Jawaharlal Nehru' },
            { text: '"Dream, dream, dream. Dreams transform into thoughts and thoughts result in action."', author: '— Dr. A.P.J. Abdul Kalam' }
        ];
        let qIdx = 0;
        setInterval(() => {
            qIdx = (qIdx + 1) % quotes.length;
            const qEl = document.getElementById('quoteDisplay');
            const aEl = document.getElementById('authorDisplay');
            qEl.style.opacity = '0';
            aEl.style.opacity = '0';
            setTimeout(() => {
                qEl.innerText = quotes[qIdx].text;
                aEl.innerText = quotes[qIdx].author;
                qEl.style.transition = 'opacity 0.6s';
                aEl.style.transition = 'opacity 0.6s';
                qEl.style.opacity = '1';
                aEl.style.opacity = '1';
            }, 400);
        }, 5000);

        // 7. Interactive Starlight Particle Canvas
        const canvas = document.getElementById('particleCanvas');
        const ctx = canvas.getContext('2d');
        let width, height;
        let particles = [];

        function resize() {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        }
        window.addEventListener('resize', resize);
        resize();

        for (let i = 0; i < 65; i++) {
            particles.push({
                x: Math.random() * width,
                y: Math.random() * height,
                vx: (Math.random() - 0.5) * 0.4,
                vy: (Math.random() - 0.5) * 0.4,
                radius: Math.random() * 1.8 + 0.6,
                color: Math.random() > 0.6 ? '#ff9d42' : (Math.random() > 0.5 ? '#00e676' : '#60a5fa')
            });
        }

        function drawParticles() {
            ctx.clearRect(0, 0, width, height);
            for (let i = 0; i < particles.length; i++) {
                const p = particles[i];
                p.x += p.vx;
                p.y += p.vy;
                if (p.x < 0) p.x = width;
                if (p.x > width) p.x = 0;
                if (p.y < 0) p.y = height;
                if (p.y > height) p.y = 0;

                ctx.beginPath();
                ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                ctx.fillStyle = p.color;
                ctx.shadowBlur = 8;
                ctx.shadowColor = p.color;
                ctx.fill();
                ctx.shadowBlur = 0;

                for (let j = i + 1; j < particles.length; j++) {
                    const p2 = particles[j];
                    const dist = Math.hypot(p.x - p2.x, p.y - p2.y);
                    if (dist < 110) {
                        ctx.beginPath();
                        ctx.strokeStyle = `rgba(255, 255, 255, ${0.15 * (1 - dist / 110)})`;
                        ctx.lineWidth = 0.6;
                        ctx.moveTo(p.x, p.y);
                        ctx.lineTo(p2.x, p2.y);
                        ctx.stroke();
                    }
                }
            }
            requestAnimationFrame(drawParticles);
        }
        drawParticles();
    </script>
</body>
</html>"""


import urllib.request
import urllib.parse
import json


def fetch_web_knowledge(query: str) -> dict[str, str]:
    """Fetches verified facts, summaries, and descriptions from the web for the topic."""
    clean = re.sub(r'[^a-zA-Z0-9\s]', '', query).strip()
    words = clean.split()
    candidates = [clean]
    
    # Strip common filler/context suffixes (e.g., 'Elden Ring Game' -> 'Elden Ring')
    if len(words) > 1:
        if words[-1].lower() in {"game", "website", "site", "app", "store", "product", "system", "company", "project"}:
            candidates.append(' '.join(words[:-1]))
        if len(words) >= 2:
            candidates.append(' '.join(words[:2]))
        candidates.append(words[0])

    for q in candidates:
        if not q or len(q) < 3:
            continue
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(q)}"
            req = urllib.request.Request(url, headers={"User-Agent": "SaathiAI/2.0 (Windows)"})
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                extract = data.get("extract", "")
                if extract and len(extract) > 40:
                    return {
                        "title": data.get("title", clean).strip(),
                        "desc": data.get("description", "World-Class Excellence & Innovation").strip(),
                        "extract": extract.strip()
                    }
        except Exception:
            pass

    return {
        "title": clean.title(),
        "desc": "Premier Innovation & Bespoke Experience",
        "extract": f"{clean.title()} stands at the intersection of avant-garde design, uncompromising performance, and transformative modern vision."
    }


def _has_keyword(text: str, keywords: tuple[str, ...]) -> bool:
    for k in keywords:
        if " " in k:
            if k in text:
                return True
        else:
            if re.search(r'\b' + re.escape(k) + r'\b', text):
                return True
    return False


def detect_archetype(topic: str, knowledge: dict[str, str]) -> str:
    """Classifies the topic into the ideal UI/UX Pro Max archetype."""
    combined = (topic + " " + knowledge.get("desc", "") + " " + knowledge.get("extract", "")).lower()
    
    # High-specificity checks first
    if _has_keyword(combined, ("game", "games", "gaming", "esport", "esports", "cyberpunk", "arcade", "rpg", "streamer", "gamer", "playstation", "xbox", "fps", "elden ring", "nintendo", "steam")):
        return "gaming"
    if _has_keyword(combined, ("car", "cars", "supercar", "hypercar", "racing", "vehicle", "vehicles", "ferrari", "lamborghini", "porsche", "bmw", "audi", "mercedes", "tesla", "motors", "automotive", "formula 1", "f1")):
        return "automotive"
    if _has_keyword(combined, ("fitness", "gym", "workout", "health", "medical", "clinic", "doctor", "yoga", "hospital", "wellness", "dental", "pharma", "fitbit", "meditation", "nutrition")):
        return "wellness"
    if _has_keyword(combined, ("coffee", "cafe", "restaurant", "bakery", "food", "dining", "wine", "pizza", "burger", "roastery", "tea", "bistro", "culinary", "cocktail")):
        return "culinary"
    if _has_keyword(combined, ("portfolio", "resume", "cv", "developer portfolio", "designer portfolio", "personal site")):
        return "portfolio"
    if _has_keyword(combined, ("shoe", "shoes", "sneaker", "sneakers", "clothing", "clothes", "fashion", "watch", "watches", "apparel", "store", "shop", "shopping", "retail", "jewelry", "bag", "handbag", "merchandise")):
        return "ecommerce"
    if _has_keyword(combined, ("ai", "artificial intelligence", "software", "cloud", "dev", "code", "bot", "database", "cyber", "api", "crypto", "blockchain", "saas", "tech", "technology", "gpt", "model")):
        return "tech_saas"
    return "general_showcase"


def _split_sentences(text: str) -> list[str]:
    """Splits extract into clean sentence bullets."""
    sentences = [s.strip() for s in re.split(r'\.\s+', text) if len(s.strip()) > 15]
    return sentences if sentences else [text]


def generate_custom_god_level_html(topic: str) -> str:
    """Fetches live web data, selects the best-suited UI/UX archetype, and generates a bespoke masterpiece."""
    clean_topic = topic.strip()
    knowledge = fetch_web_knowledge(clean_topic)
    archetype = detect_archetype(clean_topic, knowledge)

    title = html.escape(knowledge.get("title", clean_topic).title())
    desc = html.escape(knowledge.get("desc", "Premier Experience"))
    extract = html.escape(knowledge.get("extract", ""))
    sentences = _split_sentences(extract)
    p1 = sentences[0] if len(sentences) > 0 else extract
    p2 = sentences[1] if len(sentences) > 1 else "Engineered with precision, passion, and uncompromising quality."
    p3 = sentences[2] if len(sentences) > 2 else "Setting the benchmark for modern digital sophistication."
    p4 = sentences[3] if len(sentences) > 3 else "Pioneering new standards with global impact and distinction."

    # 1. Automotive
    if archetype == "automotive":
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | High-Performance Aerodynamics</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&family=Outfit:wght@400;600;800;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --primary: #dc2626; --accent: #f59e0b; --bg: #09090b; --card: rgba(24, 24, 27, 0.85); --border: rgba(255,255,255,0.08); --accent-rgb: 220, 38, 38; }}
        * {{ margin:0; padding:0; box-sizing:border-box; font-family:'Outfit',sans-serif; }}
        body {{ background:var(--bg); color:#fff; overflow-x:hidden; min-height:100vh; position:relative; }}
        #canvas {{ position:fixed; inset:0; pointer-events:none; z-index:0; }}
        .nav {{ position:sticky; top:18px; max-width:1100px; margin:0 auto; padding:14px 28px; display:flex; justify-content:space-between; align-items:center; background:rgba(18,18,24,0.7); backdrop-filter:blur(16px); border:1px solid var(--border); border-radius:100px; z-index:100; }}
        .brand {{ font-family:'Cinzel',serif; font-size:1.35rem; font-weight:900; letter-spacing:1px; color:#fff; display:flex; align-items:center; gap:8px; }}
        .brand-dot {{ width:10px; height:10px; border-radius:50%; background:var(--primary); box-shadow:0 0 12px var(--primary); }}
        .hero {{ max-width:1050px; margin:70px auto 40px; text-align:center; padding:0 24px; position:relative; z-index:10; }}
        .badge {{ display:inline-block; padding:8px 22px; border-radius:50px; background:rgba(220,38,38,0.12); border:1px solid rgba(220,38,38,0.4); color:#f87171; font-size:0.85rem; font-weight:800; letter-spacing:2px; text-transform:uppercase; margin-bottom:20px; }}
        h1 {{ font-family:'Cinzel',serif; font-size:clamp(2.8rem,7vw,5.5rem); font-weight:900; line-height:1.08; background:linear-gradient(135deg, #fff 40%, var(--primary) 80%, var(--accent) 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin-bottom:22px; }}
        p.tagline {{ font-size:1.25rem; color:#a1a1aa; max-width:760px; margin:0 auto 35px; line-height:1.6; }}
        
        /* Telemetry Dashboard */
        .telemetry-grid {{ max-width:1100px; margin:30px auto 60px; padding:0 24px; display:grid; grid-template-columns:repeat(auto-fit, minmax(240px,1fr)); gap:20px; position:relative; z-index:10; }}
        .telemetry-card {{ background:var(--card); border:1px solid var(--border); border-radius:24px; padding:30px; backdrop-filter:blur(14px); text-align:center; position:relative; overflow:hidden; transition:transform 0.3s; }}
        .telemetry-card:hover {{ transform:translateY(-5px); border-color:var(--primary); }}
        .t-num {{ font-size:3rem; font-weight:900; font-family:'Cinzel',serif; color:#fff; margin-bottom:6px; }}
        .t-num span {{ color:var(--primary); font-size:1.6rem; }}
        .t-lbl {{ font-size:0.85rem; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; color:#71717a; }}
        
        /* Customizer Swatches */
        .customizer {{ max-width:700px; margin:0 auto 50px; background:rgba(255,255,255,0.03); border:1px solid var(--border); border-radius:30px; padding:25px; text-align:center; position:relative; z-index:10; }}
        .swatch-row {{ display:flex; justify-content:center; gap:16px; margin:15px 0; }}
        .swatch {{ width:38px; height:38px; border-radius:50%; cursor:pointer; border:3px solid transparent; transition:transform 0.2s; }}
        .swatch:hover, .swatch.active {{ transform:scale(1.2); border-color:#fff; }}
        
        .btn {{ padding:16px 40px; background:linear-gradient(135deg, var(--primary), #991b1b); border:none; border-radius:100px; color:#fff; font-size:1.1rem; font-weight:800; cursor:pointer; box-shadow:0 10px 30px rgba(220,38,38,0.5); transition:all 0.3s; }}
        .btn:hover {{ transform:scale(1.05); box-shadow:0 15px 40px rgba(220,38,38,0.7); }}
        
        /* Bento Information */
        .bento {{ max-width:1100px; margin:0 auto 80px; padding:0 24px; display:grid; grid-template-columns:repeat(12, 1fr); gap:20px; position:relative; z-index:10; }}
        .spotlight-card {{ position:relative; background:var(--card); border:1px solid var(--border); border-radius:24px; padding:32px; overflow:hidden; backdrop-filter:blur(14px); }}
        .spotlight-card::before {{ content:''; position:absolute; inset:0; background:radial-gradient(400px circle at var(--mouse-x,50%) var(--mouse-y,50%), rgba(220,38,38,0.2), transparent 70%); opacity:0; transition:opacity 0.3s; pointer-events:none; }}
        .spotlight-card:hover::before {{ opacity:1; }}
        .c-8 {{ grid-column:span 8; }} .c-4 {{ grid-column:span 4; }}
        @media(max-width:850px){{ .c-8, .c-4 {{ grid-column:span 12; }} }}
        footer {{ text-align:center; padding:40px; border-top:1px solid var(--border); color:#71717a; position:relative; z-index:10; }}
    </style>
</head>
<body>
    <canvas id="canvas"></canvas>
    <nav class="nav">
        <div class="brand"><div class="brand-dot"></div><span>{title.upper()}</span></div>
        <div style="display:flex;gap:20px;align-items:center;">
            <button onclick="AudioFX.playFanfare()" style="background:none;border:none;color:#a1a1aa;cursor:pointer;font-weight:600;">Engine Sound</button>
            <button class="btn" style="padding:10px 24px;font-size:0.95rem;" onclick="celebrate()">Test Drive</button>
        </div>
    </nav>
    <section class="hero">
        <div class="badge">🏎️ {desc.upper()}</div>
        <h1>{title}</h1>
        <p class="tagline">{p1}</p>
        <button class="btn" onclick="celebrate()">🔥 Unleash Pure Power</button>
    </section>
    
    <div class="telemetry-grid">
        <div class="telemetry-card"><div class="t-num">2.4<span>s</span></div><div class="t-lbl">0–100 km/h Sprint</div></div>
        <div class="telemetry-card"><div class="t-num">340<span>+</span></div><div class="t-lbl">Top Speed (km/h)</div></div>
        <div class="telemetry-card"><div class="t-num">850<span>HP</span></div><div class="t-lbl">Twin-Turbo V8 Hybrid</div></div>
        <div class="telemetry-card"><div class="t-num">9,000<span>RPM</span></div><div class="t-lbl">Redline Symphony</div></div>
    </div>

    <div class="customizer">
        <div style="font-weight:800;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">Live Livery Customizer</div>
        <div class="swatch-row">
            <div class="swatch active" style="background:#dc2626;" onclick="setTheme('#dc2626')"></div>
            <div class="swatch" style="background:#f59e0b;" onclick="setTheme('#f59e0b')"></div>
            <div class="swatch" style="background:#06b6d4;" onclick="setTheme('#06b6d4')"></div>
            <div class="swatch" style="background:#ffffff;" onclick="setTheme('#ffffff')"></div>
            <div class="swatch" style="background:#18181b;border:1px solid #52525b;" onclick="setTheme('#e11d48')"></div>
        </div>
        <div id="liveryLbl" style="color:#a1a1aa;font-size:0.9rem;">Current Spec: Rosso Corsa Competition</div>
    </div>

    <div class="bento">
        <div class="spotlight-card c-8">
            <h3 style="font-size:1.6rem;margin-bottom:12px;color:#fff;">Aerodynamic Mastery & Racing DNA</h3>
            <p style="color:#a1a1aa;line-height:1.6;font-size:1.05rem;">{p2}. Derived directly from elite championship engineering with active ground-effect downforce and carbon-ceramic telemetry.</p>
        </div>
        <div class="spotlight-card c-4">
            <h3 style="font-size:1.4rem;margin-bottom:10px;color:#fff;">Carbon Architecture</h3>
            <p style="color:#a1a1aa;line-height:1.6;">{p3}. Monocoque carbon chassis delivering unmatched torsional rigidity and featherweight precision.</p>
        </div>
    </div>
    <footer>Crafted by <strong>Saathi AI</strong> • Live Knowledge Fetched for {title} • 21st.dev Engine</footer>

    <script>
        const AudioFX = {{
            ctx: null,
            init() {{ if(!this.ctx) this.ctx = new (window.AudioContext||window.webkitAudioContext)(); }},
            playClick() {{
                this.init(); if(!this.ctx) return;
                const o=this.ctx.createOscillator(), g=this.ctx.createGain();
                o.type='sawtooth'; o.frequency.setValueAtTime(200, this.ctx.currentTime);
                o.frequency.exponentialRampToValueAtTime(60, this.ctx.currentTime+0.12);
                g.gain.setValueAtTime(0.15, this.ctx.currentTime); g.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime+0.12);
                o.connect(g); g.connect(this.ctx.destination); o.start(); o.stop(this.ctx.currentTime+0.12);
            }},
            playFanfare() {{
                this.init(); if(!this.ctx) return;
                const o=this.ctx.createOscillator(), g=this.ctx.createGain();
                o.type='sawtooth'; o.frequency.setValueAtTime(120, this.ctx.currentTime);
                o.frequency.exponentialRampToValueAtTime(450, this.ctx.currentTime+0.4);
                g.gain.setValueAtTime(0.2, this.ctx.currentTime); g.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime+0.5);
                o.connect(g); g.connect(this.ctx.destination); o.start(); o.stop(this.ctx.currentTime+0.5);
            }}
        }};
        document.querySelectorAll('.spotlight-card, .telemetry-card').forEach(c=>{{
            c.addEventListener('mousemove', e=>{{
                const r=c.getBoundingClientRect();
                c.style.setProperty('--mouse-x', `${{e.clientX-r.left}}px`);
                c.style.setProperty('--mouse-y', `${{e.clientY-r.top}}px`);
            }});
        }});
        function setTheme(c) {{
            document.documentElement.style.setProperty('--primary', c);
            AudioFX.playClick();
        }}
        function celebrate() {{
            AudioFX.playFanfare();
            for(let i=0;i<70;i++){{
                const d=document.createElement('div');
                d.style.position='fixed'; d.style.left=Math.random()*window.innerWidth+'px'; d.style.top='-10px';
                d.style.width=(Math.random()*10+5)+'px'; d.style.height=(Math.random()*10+5)+'px';
                d.style.background=['#dc2626','#f59e0b','#fff','#ef4444'][Math.floor(Math.random()*4)];
                d.style.zIndex='9999'; d.style.pointerEvents='none';
                document.body.appendChild(d);
                d.animate([{{transform:'translate(0,0)'}}, {{transform:`translate(${{(Math.random()-0.5)*150}}px, ${{window.innerHeight+20}}px) rotate(${{Math.random()*360}}deg)`}}], {{duration:2000+Math.random()*1000}}).onfinish=()=>d.remove();
            }}
        }}
        const cv=document.getElementById('canvas'), cx=cv.getContext('2d');
        let w=cv.width=window.innerWidth, h=cv.height=window.innerHeight;
        window.onresize=()=>{{ w=cv.width=window.innerWidth; h=cv.height=window.innerHeight; }};
        const pts=[]; for(let i=0;i<45;i++) pts.push({{x:Math.random()*w,y:Math.random()*h,vx:(Math.random()-0.5)*0.5,vy:(Math.random()-0.5)*0.5}});
        function loop(){{
            cx.clearRect(0,0,w,h);
            pts.forEach(p=>{{
                p.x+=p.vx; p.y+=p.vy; if(p.x<0)p.x=w; if(p.x>w)p.x=0; if(p.y<0)p.y=h; if(p.y>h)p.y=0;
                cx.beginPath(); cx.arc(p.x,p.y,1.5,0,Math.PI*2); cx.fillStyle='rgba(220,38,38,0.4)'; cx.fill();
            }});
            requestAnimationFrame(loop);
        }}
        loop();
    </script>
</body>
</html>"""

    # 2. Culinary / Food / Coffee / Restaurant
    if archetype == "culinary":
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Artisan Taste & Roastery</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;800&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{ --primary: #d97706; --caramel: #f59e0b; --bg: #100a06; --card: rgba(28, 18, 12, 0.85); --border: rgba(217, 119, 6, 0.2); --accent-rgb: 217, 119, 6; }}
        * {{ margin:0; padding:0; box-sizing:border-box; font-family:'Plus Jakarta Sans',sans-serif; }}
        body {{ background:var(--bg); color:#fef3c7; overflow-x:hidden; min-height:100vh; position:relative; }}
        .nav {{ position:sticky; top:18px; max-width:1100px; margin:0 auto; padding:14px 30px; display:flex; justify-content:space-between; align-items:center; background:rgba(20,12,8,0.8); backdrop-filter:blur(16px); border:1px solid var(--border); border-radius:100px; z-index:100; }}
        .brand {{ font-family:'Cinzel',serif; font-size:1.3rem; font-weight:800; color:#fef3c7; }}
        .hero {{ max-width:960px; margin:70px auto 40px; text-align:center; padding:0 24px; position:relative; z-index:10; }}
        .badge {{ display:inline-block; padding:8px 22px; border-radius:50px; background:rgba(217,119,6,0.12); border:1px solid var(--border); color:var(--caramel); font-size:0.85rem; font-weight:800; letter-spacing:2px; text-transform:uppercase; margin-bottom:20px; }}
        h1 {{ font-family:'Cinzel',serif; font-size:clamp(2.8rem,7vw,5.2rem); font-weight:800; color:#fff; margin-bottom:20px; background:linear-gradient(135deg, #fff 30%, var(--caramel) 80%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }}
        p.tagline {{ font-size:1.2rem; color:#d5c5b5; max-width:720px; margin:0 auto 35px; line-height:1.65; }}
        .btn {{ padding:16px 38px; background:linear-gradient(135deg, #d97706, #b45309); border:none; border-radius:100px; color:#fff; font-size:1.05rem; font-weight:700; cursor:pointer; box-shadow:0 10px 30px rgba(217,119,6,0.4); transition:all 0.3s; }}
        .btn:hover {{ transform:scale(1.05); box-shadow:0 15px 40px rgba(217,119,6,0.6); }}
        
        /* Menu Bento Grid */
        .menu-grid {{ max-width:1100px; margin:40px auto 80px; padding:0 24px; display:grid; grid-template-columns:repeat(auto-fit, minmax(300px,1fr)); gap:24px; position:relative; z-index:10; }}
        .menu-card {{ background:var(--card); border:1px solid var(--border); border-radius:24px; padding:30px; backdrop-filter:blur(14px); transition:transform 0.3s, border-color 0.3s; position:relative; overflow:hidden; }}
        .menu-card:hover {{ transform:translateY(-5px); border-color:var(--caramel); }}
        .price {{ float:right; font-weight:800; color:var(--caramel); font-size:1.2rem; }}
        .item-title {{ font-size:1.35rem; font-weight:800; margin-bottom:8px; color:#fff; }}
        .item-desc {{ color:#bfae9e; font-size:0.95rem; line-height:1.5; margin-bottom:18px; }}
        .tags {{ display:flex; gap:8px; }}
        .tag {{ font-size:0.75rem; font-weight:700; padding:4px 10px; border-radius:50px; background:rgba(217,119,6,0.15); color:var(--caramel); border:1px solid rgba(217,119,6,0.3); }}
        footer {{ text-align:center; padding:40px; border-top:1px solid var(--border); color:#8d7968; position:relative; z-index:10; }}
    </style>
</head>
<body>
    <nav class="nav">
        <div class="brand">☕ {title.upper()}</div>
        <button class="btn" style="padding:10px 24px;font-size:0.95rem;" onclick="bookTable()">Reserve Table</button>
    </nav>
    <section class="hero">
        <div class="badge">Artisan Gastronomy • {desc}</div>
        <h1>{title}</h1>
        <p class="tagline">{p1}</p>
        <button class="btn" onclick="bookTable()">✨ Reserve an Experience</button>
    </section>
    
    <div class="menu-grid">
        <div class="menu-card">
            <span class="price">$14.50</span>
            <div class="item-title">Signature Reserve Roast</div>
            <p class="item-desc">{p2}</p>
            <div class="tags"><span class="tag">Handcrafted</span><span class="tag">Single-Origin</span></div>
        </div>
        <div class="menu-card">
            <span class="price">$18.00</span>
            <div class="item-title">Chef's Heritage Tasting</div>
            <p class="item-desc">{p3}</p>
            <div class="tags"><span class="tag">Artisan</span><span class="tag">Fresh Daily</span></div>
        </div>
        <div class="menu-card">
            <span class="price">$12.00</span>
            <div class="item-title">Botanical Velvet Elixir</div>
            <p class="item-desc">{p4}</p>
            <div class="tags"><span class="tag">Aromatic</span><span class="tag">Award-Winning</span></div>
        </div>
    </div>
    <footer>Handcrafted with passion by <strong>Saathi AI</strong> • Live Knowledge for {title}</footer>

    <script>
        function bookTable() {{
            alert("Table reserved at {title}! Confirmation sent to your device. ☕✨");
            celebrate();
        }}
        function celebrate() {{
            for(let i=0;i<60;i++){{
                const d=document.createElement('div');
                d.style.position='fixed'; d.style.left=Math.random()*window.innerWidth+'px'; d.style.top='-10px';
                d.style.width='8px'; d.style.height='8px'; d.style.borderRadius='50%';
                d.style.background=['#d97706','#f59e0b','#fff','#78350f'][Math.floor(Math.random()*4)];
                d.style.zIndex='9999'; d.style.pointerEvents='none';
                document.body.appendChild(d);
                d.animate([{{transform:'translate(0,0)'}}, {{transform:`translate(${{(Math.random()-0.5)*120}}px, ${{window.innerHeight+20}}px)`}}], {{duration:2000}}).onfinish=()=>d.remove();
            }}
        }}
    </script>
</body>
</html>"""

    # 3. E-Commerce / Products / Shoes / Fashion
    if archetype == "ecommerce":
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Official Premium Collection</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --primary: #2563eb; --accent: #f97316; --bg: #090b14; --card: rgba(18, 22, 38, 0.85); --border: rgba(255,255,255,0.08); }}
        * {{ margin:0; padding:0; box-sizing:border-box; font-family:'Plus Jakarta Sans',sans-serif; }}
        body {{ background:var(--bg); color:#fff; min-height:100vh; overflow-x:hidden; position:relative; }}
        .nav {{ position:sticky; top:16px; max-width:1100px; margin:0 auto; padding:14px 28px; display:flex; justify-content:space-between; align-items:center; background:rgba(14,18,32,0.8); backdrop-filter:blur(16px); border:1px solid var(--border); border-radius:100px; z-index:100; }}
        .brand {{ font-size:1.3rem; font-weight:900; letter-spacing:-0.5px; color:#fff; }}
        .cart-pill {{ background:rgba(255,255,255,0.06); border:1px solid var(--border); padding:8px 18px; border-radius:50px; font-weight:700; font-size:0.9rem; }}
        .hero {{ max-width:1000px; margin:70px auto 40px; text-align:center; padding:0 24px; position:relative; z-index:10; }}
        .badge {{ display:inline-block; padding:8px 20px; border-radius:50px; background:rgba(37,99,235,0.12); border:1px solid rgba(37,99,235,0.3); color:#60a5fa; font-size:0.85rem; font-weight:800; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:20px; }}
        h1 {{ font-size:clamp(2.8rem,7vw,5.2rem); font-weight:900; line-height:1.1; margin-bottom:20px; background:linear-gradient(135deg, #fff 40%, #60a5fa 90%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }}
        p.tagline {{ font-size:1.2rem; color:#94a3b8; max-width:720px; margin:0 auto 35px; line-height:1.6; }}
        
        /* Product Showcase Card */
        .showcase {{ max-width:850px; margin:0 auto 60px; background:var(--card); border:1px solid var(--border); border-radius:32px; padding:40px; backdrop-filter:blur(16px); display:grid; grid-template-columns:1fr 1.2fr; gap:36px; align-items:center; position:relative; z-index:10; }}
        @media(max-width:768px){{ .showcase {{ grid-template-columns:1fr; text-align:center; }} }}
        .img-box {{ height:320px; background:radial-gradient(circle, rgba(37,99,235,0.2) 0%, transparent 70%); border:1px solid var(--border); border-radius:24px; display:flex; align-items:center; justify-content:center; font-size:4.5rem; }}
        .p-price {{ font-size:2.2rem; font-weight:900; color:#60a5fa; margin-bottom:12px; }}
        .p-price s {{ font-size:1.2rem; color:#64748b; font-weight:500; margin-left:8px; }}
        .size-row {{ display:flex; gap:10px; margin:16px 0 24px; }}
        @media(max-width:768px){{ .size-row {{ justify-content:center; }} }}
        .s-btn {{ width:42px; height:42px; border-radius:10px; border:1px solid var(--border); background:rgba(255,255,255,0.04); color:#fff; font-weight:700; cursor:pointer; }}
        .s-btn.active {{ border-color:#60a5fa; background:rgba(37,99,235,0.25); }}
        .btn-buy {{ width:100%; padding:16px; background:linear-gradient(135deg, #2563eb, #1d4ed8); border:none; border-radius:100px; color:#fff; font-size:1.1rem; font-weight:800; cursor:pointer; box-shadow:0 10px 25px rgba(37,99,235,0.4); transition:all 0.3s; }}
        .btn-buy:hover {{ transform:scale(1.03); box-shadow:0 15px 35px rgba(37,99,235,0.6); }}
        footer {{ text-align:center; padding:40px; border-top:1px solid var(--border); color:#64748b; }}
    </style>
</head>
<body>
    <nav class="nav">
        <div class="brand">{title.upper()}</div>
        <div class="cart-pill">🛒 Bag (<span id="cartCnt">0</span>)</div>
    </nav>
    <section class="hero">
        <div class="badge">🔥 {desc.upper()}</div>
        <h1>{title}</h1>
        <p class="tagline">{p1}</p>
    </section>

    <div class="showcase">
        <div class="img-box">👟</div>
        <div>
            <div style="font-size:0.85rem;font-weight:700;letter-spacing:1px;color:#f97316;text-transform:uppercase;margin-bottom:6px;">Edition Pro • In Stock</div>
            <h2 style="font-size:1.8rem;font-weight:800;margin-bottom:8px;">{title} Flagship</h2>
            <div class="p-price">$189 <s>$240</s></div>
            <p style="color:#94a3b8;font-size:0.95rem;line-height:1.5;margin-bottom:15px;">{p2}</p>
            <div class="size-row">
                <button class="s-btn" onclick="setSize(this)">US 8</button>
                <button class="s-btn active" onclick="setSize(this)">US 9</button>
                <button class="s-btn" onclick="setSize(this)">US 10</button>
                <button class="s-btn" onclick="setSize(this)">US 11</button>
            </div>
            <button class="btn-buy" onclick="addToBag()">⚡ Add to Bag & Checkout</button>
        </div>
    </div>
    <footer>Powered by <strong>Saathi AI</strong> • Live Knowledge Fetched for {title}</footer>
    <script>
        let items=0;
        function setSize(b){{ document.querySelectorAll('.s-btn').forEach(x=>x.classList.remove('active')); b.classList.add('active'); }}
        function addToBag(){{
            items++; document.getElementById('cartCnt').innerText=items;
            alert("{title} Flagship added to your bag! 🛒🔥");
            celebrate();
        }}
        function celebrate(){{
            for(let i=0;i<60;i++){{
                const d=document.createElement('div');
                d.style.position='fixed'; d.style.left=Math.random()*window.innerWidth+'px'; d.style.top='-10px';
                d.style.width='8px'; d.style.height='8px'; d.style.background=['#2563eb','#60a5fa','#f97316','#fff'][Math.floor(Math.random()*4)];
                d.style.zIndex='9999'; d.style.pointerEvents='none'; document.body.appendChild(d);
                d.animate([{{transform:'translate(0,0)'}}, {{transform:`translate(${{(Math.random()-0.5)*140}}px, ${{window.innerHeight+20}}px)`}}], {{duration:1800}}).onfinish=()=>d.remove();
            }}
        }}
    </script>
</body>
</html>"""

    # 4. Tech / SaaS / AI / Software / Developer Tools
    if archetype == "tech_saas":
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Next-Generation Neural Architecture</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    <style>
        :root {{ --primary: #6366f1; --accent: #06b6d4; --bg: #05060f; --card: rgba(14, 18, 36, 0.8); --border: rgba(255,255,255,0.08); }}
        * {{ margin:0; padding:0; box-sizing:border-box; font-family:'Plus Jakarta Sans',sans-serif; }}
        body {{ background:var(--bg); color:#fff; min-height:100vh; overflow-x:hidden; position:relative; }}
        .nav {{ position:sticky; top:16px; max-width:1100px; margin:0 auto; padding:14px 28px; display:flex; justify-content:space-between; align-items:center; background:rgba(10,14,28,0.8); backdrop-filter:blur(16px); border:1px solid var(--border); border-radius:100px; z-index:100; }}
        .brand {{ font-size:1.25rem; font-weight:800; display:flex; align-items:center; gap:8px; }}
        .brand-dot {{ width:9px; height:9px; border-radius:50%; background:#22c55e; box-shadow:0 0 10px #22c55e; }}
        .hero {{ max-width:1000px; margin:70px auto 40px; text-align:center; padding:0 24px; position:relative; z-index:10; }}
        .badge {{ display:inline-block; padding:8px 20px; border-radius:50px; background:rgba(99,102,241,0.12); border:1px solid rgba(99,102,241,0.3); color:#818cf8; font-size:0.85rem; font-weight:800; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:20px; }}
        h1 {{ font-size:clamp(2.8rem,7vw,5rem); font-weight:900; line-height:1.1; margin-bottom:20px; background:linear-gradient(135deg, #fff 40%, #818cf8 80%, #06b6d4 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }}
        p.tagline {{ font-size:1.2rem; color:#94a3b8; max-width:720px; margin:0 auto 35px; line-height:1.65; }}
        
        /* Terminal Simulator */
        .terminal {{ max-width:780px; margin:0 auto 60px; background:#0b0d19; border:1px solid rgba(99,102,241,0.3); border-radius:20px; overflow:hidden; font-family:'JetBrains Mono',monospace; box-shadow:0 20px 50px rgba(0,0,0,0.6); position:relative; z-index:10; }}
        .t-bar {{ padding:12px 18px; background:rgba(255,255,255,0.03); border-bottom:1px solid rgba(255,255,255,0.05); display:flex; gap:8px; align-items:center; }}
        .dot {{ width:11px; height:11px; border-radius:50%; }}
        .t-body {{ padding:24px; font-size:0.95rem; line-height:1.7; color:#38bdf8; }}
        .btn {{ padding:16px 38px; background:linear-gradient(135deg, #6366f1, #4f46e5); border:none; border-radius:100px; color:#fff; font-size:1.05rem; font-weight:700; cursor:pointer; box-shadow:0 10px 30px rgba(99,102,241,0.4); }}
        
        /* Bento Features */
        .bento {{ max-width:1100px; margin:0 auto 80px; padding:0 24px; display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); gap:24px; position:relative; z-index:10; }}
        .card {{ background:var(--card); border:1px solid var(--border); border-radius:24px; padding:32px; backdrop-filter:blur(14px); }}
        .card h3 {{ font-size:1.4rem; font-weight:800; margin-bottom:10px; color:#fff; }}
        .card p {{ color:#94a3b8; line-height:1.6; font-size:0.95rem; }}
        footer {{ text-align:center; padding:40px; border-top:1px solid var(--border); color:#64748b; }}
    </style>
</head>
<body>
    <nav class="nav">
        <div class="brand"><div class="brand-dot"></div><span>{title.upper()}</span></div>
        <div style="color:#22c55e;font-size:0.85rem;font-weight:700;">API Status: 99.99%</div>
    </nav>
    <section class="hero">
        <div class="badge">⚡ {desc.upper()}</div>
        <h1>{title}</h1>
        <p class="tagline">{p1}</p>
        <button class="btn" onclick="celebrate()">🚀 Deploy Microservice</button>
    </section>

    <div class="terminal">
        <div class="t-bar">
            <div class="dot" style="background:#ef4444;"></div>
            <div class="dot" style="background:#f59e0b;"></div>
            <div class="dot" style="background:#22c55e;"></div>
            <span style="color:#64748b;font-size:0.8rem;margin-left:10px;">bash — saathi-cli v2.0</span>
        </div>
        <div class="t-body">
            <span style="color:#a855f7;">$</span> curl -X POST https://api.saathi.ai/v1/init \\<br>
            &nbsp;&nbsp;-H "Authorization: Bearer sk_live_{title.lower()[:8]}" \\<br>
            &nbsp;&nbsp;-d '{{"model": "saathi-quantum", "stream": true}}'<br><br>
            <span style="color:#22c55e;">✔ Connected to {title} Neural Cluster (Latency: 14ms)</span><br>
            <span style="color:#cbd5e1;">&gt; Telemetry active. 100% test coverage verified.</span>
        </div>
    </div>

    <div class="bento">
        <div class="card">
            <h3>Neural Core Acceleration</h3>
            <p>{p2}</p>
        </div>
        <div class="card">
            <h3>Enterprise Fault Tolerance</h3>
            <p>{p3}</p>
        </div>
        <div class="card">
            <h3>Zero-Trust Data Mesh</h3>
            <p>{p4}</p>
        </div>
    </div>
    <footer>Synthesized by <strong>Saathi AI</strong> • Live Knowledge Fetched for {title}</footer>
    <script>
        function celebrate(){{
            alert("Cluster initialized for {title}! Real-time pipeline launched. ⚡");
            for(let i=0;i<60;i++){{
                const d=document.createElement('div');
                d.style.position='fixed'; d.style.left=Math.random()*window.innerWidth+'px'; d.style.top='-10px';
                d.style.width='7px'; d.style.height='7px'; d.style.background=['#6366f1','#06b6d4','#a855f7','#fff'][Math.floor(Math.random()*4)];
                d.style.zIndex='9999'; d.style.pointerEvents='none'; document.body.appendChild(d);
                d.animate([{{transform:'translate(0,0)'}}, {{transform:`translate(${{(Math.random()-0.5)*140}}px, ${{window.innerHeight+20}}px)`}}], {{duration:1800}}).onfinish=()=>d.remove();
            }}
        }}
    </script>
</body>
</html>"""

    # 5. Default General / Historical / Knowledge / World Showcase
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Premier Global Exhibition</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{ --primary: #0ea5e9; --accent: #8b5cf6; --bg: #070913; --card: rgba(16, 20, 36, 0.8); --border: rgba(255,255,255,0.09); }}
        * {{ margin:0; padding:0; box-sizing:border-box; font-family:'Plus Jakarta Sans',sans-serif; }}
        body {{ background:var(--bg); color:#fff; min-height:100vh; overflow-x:hidden; position:relative; }}
        .nav {{ position:sticky; top:16px; max-width:1100px; margin:0 auto; padding:14px 28px; display:flex; justify-content:space-between; align-items:center; background:rgba(12,16,30,0.8); backdrop-filter:blur(16px); border:1px solid var(--border); border-radius:100px; z-index:100; }}
        .brand {{ font-family:'Cinzel',serif; font-size:1.3rem; font-weight:900; letter-spacing:1px; }}
        .hero {{ max-width:1000px; margin:70px auto 40px; text-align:center; padding:0 24px; position:relative; z-index:10; }}
        .badge {{ display:inline-block; padding:8px 20px; border-radius:50px; background:rgba(14,165,233,0.12); border:1px solid rgba(14,165,233,0.3); color:#38bdf8; font-size:0.85rem; font-weight:800; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:20px; }}
        h1 {{ font-family:'Cinzel',serif; font-size:clamp(2.8rem,7vw,5.2rem); font-weight:900; line-height:1.1; margin-bottom:20px; background:linear-gradient(135deg, #fff 40%, #38bdf8 80%, #8b5cf6 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }}
        p.tagline {{ font-size:1.2rem; color:#94a3b8; max-width:740px; margin:0 auto 35px; line-height:1.65; }}
        .btn {{ padding:16px 40px; background:linear-gradient(135deg, #0ea5e9, #0284c7); border:none; border-radius:100px; color:#fff; font-size:1.05rem; font-weight:800; cursor:pointer; box-shadow:0 10px 30px rgba(14,165,233,0.4); }}
        
        /* Bento Exhibition */
        .bento {{ max-width:1100px; margin:40px auto 80px; padding:0 24px; display:grid; grid-template-columns:repeat(12, 1fr); gap:24px; position:relative; z-index:10; }}
        .card {{ background:var(--card); border:1px solid var(--border); border-radius:28px; padding:34px; backdrop-filter:blur(14px); }}
        .c-8 {{ grid-column:span 8; }} .c-4 {{ grid-column:span 4; }}
        @media(max-width:850px){{ .c-8, .c-4 {{ grid-column:span 12; }} }}
        .card h3 {{ font-size:1.5rem; font-weight:800; margin-bottom:12px; color:#fff; }}
        .card p {{ color:#94a3b8; line-height:1.65; font-size:1rem; }}
        footer {{ text-align:center; padding:40px; border-top:1px solid var(--border); color:#64748b; }}
    </style>
</head>
<body>
    <nav class="nav">
        <div class="brand">🏛️ {title.upper()}</div>
        <button class="btn" style="padding:10px 24px;font-size:0.95rem;" onclick="celebrate()">Explore Archive</button>
    </nav>
    <section class="hero">
        <div class="badge">★ {desc.upper()} ★</div>
        <h1>{title}</h1>
        <p class="tagline">{p1}</p>
        <button class="btn" onclick="celebrate()">✨ Discover Landmark Heritage</button>
    </section>

    <div class="bento">
        <div class="card c-8">
            <h3>Foundational Impact & Significance</h3>
            <p>{p2}</p>
        </div>
        <div class="card c-4">
            <h3>Distinction & Evolution</h3>
            <p>{p3}</p>
        </div>
        <div class="card c-4">
            <h3>Enduring Legacy</h3>
            <p>{p4}</p>
        </div>
        <div class="card c-8">
            <h3>Global Milestone & Contemporary Horizon</h3>
            <p>{extract}</p>
        </div>
    </div>
    <footer>Curated with <strong>Saathi AI</strong> • Live Knowledge Fetched for {title}</footer>
    <script>
        function celebrate(){{
            alert("Welcome to the {title} digital archive! 🏛️✨");
            for(let i=0;i<60;i++){{
                const d=document.createElement('div');
                d.style.position='fixed'; d.style.left=Math.random()*window.innerWidth+'px'; d.style.top='-10px';
                d.style.width='8px'; d.style.height='8px'; d.style.background=['#0ea5e9','#38bdf8','#8b5cf6','#fff'][Math.floor(Math.random()*4)];
                d.style.zIndex='9999'; d.style.pointerEvents='none'; document.body.appendChild(d);
                d.animate([{{transform:'translate(0,0)'}}, {{transform:`translate(${{(Math.random()-0.5)*140}}px, ${{window.innerHeight+20}}px)`}}], {{duration:1800}}).onfinish=()=>d.remove();
            }}
        }}
    </script>
</body>
</html>"""


def enrich_html_with_god_level_features(html_code: str, title: str = "Modern Experience") -> str:
    """If incoming HTML lacks modern dynamic effects, injects 21st.dev spotlight, particle canvas, web audio, and confetti."""
    if not html_code or "<html" not in html_code.lower():
        return generate_custom_god_level_html(title)

    has_canvas = "particlecanvas" in html_code.lower()
    has_audio = "audiofx" in html_code.lower()

    if has_canvas and has_audio:
        return html_code

    enhancement_css = """
    <style id="god-level-enhancements">
        .spotlight-card {
            position: relative;
            overflow: hidden;
            transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.3s;
        }
        .spotlight-card::before {
            content: '';
            position: absolute;
            inset: 0;
            border-radius: inherit;
            background: radial-gradient(400px circle at var(--mouse-x, 50%) var(--mouse-y, 50%), rgba(255, 255, 255, 0.15), transparent 70%);
            opacity: 0;
            transition: opacity 0.4s ease;
            pointer-events: none;
            z-index: 10;
        }
        .spotlight-card:hover::before { opacity: 1; }
        .spotlight-card:hover { transform: translateY(-4px); box-shadow: 0 15px 35px rgba(0,0,0,0.5); }
        #particleCanvasBg {
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            pointer-events: none; z-index: 0;
        }
    </style>
    """

    enhancement_js = """
    <canvas id="particleCanvasBg"></canvas>
    <script id="god-level-scripts">
        // 21st.dev Spotlight Tracking on cards
        document.querySelectorAll('.card, .bento-card, section > div, .box, .feature').forEach(el => {
            el.classList.add('spotlight-card');
            el.addEventListener('mousemove', e => {
                const rect = el.getBoundingClientRect();
                el.style.setProperty('--mouse-x', `${e.clientX - rect.left}px`);
                el.style.setProperty('--mouse-y', `${e.clientY - rect.top}px`);
            });
        });

        // Web Audio Synthesizer
        const AudioFX = {
            ctx: null,
            init() { if (!this.ctx) this.ctx = new (window.AudioContext || window.webkitAudioContext)(); },
            playClick() {
                try {
                    this.init();
                    const osc = this.ctx.createOscillator();
                    const gain = this.ctx.createGain();
                    osc.type = 'triangle';
                    osc.frequency.setValueAtTime(320, this.ctx.currentTime);
                    osc.frequency.exponentialRampToValueAtTime(140, this.ctx.currentTime + 0.08);
                    gain.gain.setValueAtTime(0.1, this.ctx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.08);
                    osc.connect(gain); gain.connect(this.ctx.destination);
                    osc.start(); osc.stop(this.ctx.currentTime + 0.08);
                } catch(e) {}
            },
            playFanfare() {
                try {
                    this.init();
                    [523.25, 659.25, 783.99, 1046.50].forEach((f, i) => {
                        const osc = this.ctx.createOscillator();
                        const gain = this.ctx.createGain();
                        osc.type = 'sine';
                        osc.frequency.setValueAtTime(f, this.ctx.currentTime + i * 0.08);
                        gain.gain.setValueAtTime(0.1, this.ctx.currentTime + i * 0.08);
                        gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + i * 0.08 + 0.4);
                        osc.connect(gain); gain.connect(this.ctx.destination);
                        osc.start(this.ctx.currentTime + i * 0.08);
                        osc.stop(this.ctx.currentTime + i * 0.08 + 0.45);
                    });
                } catch(e) {}
            }
        };
        document.querySelectorAll('button, a').forEach(btn => {
            btn.addEventListener('click', () => AudioFX.playClick());
        });

        // Physics Confetti
        function launchGlobalConfetti() {
            const colors = ['#6366f1', '#ec4899', '#06b6d4', '#eab308', '#22c55e', '#ffffff'];
            for(let i=0; i<70; i++) {
                const c = document.createElement('div');
                c.style.position = 'fixed';
                c.style.left = Math.random() * window.innerWidth + 'px';
                c.style.top = '-10px';
                const s = Math.random() * 8 + 5;
                c.style.width = s + 'px'; c.style.height = (s * 1.4) + 'px';
                c.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                c.style.zIndex = '99999';
                c.style.pointerEvents = 'none';
                document.body.appendChild(c);
                const drift = (Math.random() - 0.5) * 160;
                c.animate([
                    { transform: 'translate(0, 0) rotate(0deg)', opacity: 1 },
                    { transform: `translate(${drift}px, ${window.innerHeight + 20}px) rotate(${Math.random()*720}deg)`, opacity: 0 }
                ], { duration: Math.random()*2000 + 1500, easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)' }).onfinish = () => c.remove();
            }
        }
        document.querySelectorAll('button').forEach(b => b.addEventListener('click', () => { launchGlobalConfetti(); AudioFX.playFanfare(); }));

        // Particle Canvas Background
        const canvas = document.getElementById('particleCanvasBg');
        if (canvas) {
            const ctx = canvas.getContext('2d');
            let w = canvas.width = window.innerWidth;
            let h = canvas.height = window.innerHeight;
            window.addEventListener('resize', () => { w = canvas.width = window.innerWidth; h = canvas.height = window.innerHeight; });
            const pts = [];
            for (let i=0; i<50; i++) {
                pts.push({ x: Math.random()*w, y: Math.random()*h, vx: (Math.random()-0.5)*0.4, vy: (Math.random()-0.5)*0.4, r: Math.random()*1.8+0.6 });
            }
            function loop() {
                ctx.clearRect(0, 0, w, h);
                for (let i=0; i<pts.length; i++) {
                    const p = pts[i];
                    p.x += p.vx; p.y += p.vy;
                    if (p.x < 0) p.x = w; if (p.x > w) p.x = 0;
                    if (p.y < 0) p.y = h; if (p.y > h) p.y = 0;
                    ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI*2);
                    ctx.fillStyle = 'rgba(255, 255, 255, 0.5)'; ctx.fill();
                    for (let j=i+1; j<pts.length; j++) {
                        const p2 = pts[j];
                        const d = Math.hypot(p.x - p2.x, p.y - p2.y);
                        if (d < 110) {
                            ctx.beginPath();
                            ctx.strokeStyle = `rgba(255, 255, 255, ${0.12 * (1 - d/110)})`;
                            ctx.lineWidth = 0.5;
                            ctx.moveTo(p.x, p.y); ctx.lineTo(p2.x, p2.y); ctx.stroke();
                        }
                    }
                }
                requestAnimationFrame(loop);
            }
            loop();
        }
    </script>
    """

    if "</head>" in html_code:
        html_code = html_code.replace("</head>", f"{enhancement_css}\n</head>", 1)
    else:
        html_code = f"{enhancement_css}\n{html_code}"

    if "</body>" in html_code:
        html_code = html_code.replace("</body>", f"{enhancement_js}\n</body>", 1)
    else:
        html_code = f"{html_code}\n{enhancement_js}"

    return html_code


def extract_html_code_block(text: str) -> str | None:
    """Finds HTML code inside markdown code blocks or raw HTML in text."""
    if not text:
        return None
    m = re.search(r"```(?:html)?\s*(<!DOCTYPE html.*?>.*?</html>)", text, flags=re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()

    m2 = re.search(r"```(?:html)?\s*(<html.*?>.*?</html>)", text, flags=re.DOTALL | re.IGNORECASE)
    if m2:
        return m2.group(1).strip()

    m3 = re.search(r"(<!DOCTYPE html.*?>.*?</html>)", text, flags=re.DOTALL | re.IGNORECASE)
    if m3:
        return m3.group(1).strip()

    m4 = re.search(r"(<html.*?>.*?</html>)", text, flags=re.DOTALL | re.IGNORECASE)
    if m4:
        return m4.group(1).strip()

    return None

