<template>
  <v-app>
    <v-main>
      <v-container fluid>
        <v-row>
          <!-- UserControlHub component-->
          <v-col cols="12">
            <UserControlHub @update-attributes="updateAttributes" />
          </v-col>
        </v-row>

        <v-row class="align-height-row">
          <!-- MedalSuccessMap component -->
          <v-col cols="12" md="4" class="align-height-col">
            <MedalSuccessMap />
          </v-col>

          <!-- RadarChartComparison component -->
          <v-col cols="12" md="3" class="align-height-col">
            <v-row>
              <RadarChartComparison
                  :userData="userData"
                  :athleteData="selectedAthleteData"
              />
            </v-row>
            <v-row>
              <CascadingDropdown @athleteSelected="fetchAthleteData" />
            </v-row>
          </v-col>

          <!-- AthleteClustering component -->
          <v-col cols="12" md="5" class="align-height-col">
            <AthleteClustering />
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" sm="6">
            <OutlierIdentification />
          </v-col>
          <v-col cols="12" sm="6">
            <AthleteAttributeDistribution :userDataForm="userData" />
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
import CascadingDropdown from "./components/AthleteCascadingDropdown.vue";

export default {
  name: 'App',
  components: {
    UserControlHub,
    MedalSuccessMap,
    AthleteAttributeDistribution,
    OutlierIdentification,
    AthleteClustering,
    RadarChartComparison,
    CascadingDropdown
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
      selectedAthleteData: null // Stores the selected athlete's data
    };
  },
  methods: {
    updateAttributes(sex, height, weight, age, sport, event) {
      this.userData = { sex, height: Number(height), weight: Number(weight), age: Number(age), sport, event };
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
.align-height-row {
  display: flex;
}

.align-height-col {
  display: flex;
  flex-direction: column;
  justify-content: stretch;
}

.align-height-col > * {
  flex: 1;
  display: flex;
}
</style>
