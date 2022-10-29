import {React, useState, useEffect} from "react";
import axios from 'axios';
import {Container, Box, Stack, Grid} from '@mui/material';
import { useParams } from 'react-router-dom';
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
import CourseCard from "../components/CourseCard";
import SkillCard from "../components/SkillCard";
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import PostAddIcon from '@mui/icons-material/PostAdd';

function EditLearningJourney() {
    const [alignment, setAlignment] = useState('skills');
    const [skills, setSkills] = useState([])
    const [courses, setCourse] = useState([])
    const [roleName, setRoleName] = useState("")
    const[journeyID, setJourneyID] = useState("")
    let { roleID } = useParams() 

    useEffect(() => {
        sessionStorage.setItem("userId", "140525");

        const journeyID = roleID + "-" + sessionStorage.userId
        setJourneyID(journeyID)
        axios.post('http://127.0.0.1:5000/journey/progress/' + journeyID, {"userId":sessionStorage.userId})
        .then ((response) => {
            const skill_data = response.data.data
            console.log(skill_data)
            setRoleName(response.data.role)
            const sorted = skill_data.sort(function(x, y) { return y.Completion_Status - x.Completion_Status})
            setSkills(sorted)
        })
        .catch(error => {
                console.log(error.message)
        })

        axios.post('http://127.0.0.1:5000/journey/' + journeyID, {"userId":sessionStorage.userId})
        .then ((response) => {
            console.log(response)
            setCourse(response.data.data)
        })
        .catch(error => {
            console.log(error.message)
        })

    },[])

    const handleChange = (event, newAlignment) => {
        if (newAlignment != null){
            setAlignment(newAlignment);
        }
    };

    const skill_posts = []
    for (let skill of skills){
        skill_posts.push(<SkillCard jobrole={roleID} completed={skill.Completion_Status} skill={skill.Skill_Name} skillId={skill.Skill_ID}/>)
    }

    const courses_post_completed = []
    const courses_post_progress = []

    for (let course of courses){
        if (course.Completion_Status === true){
            courses_post_completed.push(<CourseCard status={course.Course_Status} completed={course.Completion_Status} course={course.Course_Name} skills={course.skills}/>)
        }
        else {
            courses_post_progress.push(<CourseCard status={course.Course_Status} completed={course.Completion_Status} course={course.Course_Name} skills={course.skills} courseID={course.Course_ID} journeyID={journeyID}/>)
        }
    }
    return (
        <Container sx={{mt:5}}>
            <Box sx={{ typography: { xs: 'h6', md:'h4'}}}>{roleName}</Box>
            <Box sx={{ typography: { xs: 'body2', md:'h6'}}}>Learning Journey</Box>
            <Stack container justifyContent="center" sx={{my:3}} spacing={2}>
                <Box sx={{borderRadius:2}}>
                    <ToggleButtonGroup
                        color="success"
                        exclusive
                        value={alignment}
                        onChange={handleChange}
                        size="small"
                        fullWidth
                        >
                        <ToggleButton value="skills" sx={{fontWeight:"bold"}}>Progress</ToggleButton>
                        <ToggleButton value="courses" sx={{fontWeight:"bold"}}>Existing Courses</ToggleButton>
                    </ToggleButtonGroup>
                </Box>

                    {alignment == "courses" ? 
                        <>
                            <Accordion defaultExpanded={true}>
                                <AccordionSummary
                                    expandIcon={<ExpandMoreIcon />}
                                    aria-controls="panel1a-content"
                                    id="panel1a-header"
                                    sx={{backgroundColor:"#D9E3F0"}}
                                    >
                                    <Typography>Incomplete</Typography>
                                </AccordionSummary>
                                <AccordionDetails>
                                    <Grid container rowSpacing={2} columnSpacing={2} >
                                        {courses_post_progress.length > 0 ? courses_post_progress : <Box sx={{mx:"auto", my:5, py: 2,px:4,  border: '1px dashed grey',textAlign:"center" }}><PostAddIcon sx={{fontSize:100}}></PostAddIcon><Typography variant="h6">No courses</Typography></Box>}
                                    </Grid>
                                </AccordionDetails>
                            </Accordion>
                            <Accordion defaultExpanded={true}>
                                <AccordionSummary
                                    expandIcon={<ExpandMoreIcon />}
                                    aria-controls="panel1a-content"
                                    id="panel1a-header"
                                    sx={{backgroundColor:"#dcedc8"}}
                                    >
                                    <Typography>Completed</Typography>
                                </AccordionSummary>
                                <AccordionDetails>
                                    <Grid container rowSpacing={2} columnSpacing={2} >
                                        {courses_post_completed.length > 0 ? courses_post_completed : <Box sx={{mx:"auto", my:5, py: 2, px:4, border: '1px dashed grey',textAlign:"center"}}><PostAddIcon sx={{fontSize:100}}></PostAddIcon><Typography variant="h6">No courses</Typography></Box>}
                                    </Grid>
                                </AccordionDetails>
                            </Accordion>
                        </> : <></>}
                    
                    {alignment == "skills" ?                          
                        <Grid container rowSpacing={2} columnSpacing={2}>
                            {skill_posts}
                        </Grid>: <></>} 
            </Stack>
        </Container>
    )
}

export default EditLearningJourney;
