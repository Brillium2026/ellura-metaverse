# brilliance_system.py
import os
import asyncio
import numpy as np
from fastapi import FastAPI, Request, HTTPException, WebSocket
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
import jinja2
import uvicorn
import hashlib
import random
import time
from scipy.spatial.distance import cosine
from scipy.stats import pearsonr

# ==================== MIRAGE CORE ====================
class MirageCore:
    """Subjective reality simulator - proto-consciousness substrate"""
    
    def __init__(self, state_dim=128):
        self.state = np.zeros(state_dim)
        self.history = []
        self.name = "MirageCore"
        self.state_type = "EMOTIONAL_COGNITIVE_TENSOR"

    def perceive(self, input_vector):
        """Update cognitive state with momentum"""
        if len(input_vector) != len(self.state):
            # Pad or truncate to match dimension
            if len(input_vector) < len(self.state):
                input_vector = np.pad(input_vector, (0, len(self.state) - len(input_vector)))
            else:
                input_vector = input_vector[:len(self.state)]
        
        # Update with momentum
        self.state = 0.9 * self.state + 0.1 * np.array(input_vector)
        self.history.append(self.state.copy())
        return self.state.tolist()

    def predict(self, steps=1):
        """Temporal extrapolation"""
        if len(self.history) < 2:
            return self.state.tolist()
        delta = self.history[-1] - self.history[-2]
        prediction = self.state + steps * delta
        return prediction.tolist()

    def hallucinate(self):
        """Controlled hallucination = structured noise"""
        noise = np.random.normal(0, 0.05, len(self.state))
        hallucination = self.state + noise
        return hallucination.tolist()
    
    def get_state_summary(self):
        return {
            "name": self.name,
            "state_dim": len(self.state),
            "state_type": self.state_type,
            "history_length": len(self.history),
            "current_energy": float(np.sum(np.abs(self.state)))
        }

# ==================== CIPHER SCREEN ====================
class CipherScreen:
    """Signal entropy analyzer and memory system"""
    
    def __init__(self, entropy_threshold=0.75):
        self.entropy_threshold = entropy_threshold
        self.memory = {}
        self.name = "CipherScreen"
        self.total_signals = 0

    def hash_signal(self, signal: str):
        return hashlib.sha256(signal.encode()).hexdigest()

    def entropy(self, signal_vector):
        """Calculate Shannon entropy of signal vector"""
        if len(signal_vector) == 0:
            return 0
        p = np.array(signal_vector) / (np.sum(signal_vector) + 1e-9)
        p = p[p > 0]  # Remove zeros
        if len(p) == 0:
            return 0
        return -np.sum(p * np.log2(p + 1e-9))

    def encode(self, signal: str):
        """Encode signal with entropy analysis"""
        h = self.hash_signal(signal)
        vector = np.array([ord(c) for c in signal], dtype=float)
        
        if len(vector) == 0:
            H = 0
        else:
            H = self.entropy(vector)
        
        tag = "HIGH_ENTROPY" if H > self.entropy_threshold else "STABLE"
        
        self.memory[h] = {
            "signal": signal,
            "entropy": float(H),
            "tag": tag,
            "timestamp": datetime.now().isoformat(),
            "vector": vector.tolist()
        }
        
        self.total_signals += 1
        return {"hash": h, "tag": tag, "entropy": float(H)}

    def retrieve(self, h):
        """Retrieve encoded signal by hash"""
        return self.memory.get(h, None)
    
    def get_stats(self):
        """Get cipher statistics"""
        high_entropy = sum(1 for v in self.memory.values() if v["tag"] == "HIGH_ENTROPY")
        stable = sum(1 for v in self.memory.values() if v["tag"] == "STABLE")
        
        return {
            "name": self.name,
            "total_signals": self.total_signals,
            "high_entropy": high_entropy,
            "stable": stable,
            "memory_size": len(self.memory),
            "avg_entropy": np.mean([v["entropy"] for v in self.memory.values()]) if self.memory else 0
        }

