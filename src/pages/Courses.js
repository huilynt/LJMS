import {React,useEffect, useState} from "react";
import axios from 'axios';
import { useNavigate } from "react-router-dom";
import {Link, Container, Box} from '@mui/material';
import { styled } from '@mui/material/styles';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell, { tableCellClasses } from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';

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
    const [courses, setCourse] = useState([]);
    // const navigate = useNavigate();

    const courseDetails = (event,  message) => {
        console.log('link clicked')
        console.log(message)
        // navigate('/Courses/' + message)
    }

    useEffect(()=>{
        axios.get('http://127.0.0.1:5000/course').then(response => {
            console.log("SUCCESS", response)
            setCourse(response.data.data)
        }).catch(error => {
            console.log(error)
        })
    
        }, [])

    return (
        <Container sx={{mt:5}}>
            <Box sx={{ typography: { xs: 'h6', md:'h4'},borderBottom: 1}}>Courses</Box>

            <TableContainer component={Paper} sx={{marginTop:2}}>
                <Table sx={{minWidth: 200}}>
                    <TableHead>
                        <TableRow>
                            <StyledTableCell sx={{ display: { xs: 'none', md: 'table-cell' } }}>Code No</StyledTableCell>
                            <StyledTableCell sx={{borderRight: {xs:0, md:'0.5px solid grey'}}}>Name</StyledTableCell>
                            <StyledTableCell sx={{ display: { xs: 'none', md: 'table-cell' } }}>Description</StyledTableCell>
                            <StyledTableCell align='center'>Assign Skills</StyledTableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {courses.map((course) => (
                            <StyledTableRow key={course.Course_ID}>
                                <StyledTableCell sx={{ display: { xs: 'none', md: 'table-cell' } }}>{course.Course_ID}</StyledTableCell>
                                <StyledTableCell sx={{ borderRight: {xs:0, md:'0.5px solid grey'}} }>{course.Course_Name}</StyledTableCell>
                                <StyledTableCell sx={{ display: { xs: 'none', md: 'table-cell' } }}>{course.Course_Desc}</StyledTableCell>
                                <StyledTableCell align="center">
                                    {/* <Link onClick={event => courseDetails(event, course.Course_ID)} underline="none">
                                        <ArrowForwardIosIcon></ArrowForwardIosIcon>
                                    </Link> */}
                                    <Link href={"/hr/edit/courses/" + course.Course_ID} underline="none">
                                        <ArrowForwardIosIcon></ArrowForwardIosIcon>
                                    </Link>

                                </StyledTableCell>      
                            </StyledTableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </Container>
    )
    }

export default Courses;