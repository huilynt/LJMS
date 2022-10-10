import React from "react";
import { Link } from 'react-router-dom';
import {Grid, Button, Container, Box} from '@mui/material';

function LearningJourney() {

    return (
        
        <Container sx={{mt:5}}>
            
            <Grid container sx={{borderBottom:1, display:'flex', alignItems: 'center', pb:1}}>
                <Grid item sx={{ typography: { xs: 'h6', md:'h4'}}} xs={8} md={4}>
                    My Learning Journeys
                </Grid>
                <Grid item xs={3} md={2} >
                <Link to='/ViewAllAvailRoles' underline="none">
                    <Button variant="contained" color="success" size="medium">Create</Button>
                </Link>
                </Grid>

            </Grid>


    
            
        </Container>
    )

}

export default LearningJourney;