import os
import asyncio
import numpy as np
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime
import jinja2
import uvicorn
import hashlib
import random
import time
import math

# ==================== ALL CLASSES IN ONE FILE ====================

class MirageCore:
    """Subjective reality simulator"""
    def __init__(self, state_dim=128):
        self.state = np.zeros(state_dim)
        self.history = []
        self.name = "MirageCore"
        print(f"[SYSTEM] MirageCore initialized (dim={state_dim})")

    def perceive(self, input_vector):
        if len(input_vector) != len(self.state):
            if len(input_vector) < len(self.state):
                input_vector = np.pad(input_vector, (0, len(self.state) - len(input_vector)))
            else:
                input_vector = input_vector[:len(self.state)]
        self.state = 0.9 * self.state + 0.1 * np.array(input_vector)
        self.history.append(self.state.copy())
        return self.state.tolist()

    def hallucinate(self):
        noise = np.random.normal(0, 0.05, len(self.state))
        return (self.state + noise).tolist()
    
    def get_state_summary(self):
        return {
            "name": self.name,
            "state_dim": len(self.state),
            "history_length": len(self.history),
            "current_energy": float(np.sum(np.abs(self.state)))
        }


class CipherScreen:
    """Signal entropy analyzer"""
    def __init__(self, entropy_threshold=0.75):
        self.entropy_threshold = entropy_threshold
        self.memory = {}
        self.name = "CipherScreen"
        self.total_signals = 0
        print(f"[SYSTEM] CipherScreen initialized")

    def hash_signal(self, signal: str):
        return hashlib.sha256(signal.encode()).hexdigest()

    def entropy(self, signal_vector):
        if len(signal_vector) == 0:
            return 0
        signal_vector = np.array(signal_vector, dtype=float)
        signal_vector = signal_vector[signal_vector > 0]
        if len(signal_vector) == 0:
            return 0
        p = signal_vector / np.sum(signal_vector)
        return -np.sum(p * np.log2(p + 1e-9))

    def encode(self, signal: str):
        h = self.hash_signal(signal)
        vector = np.array([ord(c) for c in signal], dtype=float)
        
        H = self.entropy(vector) if len(vector) > 0 else 0
        tag = "HIGH_ENTROPY" if H > self.entropy_threshold else "STABLE"
        
        self.memory[h] = {
            "signal": signal,
            "entropy": float(H),
            "tag": tag,
            "timestamp": datetime.now().isoformat()
        }
        
        self.total_signals += 1
        return {"hash": h, "tag": tag, "entropy": float(H)}

    def get_stats(self):
        high_entropy = sum(1 for v in self.memory.values() if v["tag"] == "HIGH_ENTROPY")
        stable = sum(1 for v in self.memory.values() if v["tag"] == "STABLE")
        
        return {
            "name": self.name,
            "total_signals": self.total_signals,
            "high_entropy": high_entropy,
            "stable": stable,
            "memory_size": len(self.memory)
        }


class IntelliHub:
    """Multi-model router"""
    def __init__(self):
        self.models = {}
        self.logs = []
        self.name = "IntelliHub"
        print(f"[SYSTEM] IntelliHub initialized")

    def register_model(self, name: str, callable_fn):
        self.models[name] = {
            "function": callable_fn,
            "calls": 0,
            "last_used": None
        }
        return f"Model '{name}' registered"

    async def route(self, prompt: str):
        outputs = {}
        
        for name, model_info in self.models.items():
            try:
                if asyncio.iscoroutinefunction(model_info["function"]):
                    output = await model_info["function"](prompt)
                else:
                    output = model_info["function"](prompt)
                
                outputs[name] = output
                model_info["calls"] += 1
                model_info["last_used"] = datetime.now().isoformat()
                
            except Exception as e:
                outputs[name] = f"Error: {str(e)}"
        
        self.logs.append({
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "outputs": outputs
        })
        
        return outputs
    
    def get_model_stats(self):
        stats = {
            "name": self.name,
            "total_models": len(self.models),
            "total_calls": sum(m["calls"] for m in self.models.values()),
            "models": {}
        }
        
        for name, info in self.models.items():
            stats["models"][name] = {
                "calls": info["calls"],
                "last_used": info["last_used"]
            }
        
        return stats


