import React from "react";

export default function Legend() {
  return (
    <div className="legend" data-testid="legend">
      <div className="legend-row">
        <span className="legend-dot" style={{ background: "#E8600A", boxShadow: "0 0 8px rgba(232,96,10,0.8)" }} />
        Galaxy: Provider
      </div>
      <div className="legend-row">
        <span className="legend-dot" style={{ background: "#E8A01E" }} />
        Sun: Entity / Signal
      </div>
      <div className="legend-row">
        <span className="legend-dot" style={{ background: "#1EE8D8" }} />
        Planet: Property
      </div>
    </div>
  );
}
