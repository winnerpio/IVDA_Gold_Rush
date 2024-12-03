<template>
  <v-container outlined class="pt-4 pl-0" fluid>
      <v-card-text>
        <v-row no-gutters style="height: 100%;">
          <!-- Medal Map and Athlete Attribute Distribution (Left Column) -->
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
                    @update:distVariable="handleDistVariableSelection"
                />
              </v-col>
            </v-row>
          </v-col>

          <!-- Medal Tally Histogram (Right Column) -->
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
