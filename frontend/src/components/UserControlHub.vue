<template>
  <v-container class="container" fluid>
    <v-card class="form-card" outlined>
      <v-form class="form-container">
        <div class="row">
          <v-select
              :items="sex"
              v-model="userAttributes.sex"
              label="Sex"
              dense
              outlined
              hide-details
              class="field"
          />
          <v-text-field
              v-model="userAttributes.height"
              label="Height (cm)"
              type="number"
              dense
              outlined
              hide-details
              class="field"
          />
        </div>
        <div class="row">
          <v-text-field
              v-model="userAttributes.weight"
              label="Weight (kg)"
              type="number"
              dense
              outlined
              hide-details
              class="field"
          />
          <v-text-field
              v-model="userAttributes.age"
              label="Age"
              type="number"
              dense
              outlined
              hide-details
              class="field"
          />
        </div>
        <div class="row">
          <v-text-field
              v-model="userAttributes.numMedals"
              label="Number of Medals"
              type="number"
              dense
              outlined
              hide-details
              class="field"
          />
          <v-text-field
              v-model="userAttributes.bestPerformance"
              label="Best Performance"
              type="text"
              dense
              outlined
              hide-details
              class="field"
          />
        </div>
      </v-form>
      <v-btn color="primary" icon @click="applyAttributes" class="submit-btn">
        <v-icon left>mdi-send</v-icon>
      </v-btn>
    </v-card>
  </v-container>
</template>




<script>
export default {
  name: "UserControlHub",

  data() {
    return {
      userAttributes: {
        sex: "",
        height: null,
        weight: null,
        age: null,
        numMedals: null,
        bestPerformance: "",
      },
      sex: ["Male", "Female", "All"]
    };
  },
  methods: {
    applyAttributes() {
      this.$emit(
          "update-attributes",
          this.userAttributes.sex,
          this.userAttributes.height,
          this.userAttributes.weight,
          this.userAttributes.age,
          this.userAttributes.numMedals,
          this.userAttributes.bestPerformance
      );
    }
  }
};
</script>


<style scoped>
.form-container{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 80%;
  width: 80%;
}

.form-card {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
}

.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
}

.row {
  display: flex;
  justify-content: space-between;
  gap: 15px;
  width: 100%;
  margin-bottom: 30px;
}

.field {
  width: 100%;

}

.submit-btn {
  margin-top: -50px;
}
</style>