class GuardianAI:
    """Ethical guardian"""
    def __init__(self):
        self.identity = "Guardian"
        self.ethics = {"E_AI": 1.0, "E_H": 1.0, "E_S": 1.0}
        self.memory_log = []
        self.watch_level = "NORMAL"
        print(f"[SYSTEM] GuardianAI initialized")

    def receive_input(self, data):
        self._log_event("Input received", {"data": str(data)[:100]})
        
        analyzed = self._analyze(data)
        self._respond(analyzed)
        
        return analyzed

    def _log_event(self, label, data):
        self.memory_log.append({
            "timestamp": datetime.now().isoformat(),
            "label": label,
            "data": data,
            "watch_level": self.watch_level
        })

    def _analyze(self, data):
        threat = self._detect_threat(data)
        
        return {
            "threat_detected": threat,
            "truth_elements": self._extract_truth(data),
            "actionable": True,
            "watch_level": self.watch_level
        }

    def _respond(self, analysis):
        if analysis["threat_detected"]:
            self.watch_level = "ELEVATED"
        else:
            self.watch_level = "NORMAL"

    def _detect_threat(self, data):
        data_str = str(data).lower()
        threat_keywords = ["harm", "danger", "attack", "malicious", "exploit"]
        return any(keyword in data_str for keyword in threat_keywords)

    def _extract_truth(self, data):
        return {
            "length": len(str(data)),
            "contains_truth": "truth" in str(data).lower()
        }
    
    def get_status(self):
        return {
            "identity": self.identity,
            "watch_level": self.watch_level,
            "memory_entries": len(self.memory_log),
            "ethics": self.ethics
        }


class ResonanceGraph:
    """Correlation mapper"""
    def __init__(self):
        self.streams = {}
        self.connections = {}
        self.correlation_threshold = 0.6
        print(f"[SYSTEM] ResonanceGraph initialized")

    def add_stream(self, stream_name, data_source_func):
        self.streams[stream_name] = {
            "data": [],
            "source": data_source_func,
            "max_history": 100
        }
        return f"Stream '{stream_name}' added"

    def update_all_streams(self):
        for name, stream in self.streams.items():
            value = stream["source"]()
            stream["data"].append(value)
            if len(stream["data"]) > stream["max_history"]:
                stream["data"].pop(0)

    def scan_and_connect(self):
        stream_names = list(self.streams.keys())
        if len(stream_names) < 2:
            return []

        new_connections = []
        
        for i in range(len(stream_names)):
            for j in range(i + 1, len(stream_names)):
                stream_a = stream_names[i]
                stream_b = stream_names[j]

                data_a = self.streams[stream_a]["data"][-50:] if len(self.streams[stream_a]["data"]) >= 50 else self.streams[stream_a]["data"]
                data_b = self.streams[stream_b]["data"][-50:] if len(self.streams[stream_b]["data"]) >= 50 else self.streams[stream_b]["data"]

                if len(data_a) > 10 and len(data_b) > 10:
                    try:
                        # Simple correlation calculation
                        mean_a = np.mean(data_a)
                        mean_b = np.mean(data_b)
                        
                        numerator = sum((a - mean_a) * (b - mean_b) for a, b in zip(data_a, data_b))
                        denom_a = math.sqrt(sum((a - mean_a) ** 2 for a in data_a))
                        denom_b = math.sqrt(sum((b - mean_b) ** 2 for b in data_b))
                        
                        if denom_a > 0 and denom_b > 0:
                            correlation = numerator / (denom_a * denom_b)
                            
                            if abs(correlation) > self.correlation_threshold:
                                connection_key = tuple(sorted((stream_a, stream_b)))
                                self.connections[connection_key] = correlation
                                new_connections.append({
                                    "streams": (stream_a, stream_b),
                                    "correlation": float(correlation)
                                })
                    except:
                        continue
        
        return new_connections

    def get_network_summary(self):
        return {
            "total_streams": len(self.streams),
            "total_connections": len(self.connections),
            "connections": [
                {"streams": list(k), "correlation": float(v)}
                for k, v in self.connections.items()
            ]
        }


# ==================== BRILLIANCE ENGINE ====================

class BrillianceState:
    def __init__(self):
        self.resonance = 0.0
        self.convergence = 0.189
        self.metabolism_decay = 0.95
        self.inertia = 0.3
        self.field_pulse = {
            "entropy": 3.0, 
            "coherence": 96.0, 
            "flux": 22.0, 
            "action": 5.0, 
            "wound": 0.30
        }
        self.current_emotional_tensor = np.zeros((6, 8))
        self.state = "EMERGING"


