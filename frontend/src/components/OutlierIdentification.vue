<template>
  <v-container>
    <v-row>
      <v-col cols="12" sm="4">
        <v-select
            v-model="xAxis"
            :items="attributes"
            label="X-Axis Attribute"
        ></v-select>
      </v-col>
      <v-col cols="12" sm="4">
        <v-select
            v-model="yAxis"
            :items="attributes"
            label="Y-Axis Attribute"
        ></v-select>
      </v-col>
      <v-col cols="12" sm="4">
        <v-select
            v-model="selectedSport"
            :items="sports"
            label="Select Sport"
        ></v-select>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="1" md="12">
        <v-card outlined class="pa-0" fill-height>
          <v-card-title>{{ xAxis }} vs {{ yAxis }} Outlier Detection</v-card-title>
          <v-card-text class="pa-0">
            <Scatter :data="chartData" :options="chartOptions" />
          </v-card-text>
        </v-card>
      </v-col>

    </v-row>
  </v-container>
</template>

<script>
import { Scatter } from "vue-chartjs";
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
  name: "OutlierIdentification",
  components: { Scatter },

  data() {
    return {
      xAxis: 'Height',
      yAxis: 'Weight',
      selectedSport: null,
      attributes: ['Height', 'Weight', 'Age'],
      sports: ['Basketball', 'Swimming', 'Athletics'],
      chartData: this.generateRandomData(),
      chartOptions: {
        responsive: true,
        plugins: {
          legend: { display: true },
          tooltip: {
            callbacks: {
              label: (context) => {
                const { x, y } = context.raw;
                return `(${x}, ${y})${context.raw.medalist ? ' - Medalist' : ''}`;
              },
            },
          },
        },
        scales: {
          x: { title: { display: true, text: this.xAxis } },
          y: { title: { display: true, text: this.yAxis } },
        },
      },
    };
  },

  watch: {
    xAxis() { this.updateChartData(); },
    yAxis() { this.updateChartData(); },
    selectedSport() { this.updateChartData(); },
  },

  methods: {
    generateRandomData() {
      const data = Array.from({ length: 50 }, (_, i) => ({
        x: Math.floor(Math.random() * 50) + 150,
        y: Math.floor(Math.random() * 50) + 50,
        medalist: i % 10 === 0,
      }));

      return {
        datasets: [
          {
            label: `${this.xAxis} vs ${this.yAxis}`,
            data: data,
            backgroundColor: data.map((d) => (d.medalist ? '#FFD700' : '#4285F4')), // Gold for medalists
            pointRadius: data.map((d) => (d.medalist ? 6 : 4)),
          },
        ],
      };
    },

    updateChartData() {
      this.chartData = this.generateRandomData();
      this.chartOptions.scales.x.title.text = this.xAxis;
      this.chartOptions.scales.y.title.text = this.yAxis;
    },
  },
};
</script>

<style scoped>
</style>
