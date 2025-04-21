import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import SensorDashboard from "./components/SensorDashboard";
import Homepage from "./components/Homepage";
import "./App.css";

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Homepage />} />
          <Route path="/group/:groupId" element={<SensorDashboard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;