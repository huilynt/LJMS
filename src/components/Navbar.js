import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  AppBar,
  IconButton,
  Tab,
  Tabs,
  Toolbar,
  Typography,
  useMediaQuery,
  useTheme, 
  Box,
  Menu,
  MenuItem
} from "@mui/material";
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import SchoolIcon from '@mui/icons-material/School';

const Navbar = () => {
  const [value, setValue] = useState();
  const theme = useTheme();
  const isMatch = useMediaQuery(theme.breakpoints.down("md"));
  const routes = ["/journey", "/hr/courses", "/hr/skills", "/hr/roles"];
  const pages = ["Learning Journey", "Courses", "Skills", "Roles"];

  const [anchorElNav, setAnchorElNav] = React.useState(null);
  const navigate = useNavigate();
  const handleOpenNavMenu = (event) => {
    setAnchorElNav(event.currentTarget);
  };
  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  return (
    <React.Fragment>
      <AppBar sx={{ background: "#9CCAFF" }} position="inherit">
        <Toolbar>
          { isMatch === true ?
          <>
            <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' }, alignItems:"center" }}>
              <IconButton size="large" edge="start" color="inherit" onClick={handleOpenNavMenu}>
                  <SchoolIcon/>
              </IconButton>
              <Typography variant="h5" sx={{ fontWeight:'bold', verticalAlign:"center" }}>
                  LJPS
              </Typography>
              <Menu
                anchorEl={anchorElNav}
                anchorOrigin={{vertical: 'bottom',horizontal: 'left'}}
                keepMounted
                transformOrigin={{vertical: 'top',horizontal: 'left'}}
                open={Boolean(anchorElNav)}
                onClose={handleCloseNavMenu}
                sx={{display: { xs: 'block', md: 'none' }}}
              >
                {pages.map((page, idx) => (
                  <MenuItem key={page} onClick={() => {navigate(routes[idx])}}>
                    <Typography textAlign="center">{page}</Typography>
                  </MenuItem>
                ))}
              </Menu>
            </Box>
          </> :
          <>
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
            </>
          </>}
          <IconButton size="large" edge="start" color="inherit" aria-label="profile" >
            <AccountCircleIcon/> 
          </IconButton>
          <Typography variant="body2" sx={{ fontWeight:'bold' }}>
                  HR
          </Typography>
        </Toolbar> 
      </AppBar>
    </React.Fragment>
  );
};

export default Navbar;