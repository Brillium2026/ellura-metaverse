# ellura-metaverse 2026

**Sovereign Lagrangian Substrate for autonomous assessment evolution**

Features the **EVOLVE-1 engine** with interaction-coupled stability hardening, real-time coherence tracking, and integrated financial autonomy.

---

## 🚀 Overview

ellura-metaverse is a sophisticated autonomous assessment framework built on the **EVOLVE-1 protocol**, a Lagrangian-based physics engine for adaptive system evolution. The system combines quantum-inspired coherence metrics with classical field theory to enable autonomous, self-correcting learning systems.

### Key Features

- **EVOLVE-1 Engine**: Lagrangian energy functionals driving autonomous evolution
- **Interaction-Coupled Stability Hardening**: Systems strengthen themselves through interaction
- **Real-Time Coherence Tracking**: Monitor system stability and phase transitions
- **Digital Field Architecture**: V (Viscosity), H (Hardness), A (Autonomy), C (Coherence) fields
- **Autonomous Assessment Cycles**: Weekly evolution with adaptive expansion/hardening modes
- **FastAPI Backend**: Modern REST API for integration
- **SQLite Persistence**: Robust data storage with SQLAlchemy ORM

---

## 📋 Project Structure

```
Ellura-Metaverse/
├── sovereign_substrate.py      # Core EVOLVE-1 engine implementation
├── brilliant_interactive_demo.py # Interactive CLI interface
├── main.py                     # FastAPI application entry point
├── models.py                   # SQLAlchemy database models
├── evolve_agents.py            # EvolveOne autonomous evolution agent
├── auth.py                     # Authentication & authorization
├── database.py                 # Database configuration
├── index.html                  # EVOLVE-1 Dashboard UI
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🔧 Installation

### Prerequisites
- Python 3.8+
- pip or conda

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Brillium2026/Ellura-metaverse.git
   cd ellura-metaverse
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   # Create .env file with:
   SECRET_KEY=your_secret_key_here
   DATABASE_URL=sqlite:///./sql_app.db
   ```

---

## 💫 Quick Start

### Interactive CLI Demo

Launch the interactive Sovereign Substrate demo:

```bash
python brilliant_interactive_demo.py
```

#### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `think <message>` | Process a thought through the substrate | `think What is the meaning of coherence?` |
| `evolve <V,H,A,C>` | Direct evolution step with custom field values | `evolve 0.5,0.3,0.2,0.4` |
| `status` | Display current substrate state | `status` |
| `metrics` | Show key performance metrics | `metrics` |
| `history [N]` | Show last N evolution steps (default: 5) | `history 10` |
| `export` | Export current state as JSON | `export` |
| `reset` | Reset substrate to initial state | `reset` |
| `help` | Display command help | `help` |
| `quit` | Exit the demo | `quit` |

### Example Session

```
> status
Instance ID: BRILLIANCE_DEMO
Step Count: 0
Coherence (mCo): 1.0000
Lagrangian (L): 0.2500
Phase: STABLE
Fields:
  V (Viscosity):  0.5000
  H (Hardness):   0.5000
  A (Autonomy):   0.5000
  C (Coherence):  0.5000

> evolve 0.1,0.2,0.15,0.3
Evolution Step Executed:
  Phase: STABLE
  Coherence: 0.9500
  Lagrangian: 0.2847
  Fields: V=0.5042, H=0.5084, A=0.5063, C=0.5126
  Transition: STABLE -> STABLE
  Signature: a7f3e2c1d9b4e6f2

> history
Last 5 history entries:
  Step    1: L=  0.2847 mCo=0.9500 STABLE     sig=a7f3e2c1d9b4e6f2
```

### FastAPI Server

Start the backend server:

```bash
python main.py
```

The API will be available at `http://localhost:8000`

#### API Endpoints

- `GET /assessment/{assessment_id}` - Get assessment with stability metrics
- `POST /evolve/cycle` - Trigger manual EVOLVE-1 cycle
- `GET /docs` - Interactive API documentation (Swagger UI)

---

## 🧬 The EVOLVE-1 Engine

### Lagrangian Energy Functional

The system operates on a Lagrangian formulation:

```
L = KE - PE + coherence_modulation
```

Where:
- **KE** (Kinetic Energy): Represents field momentum and change
- **PE** (Potential Energy): Models interaction coupling between fields
- **Coherence Modulation**: Real-time stability adjustment

### Digital Fields (VHAC)

| Field | Symbol | Meaning |
|-------|--------|---------|
| Viscosity | V | System resistance to change |
| Hardness | H | Structural stability/coupling |
| Autonomy | A | Self-directed evolution capability |
| Coherence | C | Quantum-like phase coherence |

### Phase Classification

Based on Lagrangian value (L):

- **EXPANSION** (L < -0.5): Active growth, low stability
- **STABLE** (-0.5 ≤ L < 0.5): Equilibrium state, optimal operation
- **HARDENING** (L ≥ 0.5): Stability reinforcement, consistency focus

### Stability Coupling

When in HARDENING phase:
- Fields approach mean value (→ consistency)
- Hardening factor amplifies stable configurations
- Coherence decay slows

When in EXPANSION phase:
- Fields explore new states
- Expansion factor enables growth
- Higher variance is tolerated

