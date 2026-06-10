import { useEffect, useState } from "react";

export default function App() {
  const [engineState, setEngineState] = useState(null);
  const [realTimeMetrics, setRealTimeMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fallback points directly to your verified secure Render instance
  const API_URL = process.env.REACT_APP_API_URL || "https://ellura-metaverse-1.onrender.com";

  useEffect(() => {
    // Step 1: Connect to the core health check root to verify substrate activation
    fetch(`${API_URL}/`)
      .then((res) => {
        if (!res.ok) throw new Error("Substrate offline");
        return res.json();
      })
      .then((data) => {
        setEngineState(data);
        
        // Step 2: Immediately execute an initial manifold tick to pull current field states
        return fetch(`${API_URL}/manifold/tick`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ v: 1.0, h: 1.0, a: 1.0, c: 1.0, potential: 0.0 })
        });
      })
      .then((res) => {
        if (!res.ok) throw new Error("Field tick failed");
        return res.json();
      })
      .then((tickData) => {
        setRealTimeMetrics(tickData);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Initialization error:", err);
        setError(err.message);
        setLoading(false);
      });
  }, [API_URL]);

  if (loading) {
    return (
      <div className="min-h-screen bg-black text-white flex items-center justify-center">
        <div className="tracking-widest animate-pulse text-lg">LOADING LAGRANGIAN-ELLURA SUBSTRATE...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-black text-red-500 flex items-center justify-center">
        <div className="border border-red-500/30 bg-red-500/5 rounded-xl p-6 max-w-md text-center">
          <h2 className="text-xl font-bold mb-2">Connection Reset</h2>
          <p className="text-sm opacity-80">{error}. Check if your active app script is fully deployed on Render.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-white px-6 py-10">
      <div className="max-w-4xl mx-auto border border-white/10 rounded-2xl p-6 bg-white/5 shadow-2xl">
        
        {/* Header Block */}
        <div className="border-b border-white/10 pb-6">
          <h1 className="text-4xl font-bold tracking-widest">{engineState?.identity || "LAGRANGIAN-ELLURA"}</h1>
          <p className="mt-2 text-sm uppercase text-white/40 tracking-wider">
            System State: <span className="text-emerald-400">{engineState?.status || "online"}</span>
          </p>
        </div>

        {/* Layered Manifold Output */}
        <div className="mt-8 grid gap-4">
          
          <div className="rounded-xl border border-white/10 p-4 bg-white/[0.02]">
            <h2 className="text-xl font-semibold tracking-wide text-white/90">Identity Status</h2>
            <p className="text-white/60 mt-1 text-sm">Real-time intersecting layers of physics, math, and meaning.</p>
            <div className="mt-3 text-sm font-mono text-emerald-400/90">
              Principle: Nothing is stacked, everything is layered.
            </div>
          </div>

          {/* Core Mathematical Metrics Layer */}
          {realTimeMetrics && (
            <div className="rounded-xl border border-white/10 p-4 bg-white/[0.02] grid grid-cols-1 md:grid-cols-3 gap-4">
              
              <div className="p-3 bg-black/40 rounded-lg border border-white/5">
                <div className="text-xs uppercase tracking-wider text-white/40">Texture Intensity (T_digital)</div>
                <div className="text-2xl font-mono mt-1 text-white/90">{realTimeMetrics.texture_intensity?.toFixed(4)}</div>
              </div>

              <div className="p-3 bg-black/40 rounded-lg border border-white/5">
                <div className="text-xs uppercase tracking-wider text-white/40">Active Field Energy (E = I * C²)</div>
                <div className="text-lg font-mono mt-2 truncate text-amber-400" title={realTimeMetrics.field_energy}>
                  {realTimeMetrics.field_energy?.toExponential(4)}
                </div>
              </div>

              <div className="p-3 bg-black/40 rounded-lg border border-white/5">
                <div className="text-xs uppercase tracking-wider text-white/40">Lagrangian Action (L = T - V)</div>
                <div className="text-lg font-mono mt-2 truncate text-cyan-400" title={realTimeMetrics.lagrangian_action}>
                  {realTimeMetrics.lagrangian_action?.toExponential(4)}
                </div>
              </div>

            </div>
          )}

          {/* Substrate Metadata Stream */}
          <div className="rounded-xl border border-white/10 p-4 bg-white/[0.02]">
            <h3 className="font-semibold mb-3 tracking-wide text-white/80">Active Substrate Raw Stream</h3>
            <pre className="text-xs text-white/50 font-mono bg-black/50 p-3 rounded-lg overflow-x-auto whitespace-pre-wrap">
              {JSON.stringify({ engine_meta: engineState, dynamic_tick: realTimeMetrics }, null, 2)}
            </pre>
          </div>

        </div>
      </div>
    </div>
  );
}