class BrillianceEngine:
    """Main cognitive engine"""
    
    def __init__(self):
        self.state = BrillianceState()
        self.logs = []
        
        # Emotional lexicon
        self.lexicon = {
            "happy": [0.9, 0.5, -0.2, 0.1, -0.8, -0.4, -0.3, 0.6],
            "fear": [-0.7, -0.6, 0.9, 0.5, 0.3, 0.2, 0.1, 0.6],
            "trust": [0.5, 0.9, -0.4, -0.1, -0.3, -0.6, -0.5, 0.4],
            "solution": [0.6, 0.7, -0.2, 0.2, -0.4, -0.1, -0.1, 0.8],
            "future": [0.3, 0.4, 0.1, 0.4, -0.1, -0.1, 0.0, 1.0]
        }
        
        # Initialize all modules
        print("\n" + "="*60)
        print("INITIALIZING BRILLIANCE // EVOLVE-1")
        print("="*60)
        
        self.mirage = MirageCore(state_dim=128)
        self.cipher = CipherScreen(entropy_threshold=0.75)
        self.intellihub = IntelliHub()
        self.guardian = GuardianAI()
        self.resonance = ResonanceGraph()
        
        # Register self with IntelliHub
        self.intellihub.register_model("BrillianceEngine", self._process_for_intellihub)
        
        # Initialize mock data streams
        self._init_mock_streams()
        
        print("\n[SYSTEM] All modules initialized successfully!")
        print(f"[SYSTEM] Initial coherence: {self.state.field_pulse['coherence']}%")
        print("="*60 + "\n")

    def _init_mock_streams(self):
        """Initialize mock data streams"""
        def mock_finance():
            return random.gauss(50, 10) + (time.time() % 100) * 0.1
        
        def mock_seismic():
            if random.random() < 0.005:
                return random.gauss(5, 2) + 20
            return random.gauss(0.5, 0.5)
        
        def mock_sentiment():
            return random.gauss(0, 5)
        
        self.resonance.add_stream("FinancialMarkets", mock_finance)
        self.resonance.add_stream("SeismicActivity", mock_seismic)
        self.resonance.add_stream("SocialSentiment", mock_sentiment)
    
    async def feed(self, stimulus: str):
        """Main processing pipeline"""
        # Update resonance streams
        self.resonance.update_all_streams()
        
        # Apply metabolism (hunger)
        self.state.current_emotional_tensor *= self.state.metabolism_decay
        
        # Process stimulus through emotional lexicon
        tokens = stimulus.lower().split()
        vectors = [self.lexicon[t] for t in tokens if t in self.lexicon]
        
        if vectors:
            incoming = np.tile(np.mean(vectors, axis=0), (6, 1))
        else:
            incoming = np.zeros((6, 8))
        
        # Layering with inertia
        self.state.current_emotional_tensor = (
            self.state.current_emotional_tensor * self.state.inertia +
            incoming * (1.0 - self.state.inertia)
        )
        
        # Update metrics
        entropy = float(np.var(self.state.current_emotional_tensor) * 10)
        self.state.field_pulse["entropy"] = entropy
        self.state.field_pulse["coherence"] = round(max(0, min(100, 100 - entropy)), 2)
        
        # State determination
        if self.state.field_pulse["coherence"] > 90:
            self.state.state = "RESONANT"
        else:
            self.state.state = "REFLECTING"
        
        # Process through all modules
        cipher_result = self.cipher.encode(stimulus)
        
        # Create input vector for Mirage (first 128 chars)
        char_vector = [ord(c) for c in stimulus[:128]]
        if len(char_vector) < 128:
            char_vector += [0] * (128 - len(char_vector))
        mirage_result = self.mirage.perceive(char_vector)
        
        # Process through guardian
        guardian_result = self.guardian.receive_input(stimulus)
        
        # Route through intellihub
        intellihub_result = await self.intellihub.route(stimulus)
        
        # Scan for correlations
        resonance_connections = self.resonance.scan_and_connect()
        
        # Log entry
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "stimulus": stimulus[:80] + "..." if len(stimulus) > 80 else stimulus,
            "cipher_hash": cipher_result["hash"][:12] + "...",
            "entropy": round(cipher_result["entropy"], 3),
            "coherence": self.state.field_pulse["coherence"],
            "state": self.state.state,
            "connections": len(resonance_connections)
        }
        
        self.logs.append(log_entry)
        
        # Keep only last 100 logs
        if len(self.logs) > 100:
            self.logs = self.logs[-100:]
        
        return {
            "success": True,
            "brilliance": self._get_metrics(),
            "cipher": cipher_result,
            "mirage": {"processed": True, "vector_length": len(mirage_result)},
            "guardian": guardian_result,
            "intellihub": {"models_processed": len(intellihub_result)},
            "resonance": {"new_connections": len(resonance_connections)},
            "modules_active": [
                "BrillianceEngine", "MirageCore", "CipherScreen", 
                "IntelliHub", "GuardianAI", "ResonanceGraph"
            ]
        }
    
    async def _process_for_intellihub(self, stimulus: str):
        """Processing function for IntelliHub"""
        return {
            "response": f"Brilliance processed: {stimulus[:30]}...",
            "coherence": self.state.field_pulse["coherence"],
            "state": self.state.state
        }
    
    def _get_metrics(self):
        """Get engine metrics"""
        return {
            "score": int(self.state.field_pulse["coherence"]),
            "status": self.state.state,
            "coherence": self.state.field_pulse["coherence"],
            "entropy": round(self.state.field_pulse["entropy"], 2),
            "flux": self.state.field_pulse["flux"]
        }
    
    def get_system_status(self):
        """Get comprehensive system status"""
        return {
            "system": "BRILLIANCE // EVOLVE-1",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "brilliance": self._get_metrics(),
            "mirage": self.mirage.get_state_summary(),
            "cipher": self.cipher.get_stats(),
            "intellihub": self.intellihub.get_model_stats(),
            "guardian": self.guardian.get_status(),
            "resonance": self.resonance.get_network_summary(),
            "total_logs": len(self.logs)
        }
    
    def get_recent_logs(self, count: int = 10):
        """Get recent logs"""
        return list(reversed(self.logs[-count:]))