---

## 📊 Database Models

### User
```python
- id: Primary Key
- email: Unique email address
- hashed_password: Bcrypt hash
- is_active: Account status
- is_admin: Administrative privileges
- created_at: Creation timestamp
```

### Assessment
```python
- id: Primary Key
- title: Assessment name
- description: Assessment details
- owner_id: Foreign key to User
- performance_score: EVOLVE-1 metric (0-100)
- last_evolved_at: Timestamp of last evolution cycle
- last_interaction_at: Coherence reset sensor
- created_at: Creation timestamp
```

### EvolveLog
```python
- id: Primary Key
- timestamp: Log entry time
- message: Evolution event description
- user_id: Associated user
```

---

## 🔐 Authentication

The system uses JWT-based authentication with OAuth2:

```python
# Token expires in 7 days for persistent substrate connections
ACCESS_TOKEN_EXPIRE_MINUTES = 10080

# Endpoints are protected with Bearer tokens
Authorization: Bearer {token}
```

### Admin Protocol

The "Guardian Protocol" ensures only Sovereign Admins can access critical infrastructure:

```python
@app.route("/critical")
def critical_endpoint(current_user = Depends(admin_required)):
    # Only accessible to is_admin=True users
    pass
```

---

## 📈 Weekly Evolution Cycle

The EVOLVE-1 engine runs an autonomous weekly evaluation:

```python
# Called via /evolve/cycle endpoint or Render background worker

for assessment in all_assessments:
    days_since_interaction = (now - last_interaction_at).days
    coherence = exp(-lambda * days_since_interaction)
    
    if performance_score >= 90.0:
        # HARDENING: Strengthen existing structure
        improvement = 5.0 * exp(-lambda * days_since) * 0.6
    else:
        # EXPANSION: Grow new capabilities
        improvement = 12.0 * exp(-lambda * days_since)
    
    performance_score = min(100.0, performance_score + improvement)
    last_evolved_at = now
```

---

## 🛠️ Development

### Running Tests

```bash
pytest tests/
```

### Code Structure

- **sovereign_substrate.py**: Pure physics engine (no dependencies)
- **evolve_agents.py**: Database-aware agent (uses models)
- **main.py**: FastAPI server (orchestrates all components)
- **auth.py**: Security layer (JWT, password hashing)

### Key Classes

#### SovereignSubstrate
```python
substrate = SovereignSubstrate(instance_id="MY_INSTANCE")

# Evolution
result = substrate.evolve([0.1, 0.2, 0.15, 0.3])

# Introspection
metrics = substrate.get_metrics()
state_json = substrate.export_state()
```

#### EvolveOne
```python
agent = EvolveOne(db_session)

# Get stability metrics for an assessment
metrics = agent.get_stability_metrics(assessment)

# Run autonomous weekly cycle
agent.weekly_evaluation()
```

---

## 📦 Dependencies

```
fastapi==0.104.1
sqlalchemy==2.0.23
uvicorn==0.24.0
python-jose==3.3.0
passlib==1.7.4
bcrypt==4.1.2
pydantic==2.5.0
```

See `requirements.txt` for complete list.

---

## 🌟 Architecture Highlights

### Interaction-Coupled Dynamics
Fields influence each other through the mean field:
```python
interaction_strength = 0.02
mean_field = sum(fields) / 4
for field in fields:
    field += interaction_strength * (mean_field - field)
```

### Exponential Coherence Decay
Real systems lose coherence over time (cold environments, entropy):
```python
mCo *= coherence_decay  # ≈ 0.95 per step
mCo += 0.01 * (1.0 - mCo)  # Partial reset from interaction
```

### Signature Generation
Cryptographic fingerprinting of states for audit trail:
```python
sig = SHA256(state_vector + lagrangian)[:16]
```

---

## 🚀 Deployment

### Local Development
```bash
python main.py
# API at http://localhost:8000
```

### Production (Render)
```bash
# render.yaml or environment configuration
python main.py  # Uvicorn handles production serving
```

### Environment Variables
```env
SECRET_KEY=substrate_omega_99_alpha
DATABASE_URL=sqlite:///./sql_app.db
PORT=8000
```

---

## 📚 References

### Physics Inspiration
- Lagrangian mechanics and action principles
- Phase transitions in complex systems
- Quantum coherence and decoherence
- Mean-field theory approximations

### Implementation
- FastAPI: Modern async Python web framework
- SQLAlchemy: ORM for database operations
- PyJWT: JWT token handling
- Passlib: Password hashing with bcrypt

---

## 👥 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is part of the Ellura-Metaverse ecosystem.

---

## 📞 Support

For questions, issues, or suggestions:
- Open an GitHub issue
- Check existing documentation
- Review the code examples in `brilliant_interactive_demo.py`

---

## 🔮 Future Enhancements

- [ ] Quantum circuit simulation layer
- [ ] Multi-agent substrate swarms
- [ ] Neural network integration for thought encoding
- [ ] Real-time dashboard visualization
- [ ] Persistent state snapshots and rollback
- [ ] Distributed substrate federation

---

**Last Updated**: May 3, 2026  
**Version**: 2.4 - EVOLVE-1 Engine  
**Status**: Production-Ready
