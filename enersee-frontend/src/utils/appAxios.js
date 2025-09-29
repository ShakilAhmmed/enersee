import axios from 'axios';

const createAxios = () => {
    const appAxios = axios.create({
        baseURL: import.meta.env.API_BASE_URL,
        withCredentials: true,
    });


    appAxios.interceptors.response.use(
        (response) => {
            if (String(response.data.code).substr(0, 2) == 40) {
                return Promise.reject(response);
            }
            return Promise.resolve(response);
        },
        (error) => {
            const statusCode = parseInt(error.response.status);
            if (statusCode === 409) {
                return Promise.reject(error.response)
            }
            if (statusCode === 410) {
                return resetTokenAndReattemptRequest(error);
            }
            if (statusCode === 401) {
                console.log("TODO;Handle UnAuthenticated.")
            }
            return Promise.reject(error.response)

        },
    );
    return appAxios;
};

/**
 * Call getAxios
 *
 */
const getAxios = () => createAxios();

export default getAxios;


/**
 * Check is already processing or not
 */
let isAlreadyFetchingAccessToken = false;

/**
 * Store original requests
 */
let subscribers = [];
/**
 * Call refresh token api and regenerate the original request and set the new token in request header
 *
 * @param {*} error
 */
const resetTokenAndReattemptRequest = (error) => {
    try {
        const {response: errorResponse} = error;

        const retryOriginalRequest = new Promise(resolve => {
            addSubscriber(() => {
                resolve(axios(errorResponse.config));
            });
        });

        if (!isAlreadyFetchingAccessToken) {
            isAlreadyFetchingAccessToken = true;
            return refreshApi()
                .then((res) => {
                    reCallRequestFromQueue();
                    console.log(res);
                    return retryOriginalRequest;
                })
                .catch(refreshError => {
                    return Promise.reject(refreshError);
                })
        } else {
            return retryOriginalRequest;
        }
    } catch (err) {
        return Promise.reject(err);
    }
}

/**
 * Call the refresh token api
 *
 */
const refreshApi = async () => {
    try {
        const response = await getAxios().post(`${process.env.API_BASE_URL}/api/v1/auth/refresh`);
        return Promise.resolve(response.data)
    } catch (error) {
        return Promise.reject(error);
    }
}

/**
 * Call the original request form queue
 *
 */
const reCallRequestFromQueue = () => {
    subscribers.forEach(callback => callback());
    subscribers = [];
}

/**
 * Add request to the queue
 *
 * @param {*} callback
 */
const addSubscriber = (callback) => {
    subscribers.push(callback);
}