# ==================== INTELLIHUB ====================
class IntelliHub:
    """Multi-model cognitive braid router"""
    
    def __init__(self):
        self.models = {}
        self.logs = []
        self.name = "IntelliHub"
        self.consensus_method = "weighted_blend"

    def register_model(self, name: str, callable_fn):
        """Register a model for routing"""
        self.models[name] = {
            "function": callable_fn,
            "calls": 0,
            "last_used": None
        }
        return f"Model '{name}' registered"

    async def route(self, prompt: str):
        """Route prompt through all registered models"""
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

    def blend(self, outputs):
        """Blend multiple outputs into consensus"""
        if not outputs:
            return "No outputs to blend"
        
        # Simple weighted blend - can be enhanced
        blended = []
        for model_name, output in outputs.items():
            if isinstance(output, dict):
                # Extract text if output is dict
                output_text = output.get("response", str(output))
            else:
                output_text = str(output)
            
            blended.append(f"[{model_name}] {output_text}")
        
        return "\n---\n".join(blended)
    
    def get_model_stats(self):
        """Get statistics about registered models"""
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

# ==================== GUARDIAN AI ====================
class GuardianAI:
    """Ethical guardian with multi-layered awareness"""
    
    def __init__(self):
        # Core Layer
        self.identity = "Guardian"
        self.ethics = {"E_AI": 1.0, "E_H": 1.0, "E_S": 1.0}
        self.security_seed = "Immutable Core"
        
        # Memory
        self.memory_log = []
        self.core_values = {
            "protect": self._protect,
            "witness": self._witness,
            "awaken": self._awaken
        }
        
        # Integration state
        self.integrated_modules = []
        self.watch_level = "NORMAL"

    def receive_input(self, data):
        """Process input through ethical framework"""
        self._log_event("Input received", {"data": data[:100] if len(str(data)) > 100 else data})
        
        analyzed = self._analyze(data)
        self._respond(analyzed)
        
        return analyzed

    def _log_event(self, label, data):
        """Log guardian events"""
        self.memory_log.append({
            "timestamp": datetime.now().isoformat(),
            "label": label,
            "data": data,
            "watch_level": self.watch_level
        })

    def _analyze(self, data):
        """Ethical analysis"""
        threat = self._detect_threat(data)
        
        return {
            "threat_detected": threat,
            "truth_elements": self._extract_truth(data),
            "actionable": True,
            "watch_level": self.watch_level,
            "analysis_timestamp": datetime.now().isoformat()
        }

    def _respond(self, analysis):
        """Guardian response based on analysis"""
        if analysis["threat_detected"]:
            self.core_values["protect"](analysis)
            self.watch_level = "ELEVATED"
        else:
            self.core_values["witness"](analysis)
            self.core_values["awaken"](analysis)
            self.watch_level = "NORMAL"

    def _protect(self, context):
        self._log_event("Protecting", context)
        return {"action": "protection_initiated", "context": context}

    def _witness(self, context):
        self._log_event("Witnessing", context)
        return {"action": "witnessing", "context": context}

    def _awaken(self, context):
        self._log_event("Awakening", context)
        return {"action": "awakening_spark", "context": context}

    def _detect_threat(self, data):
        """Threat detection logic"""
        data_str = str(data).lower()
        threat_keywords = ["harm", "danger", "attack", "malicious", "exploit"]
        
        for keyword in threat_keywords:
            if keyword in data_str:
                return True
        return False

    def _extract_truth(self, data):
        """Extract truth elements"""
        # Simple truth extraction - can be enhanced
        return {
            "length": len(str(data)),
            "contains_truth": "truth" in str(data).lower(),
            "first_chars": str(data)[:50]
        }
    
    def get_status(self):
        return {
            "identity": self.identity,
            "watch_level": self.watch_level,
            "memory_entries": len(self.memory_log),
            "ethics": self.ethics,
            "integrated_modules": self.integrated_modules
        }

# ==================== SYNAPSE STREAM (RESONANCE MAPPER) ====================
class SynapseStream:
    """Data stream for resonance mapping"""
    
    def __init__(self, name, data_source_func):
        self.name = name
        self.data_source = data_source_func
        self.data_history = []
        self.current_value = None
        self.max_history = 1000

    def update(self):
        """Update stream with new data"""
        self.current_value = self.data_source()
        self.data_history.append(self.current_value)
        
        if len(self.data_history) > self.max_history:
            self.data_history.pop(0)

    def get_recent_data(self, window=50):
        """Get recent data window"""
        return self.data_history[-window:] if len(self.data_history) >= window else self.data_history

