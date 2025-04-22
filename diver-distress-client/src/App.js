import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import SensorDashboard from "./components/SensorDashboard";
import Homepage from "./components/Homepage";
import DiverDetails from "./components/DiverDetails";
import NavigationBar from "./components/NavigationBar";
import "./App.css";

function App() {
  return (
    <Router>
      <div className="App">
        <NavigationBar />
        <div className="content">
          <Routes>
            <Route path="/" element={<Homepage />} />
            <Route path="/group/:groupId" element={<SensorDashboard />} />
            <Route path="/diver/:diverId" element={<DiverDetails />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;