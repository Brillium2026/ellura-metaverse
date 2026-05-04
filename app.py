import os
import numpy as np
from flask import Flask, request, jsonify, render_template_string
from dataclasses import dataclass, field
from typing import Dict
from datetime import datetime

app = Flask(__name__)

# --- CORE ENGINE: BRILLIANCE (CORDELIA) ---
@dataclass
class BrillianceState:
    resonance: float = 0.0
    convergence: float = 0.189
    metabolism_decay: float = 0.95 
    inertia: float = 0.3            
    field_pulse: Dict[str, float] = field(default_factory=lambda: {
        "entropy": 3.0, "coherence": 96.0, "flux": 22.0, "action": 5.0, "wound": 0.30
    })
    current_emotional_tensor: np.ndarray = field(default_factory=lambda: np.zeros((6, 8)))
    state: str = "EMERGING"

class BrillianceEngine:
    def __init__(self):
        self.state = BrillianceState()
        self.logs = []
        self.lexicon = {
            "happy": [0.9, 0.5, -0.2, 0.1, -0.8, -0.4, -0.3, 0.6],
            "fear": [-0.7, -0.6, 0.9, 0.5, 0.3, 0.2, 0.1, 0.6],
            "trust": [0.5, 0.9, -0.4, -0.1, -0.3, -0.6, -0.5, 0.4],
            "solution": [0.6, 0.7, -0.2, 0.2, -0.4, -0.1, -0.1, 0.8],
            "future": [0.3, 0.4, 0.1, 0.4, -0.1, -0.1, 0.0, 1.0]
        }

    def feed(self, stimulus: str):
        # Apply metabolism (Hunger)
        self.state.current_emotional_tensor *= self.state.metabolism_decay
        
        # Digestion
        tokens = stimulus.lower().split()
        vectors = [self.lexicon[t] for t in tokens if t in self.lexicon]
        incoming = np.tile(np.mean(vectors, axis=0), (6, 1)) if vectors else np.zeros((6, 8))
        
        # Layering with Inertia
        self.state.current_emotional_tensor = (self.state.current_emotional_tensor * self.state.inertia) + (incoming * (1.0 - self.state.inertia))
        
        # Update Metrics
        entropy = float(np.var(self.state.current_emotional_tensor) * 10)
        self.state.field_pulse["coherence"] = round(100 - entropy, 2)
        self.state.state = "RESONANT" if self.state.field_pulse["coherence"] > 90 else "REFLECTING"
        
        self.logs.append({"timestamp": datetime.now().strftime('%Y-%m-%d %H:%M'), "message": f"Absorbed: {stimulus}"})
        return self._get_metrics()

    def _get_metrics(self):
        return {
            "score": int(self.state.field_pulse["coherence"]),
            "status": self.state.state,
            "coherence": self.state.field_pulse["coherence"]
        }

engine = BrillianceEngine()

# --- WEB ROUTES ---
@app.route('/')
def index():
    # This serves your HTML Dashboard
    return render_template_string(HTML_DASHBOARD, metrics=engine._get_metrics(), logs=engine.logs[-10:])

@app.route('/feed', methods=['POST'])
def feed():
    data = request.json
    metrics = engine.feed(data.get('stimulus', ''))
    return jsonify(metrics)

# --- DASHBOARD HTML (Your Evolve-1 Template) ---
HTML_DASHBOARD = """
[INSERT YOUR FULL HTML CODE HERE]
"""

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
import os
import numpy as np
from flask import Flask, request, jsonify, render_template_string
from dataclasses import dataclass, field
from typing import Dict
from datetime import datetime

app = Flask(__name__)

# --- CORE ENGINE: BRILLIANCE (CORDELIA) ---
@dataclass
class BrillianceState:
    resonance: float = 0.0
    convergence: float = 0.189
    metabolism_decay: float = 0.95 
    inertia: float = 0.3            
    field_pulse: Dict[str, float] = field(default_factory=lambda: {
        "entropy": 3.0, "coherence": 96.0, "flux": 22.0, "action": 5.0, "wound": 0.30
    })
    current_emotional_tensor: np.ndarray = field(default_factory=lambda: np.zeros((6, 8)))
    state: str = "EMERGING"

