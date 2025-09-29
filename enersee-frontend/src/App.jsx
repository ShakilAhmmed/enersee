import {Link} from "react-router";

function App() {
    return (
        <>
            <nav className="flex gap-4 p-4 bg-gray-200">
                <Link to="/">Home</Link>
                <Link to="/users">Users</Link>
            </nav>
        </>
    )
}

export default App
