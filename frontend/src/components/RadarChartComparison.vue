<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="12">
        <div class="chart-container">
          <canvas ref="radarChart"></canvas>
        </div>

      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { Chart, RadarController, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend } from 'chart.js';

Chart.register(RadarController, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

export default {
  data() {
    return {
      userData: { height: 0, weight: 0, age: 0, sport: null},
      sports: ["Athletics", "Swimming", "Basketball"],
      medalistData: {height: 0, weight: 0, age: 0},
      chart: null,
    };
  },
  methods: {
    fetchMedalistData() {
      // Placeholder function to simulate fetching average medalist data for the selected sport
      if (this.userData.sport) {
        this.medalistData = {
          height: 180, // Example values
          weight: 75,
          age: 25,
        };
      }
    },
    updateChart() {
      const canvas = this.$refs.radarChart;
      if (!canvas) return;

      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      if (this.chart) {
        this.chart.destroy();
      }

      const data = {
        labels: ["Height", "Weight", "Age"],
        datasets: [
          {
            label: "Your Data",
            data: [this.userData.height, this.userData.weight, this.userData.age],
            fill: true,
            backgroundColor: "rgba(54, 162, 235, 0.2)",
            borderColor: "rgba(54, 162, 235, 1)",
          },
          {
            label: "Medalist Average",
            data: [this.medalistData.height, this.medalistData.weight, this.medalistData.age],
            fill: true,
            backgroundColor: "rgba(255, 99, 132, 0.2)",
            borderColor: "rgba(255, 99, 132, 1)",
          },
        ],
      };

      const options = {
        responsive: true,
        maintainAspectRatio: false,
        scale: {
          ticks: { beginAtZero: true },
        },
      };
      this.chart = new Chart(ctx, { type: 'radar', data, options });
    },
  },
  mounted() {
    this.updateChart();
  },
  props: {
    userDataForm: {
      type: Object,
      required: true,
    },
  },
  watch: {
    userDataForm: {
      handler(newData) {
        this.userData = {...newData};
        this.fetchMedalistData();
        this.updateChart();
      },
      deep: true,
    },
  },
};
</script>

<style>
.chart-container {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 300px;
}
</style>

