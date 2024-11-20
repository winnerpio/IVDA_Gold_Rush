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
                      :disabled="!selectedCountry"
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
  data() {
    return {
      chart: null,
      selectedCountry: null,
      selectedAthlete: null,
      countries: ["USA", "Canada", "Germany", "China"], // Example countries
      filteredAthletes: [], // Athletes filtered by selectedCountry
      userData: {
        height: 175,
        weight: 70,
        age: 25,
      },
      athleteList: [
        {
          title: "Athlete A",
          props: { id: 1, country: "USA", height: 180, weight: 75, age: 26, name: "Athlete A" },
        },
        {
          title: "Athlete B",
          props: { id: 2, country: "China", height: 170, weight: 65, age: 24, name: "Athlete B" },
        },
        {
          title: "Athlete C",
          props: { id: 3, country: "USA", height: 185, weight: 80, age: 28, name: "Athlete C" },
        },
        {
          title: "Athlete D",
          props: { id: 4, country: "Germany", height: 178, weight: 72, age: 27, name: "Athlete D" },
        },
        {
          title: "Athlete E",
          props: { id: 5, country: "Canada", height: 172, weight: 68, age: 23, name: "Athlete E" },
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

      const labels = ["Height", "Weight", "Age"];
      const userDataset = [this.userData.height, this.userData.weight, this.userData.age];
      const athleteDataset =
          this.selectedAthlete
              ? [
                this.selectedAthlete.height,
                this.selectedAthlete.weight,
                this.selectedAthlete.age,
              ]
              : [0, 0, 0];

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
    fetchAthletes() {
      this.filteredAthletes = this.athleteList.filter(
          (athlete) => athlete.props.country === this.selectedCountry
      );
      this.selectedAthlete = null;
    },
  },
  watch: {
    selectedCountry() {
      this.fetchAthletes();
    },
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
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 300px;
}

.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  padding: 20px;
}


</style>