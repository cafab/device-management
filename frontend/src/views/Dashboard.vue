<template>
  <div class="home">
    <h2 class="title is-2">Dashboard</h2>
    <br>
    <b-loading v-model="isLoading"></b-loading>
    <div v-if="hasDevices">
      <b-table 
        :data="devices" 
        :columns="columns"
        :striped="true"
        :hoverable="true" 
        @click="editDevice">
      </b-table>
    </div>
    <div v-else>No devices available.</div>
  </div>
</template>

<script>
import * as api from "@/api";
//import EditDevice from "@/components/EditDevice.vue";

export default {
  name: "Dashboard",
  mounted() {
    this.getDevices()
  },
  data() {
    return {
      devices: [],
      columns: [
        {
           field: 'computer_name',
           label: 'Computer name',
           width: 200
         },
        {
           field: 'ip_address',
           label: 'IP Address',
         },
        {
           field: 'accounts.0.current_account',
           label: 'Current user',
         },
         {
           field: 'accounts.0.previous_account',
           label: 'Previous user',
         },
         {
           field: 'accounts.0.last_seen',
           label: 'Last seen',
         }
      ],
      isLoading: false
    }
  },
  methods: {
    getDevices() {
      this.isLoading = true;
      api
        .getDevices()
        .then((response) => {
          this.devices = response.data.devices;
        })
        .catch(console.log)
        .finally(() => this.isLoading = false);
    },
    editDevice(device_event) {
      this.$router.push({ name: 'EditDevice', params: { device: device_event }})
    }
  },
  computed: {
    hasDevices() {
      return this.devices.length != 0;
    }
  }
};
</script>

<style scoped>

</style>