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

function UpdateRoleHR(){
    const [jobrole, setJobRole] = useState(
        {
            JobRole_Name: "",
            JobRole_Desc: ""
        }
    );
    const [originalJobRole, setOriginalJobRole] = useState({})
    const [editConfirm, setEditConfirm] = useState(false);
    const [error, setError] = useState("");

    let {jobroleID} = useParams();
    let navigate = useNavigate();

    useEffect(() => {
        axios.get('http://127.0.0.1:5000/jobrole/' + jobroleID)
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
        setJobRole({ 
            ...jobrole,
            [event.target.name]: value
        });
    };

    function saveChanges(e) {
        e.preventDefault();

        if (originalJobRole === skill){
            setError("There is no changes made.")
        }
        else{
            axios.put('http://127.0.0.1:5000/jobrole/' + jobroleID, jobrole)
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
        navigate("/hr/roles")
    }

    return (
        <Container sx={{mt:5}}>
            <Box sx={{ typography: { xs: 'h6', md:'h4'}}}>Edit Role</Box>
            {error.length > 0 ? <Alert sx={{mb:-3, mt:2}} severity="error">{error}</Alert> : <></>}
            {/* <form onSubmit={saveChanges} > */}
                <Box sx={{my:5, py:5, px:2, border:'1px dashed grey'}} component="form">
                    <Stack direction={{xs:"column", md:"row" }} spacing={5}>
                        <Stack spacing={2} sx={{width: {xs:"100%",md:"50%"}}}>
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
                        <FormControl sx={{width: {xs:"100%",md:"50%"}}}>
                                    <InputLabel htmlFor="assign-skill">Assign Roles</InputLabel>
                                    <OutlinedInput
                                        id="assign-jobrole"
                                        label="assign-jobrole"
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
                    {editConfirm === true ? <EditConfirm name="JobRole"/> : <></>}
            </Box>
        {/* </form> */}
        
        </Container>
    );
}

export default UpdateRoleHR;