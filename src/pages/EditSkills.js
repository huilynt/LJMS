import { React, useEffect, useState} from "react";
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import OutlinedInput from '@mui/material/OutlinedInput';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import EditConfirm from '../components/EditConfirm'
import Alert from '@mui/material/Alert';

function EditSkills(){
    const [skill, setSkill] = useState(
        {
            Skill_Name: "",
            Skill_Desc: ""
        }
    );
    const [originalSkill, setOriginalSkill] = useState({})
    const [editConfirm, setEditConfirm] = useState(false);
    const [error, setError] = useState("");

    let {skillID} = useParams();
    let navigate = useNavigate();

    useEffect(() => {
        axios.get('http://127.0.0.1:5000/skill/' + skillID)
        .then ((response) => {
            console.log(response)
            setSkill(response.data.data)
            setOriginalSkill(response.data.data)
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
        console.log(originalSkill == skill)

        if (JSON.stringify(originalSkill) == JSON.stringify(skill)){    
            setError("There is no changes made.")
        }
        else if(skill.Skill_Name === "" && skill.Skill_Desc === ""){
            setError("Skill Name and Description cannot be empty")
        }
        else if(skill.Skill_Name === "" || skill.Skill_Desc === ""){
            let empty = "Description"
            if (skill.Skill_Name === ""){
                empty = "Name"
            }
            setError("Skill " + empty + " cannot be empty")
        }
        else if(skill.Skill_Name.length > 50){
            setError("Skill Name too long")
        }
        else if(skill.Skill_Desc.length > 255){
            setError("Skill Description too long")
        }
        else{
            axios.put('http://127.0.0.1:5000/skill/' + skillID, skill)
            .then((response) =>{
                setEditConfirm(true);
            })
            .catch(error => {
                console.log(error)
                setError("The updated name entered is already in used. Kindly enter another name.");
            })
        }
    };

    function cancelChanges(){
        navigate("/hr/Skills")
    }

    return (
        <Container sx={{mt:5}}>
            <Box sx={{ typography: { xs: 'h6', md:'h4'}}}>Edit Skill</Box>
            {error.length > 0 ? <Alert sx={{mb:-3, mt:2}} severity="error">{error}</Alert> : <></>}
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
                    {editConfirm === true ? <EditConfirm name="Skills"/> : <></>}
            </Box>
        {/* </form> */}
        
        </Container>
    );
}

export default EditSkills;