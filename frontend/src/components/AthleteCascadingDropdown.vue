<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="12">
        <div class="dropdown-container">
          <v-card>
            <v-container>
              <!-- First Row -->
              <v-row>
                <v-col cols="6">
                  <v-select
                      label="Select Country"
                      :items="countries"
                      v-model="selectedCountry"
                      @change="fetchSports"
                  ></v-select>
                </v-col>
                <v-col cols="6">
                  <v-select
                      label="Select Sport"
                      :items="sports"
                      v-model="selectedSport"
                      :disabled="!selectedCountry"
                      @change="fetchEvents"
                  ></v-select>
                </v-col>
              </v-row>
              <!-- Second Row -->
              <v-row>
                <v-col cols="6">
                  <v-select
                      label="Select Event"
                      :items="events"
                      v-model="selectedEvent"
                      :disabled="!selectedSport"
                      @change="fetchAthletes"
                  ></v-select>
                </v-col>
                <v-col cols="6">
                  <v-select
                      label="Select Athlete"
                      :items="athletes"
                      v-model="selectedAthlete"
                      :disabled="!selectedEvent"
                  ></v-select>
                </v-col>
              </v-row>
              <!-- Confirm Button -->
              <v-row>
                <v-col cols="12" class="text-center">
                  <v-btn
                      :disabled="!selectedAthlete"
                      color="success"
                      @click="confirmSelection"
                  >
                    Confirm
                  </v-btn>
                </v-col>
              </v-row>
            </v-container>
          </v-card>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "CascadingDropdown",
  data() {
    return {
      countries: [], // All countries
      sports: [], // Sports within selected country
      events: [], // Events within selected sport
      athletes: [], // Athletes within selected event
      selectedCountry: null,
      selectedSport: null,
      selectedEvent: null,
      selectedAthlete: null,
    };
  },
  mounted() {
    console.log("Countries:", this.countries);
  },
  methods: {
    fetchSports() {
      if (!this.selectedCountry) return;
      this.resetSelections();
      this.sports = this.mockFetch("sports", this.selectedCountry);
    },
    fetchEvents() {
      if (!this.selectedSport) return;
      this.resetSelections(true);
      this.events = this.mockFetch("events", this.selectedSport);
    },
    fetchAthletes() {
      if (!this.selectedEvent) return;
      this.athletes = [];
      this.selectedAthlete = null;
      this.athletes = this.mockFetch("athletes", this.selectedEvent);
    },
    confirmSelection() {
      this.$emit("athleteSelected", {
        country: this.selectedCountry,
        sport: this.selectedSport,
        event: this.selectedEvent,
        athlete: this.selectedAthlete,
      });
    },
    resetSelections(partial = false) {
      if (!partial) {
        this.sports = [];
        this.selectedSport = null;
      }
      this.events = [];
      this.selectedEvent = null;
      this.athletes = [];
      this.selectedAthlete = null;
    },
    mockFetch(type, filter) {
      const data = {
        sports: {
          USA: ["Basketball", "Swimming"],
          Canada: ["Ice Hockey", "Curling"],
        },
        events: {
          Basketball: ["3x3", "5x5"],
          Swimming: ["50m Freestyle", "200m Butterfly"],
          "Ice Hockey": ["Men's", "Women's"],
          Curling: ["Mixed Doubles", "Team"],
        },
        athletes: {
          "3x3": ["Athlete 1", "Athlete 2"],
          "5x5": ["Athlete 3", "Athlete 4"],
          "50m Freestyle": ["Athlete 5", "Athlete 6"],
          "200m Butterfly": ["Athlete 7", "Athlete 8"],
        },
      };
      return data[type][filter] || [];
    },
  },
};
</script>

<style scoped>
.dropdown-container {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 300px;
}
</style>
