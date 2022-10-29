import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogTitle from '@mui/material/DialogTitle';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import { DeleteOutlineOutlined } from '@material-ui/icons';
import DeleteOutlinedIcon from '@mui/icons-material/DeleteOutlined';
import axios from 'axios';
import { red } from '@mui/material/colors';

function DeleteConfirm(props){
    const [open, setOpen] = React.useState(true);
    // let navigate = useNavigate();

    // const handleClickOpen = () => {
    //     setOpen(true);
    // };

    // const handleClose = () => {
    //     setOpen(false);
        // navigate('/hr/' + props.name);
    // };

    const handleConfirm = () => {
        axios.post("http://127.0.0.1:5000/journey/delete",
            {
                journeyId: props.journeyId
            }
        ).then((response) => {
            console.log(response)
        })
        .catch((error) => {
            console.log(error);
        });
    }

    return (
        <div>
            <Dialog
                open={open}
                keepMounted
                // onClose={handleClose}
                aria-describedby="edit-success"
                maxWidth="sm"
            >
                <DialogTitle sx={{px: {xs:5,md:20}, textAlign: 'center'}}>{`Delete ${props.roleName} Learning Journey`}</DialogTitle>
                <div>
                    <DeleteOutlinedIcon  sx={{ fontSize: 100, display: 'block', margin:'auto', color: red[500] }}/>
                </div>
                <DialogActions sx={{ display: 'block', margin:'auto' }}>
                    <Button href={'/' + props.name} color="error" variant="contained">Cancel</Button>
                    <Button autoFocus href={'/' + props.name} color="success" variant="contained" onClick={() => handleConfirm()}>Confirm</Button>
                </DialogActions>
            </Dialog>
        </div>
    );
}

export default DeleteConfirm;