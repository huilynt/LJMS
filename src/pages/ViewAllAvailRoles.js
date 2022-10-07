import React, { useEffect, useState } from "react";
import axios from 'axios';
import {Link, Container, Box, ListItem} from '@mui/material';
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
import ListItemIcon from '@mui/material/ListItemIcon';
import CircleIcon from '@mui/icons-material/Circle';


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

// const tableData = ([
//     {
//     id:1,
//     role_name: 'Senior Manager',
//     desc: 'blah blah blah',
//     skills_required:['Critical thinking', ' Effective Communication']
//     },

//     {
//     id:2,
//     role_name: 'Senior Manager',
//     desc: 'blah blah blah',
//     skills_required:['Critical thinking', ' Effective Communication']
//     },

//     {
//     id:3,
//     role_name: 'Senior Manager',
//     desc: 'blah blah blah',
//     skills_required:['Critical thinking', ' Effective Communication']
//     }
// ]);



export default function ViewAllAvailRoles() {


    const [jobroleData, setJobRoleData] = useState([])
  
    useEffect(()=>{
      axios.get('http://127.0.0.1:5000/jobrole').then(response => {
        console.log("SUCCESS", response)
        setJobRoleData(response.data.data)
        
        console.log(response.data.data)
      }).catch(error => {
        console.log(error)
      })
    },[])

    // const [jobRoleSkillsData, setJobRoleSkillsData] = useState([])
    // useEffect(()=>{
    //     axios.get(`http://127.0.0.1:5000/${JobRole_ID}/skills`).then(response => {
    //       console.log("SUCCESS", response)
    //       setJobRoleData(response.data.data)
          
    //       console.log(response.data.data)
    //     }).catch(error => {
    //       console.log(error)
    //     })
    //   },[])



    return (
        
        <Container sx={{mt:5}}>
        <Box sx={{ typography: { xs: 'h6', md:'h4'},borderBottom: 1}}>View Roles</Box>
        
    
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
                    {jobroleData.map((row) => (
                            <StyledTableRow key={row.JobRole_ID}>
                                <StyledTableCell sx={{ display: { xs: 'none', md: 'table-cell' } }}>{row.JobRole_ID}</StyledTableCell>
                                <StyledTableCell sx={{borderRight: {xs:0, md:'0.5px solid grey'}}}>{row.JobRole_Name}</StyledTableCell>
                                <StyledTableCell sx={{ display: { xs: 'none', md: 'table-cell' } }}>{row.JobRole_Desc}</StyledTableCell>
                                <StyledTableCell>
                                <List>
                                    <ListItem>
                                        Communication
                                    </ListItem>
                                    
                                </List>
                                
                                
                                </StyledTableCell>
                                <StyledTableCell>
                                <Link to='/ViewAllAvailRoles' underline="none">
                                <ArrowForwardIosIcon></ArrowForwardIosIcon>
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

