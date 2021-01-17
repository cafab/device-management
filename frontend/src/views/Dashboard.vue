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
import EditDevice from "@/components/EditDevice.vue";

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
           field: 'id',
           label: 'ID',
           width: 50,
           numeric: true
         },
        {
           field: 'serial_number',
           label: 'Serial number',
         },
        {
           field: 'computer_name',
           label: 'Computer name',
         },
        {
           field: 'supplier',
           label: 'Supplier',
         },
        {
           field: 'price',
           label: 'Price (CHF)',
         },
         {
           field: 'purchase_date',
           label: 'Purchase date',
         },
         {
           field: 'notes',
           label: 'Notes',
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
          let devicesPrepared = []
          response.data.devices.forEach(d => {
            let device = {}
            device.id = d.id,
            device.serial_number = d.serial_number,
            device.computer_name =  d.computer_name,
            device.supplier = d.purchase_details[0].supplier,
            device.price = d.purchase_details[0].price,
            device.purchase_date = d.purchase_details[0].purchase_date,
            device.notes = d.purchase_details[0].notes
            devicesPrepared.push(device);
          });
          this.devices = devicesPrepared;
        })
        .catch(console.log)
        .finally(() => this.isLoading = false);
    },
    editDevice(device_event) {
      this.$buefy.modal.open({
      
        props: {
          title: "Edit Device",
          device: device_event,
        },
        component: EditDevice,
        parent: this,
        hasModalCard: true,
        trapFocus: true,
        /**
         * Listens for events emitted by the EditDevice
         * component.
         */
        events: {
          saved: (editedDevice) => {
            console.log(editedDevice);
            this.getDevices();
          }
        },
      });
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