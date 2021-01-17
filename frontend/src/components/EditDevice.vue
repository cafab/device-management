<template>
  <div class="modal-card">
    <header class="modal-card-head">
      <p class="modal-card-title">{{ title }}</p>
      <button type="button" class="delete" @click="close()" />
    </header>
    <section class="modal-card-body">
      <form @submit.prevent="submit">
        <b-field label="Serial number">
          <b-input v-model="config.serial_number" disabled/>
        </b-field>
        <b-field label="Computer name">
          <b-input
            v-model="config.computer_name" disabled/>
        </b-field>
        <b-field label="Supplier">
          <b-input v-model="config.supplier"/>
        </b-field>
        <b-field label="Purchase Date">
          <b-input
            v-model="config.purchase_date"
          />
        </b-field>
        <b-field label="Price">
          <b-input
            v-model="config.price"
          />
        </b-field>
        <b-field label="Notes">
            <b-input maxlength="160" type="textarea" v-model="config.notes"></b-input>
        </b-field>
        <b-button native-type="submit">Submit</b-button>
        </form>
    </section>
  </div>
</template>

<script>
import * as api from "@/api";

export default {
  name: "EditDevice",
  props: {
    device: Object,
    title: String,
  },
  created() {
      // Copy the device properties because props cannot
      // be modified directly.
      this.config.id = this.device.id;
      this.config.serial_number = this.device.serial_number;
      this.config.computer_name = this.device.computer_name;
      this.config.supplier = this.device.supplier;
      this.config.price = this.device.price;
      this.config.purchase_date = this.device.purchase_date;
      this.config.notes = this.device.notes;
  },
  data() {
      return {
          config: {
              id: Number,
              serial_number: String,
              computer_name: String,
              supplier: String,
              price: Number,
              purchase_date: String,
              notes: String
          }
      }
  },
  methods: {
    // Close the Buefy modal.
    close() {
        // Closes the Buefy modal.
        this.$emit("close");
    },
    submit() {
        api.editDevice(this.config)
           .then((response) => {
                this.$emit("saved", response.data.purchase_details);
           })
           .catch(console.log)
           .finally(() => {
                // Close the Buefy modal.
                this.close();
           });

    },
    
  },
};
</script>