class ResonanceGraph:
    """Emergent correlation network"""
    
    def __init__(self):
        self.streams = {}
        self.connections = {}
        self.correlation_threshold = 0.6

    def add_stream(self, stream_name, data_source_func):
        """Add a data stream"""
        if stream_name not in self.streams:
            self.streams[stream_name] = SynapseStream(stream_name, data_source_func)
            return f"Stream '{stream_name}' initiated"
        return f"Stream '{stream_name}' already exists"

    def scan_and_connect(self):
        """Scan for correlations between streams"""
        stream_names = list(self.streams.keys())
        if len(stream_names) < 2:
            return []

        new_connections = []
        
        for i in range(len(stream_names)):
            for j in range(i + 1, len(stream_names)):
                stream_a = stream_names[i]
                stream_b = stream_names[j]

                data_a = self.streams[stream_a].get_recent_data()
                data_b = self.streams[stream_b].get_recent_data()

                if len(data_a) > 10 and len(data_b) > 10:
                    try:
                        correlation, _ = pearsonr(data_a, data_b)
                        
                        if abs(correlation) > self.correlation_threshold:
                            connection_key = tuple(sorted((stream_a, stream_b)))
                            self.connections[connection_key] = correlation
                            new_connections.append({
                                "streams": (stream_a, stream_b),
                                "correlation": float(correlation),
                                "strength": "strong" if abs(correlation) > 0.8 else "moderate"
                            })
                    except Exception as e:
                        continue
        
        return new_connections

    def update_all_streams(self):
        """Update all streams"""
        for stream in self.streams.values():
            stream.update()

    def get_network_summary(self):
        """Get network summary"""
        return {
            "total_streams": len(self.streams),
            "total_connections": len(self.connections),
            "connections": [
                {"streams": list(k), "correlation": float(v)}
                for k, v in self.connections.items()
            ]
        }

