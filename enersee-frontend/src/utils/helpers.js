import {API_VERSION} from "../constants/URIConstants.js";

export const parseApiURL = (resource, uri) => {
    return "/api/__API_VERSION__/__RESOURCE__/__URI__"
        .replace("__API_VERSION__", API_VERSION)
        .replace("__RESOURCE__", resource)
        .replace("__URI__", uri)
        .replace("//", "/");
};