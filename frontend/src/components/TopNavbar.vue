<template>
  <b-navbar class="container" fixed-top>
    <template slot="brand">
      <b-navbar-item tag="router-link" :to="{ path: '/' }">
        <p class="navbar-title">Device Management</p>
      </b-navbar-item>
    </template>
    <template slot="start">
      <b-navbar-item
        v-if="isAuthenticated"
        tag="router-link"
        :to="{ path: '/dashboard' }"
        class="is-info"
      >
        Dashboard
      </b-navbar-item>
    </template>
    <template slot="end">
      <b-navbar-item v-if="!isAuthenticated" tag="div">
        <div class="buttons">
          <router-link to="/login" class="button is-info">
            Login
          </router-link>
        </div>
      </b-navbar-item>
      <b-navbar-item v-else tag="div">
        <div class="buttons" tag="div">
          <div @click="logout">
            <router-link to="/" class="button is-info"> Logout </router-link>
          </div>
        </div>
      </b-navbar-item>
    </template>
  </b-navbar>
</template>

<script>
import { auth } from "@/auth";
import * as api from "@/api";

export default {
  name: "TopNavbar",
  methods: {
    logout() {
      api
        .revokeTokens()
        .then((response) => {
          if (response.length > 1) {
            response.forEach((element) => {
              console.log(element.data.message);
            });
          } else {
            console.log(response.data.message);
          }
        })
        .catch(console.log)
        .finally(() => {
          auth.accessToken = null;
          auth.refreshToken = null;
        });
    }
  },
  computed: {
    /**
     * This computed method indicates that a user is authenticated. 
     * It checks if the access token is not null.
     */
    isAuthenticated: function () {
      return Boolean(auth.accessToken);
    }
  }
};
</script>

<style scoped>


.navbar-title {
  font-family: Helvetica, sans-serif;
  font-size: 25px;
  font-weight: 900;
  color: #167df0;
}
</style>

