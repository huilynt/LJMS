import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";

import Navbar from "./components/Navbar";
import LearningJourney from "./pages/LearningJourney";
import SkillCourses from "./pages/SkillCourses";
import Roles from "./pages/Roles";
import Skills from "./pages/Skills";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route exact path="/LearningJourney" element={<LearningJourney/>} />
        <Route exact path="/:jobRole/:skillID/courses" element={<SkillCourses/>} />
        <Route exact path="/Roles" element={<Roles/>} />
        <Route exact path="/Skills" element={<Skills/>} />
      </Routes>
    </Router>
  );
}

export default App;
