import axios from "axios";
import router from "@/router";
import createAuthRefreshInterceptor from "axios-auth-refresh";
import { NotificationProgrammatic as Notification } from "buefy";
import { auth } from "@/auth";

/**
 * Sets the API URL.
 */
const API_URL = "http://127.0.0.1:5000/api";

/**
 * Sets the default base URL for this axios instance.
 */
axios.defaults.baseURL = API_URL;

/**
 * The isHandlerEnabled function which will check if the global handler should 
 * be used or not. Here it's also possible to implement additional custom logic.
 */
const isHandlerEnabled = (config = {}) => {
  return Object.prototype.hasOwnProperty.call(config, "handlerEnabled") &&
    !config.handlerEnabled
    ? false
    : true;
};

const errors = ["token_expired", "authorization_required"];

/**
 * The axios response interceptor. Must be above
 * the createAuthRefreshInterceptor.
 */
axios.interceptors.response.use(
  /**
   * Returns a successful response to the original
   * API caller function.
   */
  (response) => {
    console.log("successful response intercept: " + response)
    return response;
  },
  /**
   * Handles a possible error response accordingly.
   * Any status codes that fall outside the range of
   * a 2xx HTTP response, cause the error callback function
   * to trigger.
   */
  (error) => {
    let redirect;
    /**
     * An error response from the token/refresh endpoint
     * indicates that the sent refresh token in the original
     * request has expired. The refresh and access token will
     * be deleted and the user redirected to the login page.
     * Router.replace() replaces the current page in the
     * browser history instead of pushing it on the stack.
     * Router.push()/.replace() throws an error if the
     * user is on the correct page, this may happen if multiple
     * requests fail at the time.
     */
    if (error.response.config.url.includes("token/refresh")) {
      console.log("error response intercept (includes token/refresh)")
      auth.refreshToken = null;
      auth.accessToken = null;
      redirect = "/login";
    }

    /**
     * Whenever an invalid_token error response gets returned,
     * then something is wrong with either token. The refresh
     * and access token will be deleted and the user redirected
     * to the login page.
     */
    if (error.response.data.error == "invalid_token") {
      console.log("error response intercept (equals invalid_token)")
      auth.refreshToken = null;
      auth.accessToken = null;
      router.replace("/login").catch(() => {});
    }

    /**
     * Whenever a token_expired error response gets returned,
     * which doesn't come from the token/refresh endpoint, then a
     * Promise.reject error gets returned which will trigger the
     * refreshAuthLogic function in order to refresh the access
     * token without showing an error notification to the user.
     */
    if (
      errors.indexOf(error.response.data.error) !== -1 &&
      !error.response.config.url.includes("token/refresh")
    ) {
      console.log("error response intercept (token/refresh not included): " + error.response.config.url + ", " + error.response.data.error)
      return Promise.reject(error);
    }

    /**
     * When no handlerEnabled property has been passed to an
     * axios instance and the returned error contains a
     * response, then an error notification will be shown to
     * the user.
     */
    if (isHandlerEnabled(error.config) && error.response) {
      console.log("error response intercept (handlerEnabled and response)")
      if (redirect) {
        router.replace(redirect).catch(() => {});
      }
      let message = error.response.data.message;
      if (!message) {
        message = error.message;
      }
      Notification.open({
        duration: 5000,
        type: "is-danger",
        message: message,
      });
    }
    console.log("error response intercept last promise reject!)")
    return Promise.reject(error);
  }
);

/**
 * The refreshAuthLogin function handles the token_expired error
 * which is coming back from the backend. A new request with the
 * refresh token in the Authorization header will be made to the
 * /token/refresh route in order to receive a new access token.
 */
function refreshAuthLogic(failedRequest) {
  console.log("refreshAuthLogic function triggered: ")
  console.log(failedRequest.config)
  let handlerEnabled = isHandlerEnabled(failedRequest.config);
  if (errors.indexOf(failedRequest.response.data.error) !== -1) {
    return postRefreshToken(handlerEnabled)
      .then((tokenRefreshResponse) => {
        auth.accessToken = tokenRefreshResponse.data.access_token;
        failedRequest.response.config.headers["Authorization"] =
          "Bearer " + tokenRefreshResponse.data.access_token;
        return Promise.resolve();
      });
    // catch() doesn't work here. It is never called...
    // that is why there is another inteceptor above
  }
  // Correctly reject everything that is not "token_expired"
  console.log("refreshAuthLogic Promise reject ")
  return Promise.reject();
}

/**
 * The createAuthRefreshInterceptor plugin stalls additional 
 * requests that have come in while waiting for a new authorization 
 * token and resolves them when a new token is available.
 */

console.log("createAuthRefreshInterceptor function triggered")
createAuthRefreshInterceptor(axios, refreshAuthLogic);

/**
 * The axios request interceptor is used to inject either
 * the access or refresh token to requests.
 */
axios.interceptors.request.use((request) => {
  // The refresh token is also in the Authorization header
  // We don't want to overwrite it
  // Affects the /token/refresh as well as the /logout-refresh-token route

  let token = "";

  /**
   * If for the current request the useRefreshToken has been set to true,
   * then the refresh token will be set in the Authorization header,
   * otherwise the access token gets set.
   */
  if (request.useRefreshToken) {
    token = auth.refreshToken;
  } else {
    token = auth.accessToken;
  }
  if (token) {
    console.log("request interceptor has token")
    request.headers["Authorization"] = `Bearer ${token}`;
  }
  return request;
});


/**
 * The login method returns a promise with JSON
 * data containing access and refresh tokens on a successful
 * request, otherwise an error.
 */
export function login(userData) {
  return axios.post("/login", userData);
}

/**
 * The revokeTokens method revokes/blacklists the access and
 * refresh token on the backend.
 */
export function revokeTokens() {
  let revokeAccessToken = () => axios.delete("/revoke-access-token");
  let revokeRefreshToken = () => 
    axios.delete("/revoke-refresh-token", { useRefreshToken: true });

  /**
   * Do not revoke access token if it already expired,
   * otherwise a token refresh gets triggered.
   */
  if (auth.isExpiredAccessToken()) {
    return revokeRefreshToken();
  }

  return Promise.all([revokeAccessToken(), revokeRefreshToken()]);
}

/**
 * The postRefreshToken method refreshes the access token on the
 * backend. The skipAuthRefresh property is set to true in order to
 * skip the axios interceptor and the useRefreshToken is also set
 * to true so that the axios request interceptor uses the refresh
 * token instead of the access token.
 */
export function postRefreshToken(handlerEnabled) {
  return axios.post("/token/refresh", null, {
    skipAuthRefresh: true,
    useRefreshToken: true,
    handlerEnabled: handlerEnabled,
  });
}

/**
 * Any empty request to the backend to check if the user is still logged in.
 */
export function triggerTokenRefresh() {
  return axios.get("/check-logged-in");
}

/**
 * The getDevices method returns all devices.
 */
export function getDevices() {
  return axios.get("/devices");
}

export function editDevice(payload) {
  return axios.post("/purchase-details", payload);
}


