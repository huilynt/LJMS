import { React, useEffect, useState} from "react";
import axios from 'axios';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import OutlinedInput from '@mui/material/OutlinedInput';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import Alert from '@mui/material/Alert';

function MockLogin(){
    const [userId, setUserId] = useState("");
    const [error, setError] = useState("");

    const handleChange = (event) => {
        setUserId(event.target.value);
        setError("");
        console.log(userId);
    };

    function saveChanges(e) {
        e.preventDefault();

        if(userId.length !== 6){
            setError("User ID must be 6 digits long")
        }
        else{
            axios.get('http://127.0.0.1:5000/login/' + userId)
            .then((response) =>{
                sessionStorage.setItem("userId", userId);
                sessionStorage.setItem("role", response.data.data[0]["Role"]);
                console.log(sessionStorage.getItem("role"));
                window.location.reload();
            })
            .catch(error => {
                console.log(error)
                setError("User ID does not exist");
            })
        }
    };

    return (
        <Container sx={{mt:5}}>
            <Box sx={{ typography: { xs: 'h5', md:'h3'}}}>Learning Journey Planning System</Box>
            <Box sx={{ typography: { xs: 'h6', md:'h4'}}}>Login</Box>
            {error.length > 0 ? <Alert sx={{mb:-3, mt:2}} severity="error">{error}</Alert> : <></>}
                <Box sx={{my:5, py:5, px:2, border:'1px dashed grey'}} component="form">
                    <Stack direction={{xs:"column", md:"row" }} spacing={5}>
                        <Stack spacing={2} sx={{width: {xs:"100%",md:"50%"}}}>
                            <FormControl>
                                <InputLabel htmlFor="skill-id">User ID</InputLabel>
                                <OutlinedInput
                                id="user-id"
                                value={userId}
                                onChange={handleChange}
                                name="User_ID"
                                label="user-id"
                                sx={{ m: 2, mb:3}}
                                />  
                            </FormControl>
                        </Stack>
                    </Stack>
                    <Stack direction="row" spacing={2} justifyContent="center" sx={{mt:2}}>
                        <Button variant="contained" color="success" onClick={saveChanges}>Log In</Button>
                    </Stack>
            </Box>
        
        </Container>
    );
}

export default MockLogin;