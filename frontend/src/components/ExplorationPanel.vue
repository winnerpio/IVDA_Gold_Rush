<template>
  <v-container outlined class="pt-4 pl-0" fluid>
    <!-- Help Button -->
    <v-row>
      <v-col cols="12" class="d-flex justify-end">
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

    <!-- Main Content -->
    <v-card-text>
      <v-row no-gutters style="height: 100%;">
        <v-col cols="8">
          <v-row no-gutters>
            <v-col cols="12" style="height: 50%;">
              <MedalSuccessMap
                  @country-selected="handleCountrySelected"
                  :data="sharedData"
              />
            </v-col>
            <v-col cols="12" style="height: 50%;">
              <AthleteAttributeDistribution
                  :selectedCountry="selectedCountry"
                  :dateRange="yearRange"
                  :distributionData="distributionData"
                  :selectedDistVariable="selectedDistVariable"
                  @update:distVariable="handleDistVariableSelection"
              />
            </v-col>
          </v-row>
        </v-col>

        <!-- Medal Tally Histogram -->
        <v-col cols="4" class="pl-4">
          <MedalHistogram
              style="height: 100%;"
              :country="selectedCountry"
              :sport="selectedSport"
              :event="selectedEvent"
              :dateRange="[minYear, maxYear]"
              :data="sharedData"
          />
        </v-col>
      </v-row>
    </v-card-text>

    <!-- Help Dialog -->
    <v-dialog v-model="helpDialog" max-width="600px">
      <v-card>
        <v-card-title class="headline">How to Use the Exploration Panel</v-card-title>
        <v-card-text>
          <p class="dialog-paragraph">
            The Exploration Panel allows you to visualize and interact with data about Olympic athletes and medals.
          </p>
          <ul>
            <li>
              <strong>Medal Success Map:</strong> Click on countries to view their medal data. The map highlights medal distributions across nations.
            </li>
            <li>
              <strong>Athlete Attribute Distribution:</strong> Explore the distribution of athlete attributes like age, height, or weight for a selected country.
            </li>
            <li>
              <strong>Medal Tally Histogram:</strong> View a bar chart of medals (gold, silver, bronze) by year or selected range for a chosen country.
            </li>
            <li>
              <strong>Year Filter:</strong> Adjust the year range to dynamically update all charts and visualizations.
            </li>
          </ul>
          <p class="dialog-paragraph">
            <strong>Important:</strong> You must select both a <strong>sport</strong> and an <strong>event</strong> for the data to populate correctly. Without these selections, the visualizations will remain empty.
          </p>
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="helpDialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>



<script>
import MedalSuccessMap from "./MedalSuccessMap.vue";
import AthleteAttributeDistribution from "./AthleteAttributeDistribution.vue";
// import CountryPerformanceEvolution from "./CountryPerformanceEvolution.vue";
import MedalHistogram from "./MedalHistogram.vue";

export default {
  name: "ExplorationPanel",
  components: {
    MedalSuccessMap,
    AthleteAttributeDistribution,
    // CountryPerformanceEvolution,
    MedalHistogram: MedalHistogram,
  },
  data() {
    return {
      helpDialog: false,
    };
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
    selectedCountry: {
      type: Object,
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
    sharedData: {
      type: Object,
      required: false,
    },
    distributionData: {
      type: Object,
      required: false,
    },
    selectedDistVariable: {
      type: String,
      required: true,
    },
  },
  methods: {
    handleCountrySelected({ countryName, countryCode }) {
      this.$emit('update-selected-country', { countryName, countryCode });
    },
    handleDistVariableSelection(distVariable) {
      this.$emit('update-dist-variable', distVariable);
    },
    openHelpDialog() {
      this.helpDialog = true;
    },
  },
};
</script>

<style scoped>
/* Add any styles specific to ExplorationPanel here */
</style>
