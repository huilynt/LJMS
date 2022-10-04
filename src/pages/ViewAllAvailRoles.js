import React from "react";
import {Grid, Link, Button} from '@mui/material';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell, { tableCellClasses }  from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { styled } from '@mui/material/styles';


const StyledTableCell = styled(TableCell)(({ theme }) => ({
    [`&.${tableCellClasses.head}`]: {
      backgroundColor: '#4dabf5',
      color: theme.palette.common.white,
    },
    [`&.${tableCellClasses.body}`]: {
      fontSize: 14,
    },
  }));

const tableData = ([
    {
    id:1,
    role_name: 'Senior Manager',
    desc: 'blah blah blah',
    skills_required:['Critical thinking', ' Effective Communication']
    },

    {
    id:2,
    role_name: 'Senior Manager',
    desc: 'blah blah blah',
    skills_required:['Critical thinking', ' Effective Communication']
    },

    {
    id:3,
    role_name: 'Senior Manager',
    desc: 'blah blah blah',
    skills_required:['Critical thinking', ' Effective Communication']
    }
]);



export default function ViewAllAvailRoles() {
    return (
        <div>
        
        <Grid sx={{m:2, borderBottom: 1}}>
            <Grid item>
                <h1>Job Roles</h1>
            </Grid>
        </Grid>
        
    
        <TableContainer sx={{mt:4}} component={Paper}>            
            <Table>
                <TableHead stickyHeader>
                    <TableRow>
                        <StyledTableCell>ID</StyledTableCell>
                        <StyledTableCell>Role Name</StyledTableCell>
                        <StyledTableCell>Description</StyledTableCell>
                        <StyledTableCell>Skills Required</StyledTableCell>
                        <StyledTableCell>Choose Role</StyledTableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {tableData.map((row) => (
                            <TableRow key={row.id}>
                                <TableCell>{row.id}</TableCell>
                                <TableCell>{row.role_name}</TableCell>
                                <TableCell>{row.desc}</TableCell>
                                <TableCell>{row.skills_required}</TableCell>
                                <TableCell>
                                <Link to='/ViewAllAvailRoles' underline="none">
                                <Button variant="contained" color="success">Select</Button>
                                </Link>
                                </TableCell>
                            </TableRow>
                        ))
                        
                    }
                </TableBody>
            </Table>
        </TableContainer>
        </div>
            
    )

}