import {React,useEffect, useState} from "react";
import axios from 'axios';
import { useParams } from "react-router-dom";
import { Container, Divider} from '@mui/material';
import Table from '@mui/material/Table';
import TableCell from '@mui/material/TableCell';
import TableRow from '@mui/material/TableRow';
//import Box from '@mui/material/Box';

function CourseInfo() {
    const [courseInfo, setCourseInfo] = useState("");
    let {courseId} = useParams();

    useEffect(()=>{
      axios.get('http://127.0.0.1:5000/course/' + courseId).then(response => {
        console.log("SUCCESS", response)
        setCourseInfo(response.data.data)
      }).catch(error => {
        console.log(error)
      })
  
    }, [])

    return (
        <Container sx={{mt:5}}>
            <h1>{courseInfo.Course_Name}</h1>
            <Divider />
            <Table sx={{borderCollapse:"separate", borderSpacing:"0px 10px"}}>
                <TableRow>
                    <TableCell><b>Course ID</b></TableCell>
                    <TableCell sx={{border: 2}}>{courseInfo.Course_ID}</TableCell>
                </TableRow>

                <TableRow>
                    <TableCell><b>Name of Course</b></TableCell>
                    <TableCell sx={{border: 2}}>{courseInfo.Course_Name}</TableCell>
                </TableRow>

                <TableRow>
                    <TableCell><b>Type</b></TableCell>
                    <TableCell sx={{border: 2}}>{courseInfo.Course_Type}</TableCell>
                </TableRow>

                <TableRow>
                    <TableCell><b>Category</b></TableCell>
                    <TableCell sx={{border: 2}}>{courseInfo.Course_Category}</TableCell>
                </TableRow>

                <TableRow>
                    <TableCell><b>Description</b></TableCell>
                    <TableCell sx={{border: 2}}>{courseInfo.Course_Desc}</TableCell>
                </TableRow>
            </Table>

        </Container>
        
    )
    }

export default CourseInfo;