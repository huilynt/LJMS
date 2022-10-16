import * as React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogTitle from '@mui/material/DialogTitle';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

function EditConfirm(props){
    const [open, setOpen] = React.useState(true);
    let navigate = useNavigate();
    let location = useLocation();

    const handleClickOpen = () => {
        setOpen(true);
    };

    const handleClose = () => {
        setOpen(false);
        navigate('/hr/' + props.name);
    };


    return (
        <div>
            <Dialog
                open={open}
                keepMounted
                onClose={handleClose}
                aria-describedby="edit-success"
                maxWidth="sm"
            >
                <DialogTitle sx={{px: {xs:5,md:20}}}>{"Edit Successful"}</DialogTitle>
                <div>
                    <CheckCircleIcon color="success" sx={{fontSize: {xs:100,md:200}, display: 'block', margin:'auto'}}/>
                </div>
                <DialogActions >
                    <Button autoFocus onClick={handleClose}>Return to Skills</Button>
                </DialogActions>
            </Dialog>
        </div>
    );
}

export default EditConfirm;