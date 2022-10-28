import React from "react";
import {Grid, Box} from '@mui/material';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import AddIcon from '@mui/icons-material/Add';
import CircleIcon from '@mui/icons-material/Circle';
import {Link} from 'react-router-dom';

function SkillCard(props){
    return (
        <Grid item xs={12} sm={6} md={3}>
            <Card variant="outlined" sx={{ display:"flex", maxHeight:90, borderRadius:0, py:2, px:1, alignItems:"center"}}>
                { props.completed === true ? <CheckCircleIcon  sx={{fontSize:90, color:"#8bc34a"}}></CheckCircleIcon> : <CircleIcon sx={{fontSize:90, color:"#eeeeee"}}></CircleIcon>}
                <Box sx={{ display: 'flex', flexDirection:'column' }}>
                    <CardContent>
                        <Typography variant="h6" sx={{fontSize:18}} >
                            {props.skill}
                        </Typography>
                    </CardContent>
                </Box>
            </Card>
            {props.status != "Retired" ?
            <Link   to={{
                        pathname:"/" + props.jobrole + "/" + props.skillId + "/courses",
                        state:{stateParam:true}
                        }} 
                    style={{ textDecoration: 'none' }}>
                <Button startIcon={<AddIcon />} variant="contained" sx={{width:"100%", borderRadius:0, backgroundColor:"#9CCAFF"}}>{props.completed === true ? "Add More Course" : "Add Course"}</Button>
            </Link> : <><Button disabled variant="contained" sx={{width:"100%", borderRadius:0, backgroundColor:"#9CCAFF"}}>Not Applicable</Button></>}
        </Grid>
    )
}

export default SkillCard;