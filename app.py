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
