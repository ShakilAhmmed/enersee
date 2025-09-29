import {useEffect} from "react";
import {parseApiURL} from "../utils/helpers.js";
import {USER_API_PREFIX} from "../constants/URIConstants.js";

export function Users() {

    useEffect(() => {
        console.log(parseApiURL(USER_API_PREFIX, '/'))
    }, []);

    return (
        <>
            <h1>Users</h1>
        </>
    )
}