<template>
  <div class="attribute-selection" style="width: 100%; height: 250px;">
    <h2>Attribute Selection</h2>
    <v-container>
      <v-container fluid>
        <v-row>
          <v-col cols="12" md="6">
            <v-select
              :items="attributes"
              label="X-Axis Attribute"
              v-model="xAttribute"
              outlined
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-select
              :items="attributes"
              label="Y-Axis Attribute"
              v-model="yAttribute"
              outlined
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="4">
            <v-select
              :items="sports"
              label="Sport 1"
              v-model="selectedSport1"
              outlined
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-select
              :items="sports"
              label="Sport 2"
              v-model="selectedSport2"
              outlined
            />
          </v-col>
          <v-col cols="12" md="4">
            <v-select
              :items="sports"
              label="Sport 3"
              v-model="selectedSport3"
              outlined
            />
          </v-col>
        </v-row>
      </v-container>
    </v-container>
  </div>
</template>

<script>
export default {
  name: "AttributeSelection",
  props: {
    attributes: {
      type: Array,
      required: true,
    },
    sports: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      selection: {
        xAttribute: null,
        yAttribute: null,
        selectedSport1: null,
        selectedSport2: null,
        selectedSport3: null,
      },
    };
  },
  methods: {
    emitSelection() {
      this.$emit("update-selection", { ...this.selection });
    },
  },
};
</script>

<style scoped>
.attribute-selection {
  display: flex;
  flex-direction: column;
  padding: 15px;
  background-color: #f8f8f8;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  box-sizing: border-box;
}

h2 {
  font-size: 1.2rem;
  font-weight: 500;
  color: #333;
  text-align: center;
}
</style>
