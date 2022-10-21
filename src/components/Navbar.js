import React, { useState } from "react";
import { Link } from "react-router-dom";
import {
  AppBar,
  IconButton,
  Tab,
  Tabs,
  Toolbar,
  Typography,
  useMediaQuery,
  useTheme,
} from "@mui/material";
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import SchoolIcon from '@mui/icons-material/School';

const Navbar = () => {
  const [value, setValue] = useState();
  const theme = useTheme();
  console.log(theme);
  const isMatch = useMediaQuery(theme.breakpoints.down("md"));
  console.log(isMatch);
//   const routes = ["./pages/LearningJourney", "./pages/Courses", "./pages/Skills", "./pages/Roles"];
  const routes = ["/journey", "/Courses", "/Skills", "/Roles"];

  return (
    <React.Fragment>
    <AppBar sx={{ background: "#9CCAFF" }} position="inherit">
        <Toolbar>
            <>
                <IconButton size="large" edge="start" color="inherit" aria-label="profile">
                    <SchoolIcon/>
                </IconButton>
                <Typography variant="h5" sx={{ fontWeight:'bold' }}>
                    LJPS
                </Typography>
            </>
            <>
            <Tabs
                sx={{ marginLeft: "auto" }}
                indicatorColor="primary"
                textColor="inherit"
                value={value}
                onChange={(e, value) => setValue(value)}
            >

                <Tab label="Learning Journey" value={routes[0]} component={Link} to={routes[0]}/>

                <Tab label="Courses" value={routes[1]} component={Link} to={routes[1]}/>

                <Tab label="Skills" value={routes[2]} component={Link} to={routes[2]}/>

                <Tab label="Roles" value={routes[3]} component={Link} to={routes[3]}/>

            </Tabs>
            <IconButton size="large" edge="start" color="inherit" aria-label="profile" >
                <AccountCircleIcon/> 
            </IconButton>
            <Typography variant="body2" sx={{ fontWeight:'bold' }}>
                    HR
            </Typography>
            </>
        </Toolbar>
    </AppBar>
    </React.Fragment>
    
  );
};

export default Navbar;