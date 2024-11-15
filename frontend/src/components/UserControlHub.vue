<template>
  <v-app-bar app color="primary" dark>
    <v-container class="d-flex justify-center align-center" fluid>
      <v-form class="d-flex align-center" style="flex-wrap: nowrap;">
        <v-select :items="sex" v-model="userAttributes.sex" label="Sex" width="5%" dense outlined hide-details class="mr-1 small-field" />
        <v-text-field v-model="userAttributes.height" label="Height (cm)" type="number" width="5%" dense outlined hide-details class="mr-1 small-field" />
        <v-text-field v-model="userAttributes.weight" label="Weight (kg)" type="number" width="5%" dense outlined hide-details class="mr-1 small-field" />
        <v-text-field v-model="userAttributes.age" label="Age" type="number" width="5%" dense outlined hide-details class="mr-1 extra-small-field" />
        <v-select :items="sports" v-model="userAttributes.sport" label="Sport" dense outlined hide-details class="mr-1 large-field" />
        <v-select :items="events" v-model="userAttributes.event" label="Event" dense outlined hide-details class="mr-1 large-field" />
      </v-form>

      <v-btn color="secondary" icon @click="applyAttributes" class="ml-2">
        <v-icon left>mdi-send</v-icon>
      </v-btn>
    </v-container>
  </v-app-bar>
</template>

<script>
export default {
  name: "UserControlHub",

  data() {
    return {
      userAttributes: {
        sex: '',
        height: null,
        weight: null,
        age: null,
        sport: '',
        event: ''
      },
      sex: ["Male", "Female", "All"],
      sports: ['Athletics', 'Swimming', 'Gymnastics', 'Cycling'],
      events: ['100m', '200m', 'Marathon', 'High Jump']
    };
  },
  methods: {
    applyAttributes() {
      this.$emit('update-attributes',
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
.v-app-bar .v-form .v-text-field.small-field,
.v-app-bar .v-form .v-select.small-field {
  min-width: 80px;
}

.v-app-bar .v-form .v-text-field.extra-small-field {
  min-width: 60px;
}

.v-app-bar .v-form .v-select.medium-field {
  min-width: 120px;
}

.v-app-bar .v-form .v-select.large-field {
  min-width: 140px;
}
</style>
