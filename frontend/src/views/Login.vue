<template>
  <section class="login narrow-view">
    <h3 class="title is-3">Login</h3>
    <form @submit.prevent="submitForm">
      <b-field label="Username">
        <b-input ref="username" v-model="username" required></b-input>
      </b-field>

      <b-field label="Password">
        <b-input v-model="password" type="password" password-reveal required>
        </b-input>
      </b-field>
      <b-button native-type="submit">Login</b-button>
    </form>
  </section>
</template>

<script>
import * as api from "@/api";
import { auth } from "@/auth";

export default {
  name: "Login",
  data() {
    return {
      username: "",
      password: "",
    };
  },
  mounted() {
    /**
     * Sets the cursor focus on the username field at
     * mount time.
     */
    this.$refs.username.focus();
  },
  methods: {
    /**
     * The login method logs the user in and stores the
     * received access and refresh token in the Vue
     * observable auth instance.
     */
    login: function (userData) {
      api
        .login(userData)
        .then((response) => {
          auth.accessToken = response.data.access_token;
          auth.refreshToken = response.data.refresh_token;
          this.$router.push("/dashboard");
        })
        .catch(console.log);
    },
    submitForm() {
      this.login({
        username: this.username,
        password: this.password,
      });
    },
  },
};
</script>
