import React from "react";
import { Link } from 'react-router-dom';
import {Grid, Button} from '@mui/material';

function LearningJourney() {

    return (
        <div>
        <Grid container spacing sx={{p:2,borderBottom: 1}}>
            <Grid item xs={12} md={4} display="flex" alignItems="center">
                <h1>My Learning Journeys</h1>
            </Grid>
            <Grid item xs={12} md={1} display="flex" alignItems="center">
                <Link to='/ViewAllAvailRoles' underline="none">
                <Button variant="contained" color="success">Create</Button>
                </Link>
            </Grid>
            
        </Grid>
        </div>
    )

}

export default LearningJourney;