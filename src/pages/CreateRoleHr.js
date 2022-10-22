import { React, useState} from "react";
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import OutlinedInput from '@mui/material/OutlinedInput';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import CreateConfirm from '../components/CreateConfirm'
import Alert from '@mui/material/Alert';

function CreateRoleHr(){
    const [role, setRole] = useState(
        {
            Role_ID: "",
            Role_Name: "",
            Role_Desc: ""
        }
    );
    const [createConfirm, setCreateConfirm] = useState(false);
    const [error, setError] = useState("");

    let navigate = useNavigate();

    const handleChange = (event) => {
        const value = event.target.value;
        setRole({ 
            ...role,
            [event.target.name]: value
        });
    };

    function saveChanges(e) {
        e.preventDefault();

        if(role.Role_ID === "" || role.Role_Name === "" || role.Role_Desc === ""){
            setError("All fields must be filled")
        }
        else if(role.Role_ID.length > 50){
            setError("Role ID too long")
        }
        else if(role.Role_Name.length > 50){
            setError("Role Name too long")
        }
        else if(role.Role_Desc.length > 255){
            setError("Role Description too long")
        }
        else{
            axios.post('http://127.0.0.1:5000/roles/create', role)
            .then((response) =>{
                setCreateConfirm(true);
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

    return (
        <Container sx={{mt:5}}>
            <Box sx={{ typography: { xs: 'h6', md:'h4'}}}>Create Role</Box>
            {error.length > 0 ? <Alert sx={{mb:-3, mt:2}} severity="error">{error}</Alert> : <></>}
            {/* <form onSubmit={saveChanges} > */}
                <Box sx={{my:5, py:5, px:2, border:'1px dashed grey'}} component="form">
                    <Stack direction={{xs:"column", md:"row" }} spacing={5}>
                        <Stack spacing={2} sx={{width: {xs:"100%",md:"50%"}}}>
                            <FormControl>
                                <InputLabel htmlFor="role-id">ID</InputLabel>
                                <OutlinedInput
                                id="role-id"
                                value={role.Role_ID}
                                onChange={handleChange}
                                name="Role_ID"
                                label="role-id"
                                sx={{ m: 2, mb:3}}
                                />  
                            </FormControl>
                            
                            <FormControl>
                                <InputLabel htmlFor="role-name">Name</InputLabel>
                                <OutlinedInput
                                    id="role-name"
                                    value={role.Role_Name}
                                    onChange={handleChange}
                                    name="Role_Name"
                                    label="role-name"
                                    sx={{ m: 2, mb:3}}
                                />  
                            </FormControl>

                            <FormControl>
                                <InputLabel htmlFor="role-desc">Description</InputLabel>
                                <OutlinedInput
                                    id="role-desc"
                                    label="role-desc"
                                    name="role_Desc"
                                    multiline
                                    rows={8}
                                    value={role.Role_Desc}
                                    onChange={handleChange}
                                    sx={{ m: 2 }}
                                />
                            </FormControl>
                        </Stack>
                    </Stack>
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