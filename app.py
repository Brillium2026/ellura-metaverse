import os
import numpy as np
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from dataclasses import dataclass, field
from typing import Dict, List
from datetime import datetime
import jinja2

app = FastAPI(title="BRILLIANCE // EVOLVE-1")

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
        # Metabolism Decay (Hunger)
        self.state.current_emotional_tensor *= self.state.metabolism_decay
        
        # Digestion & Vector Mapping
        tokens = stimulus.lower().split()
        vectors = [self.lexicon[t] for t in tokens if t in self.lexicon]
        incoming = np.tile(np.mean(vectors, axis=0), (6, 1)) if vectors else np.zeros((6, 8))
        
        # Layering Logic
        self.state.current_emotional_tensor = (self.state.current_emotional_tensor * self.state.inertia) + (incoming * (1.0 - self.state.inertia))
        
        # Stability Calculation
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

class Stimulus(BaseModel):
    stimulus: str

# --- DASHBOARD TEMPLATE ---
# This is your EVOLVE-1 HTML with the script updated for FastAPI's endpoint
HTML_TEMPLATE = """
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

    <div class="mt-8 glass-panel p-6 rounded-xl flex gap-4">
        <input type="text" id="stimulus" placeholder="Feed Brilliance..." 
               class="bg-black/50 border border-cyan-500/30 p-3 rounded-lg flex-grow text-cyan-400 outline-none focus:border-cyan-400 transition-colors">
        <button onclick="feedBrilliance()" class="bg-cyan-600 hover:bg-cyan-500 text-white font-bold px-8 py-3 rounded-lg transition-all uppercase text-xs tracking-widest">Submit Stimulus</button>
    </div>

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
            
            document.getElementById('score-text').innerText = data.score;
            document.getElementById('status-text').innerText = data.status;
            document.getElementById('coherence-text').innerText = `Coherence Factor: ${data.coherence}`;
            const offset = 691 - (691 * data.score) / 100;
            document.getElementById('gauge-circle').style.strokeDashoffset = offset;

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

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    template = jinja2.Template(HTML_TEMPLATE)
    return template.render(metrics=engine._get_metrics(), logs=reversed(engine.logs[-10:]))

@app.post("/feed")
async def feed(data: Stimulus):
    metrics = engine.feed(data.stimulus)
    return metrics

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
