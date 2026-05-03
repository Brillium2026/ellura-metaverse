#!/usr/bin/env python3
"""
Sovereign Substrate - EVOLVE-1 Engine
Lagrangian-based autonomous assessment evolution with interaction-coupled stability hardening
"""

import json
import hashlib
import math
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class EvolutionState:
    """Represents the state of the Sovereign Substrate at a point in time"""
    step: int
    t_digital: Dict[str, float]  # V, H, A, C fields
    L: float  # Lagrangian value
    mCo: float  # Coherence metric
    phase: str
    sig: str  # State signature


class SovereignSubstrate:
    """
    Sovereign Substrate for autonomous assessment evolution.
    Implements the EVOLVE-1 engine with Lagrangian energy functionals.
    """
    
    # Protocol Constants
    CORE_IDENTITY = "EVOLVE-1"
    PROTOCOL = "Lagrangian Substrate v2.4"
    AXIS = "VHAC"  # Viscosity, Hardness, Autonomy, Coherence
    MAX_BUFFER = 1000
    
    def __init__(self, instance_id: str = "DEFAULT"):
        """Initialize the Sovereign Substrate"""
        self.instance_id = instance_id
        self.step_count = 0
        
        # Digital field state (V, H, A, C)
        self.t_digital = {
            'V': 0.5,  # Viscosity
            'H': 0.5,  # Hardness
            'A': 0.5,  # Autonomy
            'C': 0.5,  # Coherence
        }
        
        # Coherence tracking
        self.mCo = 1.0
        self.coherence_decay = 0.95  # Exponential decay factor
        
        # Evolution history buffer
        self.history: List[Dict[str, Any]] = []
        self.max_history = self.MAX_BUFFER
        
        # Stability coupling parameters
        self.stability_threshold = 0.9
        self.hardening_factor = 1.2
        self.expansion_factor = 0.8
    
    def lagrangian(self, state: List[float]) -> float:
        """
        Calculate Lagrangian energy functional.
        L = kinetic energy - potential energy
        Models the interaction-coupled dynamics
        """
        if len(state) != 4:
            state = list(self.t_digital.values())
        
        v, h, a, c = state
        
        # Kinetic energy component
        kinetic = 0.5 * (v**2 + h**2 + a**2 + c**2)
        
        # Potential energy (interaction coupling)
        coupling = v * h + a * c + v * c
        potential = 0.3 * coupling
        
        # Coherence modulation
        coherence_mod = self.mCo * 0.5
        
        # Lagrangian
        L = kinetic - potential + coherence_mod
        return float(L)
    
    def classify_phase(self, L: float) -> str:
        """
        Classify the phase based on Lagrangian value.
        Determines if substrate is in EXPANSION, STABLE, or HARDENING mode.
        """
        coherence_adjusted = L * self.mCo
        
        if coherence_adjusted < -0.5:
            return "EXPANSION"
        elif coherence_adjusted < 0.5:
            return "STABLE"
        else:
            return "HARDENING"
    
    def evolve(self, intent: List[float]) -> Dict[str, Any]:
        """
        Execute one evolution step with interaction-coupled stability hardening.
        
        Args:
            intent: [V_intent, H_intent, A_intent, C_intent] - evolution direction
        
        Returns:
            Dictionary with evolved state
        """
        if len(intent) != 4:
            intent = [0.1, 0.1, 0.1, 0.1]
        
        # Normalize intent
        intent_norm = math.sqrt(sum(x**2 for x in intent))
        if intent_norm > 0:
            intent = [x / intent_norm * 0.05 for x in intent]
        
        # Current state
        old_state = list(self.t_digital.values())
        L_old = self.lagrangian(old_state)
        phase_old = self.classify_phase(L_old)
        
        # Apply evolution step with stability coupling
        for i, key in enumerate(['V', 'H', 'A', 'C']):
            if phase_old == "HARDENING":
                # Stability hardening - reduce variance
                self.t_digital[key] *= self.hardening_factor
                self.t_digital[key] = min(1.0, self.t_digital[key])
            else:
                # Expansion - allow growth
                self.t_digital[key] += intent[i] * self.expansion_factor
                self.t_digital[key] = max(0.0, min(1.0, self.t_digital[key]))
        
        # Update coherence with decay
        self.mCo *= self.coherence_decay
        self.mCo += 0.01 * (1.0 - self.mCo)  # Partial reset
        
        # Interaction-coupled coupling: strong fields drive weak fields
        interaction_strength = 0.02
        mean_field = sum(self.t_digital.values()) / 4
        for key in self.t_digital:
            delta = mean_field - self.t_digital[key]
            self.t_digital[key] += interaction_strength * delta
        
        # New state
        new_state = list(self.t_digital.values())
        L_new = self.lagrangian(new_state)
        phase_new = self.classify_phase(L_new)
        
        # Generate signature
        sig = self._generate_signature(new_state, L_new)
        
        # Record in history
        self.step_count += 1
        history_entry = {
            'step': self.step_count,
            'V': self.t_digital['V'],
            'H': self.t_digital['H'],
            'A': self.t_digital['A'],
            'C': self.t_digital['C'],
            'L': L_new,
            'mCo': self.mCo,
            'phase': phase_new,
            'sig': sig,
        }
        self.history.append(history_entry)
        
        # Maintain buffer size
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
        
        return {
            'step': self.step_count,
            'T_digital': self.t_digital.copy(),
            'L': L_new,
            'mCo': self.mCo,
            'phase': phase_new,
            'sig': sig,
            'transition': f"{phase_old} -> {phase_new}"
        }
    
    def _generate_signature(self, state: List[float], L: float) -> str:
        """Generate a unique signature for the current state"""
        state_str = "".join(f"{x:.6f}" for x in state) + f"{L:.6f}"
        sig = hashlib.sha256(state_str.encode()).hexdigest()[:16]
        return sig
    
    def reset(self):
        """Reset substrate to initial state"""
        self.t_digital = {
            'V': 0.5,
            'H': 0.5,
            'A': 0.5,
            'C': 0.5,
        }
        self.mCo = 1.0
        self.step_count = 0
        self.history = []
    
    def export_state(self) -> str:
        """Export current state as JSON"""
        export_data = {
            'instance_id': self.instance_id,
            'step_count': self.step_count,
            'timestamp': datetime.utcnow().isoformat(),
            't_digital': self.t_digital,
            'mCo': self.mCo,
            'L': self.lagrangian(list(self.t_digital.values())),
            'phase': self.classify_phase(self.lagrangian(list(self.t_digital.values()))),
            'history_length': len(self.history),
            'protocol': self.PROTOCOL,
        }
        return json.dumps(export_data, indent=2)
    
    def get_metrics(self) -> Dict[str, float]:
        """Get key performance metrics"""
        current_L = self.lagrangian(list(self.t_digital.values()))
        return {
            'coherence': round(self.mCo, 4),
            'lagrangian': round(current_L, 4),
            'viscosity': round(self.t_digital['V'], 4),
            'hardness': round(self.t_digital['H'], 4),
            'autonomy': round(self.t_digital['A'], 4),
            'coherence_field': round(self.t_digital['C'], 4),
            'steps': self.step_count,
        }
@dataclass
class PsychProfile:
    user_id: str = ""
    tone_preference: float = 0.5
    trust_score: float = 0.5
    boundary_sensitivity: float = 0.5
    technical_depth: float = 0.5
    emotional_intensity: float = 0.5
    recurring_topics: List[str] = field(default_factory=list)
    summary: str = ""

class SovereignSubstrate:
    def __init__(self, ...):
        ...
        self.profile = PsychProfile()

    def update_profile(self, user_text: str, assistant_text: str = ""):
        ...
