<template>
  <div class="expandable-menu">
    <!-- '+'' Button -->
    <div v-if="!isPanelOpen" class="menu-button">
      <button class="plus-icon" @click="toggleFullscreen">+</button>
    </div>

    <!-- Graph -->
    <div class="graph-container">
      <canvas id="myGraph"></canvas>
    </div>

    <!-- Expandable Panel -->
    <div v-if="isPanelOpen">
  <div class="fullscreen-overlay"></div>
  <div class="fullscreen-panel">
    <!-- Close Button -->
    <button @click="toggleFullscreen" class="close-btn">×</button>
    <div class="panel-content">
      <h1>Olympic Data by Year</h1>
      <div v-for="year in olympicYears" :key="year" class="year-charts">
        <h2>Year: {{ year }}</h2>
        <div class="chart-container">
          <canvas :id="'ageDistribution-' + year"></canvas>
        </div>
        <div class="chart-container">
          <canvas :id="'ageCorrelation-' + year"></canvas>
        </div>
      </div>
    </div>
  </div>
  </div>

  </div>
</template>

<script>
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

export default {
  name: "ExpandableMenu",
  data() {
    return {
      isPanelOpen: false,
      mainGraphInstance: null,
      olympicData: [
        { Year: 2000, "less than 19y": 10, "20-24": 50, "25-29": 30, "30-34": 20, "more than 35y": 10, "Total Medals": 120 },
        { Year: 2004, "less than 19y": 15, "20-24": 60, "25-29": 35, "30-34": 25, "more than 35y": 15, "Total Medals": 150 },
        { Year: 2008, "less than 19y": 20, "20-24": 70, "25-29": 40, "30-34": 30, "more than 35y": 20, "Total Medals": 180 },
        { Year: 2012, "less than 19y": 12, "20-24": 55, "25-29": 33, "30-34": 28, "more than 35y": 11, "Total Medals": 139 },
        { Year: 2016, "less than 19y": 18, "20-24": 65, "25-29": 42, "30-34": 35, "more than 35y": 22, "Total Medals": 182 },
      ],
      olympicYears: [], // Store unique years
      chartInstances: {}, // Store all chart instances by canvas ID
    };
  },
  methods: {
    loadOlympicData() {
      // 데이터 로드: 직접 작성한 데이터로부터 연도 추출
      this.olympicYears = this.olympicData.map((row) => row.Year);
      console.log("Loaded Olympic Data:", this.olympicData);
      console.log("Olympic Years:", this.olympicYears);
    },
    toggleFullscreen() {
      this.isPanelOpen = !this.isPanelOpen;

      if (this.isPanelOpen) {
        this.$nextTick(() => {
          this.drawOlympicCharts();
        });

        if (this.mainGraphInstance) {
          this.mainGraphInstance.destroy();
          this.mainGraphInstance = null;
        }
      } else {
        // Destroy all chart instances when closing the panel
        Object.values(this.chartInstances).forEach((chart) => {
          chart.destroy();
        });
        this.chartInstances = {};

        this.$nextTick(() => {
          this.drawMainGraph("myGraph");
        });
      }
    },
    drawMainGraph(canvasId) {
      const canvas = document.getElementById(canvasId);

      if (!canvas) {
        console.error("Canvas element not found!");
        return;
      }

      const ctx = canvas.getContext("2d");

      const histogramData = {
        labels: ["less than 19y", "20-24", "25-29", "30-34", "more than 35y"],
        datasets: [
          {
            type: "bar",
            label: "Age Distribution",
            data: [15, 25, 40, 30, 10],
            backgroundColor: "rgba(100, 149, 237, 0.7)",
            borderColor: "rgba(100, 149, 237, 1)",
            borderWidth: 1,
          },
          {
            type: "line",
            label: "Medal Count",
            data: [5, 40, 53, 27, 19],
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
            legend: {
              position: "top",
            },
            title: {
              display: true,
              text: "Age Distribution and Medal Count",
            },
          },
          scales: {
            x: {
              title: {
                display: true,
                text: "Age Groups",
              },
            },
            y: {
              title: {
                display: true,
                text: "Frequency",
              },
              beginAtZero: true,
            },
            y2: {
              title: {
                display: true,
                text: "Medal Count",
              },
              position: "right",
              beginAtZero: true,
              grid: {
                drawOnChartArea: false,
              },
            },
          },
        },
      };

      this.mainGraphInstance = new Chart(ctx, config);
    },
    drawOlympicCharts() {
      this.$nextTick(() => {
        this.olympicData.forEach((yearData) => {
          const year = yearData.Year;

          const distId = `ageDistribution-${year}`;
          const corrId = `ageCorrelation-${year}`;

          const distCanvas = document.getElementById(distId);
          const corrCanvas = document.getElementById(corrId);

          if (!distCanvas || !corrCanvas) {
            console.error(`Canvas elements for year ${year} are not found.`);
            return;
          }

          const distCtx = distCanvas.getContext("2d");
          const corrCtx = corrCanvas.getContext("2d");

          const distChart = new Chart(distCtx, {
            type: "bar",
            data: {
              labels: ["<19", "20-24", "25-29", "30-34", ">35"],
              datasets: [
                {
                  label: `Age Distribution (${year})`,
                  data: [
                    yearData["less than 19y"],
                    yearData["20-24"],
                    yearData["25-29"],
                    yearData["30-34"],
                    yearData["more than 35y"],
                  ],
                  backgroundColor: "rgba(75, 192, 192, 0.7)",
                },
              ],
            },
            options: {
              responsive: true,
              plugins: {
                legend: {
                  position: "top",
                },
                title: {
                  display: true,
                  text: `Age Distribution (${year})`,
                },
              },
            },
          });

          const corrChart = new Chart(corrCtx, {
            type: "line",
            data: {
              labels: ["<19", "20-24", "25-29", "30-34", ">35"],
              datasets: [
                {
                  label: `Age-Medal Correlation (${year})`,
                  data: [
                    yearData["less than 19y"] / yearData["Total Medals"],
                    yearData["20-24"] / yearData["Total Medals"],
                    yearData["25-29"] / yearData["Total Medals"],
                    yearData["30-34"] / yearData["Total Medals"],
                    yearData["more than 35y"] / yearData["Total Medals"],
                  ],
                  borderColor: "rgba(220, 20, 60, 0.7)",
                  fill: false,
                },
              ],
            },
            options: {
              responsive: true,
              plugins: {
                legend: {
                  position: "top",
                },
                title: {
                  display: true,
                  text: `Age-Medal Correlation (${year})`,
                },
              },
            },
          });

          this.chartInstances[distId] = distChart;
          this.chartInstances[corrId] = corrChart;
        });
      });
    },
  },
  mounted() {
    this.loadOlympicData();
    this.drawMainGraph("myGraph");
  },
};
</script>

