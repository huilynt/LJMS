import {React,useEffect, useState} from "react";
import axios from 'axios';
import { useParams,useNavigate } from "react-router-dom";
import {Container, Box, Button, Typography, Grid, Alert, Stack} from '@mui/material';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import EditConfirm from "../components/EditConfirm";


function AssignSkillsCourse(){
    const [skills, setSkill] = useState([]);
    const [selectedSkills, setselectedSkills] = useState([]);
    const [courseName, setcourseName] = useState([]);
    const [error, setError] = useState("");
    const [saveConfirm, setSaveConfirm] = useState(false);
    const { courseID } = useParams();
    let navigate = useNavigate();

    useEffect(()=>{
        axios.get('http://127.0.0.1:5000/activeskill')
        .then(response => {
            console.log("SUCCESS", response)
            setSkill(response.data.data)
        })
        .catch(error => {
            console.log(error)
        })

        axios.get('http://127.0.0.1:5000/courses/' + courseID)
        .then(response => {
            console.log("SUCCESS", response)
            setselectedSkills(response.data.data)
            setcourseName(response.data.name)
        })
        .catch(error => {
            console.log(error)
        })
    }, [])

    function cancelChanges(){
        navigate("/hr/Courses")
    }

    const handleChange = (event) => {
        let checked = event.target.checked;
        let skillId = event.target.name;
        if (checked){
            if (selectedSkills.includes(skillId) === false){
                if (selectedSkills.length === 0){
                    setselectedSkills([skillId])
                }
                else{
                    setselectedSkills(current => [...current, skillId])
                }
            }
        }
        else{
            setselectedSkills(current => 
                current.filter(skill => {
                    return skill !== skillId;
                })
            )  
        }
    }

    const saveChanges = (event) => {
        event.preventDefault();
        if (selectedSkills.length < 1){
            setError("At least one skill is required.")
        }
        else{
            console.log(selectedSkills)
            axios.post('http://127.0.0.1:5000/hr/courses/edit/' + courseID, selectedSkills)
            .then((response) =>{
                console.log(response)
                setSaveConfirm(true)
            })
            .catch(error => {
                console.log(error)
            })
        }

    }

    const skills_check = []
    for (let skill of skills){
        let checked_skill = false
        if (selectedSkills.includes(skill.Skill_ID)){
            checked_skill = true;
        }
        skills_check.push( 
            <Grid item md={8} key={skill.Skill_ID}>
                <FormControlLabel 
                    control={<Checkbox checked={checked_skill}/>} 
                    label={skill.Skill_Name} 
                    name={skill.Skill_ID}
                    onChange={handleChange}
                />
            </Grid>)
    }

    return(
        <Container sx={{mt:5}}>
            <Box sx={{ typography: { xs: 'h6', md:'h4'}}}>{courseName}</Box>
            {error.length > 0 ? <Alert sx={{mb:-3, mt:2}} severity="error">{error}</Alert> : <></>}
            <Box sx={{my:5, py:3, px:2, border:'1px dashed grey'}} component="form">
                <Typography sx={{px:2}} variant="h6">Select the skills you want to assign to the course</Typography>
                <Box sx={{ m:3}} >
                    <FormGroup component="fieldset" variant="standard">
                        <Grid container spacing={2} columns={16} data-testid="skill_list">
                            {skills_check}
                        </Grid>
                    </FormGroup>
                </Box>
            </Box>
            <Stack direction="row" spacing={2} justifyContent="center" sx={{mt:2}}>
                <Button variant="outlined" color="error" onClick={cancelChanges}>Cancel</Button>
                <Button variant="contained" color="success" onClick={saveChanges}>Save</Button>
            </Stack>
            {saveConfirm === true ? <div data-testid="editMsgCourse"><EditConfirm name="Courses"/></div> : <></>}
        </Container>
    )
}

export default AssignSkillsCourse;
