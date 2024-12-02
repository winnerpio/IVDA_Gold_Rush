<template>
  <div class="user-profile" style="width: 100%; height: 250px;">
    <h2>User Profile</h2>
    <v-form>
      <v-container fluid>
        <v-row>
          <!-- Sex -->
          <v-col cols="12" md="4">
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
          </v-col>

          <!-- Height -->
          <v-col cols="12" md="4">
            <v-text-field
                v-model="userAttributes.height"
                label="Height (cm)"
                type="number"
                dense
                outlined
                hide-details
                class="field"
                @blur="calculateDerivedAttributes"
                @keydown.enter="handleEnter"
            />
          </v-col>

          <!-- Weight -->
          <v-col cols="12" md="4">
            <v-text-field
                v-model="userAttributes.weight"
                label="Weight (kg)"
                type="number"
                dense
                outlined
                hide-details
                class="field"
                @blur="calculateDerivedAttributes"
                @keydown.enter="handleEnter"
            />
          </v-col>
        </v-row>

        <!-- Second Row -->
        <v-row>
          <!-- Age -->
          <v-col cols="12" md="4">
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
          </v-col>

          <!-- BMI -->
          <v-col cols="12" md="4">
            <v-text-field
                v-model="userAttributes.bmi"
                label="BMI"
                type="number"
                dense
                outlined
                hide-details
                class="field read-only-field"
                readonly
            />
          </v-col>

          <!-- H2W -->
          <v-col cols="12" md="4">
            <v-text-field
                v-model="userAttributes.h2w"
                label="H2W"
                type="number"
                dense
                outlined
                hide-details
                class="field read-only-field"
                readonly
            />
          </v-col>
        </v-row>
      </v-container>
    </v-form>
  </div>
</template>

<script>
export default {
  name: "UserProfile",
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
    calculateDerivedAttributes() {
      const { height, weight } = this.userAttributes;

      if (height && weight) {
        const heightInMeters = height / 100; // Convert cm to meters
        this.userAttributes.bmi = (weight / (heightInMeters ** 2)).toFixed(2);
        this.userAttributes.h2w = (height / weight).toFixed(2);
      } else {
        this.userAttributes.bmi = null;
        this.userAttributes.h2w = null;
      }

      this.submitAttributes();
    },
    submitAttributes() {
      const updatedAttributes = { ...this.userAttributes };
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
.user-profile {
  display: flex;
  flex-direction: column;
  padding: 15px;
  background-color: #f8f8f8;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  box-sizing: border-box;
}

h2 {
  font-size: 1.2rem;
  font-weight: 500;
  margin-bottom: 15px;
  color: #333;
  text-align: center;
}

.read-only-field {
  background-color: #e0e0e0 !important;
  pointer-events: none;
}

.read-only-field:hover {
  background-color: #e0e0e0 !important;
}

.read-only-field .v-input__control {
  color: #6c757d;
}

.field label {
  font-size: 0.9rem;
  font-weight: bold;
}
</style>
