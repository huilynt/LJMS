import React from "react";
import {Grid} from '@mui/material';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import RemoveCircleOutlineIcon from '@mui/icons-material/RemoveCircleOutline';

function CourseCard(props){
    return (
        <Grid item xs={12} sm={6} md={3} sx={{display:'flex'}}>
            <Card variant="outlined" sx={{backgroundColor:"#f5f5f5"}} >
                <CardContent sx={{px:2,py:1}}>
                    <Typography variant="h6" component="div">
                        {props.course}
                    </Typography>
                    <Divider/>
                    <Typography sx={{ mb: 1.5 }} color="text.secondary">
                        Skill: {props.skills.length > 1 ? props.skills.map(skill => (
                            <span>{skill["Skill_Name"]},</span>
                        )) : <span>{props.skills[0]["Skill_Name"]}</span>}
                    </Typography>
                </CardContent>
                { props.completed === false ?
                <CardActions sx={{p:2, pt:0}}>
                    <Button size="small" color="error">Remove Course 
                        <RemoveCircleOutlineIcon color="error" fontSize="small"></RemoveCircleOutlineIcon>
                    </Button>
                </CardActions> : <></>}
            </Card>
        </Grid>
    )
}

export default CourseCard;