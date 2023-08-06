<template>
  <main-container>
    <v-card :loading="$apollo.queries.data.loading">
      <v-card-title class="text-h5 grey--text pb-0" v-if="data">{{ data.order.form.title }}</v-card-title>
      <v-card-title class="text-h4">
        {{ $t("order.digital_products.my_digital_products") }}
        <span class="grey--text ml-2" v-if="data">#{{ data.order.id }}</span>
      </v-card-title>
      <v-card-text>
        <digital-products-by-order v-if="data" :data="data" @share-created="shareCreated"></digital-products-by-order>
        <div v-if="data" v-html="data.order.form.helpText"/>
      </v-card-text>
    </v-card>
  </main-container>
</template>

<script>
import MainContainer from "./MainContainer.vue";
import OrderItem from "./OrderItem.vue";
import CopyToClipboardButton from "./CopyToClipboardButton.vue";
import DigitalProductsByOrder from "./DigitalProductsByOrder.vue";

export default {
  name: "DigitalProducts",
  components: {DigitalProductsByOrder, CopyToClipboardButton, OrderItem, MainContainer},
  methods: {
    shareCreated(data) {
      this.$apollo.queries.data.refetch();
    },
  },
  apollo: {
    data: {
      query: require("./digitalProducts.graphql"),
      variables() {
        return {
          key: this.$route.params.key
        };
      }
    }
  },
}
</script>
