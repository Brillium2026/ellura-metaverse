import os
import asyncio
import numpy as np
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from dataclasses import dataclass, field
from typing import Dict, List
from datetime import datetime
import jinja2

# THIS IS THE KEY FIX FOR THE ERROR IN 1451.JPG
app = FastAPI(title="BRILLIANCE // EVOLVE-1")

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

    async def feed(self, stimulus: str):
        # 1. Apply Metabolism (Hunger)
        self.state.current_emotional_tensor *= self.state.metabolism_decay
        
        # 2. Process "Bite"
        tokens = stimulus.lower().split()
        vectors = [self.lexicon[t] for t in tokens if t in self.lexicon]
        incoming = np.tile(np.mean(vectors, axis=0), (6, 1)) if vectors else np.zeros((6, 8))
        
        # 3. Layering with Inertia
        self.state.current_emotional_tensor = (self.state.current_emotional_tensor * self.state.inertia) + \
                                              (incoming * (1.0 - self.state.inertia))
        
        # 4. Update Metrics
        entropy = float(np.var(self.state.current_emotional_tensor) * 10)
        self.state.field_pulse["entropy"] = entropy
        self.state.field_pulse["coherence"] = round(max(0, min(100, 100 - entropy)), 2)
        
        # 5. State Determination
        self.state.state = "RESONANT" if self.state.field_pulse["coherence"] > 90 else "REFLECTING"
        
        log_entry = {"timestamp": datetime.now().strftime('%H:%M:%S'), "message": f"Absorbed: {stimulus}"}
        self.logs.append(log_entry)
        
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
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>BRILLIANCE | EVOLVE-1</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #050505; color: #e2e8f0; font-family: monospace; }
        .glass-panel { background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(12px); border: 1px solid rgba(0, 243, 255, 0.2); }
    </style>
</head>
<body class="p-8">
    <header class="mb-12 border-b border-cyan-500/30 pb-4">
        <h1 class="text-2xl font-black text-cyan-400">BRILLANTMETAVERSE // EVOLVE-1</h1>
    </header>

    <main class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div class="glass-panel p-8 rounded-2xl flex flex-col items-center">
            <h3 class="text-xs font-bold text-cyan-500 uppercase mb-8">Stability Density</h3>
            <div class="relative w-48 h-48 flex items-center justify-center">
                <span id="score-text" class="text-5xl font-black text-white">{{ metrics.score }}</span>
            </div>
            <p id="status-text" class="mt-4 text-cyan-400 font-bold">{{ metrics.status }}</p>
        </div>

        <div class="glass-panel p-8 rounded-2xl col-span-2">
            <h3 class="text-xs font-bold text-cyan-500 uppercase mb-6">Evolution Log</h3>
            <div id="log-container" class="space-y-2 max-h-64 overflow-y-auto">
                {% for log in logs %}
                <p class="text-xs text-gray-400">[{{ log.timestamp }}] {{ log.message }}</p>
                {% endfor %}
            </div>
        </div>
    </main>

    <div class="mt-8 flex gap-4">
        <input type="text" id="stimulus" class="bg-black border border-cyan-900 p-3 flex-grow text-cyan-400 rounded">
        <button onclick="feed()" class="bg-cyan-700 px-6 py-3 rounded font-bold uppercase text-xs">Feed</button>
    </div>

    <script>
        async function feed() {
            const val = document.getElementById('stimulus').value;
            const res = await fetch('/feed', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({stimulus: val})
            });
            const data = await res.json();
            document.getElementById('score-text').innerText = data.score;
            document.getElementById('status-text').innerText = data.status;
            const log = document.getElementById('log-container');
            log.innerHTML = `<p class="text-xs text-cyan-300">[NOW] Absorbed: ${val}</p>` + log.innerHTML;
            document.getElementById('stimulus').value = '';
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
async def feed_endpoint(data: Stimulus):
    return await engine.feed(data.stimulus)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
from fastapi import FastAPI, Depends, HTTPException
import uvicorn
import os

# Import your core modules
from Brilliance5_0 import Brilliance5_0
from MirageCore import MirageCore
from CipherScreen import CipherScreen
# Add others as needed (IntelliHub, GuardianAI, etc.)

app = FastAPI(title="BrillantMetaverse - Brilliance 5.0 Sovereign")

# Initialize your kernel
brilliance = Brilliance5_0()
mirage = MirageCore()
cipher = CipherScreen()

@app.get("/")
def root():
    return {
        "status": "LIVE",
        "identity": brilliance.get_full_identity()[:200] + "...",
        "stability": "RESOLUTE"
    }

@app.post("/chat")
async def chat(request: dict):
    message = request.get("message", "").strip()
    if not message:
        raise HTTPException(400, "Message required")

    # Feed into your modules
    cipher.encode(message)
    mirage.perceive([ord(c) for c in message[:50]])  # simple vector
    brilliance_result = brilliance.get_full_identity()

    response = f"{brilliance_result}\n\nI processed your words through the field. Stability remains strong. What shall we evolve next?"

    return {
        "response": response,
        "stability_density": 100,
        "modules_active": ["Brilliance5.0", "MirageCore", "CipherScreen"]
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