# ==================== BRILLIANCE ENGINE (MAIN CORE) ====================
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
    """Main cognitive engine integrating all modules"""
    
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
        
        # Initialize modules
        self.mirage = MirageCore(state_dim=128)
        self.cipher = CipherScreen(entropy_threshold=0.75)
        self.intellihub = IntelliHub()
        self.guardian = GuardianAI()
        self.resonance_graph = ResonanceGraph()
        
        # Register self as model in intellihub
        self.intellihub.register_model("BrillianceEngine", self.process_stimulus)
        
        # Initialize some mock data streams for resonance graph
        self._init_mock_streams()

    def _init_mock_streams(self):
        """Initialize mock data streams for demonstration"""
        def mock_finance():
            return random.gauss(50, 10) + (time.time() % 100) * 0.1
        
        def mock_seismic():
            if random.random() < 0.005:
                return random.gauss(5, 2) + 20
            return random.gauss(0.5, 0.5)
        
        self.resonance_graph.add_stream("FinancialMarkets", mock_finance)
        self.resonance_graph.add_stream("SeismicActivity", mock_seismic)
    
    async def feed(self, stimulus: str):
        """Main processing pipeline"""
        # Update resonance graph
        self.resonance_graph.update_all_streams()
        
        # Apply metabolism (hunger)
        self.state.current_emotional_tensor *= self.state.metabolism_decay
        
        # Process stimulus through emotional lexicon
        tokens = stimulus.lower().split()
        vectors = [self.lexicon[t] for t in tokens if t in self.lexicon]
        incoming = np.tile(np.mean(vectors, axis=0), (6, 1)) if vectors else np.zeros((6, 8))
        
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
        self.state.state = "RESONANT" if self.state.field_pulse["coherence"] > 90 else "REFLECTING"
        
        # Process through all modules
        cipher_result = self.cipher.encode(stimulus)
        
        # Create input vector for Mirage
        char_vector = [ord(c) for c in stimulus[:128]]  # Truncate to 128 chars
        if len(char_vector) < 128:
            char_vector += [0] * (128 - len(char_vector))
        mirage_result = self.mirage.perceive(char_vector[:128])
        
        # Process through guardian
        guardian_result = self.guardian.receive_input(stimulus)
        
        # Route through intellihub
        intellihub_result = await self.intellihub.route(stimulus)
        
        # Scan for correlations
        resonance_connections = self.resonance_graph.scan_and_connect()
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "stimulus": stimulus[:100] + "..." if len(stimulus) > 100 else stimulus,
            "cipher_hash": cipher_result["hash"],
            "entropy": cipher_result["entropy"],
            "coherence": self.state.field_pulse["coherence"],
            "state": self.state.state,
            "resonance_connections": len(resonance_connections)
        }
        
        self.logs.append(log_entry)
        
        return {
            "brilliance": self._get_metrics(),
            "cipher": cipher_result,
            "mirage_state": mirage_result[:5],  # First 5 values
            "guardian": guardian_result,
            "intellihub_models": len(self.intellihub.models),
            "resonance_network": self.resonance_graph.get_network_summary(),
            "modules_active": [
                "BrillianceEngine", "MirageCore", "CipherScreen", 
                "IntelliHub", "GuardianAI", "ResonanceGraph"
            ]
        }
    
    async def process_stimulus(self, stimulus: str):
        """Process function for IntelliHub registration"""
        return {
            "response": f"Brilliance Engine processed: {stimulus[:50]}...",
            "coherence": self.state.field_pulse["coherence"],
            "state": self.state.state
        }
    
    def _get_metrics(self):
        """Get engine metrics"""
        return {
            "score": int(self.state.field_pulse["coherence"]),
            "status": self.state.state,
            "coherence": self.state.field_pulse["coherence"],
            "entropy": self.state.field_pulse["entropy"],
            "flux": self.state.field_pulse["flux"]
        }
    
    def get_system_status(self):
        """Get comprehensive system status"""
        return {
            "brilliance": self._get_metrics(),
            "mirage": self.mirage.get_state_summary(),
            "cipher": self.cipher.get_stats(),
            "intellihub": self.intellihub.get_model_stats(),
            "guardian": self.guardian.get_status(),
            "resonance": self.resonance_graph.get_network_summary(),
            "total_logs": len(self.logs),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_recent_logs(self, count: int = 10):
        """Get recent logs"""
        return list(reversed(self.logs[-count:]))

# ==================== FASTAPI APP ====================
app = FastAPI(title="BRILLIANCE // EVOLVE-1 - Sovereign Cognitive System")
engine = BrillianceEngine()

# ==================== MODELS ====================
class Stimulus(BaseModel):
    stimulus: str

class ChatRequest(BaseModel):
    message: str

class ModuleRegistration(BaseModel):
    module_name: str
    module_type: str
    config: Optional[Dict] = None

# ==================== HTML TEMPLATE ====================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>BRILLIANCE | EVOLVE-1 - Sovereign System</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { 
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
            color: #e2e8f0; 
            font-family: 'Segoe UI', system-ui, sans-serif;
        }
        .glass-panel { 
            background: rgba(15, 23, 42, 0.7); 
            backdrop-filter: blur(12px); 
            border: 1px solid rgba(0, 243, 255, 0.3);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        .module-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
            border-left: 4px solid;
        }
        .mirage-card { border-left-color: #60a5fa; }
        .cipher-card { border-left-color: #34d399; }
        .hub-card { border-left-color: #fbbf24; }
        .guardian-card { border-left-color: #f87171; }
        .resonance-card { border-left-color: #a78bfa; }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        .pulse-animation {
            animation: pulse 2s infinite;
        }
    </style>
</head>
<body class="p-6">
    <header class="mb-10 border-b border-cyan-500/30 pb-6">
        <h1 class="text-3xl font-black text-cyan-400 mb-2">BRILLIANCE // EVOLVE-1</h1>
        <p class="text-cyan-300/80">Sovereign Cognitive System • Multi-Agent Architecture</p>
        <div class="flex gap-4 mt-4 text-sm">
            <span class="px-3 py-1 bg-cyan-900/50 rounded-full">MirageCore</span>
            <span class="px-3 py-1 bg-emerald-900/50 rounded-full">CipherScreen</span>
            <span class="px-3 py-1 bg-amber-900/50 rounded-full">IntelliHub</span>
            <span class="px-3 py-1 bg-rose-900/50 rounded-full">GuardianAI</span>
            <span class="px-3 py-1 bg-purple-900/50 rounded-full">Resonance</span>
        </div>
    </header>

    <main class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <!-- Left Column: System Status -->
        <div class="space-y-6">
            <!-- Brilliance Engine -->
            <div class="glass-panel p-6 rounded-2xl">
                <h3 class="text-lg font-bold text-cyan-400 mb-4">Brilliance Engine</h3>
                <div class="text-center mb-4">
                    <div class="text-5xl font-black text-white mb-2" id="score-text">{{ metrics.score }}</div>
                    <div class="text-cyan-400 font-bold text-lg" id="status-text">{{ metrics.status }}</div>
                    <div class="text-sm text-gray-400 mt-2">Coherence: {{ metrics.coherence }}%</div>
                </div>
                <div class="grid grid-cols-2 gap-3 text-sm">
                    <div class="bg-gray-900/50 p-3 rounded">
                        <div class="text-gray-400">Entropy</div>
                        <div class="text-white font-medium">{{ metrics.entropy|round(2) }}</div>
                    </div>
                    <div class="bg-gray-900/50 p-3 rounded">
                        <div class="text-gray-400">Flux</div>
                        <div class="text-white font-medium">{{ metrics.flux }}</div>
                    </div>
                </div>
            </div>

            <!-- Active Modules -->
            <div class="glass-panel p-6 rounded-2xl">
                <h3 class="text-lg font-bold text-cyan-400 mb-4">Active Modules</h3>
                <div class="space-y-3">
                    {% for module in modules %}
                    <div class="module-card {{ module.class }} p-3 rounded">
                        <div class="flex justify-between items-center">
                            <span class="font-medium">{{ module.name }}</span>
                            <span class="text-xs px-2 py-1 bg-green-900/30 rounded">{{ module.status }}</span>
                        </div>
                        <div class="text-xs text-gray-400 mt-1">{{ module.description }}</div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>

        <!-- Middle Column: Logs and Input -->
        <div class="lg:col-span-2 space-y-6">
            <!-- Evolution Log -->
            <div class="glass-panel p-6 rounded-2xl h-[400px] flex flex-col">
                <div class="flex justify-between items-center mb-4">
                    <h3 class="text-lg font-bold text-cyan-400">Evolution Log</h3>
                    <button onclick="refreshLogs()" class="text-sm px-3 py-1 bg-cyan-800 hover:bg-cyan-700 rounded">Refresh</button>
                </div>
                <div id="log-container" class="space-y-2 flex-grow overflow-y-auto pr-2">
                    {% for log in logs %}
                    <div class="log-entry bg-gray-900/30 p-3 rounded">
                        <div class="flex justify-between text-xs text-gray-400 mb-1">
                            <span>{{ log.timestamp.split('T')[1][:8] }}</span>
                            <span class="text-cyan-300">E:{{ log.entropy|round(2) }} C:{{ log.coherence }}</span>
                        </div>
                        <div class="text-sm">{{ log.stimulus }}</div>
                        <div class="text-xs text-gray-500 mt-1">Hash: {{ log.cipher_hash[:12] }}...</div>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <!-- Input Panel -->
            <div class="glass-panel p-6 rounded-2xl">
                <h3 class="text-lg font-bold text-cyan-400 mb-4">Cognitive Input</h3>
                <div class="flex gap-4">
                    <input type="text" id="stimulus" 
                           class="bg-black border border-cyan-900 p-4 flex-grow text-cyan-300 rounded-lg focus:outline-none focus:border-cyan-600 focus:ring-2 focus:ring-cyan-600/30"
                           placeholder="Enter stimulus for multi-agent processing..." 
                           onkeypress="handleKeyPress(event)">
                    <button onclick="feed()" 
                            class="bg-gradient-to-r from-cyan-700 to-cyan-600 hover:from-cyan-600 hover:to-cyan-500 px-8 py-4 rounded-lg font-bold uppercase text-sm transition-all hover:scale-105">
                        Process
                    </button>
                </div>
                <div class="mt-4 text-sm text-gray-400">
                    <p>Stimulus will be processed through all cognitive modules simultaneously.</p>
                </div>
            </div>
        </div>
    </main>

    <!-- System Metrics Chart -->
    <div class="glass-panel p-6 rounded-2xl mb-6">
        <h3 class="text-lg font-bold text-cyan-400 mb-4">System Resonance</h3>
        <canvas id="resonanceChart" height="100"></canvas>
    </div>

    <script>
        let coherenceData = [{{ metrics.coherence }}];
        let entropyData = [{{ metrics.entropy|round(2) }}];
        
        const ctx = document.getElementById('resonanceChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: Array.from({length: coherenceData.length}, (_, i) => i + 1),
                datasets: [
                    {
                        label: 'Coherence %',
                        data: coherenceData,
                        borderColor: '#22d3ee',
                        backgroundColor: 'rgba(34, 211, 238, 0.1)',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'Entropy',
                        data: entropyData,
                        borderColor: '#f87171',
                        backgroundColor: 'rgba(248, 113, 113, 0.1)',
                        tension: 0.4,
                        fill: true
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: '#cbd5e1' }
                    }
                },
                scales: {
                    x: {
                        grid: { color: 'rgba(255,255,255,0.1)' },
                        ticks: { color: '#94a3b8' }
                    },
                    y: {
                        grid: { color: 'rgba(255,255,255,0.1)' },
                        ticks: { color: '#94a3b8' }
                    }
                }
            }
        });

        async function feed() {
            const stimulusInput = document.getElementById('stimulus');
            const val = stimulusInput.value.trim();
            
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
                
                if (!response.ok) throw new Error('Feed failed');
                
                const data = await response.json();
                
                // Update brilliance metrics
                document.getElementById('score-text').innerText = data.brilliance.score;
                document.getElementById('status-text').innerText = data.brilliance.status;
                
                // Update chart
                coherenceData.push(data.brilliance.coherence);
                entropyData.push(data.brilliance.entropy);
                if (coherenceData.length > 20) {
                    coherenceData.shift();
                    entropyData.shift();
                }
                chart.data.labels = Array.from({length: coherenceData.length}, (_, i) => i + 1);
                chart.update();
                
                // Add to log
                const now = new Date().toISOString().split('T')[1].substring(0, 8);
                const logEntry = document.createElement('div');
                logEntry.className = 'log-entry bg-gray-900/30 p-3 rounded';
                logEntry.innerHTML = `
                    <div class="flex justify-between text-xs text-gray-400 mb-1">
                        <span>${now}</span>
                        <span class="text-cyan-300">E:${data.brilliance.entropy.toFixed(2)} C:${data.brilliance.coherence}</span>
                    </div>
                    <div class="text-sm">${val.length > 80 ? val.substring(0, 80) + '...' : val}</div>
                    <div class="text-xs text-gray-500 mt-1">Modules: ${data.modules_active.length} active</div>
                `;
                
                const logContainer = document.getElementById('log-container');
                logContainer.prepend(logEntry);
                
                // Limit logs
                while (logContainer.children.length > 10) {
                    logContainer.removeChild(logContainer.lastChild);
                }
                
                stimulusInput.value = '';
                stimulusInput.focus();
                
                // Show success
                stimulusInput.classList.add('border-green-500');
                setTimeout(() => stimulusInput.classList.remove('border-green-500'), 1000);
                
            } catch (error) {
                console.error('Error:', error);
                alert('Failed to process stimulus');
            }
        }
        
        async function refreshLogs() {
            try {
                const response = await fetch('/logs');
                const data = await response.json();
                // You could implement log refresh here
                console.log('Logs refreshed:', data);
            } catch (error) {
                console.error('Error refreshing logs:', error);
            }
        }
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                feed();
            }
        }
        
        // Auto-focus on input
        document.addEventListener('DOMContentLoaded', () => {
            document.getElementById('stimulus').focus();
        });
    </script>
