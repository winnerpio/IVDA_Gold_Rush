<template>
  <v-container fluid>
    <v-row>
      <!-- Athlete Clustering Graph -->
      <v-col cols="12" md="6" class="d-flex">
        <AthleteClustering
            :yearRange="yearRange"
            :userDataForm="userAttributes"
        />
      </v-col>

      <!-- UserProfile and Radar Chart Comparison -->
      <v-col cols="12" md="6" class="d-flex">
        <v-row>
          <!-- UserProfile -->
          <v-col cols="12" class="d-flex pb-0">
            <UserProfile @update-attributes="updateUserAttributes" />
          </v-col>

          <!-- Radar Chart Comparison -->
          <v-col cols="12" class="d-flex pt-0">
            <RadarChartComparison
                :sport="selectedSport"
                :event="selectedEvent"
                :userDataForm="userAttributes"
                :yearRange="yearRange"
            />
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>




<script>
  import UserProfile from './UserProfile.vue';
  import AthleteClustering from './AthleteClustering.vue';
  import RadarChartComparison from './RadarChartComparison.vue';
  // import AttributeSelection from './AttributeSelection.vue';
  
  export default {
    name: 'ComparisonPanel',
    components: {
      UserProfile,
      AthleteClustering,
      RadarChartComparison,
      // AttributeSelection,
    },
    data() {
      return {
        userAttributes: {
          sex: '',
          height: null,
          weight: null,
          age: null,
          bmi: null,
          h2w: null,
        },
      };
    },
    methods: {
      updateUserAttributes(attributes) {
        this.userAttributes = { ...attributes };
      },
      updateAttributeSelection(selection) {
        this.attributeSelection = { ...selection };
      },
    },
    props: {
      minYear: {
        type: Number,
        required: true,
      },
      maxYear: {
        type: Number,
        required: true,
      },
      yearRange: {
        type: Array,
        required: true,
      },
      selectedSport: {
        type: String,
        required: false,
      },
      selectedEvent: {
        type: String,
        required: false,
      },
    },
  };
  </script>
  
  <style>
  .main-content {
    margin-left: 300px;
  }
  </style>
  