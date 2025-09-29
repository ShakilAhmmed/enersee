import {createRoot} from 'react-dom/client'
import {BrowserRouter as Router, Routes, Route, Link} from "react-router";
import App from './App.jsx'
import {Home} from "./components/Home.jsx";
import {Users} from "./components/Users.jsx";


createRoot(document.getElementById('root')).render(
    <Router>
        <App/>
        <Routes>
            <Route path="/" element={<Home/>}/>
            <Route path="/users" element={<Users/>}/>
        </Routes>
    </Router>
)
