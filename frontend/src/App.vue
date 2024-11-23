<template>
  <v-app>
    <v-main>
      <v-container fluid>
        <OlympicDataTopMenu @update-sport-event="handleSportEventUpdate" />
        <v-row class="align-height-row" no-gutters>
          <!-- MedalSuccessMap component -->
          <v-col cols="7" class="align-height-col">
            <MedalSuccessMap @country-selected="handleCountrySelected" :yearRange="yearRange" :sport="selectedSport" :event="selectedEvent"/>
          </v-col>
          <v-col cols="5" class="d-flex align-center justify-center">
            <v-row>
              <v-col cols="12" class="pa-0 mb-n3 mt-n0">
                <!-- CountryPerformanceEvolution component -->
                <CountryPerformanceEvolution
                    :event="selectedEvent"
                    :sport="selectedSport"
                    :country="selectedCountry.name"
                    :dateRange="[2000, 2020]"
                />
              </v-col>
              <v-col cols="12"  class="pa-0 mt-n5">
                <!-- MedalRadialHistogram component -->
                <MedalRadialHistogram
                    :country="selectedCountry.name"
                    :sport="selectedSport"
                    :event="selectedEvent"
                    :dateRange="[2000, 2020]"
                />
              </v-col>
            </v-row>
          </v-col>
        </v-row>

        <!-- RangeSlider component -->
        <v-row>
          <v-col cols="12">
            <DateRangeSlider
                :minYear="1896"
                :maxYear="2022"
                :initialRange="[1920, 2005]"
                @update:range="updateYearRange"
            />
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="6">
            <v-row>
              <!-- UserControlHub component -->
              <v-col cols="6">
                <UserControlHub @update-attributes="updateAttributes" />
              </v-col>

              <!-- RadarChartComparison component -->
              <v-col cols="6">
                <RadarChartComparison
                    :userDataForm="userData"
                    :athleteData="selectedAthleteData"
                    :sport="selectedSport"
                    :event="selectedEvent"
                    :selectedCountry="selectedCountry"
                />

              </v-col>
            </v-row>
            <v-row>
              <!-- OutlierIdentification component -->
              <v-col cols="12">
                <OutlierIdentification />
              </v-col>
            </v-row>
            <v-row>
              <!-- AthleteClustering component -->
              <v-col cols="12">
                <AthleteClustering />
              </v-col>
            </v-row>
          </v-col>

          <v-col cols="6">
            <!-- AthleteAttributeDistribution component -->
            <v-col cols="12">
              <AthleteAttributeDistribution
                :userDataForm="userData"
                :dateRange="yearRange"
              />
            </v-col>
          </v-col>
        </v-row>


        <v-row>

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
import DateRangeSlider from './components/DateRangeSlider.vue';
import CountryPerformanceEvolution from "./components/CountryPerformanceEvolution.vue";
import MedalRadialHistogram from "./components/MedalRadialHistogram.vue";
import OlympicDataTopMenu from "@/components/OlympicDataTopMenu.vue";

export default {
  name: 'App',
  components: {
    UserControlHub,
    MedalSuccessMap,
    AthleteAttributeDistribution,
    OutlierIdentification,
    AthleteClustering,
    RadarChartComparison,
    DateRangeSlider,
    CountryPerformanceEvolution,
    MedalRadialHistogram,
    OlympicDataTopMenu,
  },
  data() {
    return {
      userData: {
        sex: '',
        height: 0,
        weight: 0,
        age: 0,
        numMedals: 0,
        bestPerformance: ""
      },
      selectedCountry: {
        name: '',
        code: '',
      },
      yearRange: [1920, 2005], // Year range for the RangeSlider
      selectedAthleteData: null, // Stores the selected athlete's data
      selectedSport: null,
      selectedEvent: null,
    };
  },
  methods: {
    updateAttributes(sex, height, weight, age, medals, performance) {
      this.userData = {
        sex,
        height: Number(height),
        weight: Number(weight),
        age: Number(age),
        numMedals: Number(medals),
        performance
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
    },
    handleSportEventUpdate({ sport, event }) {
      this.selectedSport = sport;
      this.selectedEvent = event;
    },
    handleCountrySelected ({ countryName, countryCode }) {
      this.selectedCountry.name = countryName;
      this.selectedCountry.code = countryCode;
    }
  }
};
</script>

<style scoped>

</style>

