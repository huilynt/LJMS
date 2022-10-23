import { useEffect, useState, React } from 'react';
import axios from 'axios';
import {Grid, Container} from '@mui/material';
import { styled } from '@mui/material/styles';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell, { tableCellClasses } from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import EditIcon from '@mui/icons-material/Edit';
import DeleteOutlineIcon from '@mui/icons-material/DeleteOutline';
import IconButton from '@material-ui/core/IconButton';
import Stack from '@mui/material/Stack';
import { pink } from '@mui/material/colors';
import Chip from '@mui/material/Chip';
import Link from '@mui/material/Link';
import Button from '@mui/material/Button';

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

function LearningJourney() {
    const [learningjourney, setLearningJourney] = useState([]);
    const [jobrole, setRole] = useState([]);


    useEffect(() => {
        sessionStorage.setItem("userId", "140525");

        axios.post(`http://127.0.0.1:5000/learningjourney`, {"userId":sessionStorage.userId})
        .then ((response) => {
            console.log(response)
            setLearningJourney(response.data.data)
        })
        .catch(error => {
            console.log(error.message)
        })

        axios
        .get("http://127.0.0.1:5000/jobrole")
        .then((response) => {
            setRole(response.data.data);
        })
        .catch((error) => {
            console.log(error);
        });
    }, [])

    return (
        <Container sx={{mt:5}}>
            <Grid container sx={{borderBottom:1, display:'flex', alignItems: 'center', pb:1}}>
                <Grid item sx={{ typography: { xs: 'h6', md:'h4'}}} xs={8} md={4}>
                    Learning Journey
                </Grid>
                <Grid item xs={3} md={2} >
                <Link href='/ViewAllAvailRoles' underline="none">
                    <Button variant="contained" color="success">Create</Button>
                </Link>
                </Grid>

            </Grid>

            <TableContainer component={Paper} sx={{marginTop:2, marginBottom:10}}>
                <Table sx={{minWidth: 200}}>
                    <TableHead>
                        <TableRow>
                            <StyledTableCell sx={{ display: { xs: 'none', md: 'table-cell' } }}>Role ID</StyledTableCell>
                            <StyledTableCell sx={{ display: { xs: 0 , md: 'table-cell' } }}>Job Role</StyledTableCell>
                            <StyledTableCell sx={{borderRight: {xs:0, md:'0.5px solid grey'}}}>Status</StyledTableCell>
                            <StyledTableCell align='center'>Edit Learning Journey</StyledTableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {learningjourney.map((learningjourney) => (
                            <StyledTableRow>
                                <StyledTableCell sx={{ display: { xs: 'none', md: 'table-cell' } }}>{learningjourney.JobRole_ID}</StyledTableCell>
                                {jobrole.filter(jobrole => jobrole.JobRole_ID === learningjourney.JobRole_ID).map((jobrole) => (
                                <StyledTableCell sx={{ display: { xs: 0 , md: 'table-cell' } }}>{jobrole.JobRole_Name}</StyledTableCell>
                                ))}
                                <StyledTableCell align='center' sx={{borderRight: {xs:0, md:'0.5px solid grey'}}}>
                                    {learningjourney.LearningJourney_Status == "Completed" ? <Chip label="Completed" color="success" size="small" /> : <Chip label="Incomplete" size="small" />}
                                </StyledTableCell>
                                <StyledTableCell align='center'>
                                    <Stack direction="row" justifyContent='center'>
                                            <Link href={'/journey/' + learningjourney.JobRole_ID} underline="none">
                                                <IconButton><EditIcon></EditIcon></IconButton>
                                            </Link>
                                            <IconButton><DeleteOutlineIcon sx={{ color: pink[200] }}></DeleteOutlineIcon></IconButton>
                                    </Stack>
                                </StyledTableCell>
                            </StyledTableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </Container>
    )
}

export default LearningJourney;