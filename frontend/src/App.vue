<template>
  <v-app>
    <v-main>
      <v-container fluid>
        <v-row class="align-height-row">
          <!-- MedalSuccessMap component -->
          <v-col cols="12" md="4" class="align-height-col">
            <MedalSuccessMap />
          </v-col>
        </v-row>

        <!-- RangeSlider component -->
        <v-row>
          <v-col cols="12">
            <DateRangeSlider
                :minYear="1900"
                :maxYear="2023"
                :initialRange="[1920, 2005]"
                @update:range="updateYearRange"
            />
            <p>Selected Range: {{ yearRange[0] }} - {{ yearRange[1] }}</p>
          </v-col>
        </v-row>

        <v-row>
          <!-- UserControlHub component -->
          <v-col cols="2">
            <UserControlHub @update-attributes="updateAttributes" />
          </v-col>

          <!-- RadarChartComparison component -->
          <v-col cols="3">
            <RadarChartComparison
                :userData="userData"
                :athleteData="selectedAthleteData"
            />
          </v-col>

          <!-- AthleteAttributeDistribution component -->
          <v-col cols="12" md="5">
            <AthleteAttributeDistribution :userDataForm="userData" />
          </v-col>
        </v-row>


        <v-row>
          <v-col cols="12" sm="6">
            <OutlierIdentification />
          </v-col>
        </v-row>

        <v-row>
          <!-- AthleteClustering component -->
          <v-col cols="12" md="5" class="align-height-col">
            <AthleteClustering />
          </v-col>
        </v-row>

      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import UserControlHub from './components/UserControlHub.vue';
import MedalSuccessMap from "./components/MedalSuccessMap.vue";
import AthleteAttributeDistribution from "./components/AthleteAttributeDistribution.vue";
import OutlierIdentification from "./components/OutlierIdentification.vue";
import AthleteClustering from "./components/AthleteClustering.vue";
import RadarChartComparison from "./components/RadarChartComparison.vue";
// import CascadingDropdown from "./components/AthleteCascadingDropdown.vue";
import DateRangeSlider from './components/DateRangeSlider.vue';

export default {
  name: 'App',
  components: {
    UserControlHub,
    MedalSuccessMap,
    AthleteAttributeDistribution,
    OutlierIdentification,
    AthleteClustering,
    RadarChartComparison,
    // CascadingDropdown,
    DateRangeSlider,
  },
  data() {
    return {
      userData: {
        sex: '',
        height: 0,
        weight: 0,
        age: 0,
        sport: '',
        event: ''
      },
      yearRange: [1920, 2005], // Year range for the RangeSlider
      selectedAthleteData: null, // Stores the selected athlete's data
    };
  },
  methods: {
    updateAttributes(sex, height, weight, age, sport, event) {
      this.userData = {
        sex,
        height: Number(height),
        weight: Number(weight),
        age: Number(age),
        sport,
        event
      };
    },
    updateYearRange(range) {
      this.yearRange = range;
      console.log('Year range updated:', range);
    },
    async fetchAthleteData(selection) {
      console.log("Athlete Selected:", selection);

      // Replace mock with real API call
      this.selectedAthleteData = await this.fetchAthleteStatsFromBackend();
    },
    async fetchAthleteStatsFromBackend() {
      // Placeholder for actual API call
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            height: 182,
            weight: 78,
            age: 24
          });
        }, 1000); // Simulate network delay
      });
    }
  }
};
</script>

<style scoped>

</style>

