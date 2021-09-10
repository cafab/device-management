<template>
<div>
  <div class="tile is-ancestor">
    <div class="tile is-8 is-parent">
      <div class="tile is-child box">
        <p class="title">Computer</p>
        <table class="table">
          <tbody>
            <tr>
               <th>Computer name</th>
               <td>{{ computer.computer_name }}</td>
            </tr>
            <tr>
               <th>Serial number</th>
               <td>{{ computer.serial_number }}</td>
            </tr>
            <tr>
               <th>IP address</th>
               <td>{{ computer.ip_address}}</td>
            </tr>
            <tr>
               <th>Computer model</th>
               <td>{{ computer.computer_model }}</td>
            </tr>
            <tr>
               <th>CPU</th>
               <td>{{ computer.cpu }}</td>
            </tr>
            <tr>
               <th>Memory</th>
               <td>{{ computer.memory }}</td>
            </tr>
            <tr>
               <th>Hard disk</th>
               <td>{{ computer.hard_disk }}</td>
            </tr>
            <tr>
               <th>OS</th>
               <td>{{ computer.os }}</td>
            </tr>
            <tr>
               <th>OS installation date</th>
               <td>{{ computer.os_install_date }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <PurchaseDetailsForm :device="device"/>
  </div>
</div>
</template>

<script>
//import * as api from "@/api";
import PurchaseDetailsForm from '@/components/PurchaseDetailsForm.vue';

export default {
  name: "EditDevice",
  components: {
    PurchaseDetailsForm
  },
  props: {
    device: Object,
    title: String,
  },
  created() {
      // Copy the device properties because props cannot
      // be modified directly.
      this.computer.computer_name = this.device.computer_name;
      this.computer.serial_number = this.device.serial_number;
      this.computer.ip_address = this.device.ip_address;
      this.computer.computer_model = this.device.computer_model;
      this.computer.cpu = this.device.cpu;
      this.computer.memory = this.device.memory;
      this.computer.hard_disk = this.device.hard_disk;
      this.computer.os = this.device.os;
      this.computer.os_install_date = this.device.os_install_date;
  },
  data() {
      return {
          computer: {
            computer_name: String,
            serial_number: String,
            ip_address: String,
            computer_model: String,
            cpu: String,
            memory: String,
            hard_disk: String,
            os: String,
            os_install_date: String
          },
          accounts: {
            current_account: String,
            previous_account: String,
            last_seen: String
          }
      }
  },
  methods: {
    // Close the Buefy modal.
    close() {
        // Closes the Buefy modal.
        this.$router.push({ name: 'Dashboard' })
    },
    // submit() {
    //     api.editDevice(this.purchase_details)
    //        .then(() => {
    //             //this.$emit("saved", response.data.purchase_details);
    //             this.$router.push({ name: 'Dashboard' })
    //        })
    //        .catch(console.log)
    //        .finally(() => {
    //             // Close the Buefy modal.
    //             this.close();
    //        });

    // },
    
  },
};
</script>