import Vue from "vue";

/**
 * The Vue observable state instance is a simple
 * store that holds the access and refresh token.
 * In order for the different Vue components to
 * react to changes in the state instance, it must
 * be Vue observable.
 */
export const auth = Vue.observable({
    data: {
      accessToken: "",
      refreshToken: ""
    },
    get accessToken() {
      return this.data.accessToken;
    },
    set accessToken(value) {
      this.data.accessToken = value;
    },
    get refreshToken() {
      return this.data.refreshToken;
    },
    set refreshToken(value) {
      this.data.refreshToken = value;
    },
    isExpiredAccessToken() {
      try {
        const data = JSON.parse(atob(this.accessToken.split(".")[1]));
        // JS deals with dates in milliseconds since epoch
        const exp = new Date(data.exp * 1000);
        const now = new Date();
        return now > exp;
      } catch {
        return true;
      }
    },
  });