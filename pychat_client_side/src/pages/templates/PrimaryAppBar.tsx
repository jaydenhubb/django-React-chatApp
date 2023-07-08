// import { Link } from "@mui/icons-material";
import { AppBar, Link, Toolbar, Typography } from "@mui/material"
import { useTheme } from "@mui/material/styles";


const PrimaryAppBar = () => {
    const theme = useTheme()
  return (
    <AppBar sx={{
        backgroundColor: "#b1bccc", 
        borderBottom: `1px solid white`
        }}
        >
        <Toolbar variant="dense" sx={{
            height: theme.primaryAppBar.height,
            minHeight: theme.primaryAppBar.height
            }}
        >
            <Link href="/" underline="none" color="inherit">
                <Typography 
                variant="h6" 
                noWrap 
                component="div" 
                sx={{ display: { fontWeight: 700, letterSpacing: "-0.5px" } }}>
                    Pychat
                </Typography>
            </Link>
        </Toolbar>
    </AppBar>
  )
}

export default PrimaryAppBar