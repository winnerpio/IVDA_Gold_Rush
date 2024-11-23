<template>
  <v-app>
    <v-main>
      <!-- Sidebar -->
      <OlympicSidebar
          :minYear="minYear"
          :maxYear="maxYear"
          v-model:yearRange="yearRange"
          :class="{ 'is-expanded': is_expanded }"
          @update-sport-event="handleSportEventUpdate"
          @update-user-data="updateAttributes"
          @update:range="updateYearRange"
          @toggle-menu="toggleSidebar"
      />

      <!-- Main Content -->
      <div :class="['main-content', { 'with-sidebar': is_expanded }]">
        <!-- Carousel -->
        <v-carousel hide-delimiters show-arrows="hover" style="height: auto">
          <!-- Slide 1 -->
          <v-carousel-item>
            <v-container outlined class="pa-4" fluid>
              <v-card outlined>
                <v-card-title style="text-align: center; justify-content: center;">Explore Medal Success by Country, Sport, and Event</v-card-title>
                <v-card-text>
                  <v-row class="align-height-row" no-gutters>
                    <div class="container">

                    </div>
                    <v-col cols="7" class="align-height-col">
                      <MedalSuccessMap
                          @country-selected="handleCountrySelected"
                          :yearRange="yearRange"
                          :sport="selectedSport"
                          :event="selectedEvent"
                      />
                    </v-col>
                    <v-col cols="5" class="d-flex align-center justify-center">
                      <v-row>
                        <v-col cols="12" class="pa-0 mb-n3 mt-n0">
                          <CountryPerformanceEvolution
                              :event="selectedEvent"
                              :sport="selectedSport"
                              :country="selectedCountry.name"
                              :dateRange="[2000, 2020]"
                          />
                        </v-col>
                        <v-col cols="12" class="pa-0 mt-n5">
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
                </v-card-text>
              </v-card>
            </v-container>
          </v-carousel-item>

          <!-- Slide 2 -->
          <v-carousel-item>
            <v-container outlined class="pa-4" fluid>
              <v-card outlined>
                <v-card-title style="text-align: center; justify-content: center;">Compare Yourself with Olympic Medalists</v-card-title>
                <v-card-text>
                  <RadarChartComparison
                      :userDataForm="userData"
                      :athleteData="selectedAthleteData"
                      :sport="selectedSport"
                      :event="selectedEvent"
                      :selectedCountry="selectedCountry"
                  />
                </v-card-text>
              </v-card>
            </v-container>
          </v-carousel-item>

          <!-- Slide 3 -->
          <v-carousel-item>
            <v-container outlined class="pa-4" fluid>
              <v-card outlined>
                <v-card-title style="text-align: center; justify-content: center;">Identify Outliers Among Successful Athletes</v-card-title>
                <v-card-text>
                  <OutlierIdentification />
                </v-card-text>
              </v-card>
            </v-container>
          </v-carousel-item>

          <!-- Slide 4 -->
          <v-carousel-item>
            <v-container outlined class="pa-4" fluid>
              <v-card outlined>
                <v-card-title style="text-align: center; justify-content: center;">Discover Similar Athletes Using Clustering</v-card-title>
                <v-card-text>
                  <AthleteClustering />
                </v-card-text>
              </v-card>
            </v-container>
          </v-carousel-item>

          <!-- Slide 5 -->
          <v-carousel-item>
            <v-container outlined class="pa-4" fluid>
              <v-card outlined>
                <v-card-title style="text-align: center; justify-content: center;">Explore Attribute Distributions Among Athletes</v-card-title>
                <v-card-text>
                  <AthleteAttributeDistribution
                      :userDataForm="userData"
                      :dateRange="yearRange"
                  />
                </v-card-text>
              </v-card>
            </v-container>
          </v-carousel-item>
        </v-carousel>
      </div>
    </v-main>
  </v-app>
</template>



<script>
import MedalSuccessMap from "./components/MedalSuccessMap.vue";
import AthleteAttributeDistribution from "./components/AthleteAttributeDistribution.vue";
import OutlierIdentification from "./components/OutlierIdentification.vue";
import AthleteClustering from "./components/AthleteClustering.vue";
import RadarChartComparison from "./components/RadarChartComparison.vue";
import CountryPerformanceEvolution from "./components/CountryPerformanceEvolution.vue";
import MedalRadialHistogram from "./components/MedalRadialHistogram.vue";
import OlympicSidebar from "./components/OlympicSidebar.vue";

export default {
  name: "App",
  components: {
    MedalSuccessMap,
    AthleteAttributeDistribution,
    OutlierIdentification,
    AthleteClustering,
    RadarChartComparison,
    CountryPerformanceEvolution,
    MedalRadialHistogram,
    OlympicSidebar,
  },
  data() {
    return {
      userData: {
        sex: "",
        height: 0,
        weight: 0,
        age: 0,
        medals: 0,
        performance: "",
      },
      selectedCountry: {
        name: "",
        code: "",
      },
      yearRange: [1920, 2005],
      selectedAthleteData: null,
      selectedSport: null,
      selectedEvent: null,
      is_expanded: false,
      minYear: 1896,
      maxYear: 2022,
    };
  },
  methods: {
    updateAttributes(attributes) {
      this.userData = { ...this.userData, ...attributes };
    },
    updateYearRange(range) {
      this.yearRange = range;
      console.log("Year range updated:", range);
    },
    async fetchAthleteData(selection) {
      console.log("Athlete Selected:", selection);

      this.selectedAthleteData = await this.fetchAthleteStatsFromBackend();
    },
    async fetchAthleteStatsFromBackend() {
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            height: 182,
            weight: 78,
            age: 24,
          });
        }, 1000);
      });
    },
    handleSportEventUpdate({ sport, event }) {
      console.log(sport, event);
      this.selectedSport = sport;
      this.selectedEvent = event;
    },
    handleCountrySelected({ countryName, countryCode }) {
      this.selectedCountry.name = countryName;
      this.selectedCountry.code = countryCode;
    },
    toggleSidebar() {
      this.is_expanded = !this.is_expanded;
    },
  },
};
</script>

<style scoped>
.main-content {
  margin-left: calc(2rem + 32px);
  max-width: calc(100% - (2rem + 32px));
  transition: margin-left 0.2s ease-in-out, max-width 0.2s ease-in-out;
}

.main-content.with-sidebar {
  margin-left: 350px;
  max-width: calc(100% - 350px);
}

.align-height-row {
  height: 100%;
}

.align-height-col {
  height: 100%;
}

.v-carousel-item {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  max-height: 100vh;
  overflow: auto;
}

.v-container {
  width: 95%; /* Adjust the width as needed */
  max-width: 1200px; /* Optional: Limit the maximum width */
  
}

.v-card {
  width: 100%; /* Make the card take the full width of the container */
}
</style>
