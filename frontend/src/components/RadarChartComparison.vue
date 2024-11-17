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
  props: {
    userData: {
      type: Object,
      required: true
    },
    athleteData: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      chart: null,
    };
  },
  methods: {
    updateChart() {
      const canvas = this.$refs.radarChart;
      if (!canvas) return;

      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      if (this.chart) {
        this.chart.destroy();
      }

      const labels = ["Height", "Weight", "Age"];
      const userDataset = [this.userData.height, this.userData.weight, this.userData.age];
      const athleteDataset = this.athleteData
          ? [this.athleteData.height, this.athleteData.weight, this.athleteData.age]
          : [0, 0, 0]; // Placeholder if no athlete data is selected

      const data = {
        labels,
        datasets: [
          {
            label: "Your Data",
            data: userDataset,
            fill: true,
            backgroundColor: "rgba(54, 162, 235, 0.2)",
            borderColor: "rgba(54, 162, 235, 1)"
          },
          {
            label: "Athlete Data",
            data: athleteDataset,
            fill: true,
            backgroundColor: "rgba(255, 99, 132, 0.2)",
            borderColor: "rgba(255, 99, 132, 1)"
          }
        ]
      };

      const options = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          r: {
            beginAtZero: true
          }
        }
      };

      this.chart = new Chart(ctx, { type: 'radar', data, options });
    }
  },
  watch: {
    userData: {
      handler() {
        this.updateChart();
      },
      deep: true
    },
    athleteData: {
      handler() {
        this.updateChart();
      },
      deep: true
    }
  },
  mounted() {
    this.updateChart();
  }
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
