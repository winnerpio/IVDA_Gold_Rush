<template>
    <v-container fluid>
      <v-row>
        <!-- Attribute Selection Dropdowns -->
        <v-col cols="12" md="6">
          <AttributeSelection
            :attributes="attributes"
            :sports="sports"
            @update-selection="updateAttributeSelection"
          />
        </v-col>

        <!-- UserProfile -->
        <v-col cols="12" md="6">
          <UserProfile @update-attributes="updateUserAttributes" />
        </v-col>
      </v-row>
  
      <v-row>
        <!-- Athlete Clustering Graph -->
        <v-col cols="12" md="6">
          <AthleteClustering
            :yearRange="yearRange"
            :userDataForm="userAttributes"
            :attributeSelection="attributeSelection"
            @update-sports="updateSportsList"
          />
        </v-col>
  
        <!-- Radar Chart Comparison -->
        <v-col cols="12" md="6">
          <RadarChartComparison
            :sport="selectedSport"
            :event="selectedEvent"
            :userDataForm="userAttributes"
            :yearRange="yearRange"
          />
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  import UserProfile from './UserProfile.vue';
  import AthleteClustering from './AthleteClustering.vue';
  import RadarChartComparison from './RadarChartComparison.vue';
  import AttributeSelection from './AttributeSelection.vue';
  
  export default {
    name: 'ComparisonPanel',
    components: {
      UserProfile,
      AthleteClustering,
      RadarChartComparison,
      AttributeSelection,
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
        attributeSelection: {
          xAttribute: null,
          yAttribute: null,
          selectedSport1: null,
          selectedSport2: null,
          selectedSport3: null,
        },
        attributes: ['Age', 'Height', 'Weight', 'BMI', 'H2W'],
        sports: [], // This will be populated from AthleteClustering
      };
    },
    methods: {
      updateUserAttributes(attributes) {
        this.userAttributes = { ...attributes };
      },
      updateAttributeSelection(selection) {
        this.attributeSelection = { ...selection };
      },
      updateSportsList(sportsList) {
        this.sports = sportsList;
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
    margin-left: 350px;
  }
  </style>
  