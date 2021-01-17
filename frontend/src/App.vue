<template>
  <div id="app">
    <TopNavbar></TopNavbar>
    <div class="container router-view">
      <router-view />
    </div>
    <Footer></Footer>
  </div>
</template>

<script>
import TopNavbar from "@/components/TopNavbar.vue";
import Footer from "@/components/Footer.vue";

export default {
  name: "App",
  components: {
    TopNavbar,
    Footer,
  },
};
</script>

<style scoped>
.router-view {
  min-height: 100vh;
  margin-top: 7vh;
  padding-left: 0.5vw;
  padding-right: 0.5vw;
}
.narrow-view {
  margin: 0 auto;
  max-width: 768px;
  width: 100%;
  height: 100%;
}
</style>