<style scoped>
/* Container */
.expandable-menu {
  position: relative;
  width: 100%;
  height: 100%;
}

/* '+' button style */
.menu-button {
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 2000;
}

.plus-icon {
  font-size: 32px;
  cursor: pointer;
}

.plus-icon:hover {
  transform: scale(1.2);
}

/* graph */
.graph-container {
  width: 160%;
  margin: 50px auto;
  text-align: center;
  z-index: 1;
}

#myGraph {
  width: 100%;
  max-width: 600px;
  height: 400px;
  margin: 0 auto;
}

/* expandable panel */
.fullscreen-panel {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80%;
  height: 80%;
  background-color: #f5f5f5;
  overflow-y: auto;
  padding: 20px;
  z-index: 1000;
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
}

.fullscreen-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

.chart-container {
  position: relative;
  width: 90%;
  margin: 20px auto;
  z-index: 1001;
}

.year-charts {
  margin-bottom: 40px;
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  color: black;
  font-size: 24px;
  cursor: pointer;
}

.close-btn:hover {
  color: #aaa;
}

.panel-content {
  text-align: center;
  width: 100%;
}

.panel-content h1 {
  font-size: 32px;
  margin-bottom: 20px;
}

.chart-container {
  width: 90%;
  height: 40%; /* Adjust height to fit both charts */
  margin: 20px 0;
}
</style>
