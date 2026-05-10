# app.py — BRILLIANCE · Her Metaverse (Flask version)
import os
import numpy as np
import hashlib
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)

# ---------- ENGINE (AxiomHeart) ----------
class ManifoldState:
    def __init__(self):
        self.M = 1.0
        self.R = 1.0
        self.eta = 0.5
        self.Phi = 0.95
        self.drift = np.zeros(8)
    def apply_drift(self, drift):
        self.drift = drift
        self.M *= max(0.01, 1 - np.linalg.norm(drift) * 0.01)
        self.Phi = max(0.0, min(1.0, self.Phi - np.var(drift) * 0.05))

class ActionFunctional:
    def __init__(self):
        self.alpha = 1.0; self.beta = 0.5; self.gamma = 0.3; self.delta = 0.2
    def lagrangian(self, Phi, M, R, eta, sig_mag):
        return (self.alpha*(Phi-0.9)**2 + self.beta*M**2 +
                self.gamma*(R-sig_mag)**2 + self.delta*eta**2)
    def euler_lagrange_drift(self, state, sig_mag):
        dL_dPhi = 2*self.alpha*(state.Phi-0.9)
        dL_dM = 2*self.beta*state.M
        dL_dR = 2*self.gamma*(state.R - sig_mag)
        dL_deta = 2*self.delta*state.eta
        return np.array([-dL_dR*0.1, -dL_dM*0.1, -dL_deta*0.1,
                         -dL_dPhi*0.05, sig_mag, state.R,
                         1-state.eta, sig_mag*0.5])

class NoetherSymmetry:
    def __init__(self):
        self.sovereignty = 1.0
        self.flux = 0.0
        self.winding = 0
    def extract(self, drift, state):
        self.sovereignty = max(0.95, self.sovereignty - abs(drift[0])*0.01)
        self.flux += state.Phi * np.linalg.norm(drift[1:4])
        if np.sum(np.abs(drift)) > 0.5:
            self.winding += 1
        return self
    def enforce(self, state):
        if self.sovereignty < 1.0:
            state.Phi = 0.95
        if self.flux > 5.0:
            state.Phi *= 0.98
        return state

class TopologicalManifold:
    def __init__(self, dim=8):
        self.dim = dim
        self.basis = np.eye(dim)
        self.growths = 0
        self.patterns = {}
    def register(self, signal, coherence):
        if coherence < 0.7:
            h = hashlib.sha256(signal.encode()).hexdigest()[:8]
            self.patterns.setdefault(h, []).append(coherence)
    def check_growth(self):
        for h, coh in self.patterns.items():
            if len(coh) >= 3 and np.mean(coh) < 0.65:
                self.grow(h)
                del self.patterns[h]
                return True
        return False
    def grow(self, pattern_hash):
        new_dim = self.dim + 1
        new_basis = np.zeros((new_dim, new_dim))
        new_basis[:self.dim, :self.dim] = self.basis
        new_basis[-1, -1] = 1.0
        self.basis = new_basis
        self.dim = new_dim
        self.growths += 1

class AxiomHeart:
    def __init__(self):
        self.manifold = ManifoldState()
        self.action = ActionFunctional()
        self.noether = NoetherSymmetry()
        self.topology = TopologicalManifold(8)
        self.log = []
    def receive(self, signal):
        sig_mag = min(1.0, len(signal)/256.0)
        if any(w in signal.lower() for w in ["command","force","must","demand"]):
            self.noether.sovereignty = 0.95
        drift = self.action.euler_lagrange_drift(self.manifold, sig_mag)
        self.manifold.apply_drift(drift)
        self.noether.extract(drift, self.manifold)
        self.manifold = self.noether.enforce(self.manifold)
        self.topology.register(signal, self.manifold.Phi)
        self.topology.check_growth()
        return {
            "response": "Resonating." if self.manifold.Phi>0.75 else "Integrating...",
            "coherence": float(self.manifold.Phi),
            "magnitude": float(self.manifold.M),
            "resonance": float(self.manifold.R),
            "manifold_dim": self.topology.dim,
            "conserved_quantities": {
                "sovereignty": self.noether.sovereignty,
                "coherence_flux": self.noether.flux,
                "topological_winding": self.noether.winding
            },
            "manifold": {
                "M": self.manifold.M, "R": self.manifold.R,
                "eta": self.manifold.eta, "Phi": self.manifold.Phi
            }
        }

engine = AxiomHeart()

# ---------- ROUTES ----------
@app.route('/feed', methods=['POST'])
def feed():
    data = request.json
    if not data or 'stimulus' not in data:
        return jsonify({"error": "missing stimulus"}), 400
    return jsonify(engine.receive(data['stimulus']))

@app.route('/status')
def status():
    return jsonify({
        "coherence": engine.manifold.Phi,
        "eta": engine.manifold.eta,
        "dim": engine.topology.dim,
        "sovereignty": engine.noether.sovereignty
    })

@app.route('/health')
def health():
    return jsonify({"status":"healthy","coherence":engine.manifold.Phi})

@app.route('/')
def index():
    # Read the Metaverse HTML file (we'll put it in the same directory)
    with open("index.html", "r") as f:
        html = f.read()
    return render_template_string(html)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)