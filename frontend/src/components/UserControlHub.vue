<template>
  <div class="user-control-hub">
    <h2>User Attributes</h2>
    <v-form>
      <!-- Sex -->
      <v-select
          :items="sex"
          v-model="userAttributes.sex"
          label="Sex"
          dense
          outlined
          hide-details
          class="field"
          @blur="submitAttributes"
          @keydown.enter="handleEnter"
      />
      <!-- Height -->
      <v-text-field
          v-model="userAttributes.height"
          label="Height (cm)"
          type="number"
          dense
          outlined
          hide-details
          class="field"
          @blur="submitAttributes"
          @keydown.enter="handleEnter"
      />
      <!-- Weight -->
      <v-text-field
          v-model="userAttributes.weight"
          label="Weight (kg)"
          type="number"
          dense
          outlined
          hide-details
          class="field"
          @blur="submitAttributes"
          @keydown.enter="handleEnter"
      />
      <!-- Age -->
      <v-text-field
          v-model="userAttributes.age"
          label="Age"
          type="number"
          dense
          outlined
          hide-details
          class="field"
          @blur="submitAttributes"
          @keydown.enter="handleEnter"
      />
      <!-- BMI -->
      <v-text-field
          v-model="userAttributes.bmi"
          label="BMI"
          type="number"
          dense
          outlined
          hide-details
          class="field"
          @blur="submitAttributes"
          @keydown.enter="handleEnter"
      />
      <!-- H2W -->
      <v-text-field
          v-model="userAttributes.h2w"
          label="H2W"
          type="number"
          dense
          outlined
          hide-details
          class="field"
          @blur="submitAttributes"
          @keydown.enter="handleEnter"
      />
    </v-form>
  </div>
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
        bmi: null,
        h2w: null,
      },
      sex: ["Male", "Female", "All"],
    };
  },
  methods: {
    submitAttributes() {
      const updatedAttributes = {
        ...this.userAttributes,
      };

      this.$emit("update-attributes", updatedAttributes);
    },
    handleEnter(event) {
      this.submitAttributes();
      event.target.blur();
    },
  },
};
</script>

<style scoped>
.user-control-hub {
  display: flex;
  flex-direction: column;
  padding: 15px;
  background-color: #f8f8f8;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%; /* Occupy the full width of the sidebar */
  box-sizing: border-box;
}

h2 {
  font-size: 1.2rem;
  font-weight: 500;
  margin-bottom: 15px;
  color: #333;
  text-align: center;
}

.field {
  margin-bottom: 15px;
  width: 100%; /* Dynamically resize with the parent container */
}

.field:last-child {
  margin-bottom: 0; /* Remove margin for the last field */
}

@media (max-width: 600px) {
  .user-control-hub {
    padding: 10px; /* Adjust padding for smaller screens */
  }

  h2 {
    font-size: 1rem; /* Adjust heading size for smaller screens */
  }
}
</style>
