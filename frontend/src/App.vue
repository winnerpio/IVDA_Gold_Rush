<template>
  <v-app>
    <!-- Toolbar -->
    <v-app-bar app>
      <v-img
          src="./assets/olympic_rings.png"
          alt="Olympic Rings"
          max-width="70"
          max-heihgt="70"
          contain
          style="margin-left:20px"
      ></v-img>
      <v-toolbar-title>The Gold Rush</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items>
        <v-btn
            text
            @click="activePanel = 'panel1'"
            :class="{ 'active-btn': activePanel === 'panel1' }"
        >
          Exploration
        </v-btn>
        <v-btn
            text
            @click="activePanel = 'panel2'"
            :class="{ 'active-btn': activePanel === 'panel2' }"
        >
          Comparison
        </v-btn>
        <v-btn
            text
            @click="activePanel = 'panel3'"
            :class="{ 'active-btn': activePanel === 'panel3' }"
        >
          Outlier Identification
        </v-btn>
      </v-toolbar-items>
    </v-app-bar>

    <!-- OlympicSidebar -->
    <OlympicSidebar
      :minYear="minYear"
      :maxYear="maxYear"
      v-model:yearRange="yearRange"
      @update-sport-event="handleSportEventUpdate"
      @update-user-data="updateUserAttributes"
    />
      <!-- Main Content -->
      <v-main class="d-flex align-start pl-0 pt-10">
        <v-container class="main-content" fluid>
          <!-- Panel 1 -->
          <div v-if="activePanel === 'panel1'">
            <ExplorationPanel
              :minYear="minYear"
              :maxYear="maxYear"
              :yearRange="yearRange"
              :selectedCountry="selectedCountry"
              :selectedSport="selectedSport"
              :selectedEvent="selectedEvent"
              :sharedData="sharedData"
              :distributionData="distributionData"
              :selectedDistVariable="selectedDistVariable"
              @update-selected-country="handleCountrySelected"
              @update-year-range="updateYearRange"
              @update-sport-event="handleSportEventUpdate"
              @update-dist-variable="handleDistVariableSelection"
            />
          </div>

          <!-- Panel 2 -->
          <div v-if="activePanel === 'panel2'">
            <ComparisonPanel
              :yearRange="yearRange"
              :minYear="minYear"
              :maxYear="maxYear"
              :userData="userData"
              :selectedSport="selectedSport"
              :selectedEvent="selectedEvent"
              :selectedCountry="selectedCountry"
              @update-user-attributes="updateUserAttributes"
              @update-sport-event="handleSportEventUpdate"
              @update-selected-country="handleCountrySelected"
            />
          </div>

          <!-- Panel 3 -->
          <div v-if="activePanel === 'panel3'">
            <OutlierIdentificationPanel
              :sport="selectedSport"
              :event="selectedEvent"
              :yearRange="yearRange"
            />
          </div>
        </v-container>
      </v-main>
  </v-app>
</template>

<script>
import axios from 'axios';
import OlympicSidebar from './components/OlympicSidebar.vue';
import OutlierIdentificationPanel from "./components/OutlierIdentificationPanel.vue";
import ComparisonPanel from './components/ComparisonPanel.vue';
import ExplorationPanel from './components/ExplorationPanel.vue';

export default {
  name: "App",
  components: {
    OlympicSidebar,
    ExplorationPanel,
    ComparisonPanel,
    OutlierIdentificationPanel,
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
      minYear: 1896,
      maxYear: 2022,
      selectedAthleteData: null,
      selectedSport: null,
      selectedEvent: null,
      sharedData: null,
      isLoading: false,
      distributionData: null,
      selectedDistVariable: 'age',
      activePanel: 'panel1',
    };
  },
  methods: {
    async fetchSharedData() {
      if (!this.yearRange) {
        console.warn("Missing filters for data fetching.");
        return;
      }

      this.isLoading = true;

      try {
        const params = {
          year_lower: this.yearRange[0],
          year_upper: this.yearRange[1],
        };

        if (this.selectedSport) params.sport = this.selectedSport;
        if (this.selectedEvent) params.event = this.selectedEvent;

        const response = await axios.get("http://127.0.0.1:5000/MedalCount", { params });

        this.sharedData = response.data;
      } catch (error) {
        console.error("Error fetching shared data:", error.message);
      } finally {
        this.isLoading = false;
      }
    },
    updateUserAttributes(attributes) {
      this.userData = { ...this.userData, ...attributes };
    },
    handleSportEventUpdate({ sport, event }) {
      this.selectedSport = sport;
      this.selectedEvent = event;
    },
    handleCountrySelected({ countryName, countryCode }) {
      this.selectedCountry = { name: countryName, code: countryCode };
    },
    updateYearRange(range) {
      this.yearRange = range;
    },
    async fetchDistribution() {
      if (!this.yearRange || !this.selectedDistVariable) {
        console.warn("Missing filters for distribution data fetching.");
        return;
      }

      this.isLoading = true;

      try {
        const params = {
          year_lower: this.yearRange[0],
          year_upper: this.yearRange[1],
          dist_variable: this.selectedDistVariable,
          bins: 10,
        };

        if (this.selectedSport) params.sport = this.selectedSport;
        if (this.selectedEvent) params.event = this.selectedEvent;

        if (this.selectedCountry && this.selectedCountry.code) {
          params.country_code = this.selectedCountry.code;
          // console.log("Country code included in params:", params.noc);
        } else {
          // console.log("No country selected, fetching data for all countries.");
        }

        // console.log("Fetching distribution data with params:", params);

        const response = await axios.get("http://127.0.0.1:5000/GetDistribution", { params });

        // console.log("Distribution data response:", response);
        this.distributionData = response.data;
      } catch (error) {
        console.error("Error fetching distribution data:", error.message);
      } finally {
        this.isLoading = false;
      }
    },
    handleDistVariableSelection(distVariable) {
      this.selectedDistVariable = distVariable;
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
    selectedCountry() {
      if (this.yearRange && this.yearRange.length === 2) {
        this.fetchDistribution();
      }
    },
    selectedDistVariable() {
      if (this.yearRange && this.yearRange.length === 2) {
        this.fetchDistribution();
      }
    },
  },
};
</script>

<style scoped>
.main-content {
  padding: 20px;
  background-color: #fff;
}

.v-toolbar-title__placeholder {
  overflow: auto;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.custom-sidebar {
  width: 400px !important; /* Override default width */
}

.v-application--wrap {
  min-height: 100vh;
}

h2 {
  font-size: 1.2rem;
  font-weight: 500;
  margin-bottom: 15px;
  color: #333;
  text-align: center;
}


</style>
