<template>
<div class="is-parent">
  <div class="tile is-child box">
    <p class="title">Purchase Details</p>
    <section v-if="hasPurchaseDetails">
      <table class="table" >
        <tbody>
          <tr>
             <th>Supplier</th>
             <td>{{ config.supplier }}</td>
          </tr>
          <tr>
             <th>Purchase date</th>
             <td>{{ config.purchase_date }}</td>
          </tr>
          <tr>
             <th>Price</th>
             <td>{{ config.price }}</td>
          </tr>
          <tr>
             <th>Notes</th>
             <td>{{ config.notes }}</td>
          </tr>
        </tbody>
      </table>
    </section>
    <section v-else>
      <b-field expanded>
        <b-button v-if="!addPurchaseDetails" class="button is-info" @click="addPurchaseDetails = !addPurchaseDetails">Add</b-button>
      </b-field>
      <div v-if="addPurchaseDetails">
        <form @submit.prevent="submit">
          <b-field grouped>
            <b-field label="Supplier" expanded>
            <b-input v-model="config.supplier"/>
          </b-field>
          <b-field label="Purchase Date" expanded>
            <b-input
              v-model="config.purchase_date"
            />
          </b-field>
          </b-field>
          <b-field label="Price">
            <b-input
              v-model="config.price"
            />
          </b-field>
          <b-field label="Notes">
              <b-input maxlength="160" type="textarea" v-model="config.notes"></b-input>
          </b-field>
          <b-field grouped>
            <b-field>
              <b-button class="button is-info" native-type="submit">Submit</b-button>
            </b-field>
            <b-field position="is-right">
              <b-button @click="addPurchaseDetails = !addPurchaseDetails">Cancel</b-button>
            </b-field>
          </b-field>
        </form>
      </div>
    </section>
  </div>
</div>
</template>

<script>
import * as api from "@/api";

export default {
  name: "PurchaseDetailsForm",
  props: {
    device: Object
  },
  created() {
     if (this.device.purchase_details[0]) {
        this.config = this.device.purchase_details[0];
        this.hasPurchaseDetails = true;
     }
     this.config.serial_number = this.device.serial_number;
  },
  data() {
    return {
      hasPurchaseDetails: false,
      addPurchaseDetails: false,
      config: {
        supplier: "",
        purchase_date: "",
        price: "",
        notes: "",
        serial_number: ""
      },
      serial_number: ""
    }
  },
  methods: {
    submit() {
        api.editDevice(this.config)
           .then(() => {
                this.$router.push({ name: 'Dashboard' })
           })
           .catch(console.log);
    }  
  },
  computed: {
   
  }
};
</script>