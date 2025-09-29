import getAxios from "../utils/appAxios.js";
import {parseApiURL} from "../utils/helpers.js";
import {USER_API_PREFIX} from "../constants/URIConstants.js";

export const getUsers = async (params) => {
    try {
        const response = await getAxios().get(parseApiURL(USER_API_PREFIX),
            {params: {...params}}
        );
        return Promise.resolve(response.data);
    } catch (error) {
        return Promise.reject(error.data);
    }
}