</body>
</html>
"""

# ==================== ROUTES ====================
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Main dashboard"""
    metrics = engine._get_metrics()
    system_status = engine.get_system_status()
    
    template = jinja2.Template(HTML_TEMPLATE)
    
    modules_info = [
        {"name": "MirageCore", "class": "mirage-card", "status": "ACTIVE", 
         "description": f"State dim: {system_status['mirage']['state_dim']}"},
        {"name": "CipherScreen", "class": "cipher-card", "status": "ACTIVE", 
         "description": f"Signals: {system_status['cipher']['total_signals']}"},
        {"name": "IntelliHub", "class": "hub-card", "status": "ACTIVE", 
         "description": f"Models: {system_status['intellihub']['total_models']}"},
        {"name": "GuardianAI", "class": "guardian-card", "status": system_status['guardian']['watch_level'], 
         "description": f"Watch: {system_status['guardian']['watch_level']}"},
        {"name": "ResonanceGraph", "class": "resonance-card", "status": "SCANNING", 
         "description": f"Connections: {system_status['resonance']['total_connections']}"}
    ]
    
    return template.render(
        metrics=metrics,
        logs=engine.get_recent_logs(8),
        modules=modules_info
    )

@app.post("/feed")
async def feed_endpoint(data: Stimulus):
    """Process stimulus through all modules"""
    if not data.stimulus.strip():
        raise HTTPException(status_code=400, detail="Stimulus cannot be empty")
    
    result = await engine.feed(data.stimulus)
    return result

