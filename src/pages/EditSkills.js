import { React, useEffect, useState} from "react";
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import OutlinedInput from '@mui/material/OutlinedInput';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';


function EditSkills(){
    const [skill, setSkill] = useState(
        {
            Skill_Name: "",
            Skill_Desc: ""
        }
    );
    let {skillID} = useParams();
    let navigate = useNavigate();

    useEffect(() => {
        axios.get('http://127.0.0.1:5000/skill/' + skillID)
        .then ((response) => {
            console.log(response)
            setSkill(response.data.data)
        })
        .catch(error => {
            console.log(error.message)
        })
    },[]);

    const handleChange = (event) => {
        const value = event.target.value;
        setSkill({ 
            ...skill,
            [event.target.name]: value
        });
    };

    function saveChanges(e) {
        e.preventDefault();

        axios.put('http://127.0.0.1:5000/skill/' + skillID, skill)
        .then((response) =>{
            console.log(response)
        })
        .catch(error => {
            console.log(error)
        })

        navigate('/Skills')
    };

    function cancelChanges(){
        window.location.reload();
    }

    return (
        <Container sx={{mt:5}}>
            <Box sx={{ typography: { xs: 'h6', md:'h4'}}}>Video Editing</Box>
        
            {/* <form onSubmit={saveChanges} > */}
                <Box sx={{my:5, py:5, px:2, border:'1px dashed grey'}} component="form">
                    <Stack direction={{xs:"column", md:"row" }} spacing={5}>
                        <Stack spacing={2} sx={{width: {xs:"100%",md:"50%"}}}>
                            <FormControl>
                                <InputLabel htmlFor="skill-name">Name</InputLabel>
                                <OutlinedInput
                                id="skill-name"
                                value={skill.Skill_Name}
                                onChange={handleChange}
                                name="Skill_Name"
                                label="-namskille"
                                sx={{ m: 2, mb:3}}
                                />  
                            </FormControl>

                            <FormControl>
                                <InputLabel htmlFor="skill-desc">Description</InputLabel>
                                <OutlinedInput
                                    id="skill-desc"
                                    label="skill-desc"
                                    name="Skill_Desc"
                                    multiline
                                    rows={8}
                                    value={skill.Skill_Desc}
                                    onChange={handleChange}
                                    sx={{ m: 2 }}
                                />
                            </FormControl>
                        </Stack>
                        <FormControl sx={{width: {xs:"100%",md:"50%"}}}>
                                    <InputLabel htmlFor="assign-skill">Assign Skills</InputLabel>
                                    <OutlinedInput
                                        id="assign-skill"
                                        label="assign-skill"
                                        multiline
                                        rows={8}
                                        defaultValue="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Sit amet dictum sit amet. Egestas erat imperdiet sed euismod nisi porta. Arcu felis bibendum ut tristique et egestas quis ipsum."
                                        sx={{ m: 2 }}
                                    />
                        </FormControl>
                    </Stack>
                    <Stack direction="row" spacing={2} justifyContent="center" sx={{mt:2}}>
                        <Button variant="outlined" color="error" onClick={cancelChanges}>Cancel</Button>
                        <Button variant="contained" color="success" onClick={saveChanges}>Save</Button>
                    </Stack>
            </Box>
        {/* </form> */}

        </Container>
    );
}

export default EditSkills;