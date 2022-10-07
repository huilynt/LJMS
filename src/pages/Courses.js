import {React,useEffect, useState} from "react";
import axios from 'axios';
import Container from '@mui/material/Container';
import { styled } from '@mui/material/styles';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell, { tableCellClasses } from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import Box from '@mui/material/Box';

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

function Courses() {
    const [courses, setCourse] = useState([])
  
    useEffect(()=>{
      axios.get('http://127.0.0.1:5000/course').then(response => {
        console.log("SUCCESS", response)
        setCourse(response.data.data)
        console.log(typeof response.data.data)
        console.log(response.data.data)
      }).catch(error => {
        console.log(error)
      })
  
    }, [])

    return (
        <Container sx={{mt:5}}>
            <TableContainer component={Paper} sx={{marginTop:2}}>
                <Table sx={{minWidth: 200}}>
                    <TableHead>
                        <TableRow>
                            <StyledTableCell sx={{ display: { xs: 'none', md: 'table-cell' } }}>Code No</StyledTableCell>
                            <StyledTableCell sx={{borderRight: {xs:0, md:'0.5px solid grey'}}}>Name</StyledTableCell>
                            <StyledTableCell sx={{ display: { xs: 'none', md: 'table-cell' } }}>Description</StyledTableCell>
                            <StyledTableCell align='center'>Select Skill</StyledTableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {courses.map((course) => (
                            <StyledTableRow key={course.Course_ID}>
                                <StyledTableCell sx={{ display: { xs: 'none', md: 'table-cell' } }}>{course.Course_ID}</StyledTableCell>
                                <StyledTableCell sx={{ borderRight: {xs:0, md:'0.5px solid grey'}} }>{course.Course_Name}</StyledTableCell>
                                <StyledTableCell sx={{ display: { xs: 'none', md: 'table-cell' } }}>{course.Course_Desc}</StyledTableCell>
                                <StyledTableCell align='center'><ArrowForwardIosIcon></ArrowForwardIosIcon></StyledTableCell>
                            </StyledTableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </Container>
    )
    }

export default Courses;