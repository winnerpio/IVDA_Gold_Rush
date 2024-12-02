<template>
  <v-container outlined class="pa-4" fluid>
    <v-card outlined>
      <v-card-title class="text-center justify-center">
        Explore Medal Success and Athlete Attributes
      </v-card-title>
      <v-card-text>
        <v-row no-gutters>
          <v-col cols="12">
            <MedalSuccessMap
              @country-selected="handleCountrySelected"
              :data="sharedData"
            />
          </v-col>
        </v-row>

        <v-row no-gutters>
          <v-col cols="4">
            <CountryPerformanceEvolution
              :event="selectedEvent"
              :sport="selectedSport"
              :country="selectedCountry"
              :dateRange="yearRange"
              :data="sharedData"
            />
          </v-col>
          <v-col cols="4">
            <MedalRadialHistogram
              :country="selectedCountry"
              :sport="selectedSport"
              :event="selectedEvent"
              :dateRange="[1896, 2022]"
              :data="sharedData"
            />
          </v-col>
          <v-col cols="4">
            <AthleteAttributeDistribution
              :selectedCountry="selectedCountry"
              :dateRange="yearRange"
              :distributionData="distributionData"
              @update:distVariable="handleDistVariableSelection"
            />
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import MedalSuccessMap from "./MedalSuccessMap.vue";
import AthleteAttributeDistribution from "./AthleteAttributeDistribution.vue";
import CountryPerformanceEvolution from "./CountryPerformanceEvolution.vue";
import MedalRadialHistogram from "./MedalRadialHistogram.vue";

export default {
  name: "ExplorationPanel",
  components: {
    MedalSuccessMap,
    AthleteAttributeDistribution,
    CountryPerformanceEvolution,
    MedalRadialHistogram,
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
  },
  methods: {
    handleCountrySelected({ countryName, countryCode }) {
      this.$emit('update-selected-country', { countryName, countryCode });
    },
    handleDistVariableSelection(distVariable) {
      this.$emit('update-dist-variable', distVariable);
    },
  },
};
</script>

<style scoped>
/* Add any styles specific to ExplorationPanel here */
</style>
