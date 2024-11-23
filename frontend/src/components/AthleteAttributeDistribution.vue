<template>
  <div class="layout-container">
    <!-- Attribute Selection -->
    <div class="attribute-selection">
      <label class="custom-radio">
        <input
          type="radio"
          value="age"
          v-model="selectedAttribute"
        />
        <span class="radio-btn"></span>
        Age
      </label>
      <label class="custom-radio">
        <input
          type="radio"
          value="weight"
          v-model="selectedAttribute"
        />
        <span class="radio-btn"></span>
        Weight
      </label>
      <label class="custom-radio">
        <input
          type="radio"
          value="height"
          v-model="selectedAttribute"
        />
        <span class="radio-btn"></span>
        Height
      </label>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Attribute Distribution and Medal Count -->
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
            <div
              class="chart-container"
              :id="'canvas-container-' + data.Year"
            >
              <!-- Canvas will be managed by Vue -->
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
      default: () => [1896, 2023],
    },
  },
  data() {
    return {
      selectedAttribute: "age", // Default attribute
      mainGraphInstance: null,
      olympicData: [],
      chartInstances: {},
    };
  },
  computed: {
    filteredOlympicData() {
      return this.olympicData.filter(
        (data) =>
          data.Year >= this.dateRange[0] && data.Year <= this.dateRange[1]
      );
    },
    attributeGroups() {
      if (this.selectedAttribute === "age") {
        return ["<19", "20-24", "25-29", "30-34", ">35"];
      } else if (this.selectedAttribute === "weight") {
        return ["<60kg", "60-70kg", "70-80kg", "80-90kg", ">90kg"];
      } else if (this.selectedAttribute === "height") {
        return ["<160cm", "160-170cm", "170-180cm", "180-190cm", ">190cm"];
      }
      return [];
    },
  },
  methods: {
    generateMockData() {
      const startYear = 1896;
      const endYear = 2020;
      const data = [];

      for (let year = startYear; year <= endYear; year += 4) {
        const ageGroups = {
          "<19": this.randomInt(10, 30),
          "20-24": this.randomInt(20, 50),
          "25-29": this.randomInt(15, 40),
          "30-34": this.randomInt(10, 30),
          ">35": this.randomInt(5, 25),
        };

        const weightGroups = {
          "<60kg": this.randomInt(15, 35),
          "60-70kg": this.randomInt(20, 50),
          "70-80kg": this.randomInt(15, 40),
          "80-90kg": this.randomInt(10, 30),
          ">90kg": this.randomInt(5, 25),
        };

        const heightGroups = {
          "<160cm": this.randomInt(10, 30),
          "160-170cm": this.randomInt(20, 50),
          "170-180cm": this.randomInt(15, 40),
          "180-190cm": this.randomInt(10, 30),
          ">190cm": this.randomInt(5, 25),
        };

        const medalsByAge = Object.values(ageGroups).map(() =>
          this.randomInt(10, 100)
        );
        const medalsByWeight = Object.values(weightGroups).map(() =>
          this.randomInt(10, 100)
        );
        const medalsByHeight = Object.values(heightGroups).map(() =>
          this.randomInt(10, 100)
        );

        data.push({
          Year: year,
          ageGroups: ageGroups,
          weightGroups: weightGroups,
          heightGroups: heightGroups,
          MedalsByGroup: {
            age: medalsByAge,
            weight: medalsByWeight,
            height: medalsByHeight,
          },
        });
      }

      this.olympicData = data;
    },
    randomInt(min, max) {
      return Math.floor(Math.random() * (max - min + 1)) + min;
    },
    computeAttributeDistribution() {
      const attributeGroups = this.attributeGroups;
      const attributeDistribution = {};
      const medalCount = {};
      attributeGroups.forEach((group) => {
        attributeDistribution[group] = 0;
        medalCount[group] = 0;
      });
      this.filteredOlympicData.forEach((data) => {
        const groupData = data[`${this.selectedAttribute}Groups`];
        const medals = data.MedalsByGroup[this.selectedAttribute];
        attributeGroups.forEach((group, index) => {
          attributeDistribution[group] += groupData[group] || 0;
          medalCount[group] += medals[index] || 0;
        });
      });
      return { attributeDistribution, medalCount };
    },
    updateMainGraph() {
      const { attributeDistribution, medalCount } =
        this.computeAttributeDistribution();
      const labels = this.attributeGroups;
      const athleteData = labels.map((label) => attributeDistribution[label]);
      const medalData = labels.map((label) => medalCount[label]);

      if (this.mainGraphInstance) {
        this.mainGraphInstance.destroy();
        // Reset the canvas
        const mainCanvas = document.getElementById("mainGraph");
        if (mainCanvas) {
          const parent = mainCanvas.parentNode;
          parent.removeChild(mainCanvas);
          const newCanvas = document.createElement("canvas");
          newCanvas.id = "mainGraph";
          parent.appendChild(newCanvas);
        }
      }

      this.$nextTick(() => {
        const canvas = document.getElementById("mainGraph");

        if (!canvas) {
          console.error("Canvas element not found!");
          return;
        }

        const ctx = canvas.getContext("2d");

        const histogramData = {
          labels: labels,
          datasets: [
            {
              type: "bar",
              label: `${
                this.selectedAttribute.charAt(0).toUpperCase() +
                this.selectedAttribute.slice(1)
              } Distribution`,
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
              title: {
                display: true,
                text: `${
                  this.selectedAttribute.charAt(0).toUpperCase() +
                  this.selectedAttribute.slice(1)
                } Distribution and Medal Count`,
              },
            },
            scales: {
              x: {
                title: {
                  display: true,
                  text: `${
                    this.selectedAttribute.charAt(0).toUpperCase() +
                    this.selectedAttribute.slice(1)
                  } Groups`,
                },
              },
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
        this.filteredOlympicData.forEach((data) => {
          const canvasId = `combinedChart-${data.Year}`;
          const canvasContainer = document.getElementById(
            `canvas-container-${data.Year}`
          );

          // Reset the canvas
          if (canvasContainer) {
            canvasContainer.innerHTML = `<canvas id="${canvasId}"></canvas>`;
          }

          const canvas = document.getElementById(canvasId);
          if (!canvas) return;

          const ctx = canvas.getContext("2d");

          const attributeGroups = this.attributeGroups;
          const groupData = data[`${this.selectedAttribute}Groups`];
          const medals = data.MedalsByGroup[this.selectedAttribute];

          const chartInstance = new Chart(ctx, {
            type: "bar",
            data: {
              labels: attributeGroups,
              datasets: [
                {
                  type: "bar",
                  label: `Number of Athletes (${data.Year})`,
                  data: attributeGroups.map(
                    (group) => groupData[group] || 0
                  ),
                  backgroundColor: "rgba(75, 192, 192, 0.7)",
                  borderColor: "rgba(75, 192, 192, 1)",
                  borderWidth: 1,
                },
                {
                  type: "line",
                  label: `Medals (${data.Year})`,
                  data: medals,
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
                title: {
                  display: true,
                  text: `Combined Chart (${data.Year})`,
                },
              },
              scales: {
                x: {
                  title: {
                    display: true,
                    text: `${
                      this.selectedAttribute.charAt(0).toUpperCase() +
                      this.selectedAttribute.slice(1)
                    } Groups`,
                  },
                },
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

          // Store the chart instance for later destruction
          this.chartInstances[canvasId] = chartInstance;
        });
      });
    },
    destroyCharts() {
      // Destroy main graph instance
      if (this.mainGraphInstance) {
        this.mainGraphInstance.destroy();
        // Reset the canvas
        const mainCanvas = document.getElementById("mainGraph");
        if (mainCanvas) {
          const parent = mainCanvas.parentNode;
          parent.removeChild(mainCanvas);
          const newCanvas = document.createElement("canvas");
          newCanvas.id = "mainGraph";
          parent.appendChild(newCanvas);
        }
        this.mainGraphInstance = null;
      }

      // Destroy existing chart instances
      Object.entries(this.chartInstances).forEach(([canvasId, chart]) => {
        chart.destroy();
        // Reset the canvas
        const canvas = document.getElementById(canvasId);
        if (canvas) {
          const parent = canvas.parentNode;
          parent.removeChild(canvas);
          const newCanvas = document.createElement("canvas");
          newCanvas.id = canvasId;
          parent.appendChild(newCanvas);
        }
      });
      this.chartInstances = {};
    },
  },
  watch: {
    dateRange: {
      immediate: true,
      handler() {
        this.destroyCharts();
        this.$nextTick(() => {
          this.updateMainGraph();
          this.drawOlympicCharts();
        });
      },
    },
    selectedAttribute: {
      immediate: true,
      handler() {
        this.destroyCharts();
        this.$nextTick(() => {
          this.updateMainGraph();
          this.drawOlympicCharts();
        });
      },
    },
  },
  mounted() {
    this.generateMockData();
  },
};
</script>

<style scoped>
.layout-container {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.attribute-selection {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.attribute-selection label {
  margin-right: 15px;
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
