<template>
  <v-container class="container" fluid>
    <v-row>
      <v-col cols="12" md="12">
        <div class="dropdown-container">
          <v-card>
            <v-container>
              <!-- Dropdowns -->
              <v-row>
                <v-col cols="6">
                  <v-select
                      label="Select Country"
                      :items="countries"
                      v-model="selectedCountry"
                  ></v-select>
                </v-col>
                <v-col cols="6">
                  <v-select
                      label="Select Athlete"
                      :items="filteredAthletes"
                      v-model="selectedAthlete"
                      item-value="props"
                      item-text="title"
                      :disabled="!selectedCountry || !sport || !event"
                  ></v-select>
                </v-col>
              </v-row>
              <!-- Radar Chart -->
              <v-row>
                <v-col cols="12">
                  <canvas ref="radarChart"></canvas>
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
import {
  Chart,
  RadarController,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from "chart.js";

Chart.register(RadarController, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

export default {
  props: {
    sport: {
      type: String,
      required: true,
    },
    event: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      chart: null,
      selectedCountry: null,
      selectedAthlete: null,
      countries: ["USA", "China", "Germany", "Canada"], // Example countries
      filteredAthletes: [], // Athletes filtered by selectedCountry, sport, and event
      userData: {
        height: 175,
        weight: 70,
        age: 25,
        medals: 10,
        performance: 179,
      },
      athleteList: [
        {
          title: "Athlete A",
          props: {
            id: 1,
            country: "USA",
            sport: "Swimming",
            event: "200m Freestyle",
            height: 180,
            weight: 75,
            age: 26,
            medals: 8,
            performance: 200,
          },
        },
        {
          title: "Athlete B",
          props: {
            id: 2,
            country: "China",
            sport: "Running",
            event: "100m",
            height: 170,
            weight: 65,
            age: 24,
            medals: 12,
            performance: 220,
          },
        },
        {
          title: "Athlete C",
          props: {
            id: 3,
            country: "USA",
            sport: "Swimming",
            event: "200m Freestyle",
            height: 185,
            weight: 80,
            age: 28,
            medals: 6,
            performance: 190,
          },
        },
        {
          title: "Athlete D",
          props: {
            id: 4,
            country: "Germany",
            sport: "Cycling",
            event: "Road Race",
            height: 178,
            weight: 72,
            age: 27,
            medals: 9,
            performance: 210,
          },
        },
        {
          title: "Athlete E",
          props: {
            id: 5,
            country: "Canada",
            sport: "Running",
            event: "200m",
            height: 172,
            weight: 68,
            age: 23,
            medals: 15,
            performance: 230,
          },
        },
      ],
    };
  },
  methods: {
    updateChart() {
      const canvas = this.$refs.radarChart;
      if (!canvas) return;

      const ctx = canvas.getContext("2d");
      if (!ctx) return;

      if (this.chart) {
        this.chart.destroy();
      }

      const labels = ["Height", "Weight", "Age", "Number of Medals", "Performance"];
      const userDataset = [
        this.userData.height,
        this.userData.weight,
        this.userData.age,
        this.userData.medals,
        this.userData.performance,
      ];
      const athleteDataset = this.selectedAthlete
          ? [
            this.selectedAthlete.height,
            this.selectedAthlete.weight,
            this.selectedAthlete.age,
            this.selectedAthlete.medals,
            this.selectedAthlete.performance,
          ]
          : [0, 0, 0, 0, 0];

      const data = {
        labels,
        datasets: [
          {
            label: "Your Data",
            data: userDataset,
            fill: true,
            backgroundColor: "rgba(54, 162, 235, 0.2)",
            borderColor: "rgba(54, 162, 235, 1)",
          },
          {
            label: "Athlete Data",
            data: athleteDataset,
            fill: true,
            backgroundColor: "rgba(255, 99, 132, 0.2)",
            borderColor: "rgba(255, 99, 132, 1)",
          },
        ],
      };

      const options = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          r: {
            beginAtZero: true,
          },
        },
      };

      this.chart = new Chart(ctx, { type: "radar", data, options });
    },
    filterAthletes() {
      this.filteredAthletes = this.athleteList.filter(
          (athlete) =>
              athlete.props.country === this.selectedCountry &&
              athlete.props.sport === this.sport &&
              athlete.props.event === this.event
      );
      this.selectedAthlete = null;
    },
  },
  watch: {
    selectedCountry: "filterAthletes",
    sport: "filterAthletes",
    event: "filterAthletes",
    selectedAthlete() {
      this.updateChart();
    },
  },
  mounted() {
    this.updateChart();
  },
};
</script>

<style scoped>
.dropdown-container {
  width: 100%;
  height: auto; /* Let the height adjust dynamically */
  min-height: 300px;
  max-width: 100%; /* Prevent overflow */
}
</style>
