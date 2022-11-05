import { React, useState, useEffect} from "react";
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import {Container, Box, Button, Typography, Grid, Alert} from '@mui/material';
import FormControl from '@mui/material/FormControl';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormGroup from '@mui/material/FormGroup';
import Checkbox from '@mui/material/Checkbox';
import InputLabel from '@mui/material/InputLabel';
import OutlinedInput from '@mui/material/OutlinedInput';
import Stack from '@mui/material/Stack';
import CreateConfirm from '../components/CreateConfirm'

function CreateRoleHr(){
    const [jobrole, setJobRole] = useState(
        {
            JobRole_ID: "",
            JobRole_Name: "",
            JobRole_Desc: ""
        }
    );
    const [createConfirm, setCreateConfirm] = useState(false);
    const [error, setError] = useState("");
    const [skills, setSkill] = useState([]);
    const [selectedSkills, setselectedSkills] = useState([]);

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

    }, [])

    const handleChange = (event) => {
        const value = event.target.value;
        setJobRole({ 
            ...jobrole,
            [event.target.name]: value
        });

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
    };

    function saveChanges(e) {
        e.preventDefault();
            
        jobrole.JobRole_ID = jobrole.JobRole_ID.trim()
        jobrole.JobRole_Name = jobrole.JobRole_Name.trim()

        if(jobrole.JobRole_ID === "" || jobrole.JobRole_Name === "" || jobrole.JobRole_Desc === ""){
            setError("All fields must be filled")
        }
        else if(jobrole.JobRole_ID.length > 50){
            setError("Role ID too long")
        }
        else if(jobrole.JobRole_Name.length > 50){
            setError("Role Name too long")
        }
        else if(jobrole.JobRole_Desc.length > 255){
            setError("Role Description too long")
        }
        else if(selectedSkills.length < 1){
            setError("At least one skill is required.")
        }
        else{
            axios.post('http://127.0.0.1:5000/jobrole/create',jobrole)
            .then((response) =>{
                console.log(response)
                axios.post('http://127.0.0.1:5000/hr/jobrole/edit/' + jobrole.JobRole_ID, selectedSkills)
                .then((response) =>{
                    setCreateConfirm(true);
                })
                .catch(error => {
                    console.log(error)
                })
            })
            .catch(error => {
                console.log(error)
                setError("The role ID or name entered is already in used. Kindly enter another ID or name.");
            })
            
        }
    };

    function cancelChanges(){
        navigate("/hr/Roles")
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

    return (
        <Container sx={{mt:5}}>
            <Box sx={{ typography: { xs: 'h6', md:'h4'}}}>Create Role</Box>
            {error.length > 0 ? <Alert sx={{mb:-3, mt:2}} severity="error">{error}</Alert> : <></>}
            {/* <form onSubmit={saveChanges} > */}
                <Box sx={{my:5, py:5, px:2, border:'1px dashed grey'}} component="form">
                    <Stack direction={{xs:"column", md:"row" }} spacing={5}>
                        <Stack spacing={2} sx={{width: {xs:"100%",md:"100%"}}}>
                            <FormControl>
                                <InputLabel htmlFor="jobrole-id">ID</InputLabel>
                                <OutlinedInput
                                id="jobrole-id"
                                value={jobrole.JobRole_ID}
                                onChange={handleChange}
                                name="JobRole_ID"
                                label="jobrole-id"
                                sx={{ m: 2, mb:3}}
                                />  
                            </FormControl>
                            
                            <FormControl>
                                <InputLabel htmlFor="jobrole-name">Name</InputLabel>
                                <OutlinedInput
                                    id="jobrole-name"
                                    value={jobrole.JobRole_Name}
                                    onChange={handleChange}
                                    name="JobRole_Name"
                                    label="jobrole-name"
                                    sx={{ m: 2, mb:3}}
                                />  
                            </FormControl>

                            <FormControl>
                                <InputLabel htmlFor="jobrole-desc">Description</InputLabel>
                                <OutlinedInput
                                    id="jobrole-desc"
                                    label="jobrole-desc"
                                    name="JobRole_Desc"
                                    multiline
                                    rows={8}
                                    value={jobrole.JobRole_Desc}
                                    onChange={handleChange}
                                    sx={{ m: 2 }}
                                />
                            </FormControl>
                        </Stack>
                    </Stack>
                    <Typography sx={{px:2}} variant="h6">Select the skills you want to assign to the role</Typography>
                    <Box sx={{ m:3}} >
                        <FormGroup component="fieldset" variant="standard">
                            <Grid container spacing={2} columns={16} data-testid="skill_list">
                                {skills_check}
                            </Grid>
                        </FormGroup>
                    </Box>
                    <Stack direction="row" spacing={2} justifyContent="center" sx={{mt:2}}>
                        <Button variant="outlined" color="error" onClick={cancelChanges}>Cancel</Button>
                        <Button variant="contained" color="success" onClick={saveChanges}>Save</Button>
                    </Stack>
                    {createConfirm === true ? <CreateConfirm name="Roles"/> : <></>}
            </Box>
        {/* </form> */}
        
        </Container>
    );
}

export default CreateRoleHr;