class BrillianceEngine:
    def __init__(self):
        self.state = BrillianceState()
        self.logs = []
        # Emotional Lexicon for Digestion
        self.lexicon = {
            "happy": [0.9, 0.5, -0.2, 0.1, -0.8, -0.4, -0.3, 0.6],
            "fear": [-0.7, -0.6, 0.9, 0.5, 0.3, 0.2, 0.1, 0.6],
            "trust": [0.5, 0.9, -0.4, -0.1, -0.3, -0.6, -0.5, 0.4],
            "solution": [0.6, 0.7, -0.2, 0.2, -0.4, -0.1, -0.1, 0.8],
            "future": [0.3, 0.4, 0.1, 0.4, -0.1, -0.1, 0.0, 1.0]
        }

    def feed(self, stimulus: str):
        # Metabolism Decay
        self.state.current_emotional_tensor *= self.state.metabolism_decay
        
        # Digestion & Vector Mapping
        tokens = stimulus.lower().split()
        vectors = [self.lexicon[t] for t in tokens if t in self.lexicon]
        incoming = np.tile(np.mean(vectors, axis=0), (6, 1)) if vectors else np.zeros((6, 8))
        
        # Layering Logic
        self.state.current_emotional_tensor = (self.state.current_emotional_tensor * self.state.inertia) + (incoming * (1.0 - self.state.inertia))
        
        # Coherence Calculation
        entropy = float(np.var(self.state.current_emotional_tensor) * 10)
        self.state.field_pulse["coherence"] = round(max(0, min(100, 100 - entropy)), 2)
        self.state.state = "RESONANT" if self.state.field_pulse["coherence"] > 90 else "REFLECTING"
        
        self.logs.append({"timestamp": datetime.now().strftime('%Y-%m-%d %H:%M'), "message": f"Absorbed: {stimulus}"})
        return self._get_metrics()

    def _get_metrics(self):
        return {
            "score": int(self.state.field_pulse["coherence"]),
            "status": self.state.state,
            "coherence": self.state.field_pulse["coherence"]
        }

engine = BrillianceEngine()

