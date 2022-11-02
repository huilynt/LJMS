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
  const userRoutes = ["/journey", "/courses", "/skills", "/roles"];
  const hrRoutes = ["/hr/courses", "/hr/skills", "/hr/roles"];
  const hrPages = ["Courses", "Skills", "Roles"];
  const userPages = ["Learning Journey", "Courses", "Skills", "Roles"];

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
              {sessionStorage.role === "1" ?
                <Menu
                  anchorEl={anchorElNav}
                  anchorOrigin={{vertical: 'bottom',horizontal: 'left'}}
                  keepMounted
                  transformOrigin={{vertical: 'top',horizontal: 'left'}}
                  open={Boolean(anchorElNav)}
                  onClose={handleCloseNavMenu}
                  sx={{display: { xs: 'block', md: 'none' }}}
                >
                  {hrPages.map((page, idx) => (
                    <MenuItem key={page} onClick={() => {navigate(hrRoutes[idx])}}>
                      <Typography textAlign="center">{page}</Typography>
                    </MenuItem>
                  ))}
                </Menu> 
              :
                <Menu
                anchorEl={anchorElNav}
                anchorOrigin={{vertical: 'bottom',horizontal: 'left'}}
                keepMounted
                transformOrigin={{vertical: 'top',horizontal: 'left'}}
                open={Boolean(anchorElNav)}
                onClose={handleCloseNavMenu}
                sx={{display: { xs: 'block', md: 'none' }}}
              >
                {userPages.map((page, idx) => (
                  <MenuItem key={page} onClick={() => {navigate(userRoutes[idx])}}>
                    <Typography textAlign="center">{page}</Typography>
                  </MenuItem>
                ))}
              </Menu>
              }      
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
                {sessionStorage.role === "1" ? <Tab label="Courses" value={hrRoutes[0]} component={Link} to={hrRoutes[0]}/> 
                : <Tab label="Learning Journey" value={userRoutes[0]} component={Link} to={userRoutes[0]}/>}

                {sessionStorage.role === "1" ? <Tab label="Skills" value={hrRoutes[1]} component={Link} to={hrRoutes[1]}/>
                : <Tab label="Courses" value={userRoutes[1]} component={Link} to={userRoutes[1]}/>}

                {sessionStorage.role === "1" ? <Tab label="Roles" value={hrRoutes[2]} component={Link} to={hrRoutes[2]}/>
                : <Tab label="Skills" value={userRoutes[2]} component={Link} to={userRoutes[2]}/>}

                {sessionStorage.role === "1" ? <></>
                : <Tab label="Roles" value={userRoutes[3]} component={Link} to={userRoutes[3]}/>}

              </Tabs>
            </>
          </>}
          <IconButton size="large" edge="start" color="inherit" aria-label="profile" >
            <AccountCircleIcon/> 
          </IconButton>
          {sessionStorage.role === "1" ? 
          <Typography variant="body2" sx={{ fontWeight:'bold' }}>
                  Admin
          </Typography>
          : 
          <Typography variant="body2" sx={{ fontWeight:'bold' }}>
                  User
          </Typography>}
          
        </Toolbar> 
      </AppBar>
    </React.Fragment>
  );
};

export default Navbar;