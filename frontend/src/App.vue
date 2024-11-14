<template>
  <v-app>
    <v-main>
      <v-container fluid>
        <v-row>
          <!-- UserControlHub spans the full width of the row -->
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
              <RadarChartComparison :userDataForm="userData" />
            </v-row>
            <v-row>
              <RadarChartComparison :userDataForm="userData" />
            </v-row>
          </v-col>

          <!-- AthleteClustering component -->
          <v-col cols="12" md="5" class="align-height-col">
            <AthleteClustering />
          </v-col>
        </v-row>

        <v-row>
          <v-col
              cols="12" sm="6"
          >
            <OutlierIdentification />
          </v-col>
          <v-col
              cols="12" sm="6"
          >
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

export default {
  name: 'App',
  components: {
    UserControlHub,
    MedalSuccessMap,
    AthleteAttributeDistribution,
    OutlierIdentification,
    AthleteClustering,
    RadarChartComparison,
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
    };
  },
  methods: {
    updateAttributes(sex, height, weight, age, sport, event) {
      console.log("Props Updated:", { height, weight, age, sport });
      this.userData.sex = sex;
      this.userData.height = Number(height);
      this.userData.weight = Number(weight);
      this.userData.age = Number(age);
      this.userData.sport = sport;
      this.userData.event = event;
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