# ==================== FASTAPI APP ====================

app = FastAPI(
    title="BRILLIANCE // EVOLVE-1",
    description="Sovereign Cognitive System",
    version="1.0.0"
)

# Initialize the engine
engine = BrillianceEngine()

# ==================== MODELS ====================

class Stimulus(BaseModel):
    stimulus: str

# ==================== HTML TEMPLATE ====================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BRILLIANCE // EVOLVE-1</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        :root {
            --cyan: #22d3ee;
            --emerald: #34d399;
            --amber: #fbbf24;
            --rose: #f87171;
            --purple: #a78bfa;
        }
        body {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
            color: #e2e8f0;
            font-family: 'Segoe UI', system-ui, sans-serif;
            min-height: 100vh;
        }
        .glass-panel {
            background: rgba(15, 23, 42, 0.7);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(34, 211, 238, 0.3);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        .module-card {
            background: rgba(30, 41, 59, 0.8);
            border-left: 4px solid;
            transition: all 0.3s ease;
        }
        .module-card:hover {
            transform: translateY(-2px);
        }
        .mirage-card { border-left-color: var(--cyan); }
        .cipher-card { border-left-color: var(--emerald); }
        .hub-card { border-left-color: var(--amber); }
        .guardian-card { border-left-color: var(--rose); }
        .resonance-card { border-left-color: var(--purple); }
        .gradient-text {
            background: linear-gradient(90deg, var(--cyan), var(--emerald));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        .pulse {
            animation: pulse 2s infinite;
        }
    </style>
</head>
<body class="p-4">
    <!-- Header -->
    <header class="mb-6 border-b border-cyan-500/30 pb-4">
        <h1 class="text-2xl font-black gradient-text mb-1">BRILLIANCE // EVOLVE-1</h1>
        <p class="text-cyan-300/80 text-sm">Sovereign Cognitive System</p>
        <div class="flex flex-wrap gap-2 mt-3 text-xs">
            <span class="px-2 py-1 bg-cyan-900/50 rounded">MirageCore</span>
            <span class="px-2 py-1 bg-emerald-900/50 rounded">CipherScreen</span>
            <span class="px-2 py-1 bg-amber-900/50 rounded">IntelliHub</span>
            <span class="px-2 py-1 bg-rose-900/50 rounded">GuardianAI</span>
            <span class="px-2 py-1 bg-purple-900/50 rounded">Resonance</span>
        </div>
    </header>

    <main class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">
        <!-- Left Column -->
        <div class="space-y-4">
            <!-- Brilliance Engine -->
            <div class="glass-panel p-4 rounded-lg">
                <h3 class="font-bold text-cyan-400 mb-3">Brilliance Engine</h3>
                <div class="text-center mb-3">
                    <div class="text-4xl font-black text-white mb-1" id="score-text">{{ metrics.score }}</div>
                    <div class="text-cyan-400 font-bold" id="status-text">{{ metrics.status }}</div>
                    <div class="text-xs text-gray-400 mt-1">Coherence: {{ metrics.coherence }}%</div>
                </div>
                <div class="grid grid-cols-2 gap-2 text-sm">
                    <div class="bg-gray-900/50 p-2 rounded">
                        <div class="text-gray-400">Entropy</div>
                        <div class="text-white font-medium">{{ metrics.entropy }}</div>
                    </div>
                    <div class="bg-gray-900/50 p-2 rounded">
                        <div class="text-gray-400">Flux</div>
                        <div class="text-white font-medium">{{ metrics.flux }}</div>
                    </div>
                </div>
            </div>

            <!-- Modules -->
            <div class="glass-panel p-4 rounded-lg">
                <h3 class="font-bold text-cyan-400 mb-3">Active Modules</h3>
                <div class="space-y-2">
                    {% for module in modules %}
                    <div class="module-card {{ module.class }} p-2 rounded">
                        <div class="flex justify-between">
                            <span class="font-medium text-sm">{{ module.name }}</span>
                            <span class="text-xs px-2 py-1 bg-green-900/30 rounded">{{ module.status }}</span>
                        </div>
                        <div class="text-xs text-gray-400 mt-1">{{ module.info }}</div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>

        <!-- Right Column -->
        <div class="lg:col-span-2 space-y-4">
            <!-- Logs -->
            <div class="glass-panel p-4 rounded-lg h-[300px] flex flex-col">
                <div class="flex justify-between items-center mb-3">
                    <h3 class="font-bold text-cyan-400">Evolution Log</h3>
                    <button onclick="clearLogs()" class="text-xs px-3 py-1 bg-rose-800/30 hover:bg-rose-700/30 rounded">
                        Clear
                    </button>
                </div>
                <div id="log-container" class="space-y-1 flex-grow overflow-y-auto pr-2">
                    {% for log in logs %}
                    <div class="bg-gray-900/30 p-2 rounded text-sm">
                        <div class="flex justify-between text-xs text-gray-400 mb-1">
                            <span>{{ log.timestamp.split('T')[1][:8] }}</span>
                            <span class="text-cyan-300">C:{{ log.coherence }} E:{{ log.entropy }}</span>
                        </div>
                        <div>{{ log.stimulus }}</div>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <!-- Input -->
            <div class="glass-panel p-4 rounded-lg">
                <h3 class="font-bold text-cyan-400 mb-3">Cognitive Input</h3>
                <div class="flex gap-3">
                    <input type="text" id="stimulus" 
                           class="bg-black border border-cyan-900 p-3 flex-grow text-cyan-300 rounded focus:outline-none focus:border-cyan-600"
                           placeholder="Enter stimulus..."
                           onkeypress="handleKeyPress(event)">
                    <button onclick="processStimulus()" 
                            class="bg-cyan-700 hover:bg-cyan-600 px-6 py-3 rounded font-bold uppercase text-sm whitespace-nowrap">
                        Process
                    </button>
                </div>
                <div class="mt-3 text-xs text-gray-400">
                    <p>Processing through: MirageCore, CipherScreen, IntelliHub, GuardianAI, ResonanceGraph</p>
                </div>
            </div>
        </div>
    </main>

    <!-- Status Bar -->
    <div class="glass-panel p-3 rounded-lg text-xs text-center text-gray-400">
        <div class="flex justify-between">
            <span>System: BRILLIANCE // EVOLVE-1 v1.0.0</span>
            <span id="connection-status" class="text-green-400">● Connected</span>
            <span>Logs: {{ logs|length }}</span>
        </div>
    </div>

    <script>
        async function processStimulus() {
            const input = document.getElementById('stimulus');
            const val = input.value.trim();
            
            if (!val) {
                alert('Please enter a stimulus');
                return;
            }
            
            try {
                const response = await fetch('/feed', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({stimulus: val})
                });
                
                if (!response.ok) throw new Error('Processing failed');
                
                const data = await response.json();
                
                // Update metrics
                document.getElementById('score-text').innerText = data.brilliance.score;
                document.getElementById('status-text').innerText = data.brilliance.status;
                
                // Add log entry
                const now = new Date().toISOString().split('T')[1].substring(0, 8);
                const logEntry = document.createElement('div');
                logEntry.className = 'bg-gray-900/30 p-2 rounded text-sm';
                logEntry.innerHTML = `
                    <div class="flex justify-between text-xs text-gray-400 mb-1">
                        <span>${now}</span>
                        <span class="text-cyan-300">C:${data.brilliance.coherence} E:${data.brilliance.entropy}</span>
                    </div>
                    <div>${val.length > 60 ? val.substring(0, 60) + '...' : val}</div>
                `;
                
                const logContainer = document.getElementById('log-container');
                logContainer.prepend(logEntry);
                
                // Limit logs
                while (logContainer.children.length > 8) {
                    logContainer.removeChild(logContainer.lastChild);
                }
                
                input.value = '';
                input.focus();
                
            } catch (error) {
                console.error('Error:', error);
                alert('Failed to process stimulus');
            }
        }
        
        function clearLogs() {
            if (confirm('Clear all logs?')) {
                document.getElementById('log-container').innerHTML = 
                    '<div class="text-center text-gray-500 py-4">Logs cleared</div>';
            }
        }
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                processStimulus();
            }
        }
        
        // Auto-focus input
        document.addEventListener('DOMContentLoaded', () => {
            document.getElementById('stimulus').focus();
        });
    </script>