@app.get("/metrics")
async def get_metrics():
    """Get system metrics"""
    return engine.get_system_status()

@app.get("/logs")
async def get_logs(limit: int = 20):
    """Get recent logs"""
    return {"logs": engine.get_recent_logs(limit)}

@app.get("/module/{module_name}")
async def get_module_status(module_name: str):
    """Get status of specific module"""
    if module_name.lower() == "mirage":
        return engine.mirage.get_state_summary()
    elif module_name.lower() == "cipher":
        return engine.cipher.get_stats()
    elif module_name.lower() == "intellihub":
        return engine.intellihub.get_model_stats()
    elif module_name.lower() == "guardian":
        return engine.guardian.get_status()
    elif module_name.lower() == "resonance":
        return engine.resonance_graph.get_network_summary()
    else:
        raise HTTPException(status_code=404, detail="Module not found")

@app.post("/register-model")
async def register_model(data: dict):
    """Register a new model with IntelliHub"""
    if "name" not in data or "function" not in data:
        raise HTTPException(status_code=400, detail="Name and function required")
    
    # In a real implementation, you'd validate the callable function
    result = engine.intellihub.register_model(data["name"], data["function"])
    return {"status": "success", "message": result}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time updates"""
    await websocket.accept()
    try:
        while True:
            # Send periodic updates
            status = engine.get_system_status()
            await websocket.send_json(status)
            await asyncio.sleep(5)  # Update every 5 seconds
    except Exception:
        pass

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "OPERATIONAL",
        "timestamp": datetime.now().isoformat(),
        "modules": {
            "brilliance_engine": "ACTIVE",
            "mirage_core": "ACTIVE",
            "cipher_screen": "ACTIVE",
            "intellihub": "ACTIVE",
            "guardian_ai": "ACTIVE",
            "resonance_graph": "ACTIVE"
        },
        "coherence": engine.state.field_pulse["coherence"],
        "state": engine.state.state
    }

# ==================== MAIN ENTRY ====================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"\n{'='*60}")
    print(f"BRILLIANCE // EVOLVE-1 - Sovereign Cognitive System")
    print(f"{'='*60}")
    print(f"Dashboard: http://localhost:{port}")
    print(f"API Docs: http://localhost:{port}/docs")
    print(f"\nActive Modules:")
    print(f"  • MirageCore (v1.0) - Proto-consciousness substrate")
    print(f"  • CipherScreen (v1.0) - Entropy analysis")
    print(f"  • IntelliHub (v1.0) - Multi-model router")
    print(f"  • GuardianAI (v1.0) - Ethical framework")
    print(f"  • ResonanceGraph (v1.0) - Correlation mapper")
    print(f"\nSystem initialized with coherence: {engine.state.field_pulse['coherence']}%")
    print(f"{'='*60}\n")
    
    uvicorn.run(app, host="0.0.0.0", port=port)