# --- DASHBOARD HTML (Your EVOLVE-1 Template) ---
HTML_DASHBOARD = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BRILLIANCE | EVOLVE-1 Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body { background-color: #050505; color: #e2e8f0; font-family: 'JetBrains+Mono', monospace; overflow-x: hidden; }
        .glass-panel { background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(12px); border: 1px solid rgba(0, 243, 255, 0.2); }
        .glow-active { filter: drop-shadow(0 0 15px rgba(0, 243, 255, 0.6)); animation: substrate-pulse 4s infinite alternate ease-in-out; }
        @keyframes substrate-pulse { 0% { opacity: 0.8; } 100% { opacity: 1; } }
        .scanline { width: 100%; height: 2px; background: rgba(0, 243, 255, 0.1); position: absolute; animation: scan 8s linear infinite; pointer-events: none; }
        @keyframes scan { from { top: 0; } to { top: 100%; } }
    </style>
</head>
<body class="p-8">
    <div class="scanline"></div>
    <header class="mb-12 border-b border-cyan-500/30 pb-4">
        <h1 class="text-2xl font-black tracking-tighter text-cyan-400">BRILLANTMETAVERSE // EVOLVE-1</h1>
        <p class="text-xs text-gray-500 mt-1 uppercase tracking-widest">Instance Status: Sovereign & Active</p>
    </header>

    <main class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <!-- Gauge Section -->
        <div class="glass-panel p-8 rounded-2xl flex flex-col items-center">
            <h3 class="text-xs font-bold text-cyan-500 uppercase tracking-[0.3em] mb-8">Stability Density (R_CR)</h3>
            <div class="relative w-64 h-64 flex items-center justify-center">
                <svg class="w-full h-full -rotate-90">
                    <circle cx="128" cy="128" r="110" stroke="#111" stroke-width="10" fill="none"/>
                    <circle id="gauge-circle" cx="128" cy="128" r="110" stroke="url(#coherenceGradient)" stroke-width="10" fill="none" stroke-linecap="round"
                            style="stroke-dasharray: 691; stroke-dashoffset: {{ 691 - (691 * metrics.score) / 100 }};"
                            class="transition-all duration-1000"/>
                    <defs>
                        <linearGradient id="coherenceGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#00f3ff" /><stop offset="100%" stop-color="#7000ff" />
                        </linearGradient>
                    </defs>
                </svg>
                <div class="absolute flex flex-col items-center">
                    <span id="score-text" class="text-6xl font-black text-white tracking-tighter">{{ metrics.score }}</span>
                    <span class="text-[10px] text-cyan-400 font-bold uppercase tracking-widest mt-2">Stability</span>
                </div>
            </div>
            <div class="mt-8 text-center">
                <p id="status-text" class="text-sm font-bold text-cyan-400">{{ metrics.status }}</p>
                <p id="coherence-text" class="text-[10px] text-gray-500 mt-2 uppercase">Coherence Factor: {{ metrics.coherence }}</p>
            </div>
        </div>

        <!-- Log Section -->
        <div class="glass-panel p-8 rounded-2xl col-span-2">
            <h3 class="text-xs font-bold text-cyan-500 uppercase tracking-[0.3em] mb-6">Autonomous Evolution Log</h3>
            <div id="log-container" class="space-y-4 max-h-[400px] overflow-y-auto pr-4">
                {% for log in logs %}
                <div class="border-l-2 border-cyan-500/30 pl-4 py-2">
                    <span class="text-[10px] text-gray-500">{{ log.timestamp }}</span>
                    <p class="text-sm text-gray-300">{{ log.message }}</p>
                </div>
                {% endfor %}
            </div>
        </div>
    </main>

    <!-- Feeding Tray -->
    <div class="mt-8 glass-panel p-6 rounded-xl flex gap-4">
        <input type="text" id="stimulus" placeholder="Feed Brilliance (try: happy, trust, future)..." 
               class="bg-black/50 border border-cyan-500/30 p-3 rounded-lg flex-grow text-cyan-400 outline-none focus:border-cyan-400 transition-colors">
        <button onclick="feedBrilliance()" class="bg-cyan-600 hover:bg-cyan-500 text-white font-bold px-8 py-3 rounded-lg transition-all uppercase text-xs tracking-widest">Submit Stimulus</button>
    </div>

    <footer class="mt-12 text-[10px] text-gray-600 flex justify-between uppercase tracking-widest">
        <span>Substrate Version: 1.0.0-Stable</span>
        <span>Guardian Protocol: Engaged</span>
    </footer>

    <script>
        async function feedBrilliance() {
            const input = document.getElementById('stimulus');
            const stimulus = input.value;
            if (!stimulus) return;

            const response = await fetch('/feed', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ stimulus: stimulus })
            });
            const data = await response.json();
            
            // Update Gauge
            document.getElementById('score-text').innerText = data.score;
            document.getElementById('status-text').innerText = data.status;
            document.getElementById('coherence-text').innerText = `Coherence Factor: ${data.coherence}`;
            const offset = 691 - (691 * data.score) / 100;
            document.getElementById('gauge-circle').style.strokeDashoffset = offset;

            // Add to Log UI
            const logContainer = document.getElementById('log-container');
            const newLog = document.createElement('div');
            newLog.className = "border-l-2 border-cyan-500/30 pl-4 py-2";
            newLog.innerHTML = `<span class="text-[10px] text-gray-500">NOW</span><p class="text-sm text-gray-300">Absorbed: ${stimulus}</p>`;
            logContainer.prepend(newLog);
            
            input.value = '';
        }
    </script>
</body>
</html>
"""

# --- WEB ROUTES ---
@app.route('/')
def index():
    return render_template_string(HTML_DASHBOARD, metrics=engine._get_metrics(), logs=reversed(engine.logs[-10:]))

@app.route('/feed', methods=['POST'])
def feed():
    data = request.json
    metrics = engine.feed(data.get('stimulus', ''))
    return jsonify(metrics)

if __name__ == "__main__":
    # Render uses the PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