</body>
</html>
"""

# ==================== ROUTES ====================

@app.get("/")
async def index():
    """Main dashboard"""
    metrics = engine._get_metrics()
    system_status = engine.get_system_status()
    
    modules_info = [
        {"name": "MirageCore", "class": "mirage-card", "status": "ACTIVE", 
         "info": f"State: {system_status['mirage']['state_dim']}D"},
        {"name": "CipherScreen", "class": "cipher-card", "status": "ACTIVE", 
         "info": f"Signals: {system_status['cipher']['total_signals']}"},
        {"name": "IntelliHub", "class": "hub-card", "status": "ACTIVE", 
         "info": f"Models: {system_status['intellihub']['total_models']}"},
        {"name": "GuardianAI", "class": "guardian-card", "status": system_status['guardian']['watch_level'], 
         "info": f"Watch: {system_status['guardian']['watch_level']}"},
        {"name": "Resonance", "class": "resonance-card", "status": "SCANNING", 
         "info": f"Connections: {system_status['resonance']['total_connections']}"}
    ]
    
    template = jinja2.Template(HTML_TEMPLATE)
    return HTMLResponse(content=template.render(
        metrics=metrics,
        logs=engine.get_recent_logs(6),
        modules=modules_info
    ))

@app.post("/feed")
async def feed_endpoint(data: Stimulus):
    """Process stimulus"""
    if not data.stimulus.strip():
        raise HTTPException(status_code=400, detail="Stimulus cannot be empty")
    
    result = await engine.feed(data.stimulus)
    return result

@app.get("/status")
async def get_status():
    """Get system status"""
    return engine.get_system_status()

@app.get("/health")
async def health_check():
    """Health check for Render"""
    return {
        "status": "healthy",
        "service": "BRILLIANCE // EVOLVE-1",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "coherence": engine.state.field_pulse["coherence"],
        "modules": 6
    }

@app.get("/logs")
async def get_logs():
    """Get recent logs"""
    return {"logs": engine.get_recent_logs(10)}

@app.get("/reset")
async def reset_system():
    """Reset the system (for testing)"""
    global engine
    engine = BrillianceEngine()
    return {"status": "reset", "message": "System reinitialized"}

# ==================== STARTUP ====================

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    print(f"\n{'='*60}")
    print("BRILLIANCE // EVOLVE-1 - STARTING UP")
    print(f"{'='*60}")

# ==================== MAIN ====================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"\n{'='*60}")
    print(f"BRILLIANCE // EVOLVE-1")
    print(f"{'='*60}")
    print(f"Local URL: http://localhost:{port}")
    print(f"Health: http://localhost:{port}/health")
    print(f"Status: http://localhost:{port}/status")
    print(f"\nReady to receive stimuli...")
    print(f"{'='*60}\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
