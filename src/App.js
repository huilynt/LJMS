import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";

import Navbar from "./components/Navbar";
import LearningJourney from "./pages/LearningJourney";
import Courses from "./pages/Courses";
import Roles from "./pages/Roles";
import Skills from "./pages/Skills";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route exact path="/" component={LearningJourney} />
        <Route exact path="/" component={Courses} />
        <Route exact path="/" component={Roles} />
        <Route exact path="/" component={Skills} />
      </Routes>
    </Router>
  );
}

export default App;
