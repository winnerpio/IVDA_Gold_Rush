<template>
  <div class="layout-container">
    <!-- Main Content -->
    <div class="main-content">
      <!-- Age Distribution and Medal Count -->
      <div class="graph-container">
        <canvas id="mainGraph"></canvas>
      </div>

      <!-- Olympic Data by Year -->
      <div class="panel-content">
        <h1>Olympic Data by Year</h1>
        <div v-if="filteredOlympicData.length > 0">
          <!-- Filtered Data Charts -->
          <div
            v-for="data in filteredOlympicData"
            :key="data.Year"
            class="year-charts"
          >
            <h2>Year: {{ data.Year }}</h2>
            <div class="chart-container" :id="'canvas-container-' + data.Year">
              <!-- Canvas will be recreated here -->
              <canvas :id="'combinedChart-' + data.Year"></canvas>
            </div>
          </div>
        </div>
        <div v-else>
          <p>No data available for the selected range.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

export default {
  name: "AthleteAttributeDistribution",
  props: {
    dateRange: {
      type: Array,
      default: () => [1896, 2020],
    },
  },
  data() {
    return {
      mainGraphInstance: null,
      olympicData: [
        { "Year": 1896, "less than 19y": 26, "20-24": 28, "25-29": 19, "30-34": 18, "more than 35y": 61, "Total Medals": 364, "MedalsByAge": [40, 100, 80, 70, 74] },
        { "Year": 1900, "less than 19y": 19, "20-24": 19, "25-29": 19, "30-34": 21, "more than 35y": 54, "Total Medals": 362, "MedalsByAge": [35, 90, 85, 70, 82] },
        { "Year": 1904, "less than 19y": 8, "20-24": 8, "25-29": 8, "30-34": 6, "more than 35y": 29, "Total Medals": 146, "MedalsByAge": [10, 25, 30, 25, 56] },
        { "Year": 1908, "less than 19y": 18, "20-24": 29, "25-29": 35, "30-34": 21, "more than 35y": 74, "Total Medals": 443, "MedalsByAge": [50, 120, 130, 80, 63] },
        { "Year": 1912, "less than 19y": 10, "20-24": 13, "25-29": 12, "30-34": 21, "more than 35y": 50, "Total Medals": 270, "MedalsByAge": [15, 40, 35, 50, 130] },
        { "Year": 1920, "less than 19y": 4, "20-24": 12, "25-29": 8, "30-34": 7, "more than 35y": 23, "Total Medals": 121, "MedalsByAge": [5, 30, 20, 15, 51] },
        { "Year": 1924, "less than 19y": 14, "20-24": 9, "25-29": 4, "30-34": 12, "more than 35y": 26, "Total Medals": 164, "MedalsByAge": [15, 25, 10, 35, 79] },
        { "Year": 1928, "less than 19y": 10, "20-24": 20, "25-29": 11, "30-34": 10, "more than 35y": 37, "Total Medals": 189, "MedalsByAge": [20, 60, 40, 30, 39] },
        { "Year": 1932, "less than 19y": 8, "20-24": 14, "25-29": 10, "30-34": 5, "more than 35y": 28, "Total Medals": 112, "MedalsByAge": [15, 40, 35, 10, 12] },
        { "Year": 1936, "less than 19y": 7, "20-24": 19, "25-29": 15, "30-34": 9, "more than 35y": 32, "Total Medals": 182, "MedalsByAge": [10, 45, 50, 20, 57] },
        { "Year": 1940, "less than 19y": 7, "20-24": 15, "25-29": 16, "30-34": 14, "more than 35y": 34, "Total Medals": 185, "MedalsByAge": [10, 50, 55, 40, 30] },
        { "Year": 1944, "less than 19y": 8, "20-24": 8, "25-29": 6, "30-34": 10, "more than 35y": 18, "Total Medals": 137, "MedalsByAge": [10, 30, 20, 25, 52] },
        { "Year": 1948, "less than 19y": 6, "20-24": 18, "25-29": 8, "30-34": 15, "more than 35y": 22, "Total Medals": 172, "MedalsByAge": [12, 48, 40, 30, 42] },
        { "Year": 1952, "less than 19y": 12, "20-24": 20, "25-29": 24, "30-34": 21, "more than 35y": 71, "Total Medals": 369, "MedalsByAge": [40, 90, 80, 70, 89] },
        { "Year": 1956, "less than 19y": 10, "20-24": 36, "25-29": 32, "30-34": 34, "more than 35y": 85, "Total Medals": 514, "MedalsByAge": [50, 100, 120, 80, 164] },
        { "Year": 1960, "less than 19y": 16, "20-24": 17, "25-29": 9, "30-34": 19, "more than 35y": 44, "Total Medals": 265, "MedalsByAge": [20, 40, 35, 70, 100] },
        { "Year": 1964, "less than 19y": 6, "20-24": 8, "25-29": 18, "30-34": 15, "more than 35y": 21, "Total Medals": 157, "MedalsByAge": [10, 30, 40, 50, 27] },
        { "Year": 1968, "less than 19y": 8, "20-24": 16, "25-29": 23, "30-34": 24, "more than 35y": 50, "Total Medals": 312, "MedalsByAge": [20, 50, 60, 80, 102] },
        { "Year": 1972, "less than 19y": 21, "20-24": 29, "25-29": 35, "30-34": 29, "more than 35y": 54, "Total Medals": 418, "MedalsByAge": [50, 100, 120, 100, 48] },
        { "Year": 1976, "less than 19y": 17, "20-24": 37, "25-29": 36, "30-34": 30, "more than 35y": 64, "Total Medals": 452, "MedalsByAge": [50, 110, 90, 80, 122] },
        { "Year": 1980, "less than 19y": 14, "20-24": 35, "25-29": 25, "30-34": 31, "more than 35y": 63, "Total Medals": 382, "MedalsByAge": [40, 100, 70, 50, 122] },
        { "Year": 1984, "less than 19y": 22, "20-24": 34, "25-29": 34, "30-34": 43, "more than 35y": 65, "Total Medals": 514, "MedalsByAge": [50, 140, 100, 100, 124] },
        { "Year": 1988, "less than 19y": 20, "20-24": 25, "25-29": 31, "30-34": 25, "more than 35y": 60, "Total Medals": 380, "MedalsByAge": [30, 100, 120, 60, 70] },
        { "Year": 1992, "less than 19y": 8, "20-24": 9, "25-29": 11, "30-34": 11, "more than 35y": 23, "Total Medals": 145, "MedalsByAge": [10, 40, 30, 20, 45] },
        { "Year": 1996, "less than 19y": 14, "20-24": 22, "25-29": 25, "30-34": 26, "more than 35y": 73, "Total Medals": 364, "MedalsByAge": [40, 100, 90, 70, 64] },
        { "Year": 2000, "less than 19y": 11, "20-24": 34, "25-29": 33, "30-34": 26, "more than 35y": 77, "Total Medals": 403, "MedalsByAge": [35, 110, 100, 80, 78] },
        { "Year": 2004, "less than 19y": 16, "20-24": 27, "25-29": 34, "30-34": 21, "more than 35y": 60, "Total Medals": 425, "MedalsByAge": [45, 120, 130, 70, 60] },
        { "Year": 2008, "less than 19y": 15, "20-24": 17, "25-29": 24, "30-34": 37, "more than 35y": 57, "Total Medals": 403, "MedalsByAge": [40, 70, 110, 120, 63] },
        { "Year": 2012, "less than 19y": 2, "20-24": 17, "25-29": 19, "30-34": 21, "more than 35y": 36, "Total Medals": 241, "MedalsByAge": [10, 60, 80, 50, 41] },
        { "Year": 2016, "less than 19y": 10, "20-24": 32, "25-29": 27, "30-34": 36, "more than 35y": 78, "Total Medals": 462, "MedalsByAge": [30, 140, 120, 110, 62] },
        { "Year": 2020, "less than 19y": 8, "20-24": 11, "25-29": 15, "30-34": 10, "more than 35y": 30, "Total Medals": 188, "MedalsByAge": [20, 50, 70, 30, 18] },
      ],
      chartInstances: {},
      minYear: 1896,
      maxYear: 2020,
    };
  },
  computed: {
    filteredOlympicData() {
      return this.olympicData.filter(
        (data) =>
          data.Year >= this.dateRange[0] && data.Year <= this.dateRange[1]
      );
    },
  },
  methods: {
    computeAgeDistribution() {
      const ageGroups = [
        "less than 19y",
        "20-24",
        "25-29",
        "30-34",
        "more than 35y",
      ];
      const ageDistribution = {};
      const medalCount = {};
      ageGroups.forEach((group) => {
        ageDistribution[group] = 0;
        medalCount[group] = 0;
      });
      this.filteredOlympicData.forEach((data) => {
        ageGroups.forEach((group, index) => {
          ageDistribution[group] += data[group];
          medalCount[group] += data.MedalsByAge[index];
        });
      });
      return { ageDistribution, medalCount };
    },
    updateMainGraph() {
      const { ageDistribution, medalCount } = this.computeAgeDistribution();
      const labels = [
        "less than 19y",
        "20-24",
        "25-29",
        "30-34",
        "more than 35y",
      ];
      const athleteData = labels.map((label) => ageDistribution[label]);
      const medalData = labels.map((label) => medalCount[label]);

      if (this.mainGraphInstance) {
        this.mainGraphInstance.destroy();
      }

      this.drawMainGraph("mainGraph", athleteData, medalData);
    },
    drawMainGraph(canvasId, athleteData, medalData) {
      this.$nextTick(() => {
        const canvas = document.getElementById(canvasId);

        if (!canvas) {
          console.error("Canvas element not found!");
          return;
        }

        const ctx = canvas.getContext("2d");

        const labels = [
          "less than 19y",
          "20-24",
          "25-29",
          "30-34",
          "more than 35y",
        ];

        const histogramData = {
          labels: labels,
          datasets: [
            {
              type: "bar",
              label: "Age Distribution",
              data: athleteData,
              backgroundColor: "rgba(100, 149, 237, 0.7)",
              borderColor: "rgba(100, 149, 237, 1)",
              borderWidth: 1,
            },
            {
              type: "line",
              label: "Medal Count",
              data: medalData,
              borderColor: "rgba(220, 20, 60, 0.8)",
              backgroundColor: "rgba(220, 20, 60, 0.2)",
              fill: false,
              borderWidth: 2,
              tension: 0.4,
              yAxisID: "y2",
            },
          ],
        };

        const config = {
          type: "bar",
          data: histogramData,
          options: {
            responsive: true,
            plugins: {
              legend: { position: "top" },
              title: { display: true, text: "Age Distribution and Medal Count" },
            },
            scales: {
              x: { title: { display: true, text: "Age Groups" } },
              y: {
                title: { display: true, text: "Number of Athletes" },
                beginAtZero: true,
              },
              y2: {
                title: { display: true, text: "Medal Count" },
                position: "right",
                beginAtZero: true,
                grid: { drawOnChartArea: false },
              },
            },
          },
        };

        this.mainGraphInstance = new Chart(ctx, config);
      });
    },
    drawOlympicCharts() {
      this.$nextTick(() => {
        const filteredData = this.filteredOlympicData;

        filteredData.forEach((data) => {
          const canvasId = `combinedChart-${data.Year}`;
          const canvas = document.getElementById(canvasId);
          if (!canvas) return;

          const ctx = canvas.getContext("2d");

          this.chartInstances[canvasId] = new Chart(ctx, {
            type: "bar",
            data: {
              labels: ["<19", "20-24", "25-29", "30-34", ">35"],
              datasets: [
                {
                  type: "bar",
                  label: `Number of Athletes (${data.Year})`,
                  data: [
                    data["less than 19y"],
                    data["20-24"],
                    data["25-29"],
                    data["30-34"],
                    data["more than 35y"],
                  ],
                  backgroundColor: "rgba(75, 192, 192, 0.7)",
                  borderColor: "rgba(75, 192, 192, 1)",
                  borderWidth: 1,
                },
                {
                  type: "line",
                  label: `Medals (${data.Year})`,
                  data: data.MedalsByAge,
                  borderColor: "rgba(220, 20, 60, 0.7)",
                  backgroundColor: "rgba(220, 20, 60, 0.2)",
                  fill: false,
                  borderWidth: 2,
                  tension: 0.4,
                  yAxisID: "y2",
                },
              ],
            },
            options: {
              responsive: true,
              plugins: {
                legend: { position: "top" },
                title: { display: true, text: `Combined Chart (${data.Year})` },
              },
              scales: {
                x: { title: { display: true, text: "Age Groups" } },
                y: {
                  title: { display: true, text: "Number of Athletes" },
                  beginAtZero: true,
                },
                y2: {
                  type: "linear",
                  position: "right",
                  title: { display: true, text: "Medal Count" },
                  grid: { drawOnChartArea: false },
                  beginAtZero: true,
                },
              },
            },
          });
        });
      });
    },
    clearCharts() {
      // Destroy existing chart instances
      Object.values(this.chartInstances).forEach((chart) => chart.destroy());
      this.chartInstances = {};
    },
  },
  watch: {
    // Watch for changes in filteredOlympicData
    filteredOlympicData: {
      immediate: true,
      handler() {
        this.clearCharts();
        this.updateMainGraph();
        this.drawOlympicCharts();
      },
    },
  },
  mounted() {
    // Initial rendering is handled by the watcher
  },
};
</script>

<style scoped>
.layout-container {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.main-content {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.graph-container {
  width: 100%;
  max-width: 1200px;
  margin-bottom: 20px;
}

#mainGraph {
  width: 100%;
  height: auto;
}

.panel-content {
  text-align: center;
  width: 100%;
}

.year-charts {
  margin-top: 20px;
  width: 100%;
}

.chart-container {
  width: 100%;
  height: auto;
}
</style>
