<template>
  <v-container class="container" fluid>
    <v-card class="form-card" outlined>
      <v-form class="form-container">
        <v-select
            :items="sex"
            v-model="userAttributes.sex"
            label="Sex"
            dense
            outlined
            hide-details
            class="field small-field"
        />
        <v-text-field
            v-model="userAttributes.height"
            label="Height (cm)"
            type="number"
            dense
            outlined
            hide-details
            class="field small-field"
        />
        <v-text-field
            v-model="userAttributes.weight"
            label="Weight (kg)"
            type="number"
            dense
            outlined
            hide-details
            class="field small-field"
        />
        <v-text-field
            v-model="userAttributes.age"
            label="Age"
            type="number"
            dense
            outlined
            hide-details
            class="field extra-small-field"
        />
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
        sport: "",
        event: ""
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
          this.userAttributes.sport,
          this.userAttributes.event
      );
    }
  }
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  padding: 20px;
}

.form-card {
  width: 400px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.form-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.field {
  margin-bottom: 10px;
}

.small-field {
  min-width: 120px;
}

.extra-small-field {
  min-width: 80px;
}

.submit-btn {
  margin-top: 20px;
}
</style>
