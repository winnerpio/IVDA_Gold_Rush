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
                          :data="sharedData"
                      />
                    </v-col>
                    <v-col cols="5" class="d-flex align-center justify-center">
                      <v-row>
                        <v-col cols="12" class="pa-0 mb-n3 mt-n0">
                          <CountryPerformanceEvolution
                              :event="selectedEvent"
                              :sport="selectedSport"
                              :country="selectedCountry"
                              :dateRange="yearRange"
                              :data="sharedData"
                          />
                        </v-col>
                        <v-col cols="12" class="pa-0 mt-n5">
                          <MedalRadialHistogram
                              :country="selectedCountry"
                              :sport="selectedSport"
                              :event="selectedEvent"
                              :dateRange="[1896, 2022]"
                              :data="sharedData"
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
                      :yearRange="yearRange"
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
                  <OutlierIdentification :sport="selectedSport" :event="selectedEvent" :yearRange="yearRange" />
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
                  <AthleteClustering :yearRange="yearRange" :userDataForm="userData"/>
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
                    :distributionData="distributionData"
                    :detailedDistributionData="detailedDistributionData"
                    @update:distVariable="handleDistVariableSelection"
                    @fetch-detailed-distribution="fetchDetailedDistribution"
                    @panel-opened="handlePanelOpened"
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
import axios from 'axios';
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
        bmi: 0,
        h2w: 0,
      },
      selectedCountry: {
        name: "",
        code: "",
      },
      yearRange: [1896, 2022],
      selectedAthleteData: null,
      selectedSport: null,
      selectedEvent: null,
      is_expanded: false,
      minYear: 1896,
      maxYear: 2022,
      sharedData: null,
      isLoading: false,
      distributionData: null,
      selectedDistVariable: 'age',
      detailedDistributionData: null,
      isPanelOpen: false,
    };
  },
  methods: {
    async fetchSharedData() {
      if (!this.yearRange && !this.selectedSport && !this.selectedEvent) {
        console.warn("Missing filters for data fetching.");
        return;
      }

      this.isLoading = true;

      try {
        const response = await axios.get("http://127.0.0.1:5000/MedalCount", {
          params: {
            year_lower: this.yearRange[0],
            year_upper: this.yearRange[1],
            sport: this.selectedSport,
            event: this.selectedEvent,
          },
        });

        console.log(response);
        this.sharedData = response.data;
      } catch (error) {
        console.error("Error fetching shared data:", error.message);
      } finally {
        this.isLoading = false;
      }
    },
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

    async fetchDistribution() {
      if (!this.yearRange || !this.selectedDistVariable) {
        console.warn("Missing filters for distribution data fetching.");
        return;
      }

      this.isLoading = true;

      try {
        const response = await axios.get("http://127.0.0.1:5000/GetDistribution", {
          params: {
            year_lower: this.yearRange[0],
            year_upper: this.yearRange[1],
            ...(this.selectedSport && { sport: this.selectedSport }),
            ...(this.selectedEvent && { event: this.selectedEvent }),
            dist_variable: this.selectedDistVariable,
            bins: 10,
          },
        });

        console.log("Distribution data response:", response);
        this.distributionData = response.data;
      } catch (error) {
        console.error("Error fetching distribution data:", error.message);
      } finally {
        this.isLoading = false;
      }
    },
    handleDistVariableSelection(distVariable) {
      this.selectedDistVariable = distVariable;
      this.fetchDistribution();

      if (this.isPanelOpen) {
        this.fetchDetailedDistribution();
      }
    },
    async fetchDetailedDistribution() {
      if (!this.yearRange || !this.selectedDistVariable) {
        console.warn("Missing filters for detailed distribution data fetching.");
        return;
      }

      this.isLoading = true;

      try {
        const response = await axios.get("http://127.0.0.1:5000/GetDistribution2", {
          params: {
            year_lower: this.yearRange[0],
            year_upper: this.yearRange[1],
            ...(this.selectedSport && { sport: this.selectedSport }),
            ...(this.selectedEvent && { event: this.selectedEvent }),
            dist_variable: this.selectedDistVariable,
            bins: 10,
          },
        });

        console.log("Detailed distribution data response:", response);
        this.detailedDistributionData = response.data;
      } catch (error) {
        console.error("Error fetching detailed distribution data:", error.message);
      } finally {
        this.isLoading = false;
      }
    },
    handlePanelOpened(isOpen) {
      this.isPanelOpen = isOpen;
    },
  },
  watch: {
    selectedEvent() {
      if (this.selectedSport && this.selectedEvent && this.yearRange && this.yearRange.length === 2) {
        this.fetchSharedData();
        this.fetchDistribution();
      } else {
        console.warn("Missing required filters: sport, event, or year range.");
      }
    },
    yearRange(newRange) {
    if (this.selectedSport && this.selectedEvent && newRange.length === 2) {
      this.fetchSharedData();
      this.fetchDistribution();
    } else {
      console.warn("Missing required filters: sport, event, or year range.");
    }
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
  overflow: hidden;
}

.v-container {
  width: 100%; /* Adjust the width as needed */
  max-width: 100%; /* Optional: Limit the maximum width */
  justify-content: center;
  align-items: center;
}

.v-card {
  position: relative;
  width: 100%; /* Make the card take the full width of the container */
  justify-content: center;
  align-items: center;
}
</style>
