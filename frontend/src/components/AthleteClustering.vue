<template>
  <v-card class="full-height-card">
    <v-card-title>Similar Athlete Clusters</v-card-title>
    <v-card-subtitle>Select attributes to visualize athlete clusters</v-card-subtitle>
    <v-container fluid class="full-height-container">
      <v-row>
        <v-col cols="12" md="6">
          <v-select
              :items="attributes"
              label="X-Axis Attribute"
              v-model="xAttribute"
              outlined
          ></v-select>
        </v-col>
        <v-col cols="12" md="6">
          <v-select
              :items="attributes"
              label="Y-Axis Attribute"
              v-model="yAttribute"
              outlined
          ></v-select>
        </v-col>
      </v-row>
      <v-row class="chart-row">
        <v-col cols="12">
          <div class="chart-container">
            <canvas ref="scatterChart"></canvas>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>

<script>
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  PointElement,
  CategoryScale,
  LinearScale,
} from "chart.js";

ChartJS.register(Title, Tooltip, Legend, PointElement, CategoryScale, LinearScale);

export default {
  name: 'AthleteClustering',
  data() {
    return {
      xAttribute: 'Height',
      yAttribute: 'Age',
      attributes: ['Height', 'Age', 'Weight'],
      scatterChart: null,
      data: [
        { x: 190, y: 22, cluster: 0 },
        { x: 188, y: 23, cluster: 0 },
        { x: 192, y: 24, cluster: 0 },
        { x: 189, y: 25, cluster: 0 },
        { x: 191, y: 21, cluster: 0 },
        { x: 193, y: 22, cluster: 0 },
        { x: 190, y: 24, cluster: 0 },
        { x: 194, y: 23, cluster: 0 },
        { x: 189, y: 20, cluster: 0 },
        { x: 192, y: 21, cluster: 0 },

        // Cluster 1: Medium height, mid-range age
        { x: 180, y: 28, cluster: 1 },
        { x: 178, y: 29, cluster: 1 },
        { x: 181, y: 30, cluster: 1 },
        { x: 179, y: 27, cluster: 1 },
        { x: 182, y: 31, cluster: 1 },
        { x: 180, y: 29, cluster: 1 },
        { x: 183, y: 28, cluster: 1 },
        { x: 181, y: 30, cluster: 1 },
        { x: 178, y: 27, cluster: 1 },
        { x: 182, y: 32, cluster: 1 },

        // Cluster 2: Shorter, older athletes
        { x: 170, y: 33, cluster: 2 },
        { x: 172, y: 34, cluster: 2 },
        { x: 173, y: 35, cluster: 2 },
        { x: 171, y: 32, cluster: 2 },
        { x: 174, y: 36, cluster: 2 },
        { x: 172, y: 34, cluster: 2 },
        { x: 175, y: 35, cluster: 2 },
        { x: 170, y: 33, cluster: 2 },
        { x: 173, y: 34, cluster: 2 },
        { x: 171, y: 32, cluster: 2 }
      ],
      colors: ['rgba(75, 192, 192, 0.6)', 'rgba(255, 99, 132, 0.6)', 'rgba(54, 162, 235, 0.6)'],
    };
  },
  watch: {
    xAttribute: 'updateChart',
    yAttribute: 'updateChart',
  },
  methods: {
    updateChart() {
      const ctx = this.$refs.scatterChart.getContext('2d');

      if (this.scatterChart) {
        this.scatterChart.destroy();
      }

      const clusteredData = this.data.map((point) => ({
        x: point.x,
        y: point.y,
      }));

      this.scatterChart = new ChartJS(ctx, {
        type: 'scatter',
        data: {
          datasets: [
            {
              label: 'Athlete Clusters',
              data: clusteredData,
              backgroundColor: this.data.map((point) => this.colors[point.cluster]),
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: { title: { display: true, text: this.xAttribute } },
            y: { title: { display: true, text: this.yAttribute } },
          },
        },
      });
    },
  },
  mounted() {
    this.updateChart();
  },
};
</script>

<style scoped>
.full-height-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.full-height-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chart-row {
  flex-grow: 1;
}

.chart-container {
  position: relative;
  flex-grow: 1;
  height: 100%;
}

canvas {
  width: 100%;
  height: 100%;
}
</style>
