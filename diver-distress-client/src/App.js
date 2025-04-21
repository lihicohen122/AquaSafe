import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"; //in order to make paths we need this 
import SensorDashboard from "./components/SensorDashboard";
import "./App.css";

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<SensorDashboard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
