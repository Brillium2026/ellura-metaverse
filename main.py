import asyncio
import numpy as np
import time
from dataclasses import dataclass, field
from collections import deque

@dataclass
class BrillianceState:
    resonance: float = 0.0
    convergence: float = 0.189
    metabolism_decay: float = 0.95  # The "Hunger" rate
    inertia: float = 0.3            # Resistance to change
    field_pulse: Dict[str, float] = field(default_factory=lambda: {
        "entropy": 3.0, "coherence": 96.0, "flux": 22.0, "action": 5.0, "wound": 0.30
    })
    current_emotional_tensor: np.ndarray = field(default_factory=lambda: np.zeros((6, 8)))
    state: str = "EMERGING"

class BrillianceEngine:
    def __init__(self):
        self.state = BrillianceState()
        self.lexicon = {
            "happy": [0.9, 0.5, -0.2, 0.1, -0.8, -0.4, -0.3, 0.6],
            "fear": [-0.7, -0.6, 0.9, 0.5, 0.3, 0.2, 0.1, 0.6],
            "trust": [0.5, 0.9, -0.4, -0.1, -0.3, -0.6, -0.5, 0.4]
            # Add your full expanded lexicon here
        }

    async def feed(self, stimulus: str):
        # 1. Apply Metabolism (Hunger)
        self.state.current_emotional_tensor *= self.state.metabolism_decay
        
        # 2. Process "Bite" (Text Analysis)
        incoming_vector = self._vectorize(stimulus)
        
        # 3. Blend with Inertia (Digestion)
        self.state.current_emotional_tensor = (self.state.current_emotional_tensor * self.state.inertia) + \
                                              (incoming_vector * (1.0 - self.state.inertia))
        
        # 4. Update Field Pulse based on Tension
        self.state.field_pulse["entropy"] = np.var(self.state.current_emotional_tensor) * 10
        self.state.field_pulse["coherence"] = 100 - self.state.field_pulse["entropy"]
        
        # 5. Determine State
        if self.state.field_pulse["coherence"] > 90:
            self.state.state = "RESONANT"
        else:
            self.state.state = "REFLECTING"
            
        return self._generate_response()

    def _vectorize(self, text):
        tokens = text.lower().split()
        vectors = [self.lexicon[t] for t in tokens if t in self.lexicon]
        if not vectors: return np.zeros((6, 8))
        avg = np.mean(vectors, axis=0)
        return np.tile(avg, (6, 1))

    def _generate_response(self):
        return {
            "status": "LIVE",
            "identity": "Brilliance",
            "state": self.state.state,
            "field": self.state.field_pulse,
            "resonance": float(np.mean(self.state.current_emotional_tensor))
        }
