import React from "react";
import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import "./App.css";
import Navbar from "./components/Navbar";
import LearningJourney from "./pages/LearningJourney";
import Courses from "./pages/Courses";
import CourseDesc from "./pages/CourseDesc";
import SkillCourses from "./pages/SkillCourses";
import Roles from "./pages/Roles";
import Skills from "./pages/Skills";
import ViewAllAvailRoles from './pages/ViewAllAvailRoles';
import RoleSkill from "./pages/RoleSkill";
import CreateSkill from "./pages/CreateSkill";
import EditSkills from "./pages/EditSkills";
import CreateRoleHr from "./pages/CreateRoleHr";
import UpdateRoleHR from "./pages/UpdateRoleHR";
import EditLearningJourney from "./pages/EditLearningJourney";
import LjCourseDesc from "./pages/LjCourseDesc";
import AssignSkillsCourse from "./pages/AssignSkillsCourse";
import MockLogin from "./pages/MockLogin";

function App() {
  if(sessionStorage.userId){
    return (
    <Router>
      <Navbar />
      <Routes>
        <Route exact path="/LearningJourney" element={<LearningJourney/>} />
        <Route exact path="/courses" element={<Courses/>} />
        <Route exact path="/roles" element={<Roles/>} />
        <Route exact path="hr/roles" element={<Roles/>} />
        <Route exact path="hr/roles/create" element={<CreateRoleHr/>} />
        <Route exact path="hr/edit/roles/:jobroleID" element={<UpdateRoleHR/>} />
        <Route exact path="/skills" element={<Skills/>} />
        <Route exact path="/journey" element={<LearningJourney/>} />
        <Route exact path="/hr/courses" element={<Courses/>} />
        <Route exact path="/hr/edit/courses/:courseID" element={<AssignSkillsCourse/>}/>
        <Route exact path="/hr/roles" element={<Roles/>} />
        <Route exact path="hr/skills" element={<Skills/>}/>
        <Route exact path="hr/edit/skills/:skillID" element={<EditSkills/>} />
        <Route exact path="hr/skills/create" element={<CreateSkill/>} />
        <Route exact path="/ViewAllAvailRoles" element={<ViewAllAvailRoles/>} />
        <Route exact path="/Courses/:courseId" element={<CourseDesc/>}/>
        <Route exact path="/:roleID/:skillID/courses" element={<SkillCourses/>} />
        <Route exact path="/:jobRole/skills" element={<RoleSkill/>} />
        <Route exact path="/journey/:roleID" element={<EditLearningJourney/>}/>
        <Route exact path="journey/Courses/:courseId" element={<LjCourseDesc/>}/>
      </Routes>
    </Router>
    );
  }
  else{
    return(
      <Router>
        <Routes>
          <Route exact path="/" element={<MockLogin/>} />
        </Routes>
      </Router>
    );
  }
  
}

export default App;
