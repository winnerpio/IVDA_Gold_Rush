<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12" class="d-flex justify-end">
        <!-- Help Button -->
        <v-btn
            icon
            density="compact"
            @click="openHelpDialog"
            aria-label="Help"
            style="font-size: 14px; padding: 4px;"
        >
          <v-icon>mdi-help-circle</v-icon>
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <!-- Athlete Clustering Graph -->
      <v-col cols="12" md="6" class="d-flex">
        <AthleteClustering :yearRange="yearRange" :userDataForm="userAttributes" />
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

    <!-- Help Dialog -->
    <v-dialog v-model="helpDialog" max-width="600px">
      <v-card>
        <v-card-title class="headline">How to Use the Comparison Panel</v-card-title>
        <v-card-text>
          <p class="dialog-paragraph">
            The Comparison Panel helps you compare your personal attributes with historical Olympic athletes' data and explore athlete clusters.
          </p>
          <ul>
            <li>
              <strong>Athlete Clustering Graph:</strong> Visualizes athlete clusters based on selected X and Y attributes.
              You must input your information in the <strong>User Profile</strong> section for the cluster visualization to work correctly.
            </li>
            <li>
              <strong>User Profile:</strong> Input your personal attributes such as height, weight, and age. The system automatically calculates derived attributes like BMI and H2W.
            </li>
            <li>
              <strong>Radar Chart Comparison:</strong> Compares your attributes against a selected athlete's data.
              To populate the country and athlete dropdowns, you need to input your information in the <strong>User Profile</strong> and select a <strong>sport</strong> and <strong>event</strong>.
            </li>
            <li>
              <strong>Year Filter:</strong> Changing the year range dynamically updates the data across all visualizations, including available sports, events, and athlete clusters.
            </li>
          </ul>
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="helpDialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>




<script>
  import UserProfile from './UserProfile.vue';
  import AthleteClustering from './AthleteClustering.vue';
  import RadarChartComparison from './RadarChartComparison.vue';

  export default {
    name: 'ComparisonPanel',
    components: {
      UserProfile,
      AthleteClustering,
      RadarChartComparison,
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
        helpDialog: false,
      };
    },
    methods: {
      updateUserAttributes(attributes) {
        this.userAttributes = { ...attributes };
      },
      openHelpDialog() {
        this.helpDialog = true;
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

  .dialog-paragraph {
    margin-bottom: 12px;
  }
  </style>
  