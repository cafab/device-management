<template>
<div class="tile is-child box">
  <p class="title">Purchase Details</p>
  <div v-if="purchase_details">
    <table class="table" >
      <tbody>
        <tr>
           <th>Supplier</th>
           <td>{{ purchase_details.supplier }}</td>
        </tr>
        <tr>
           <th>Purchase date</th>
           <td>{{ purchase_details.purchase_date }}</td>
        </tr>
        <tr>
           <th>Price</th>
           <td>{{ purchase_details.price }}</td>
        </tr>
        <tr>
           <th>Notes</th>
           <td>{{ purchase_details.notes }}</td>
        </tr>
      </tbody>
    </table>
  </div>
  <section v-else>
    <b-button v-if="!addPurchaseDetails" class="button is-info" @click="addPurchaseDetails = !addPurchaseDetails">Add</b-button>
    <div v-if="addPurchaseDetails">
      <form @submit.prevent="submit">
        <b-field grouped>
          <b-field label="Supplier">
          <b-input v-model="config.supplier"/>
        </b-field>
        <b-field label="Purchase Date">
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
        <b-button native-type="submit">Submit</b-button>
      </form>
    </div>
  </section>
</div>
</template>

<script>
import * as api from "@/api";

export default {
  name: "PurchaseDetailsForm",
  props: {
    purchase_details: Object
  },
  created() {
    if (this.purchase_details) {
      this.config = this.purchase_details;
    }
  },
  data() {
    return {
      addPurchaseDetails: false,
      config: {
        supplier: "",
        purchase_date: "",
        price: "",
        notes: ""
      },
    }
  },
  methods: {
    submit() {
        api.editDevice(this.config)
           .then(() => {
                this.$router.push({ name: 'Dashboard' })
           })
           .catch(console.log);
    },
  },
};
</script>