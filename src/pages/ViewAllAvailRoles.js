import React, { useEffect, useState } from "react";
import axios from 'axios';
import { Container, Box, ListItem} from '@mui/material';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell, { tableCellClasses }  from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { styled } from '@mui/material/styles';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import List from '@mui/material/List';
import {Link} from 'react-router-dom';



const StyledTableCell = styled(TableCell)(({ theme }) => ({
    [`&.${tableCellClasses.head}`]: {
        backgroundColor: "#9CCAFF",
        color: theme.palette.common.white

    },
    [`&.${tableCellClasses.body}`]: {
        fontSize: 14,
    },
    borderLeft: 0,
    borderRight:'0.5px solid grey',

    '&:last-child': {
        borderRight: 0,
    },

}));

const StyledTableRow = styled(TableRow)(({ theme }) => ({
    '&:last-child td, &:last-child th': {
        borderBottom: 0,
    },
}));


export default function ViewAllAvailRoles(props) {


    const [jobroleData, setJobRoleData] = useState([])

    useEffect(()=>{
        axios.get('http://127.0.0.1:5000/'+ sessionStorage.getItem("userId") +'/jobrole').then(response => {
            console.log("SUCCESS", response)
            // setJobRoleData(response.data.data)

            let jobrole_list = response.data.data
            for (let i=0; i<jobrole_list.length; i++){
                let id = jobrole_list[i]['JobRole_ID']

                axios.get('http://127.0.0.1:5000/' + id + '/skills').then(response => {
                    console.log("SUCCESS", response)
                    var skill_list = response.data.data
                    jobrole_list[i]["skills"] = skill_list;
                    console.log(jobrole_list[i])
                    setJobRoleData(prevState => [...prevState, jobrole_list[i]])
                    
                }).catch(error => {
                    console.log(error)
                })
            }
        }).catch(error => {
            console.log(error)
        })

    },[])

    console.log(jobroleData)

    return (
        <Container sx={{mt:5}}>
        <Box sx={{ typography: { xs: 'h6', md:'h4'},borderBottom: 1}}>Roles</Box>
        
    
        <TableContainer sx={{mt:2}} component={Paper}>            
            <Table sx={{minWidth: 200}}>
                <TableHead stickyHeader>
                    <TableRow>
                        <StyledTableCell sx={{ display: { xs: 'none', md: 'table-cell' } }}>ID</StyledTableCell>
                        <StyledTableCell sx={{borderRight: {xs:0, md:'0.5px solid grey'}}}>Role Name</StyledTableCell>
                        <StyledTableCell sx={{ display: { xs: 'none', md: 'table-cell' } }}>Description</StyledTableCell>
                        <StyledTableCell>Skills Required</StyledTableCell>
                        <StyledTableCell>Choose Role</StyledTableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {jobroleData.map((row,index) => (
                            <StyledTableRow key={index}>
                                <StyledTableCell sx={{ display: { xs: 'none', md: 'table-cell' } }}>{row.JobRole_ID}</StyledTableCell>
                                <StyledTableCell sx={{borderRight: {xs:0, md:'0.5px solid grey'}}}>{row.JobRole_Name}</StyledTableCell>
                                <StyledTableCell sx={{ display: { xs: 'none', md: 'table-cell' } }}>{row.JobRole_Desc}</StyledTableCell>
                                <StyledTableCell>
                                    
                                    <List>
                                            {row.skills.map(skill => (
                                                <ListItem key={index}>{skill.Skill_Name}</ListItem>
                                            ))}
                                    </List>
                                
                                </StyledTableCell>
                                <StyledTableCell>
                                <Link to={{
                                    pathname:"/"+row.JobRole_ID+"/skills",
                                    state:{stateParam:true}
                                }}>
                                <ArrowForwardIosIcon></ArrowForwardIosIcon>
                                {}
                                </Link>
                                </StyledTableCell>
                            </StyledTableRow>
                        ))
                        
                    }
                </TableBody>
            </Table>
        </TableContainer>

        </Container>
        
            
    )

}
