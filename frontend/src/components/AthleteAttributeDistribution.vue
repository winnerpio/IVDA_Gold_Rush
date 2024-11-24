<template>
  <div class="layout-container">
    <!-- '+' Button -->
    <div v-if="!isPanelOpen" class="menu-button">
      <button class="plus-icon" @click="toggleFullscreen">+</button>
    </div>

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

    <!-- Main Graph -->
    <div class="graph-container">
      <canvas id="mainGraph"></canvas>
    </div>

    <!-- Expandable Panel -->
    <div v-if="isPanelOpen">
      <div class="fullscreen-overlay" @click="toggleFullscreen"></div>
      <div class="fullscreen-panel">
        <button @click="toggleFullscreen" class="close-btn">×</button>
        <div class="panel-content">
          <h1>{{ dynamicPanelTitle }}</h1>
          <div v-for="data in filteredOlympicData" :key="data.Year" class="year-charts">
            <h2>Year: {{ data.Year }}</h2>
            <div :id="'canvas-container-' + data.Year" class="chart-container">
              <canvas :id="'combinedChart-' + data.Year"></canvas>
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
  name: "AthleteAttributeDistribution",
  props: {
    dateRange: {
      type: Array,
      default: () => [1896, 2023],
    },
  },
  data() {
    return {
      selectedAttribute: "age",
      mainGraphInstance: null,
      olympicData: [],
      chartInstances: {},
      isPanelOpen: false,
    };
  },
  computed: {
    dynamicPanelTitle() {
      const capitalizedAttribute =
        this.selectedAttribute.charAt(0).toUpperCase() +
        this.selectedAttribute.slice(1);
      return `${capitalizedAttribute} Distribution during Selected Years`;
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
    filteredOlympicData() {
      return this.olympicData.filter(
        (data) =>
          data.Year >= this.dateRange[0] && data.Year <= this.dateRange[1]
      );
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
    async updateMainGraph() {
      const { attributeDistribution, medalCount } = this.computeAttributeDistribution();
      const labels = this.attributeGroups;
      const athleteData = labels.map((label) => attributeDistribution[label]);
      const medalData = labels.map((label) => medalCount[label]);

      // Destroy existing chart instance if it exists
      if (this.mainGraphInstance) {
        this.mainGraphInstance.destroy();
        this.mainGraphInstance = null;
      }

      await this.$nextTick(); // Ensure the DOM is updated

      const canvas = document.getElementById("mainGraph");
      if (!canvas) {
        console.error("Canvas element not found!");
        return;
      }

      const ctx = canvas.getContext("2d");
      if (!ctx) {
        console.error("Canvas context is null!");
        return;
      }

      // Create a new chart
      this.mainGraphInstance = new Chart(ctx, {
        type: "bar",
        data: {
          labels: labels,
          datasets: [
            {
              type: "bar",
              label: `${this.selectedAttribute.charAt(0).toUpperCase() + this.selectedAttribute.slice(1)} Distribution`,
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
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: "top" },
            title: {
              display: true,
              text: `${this.selectedAttribute.charAt(0).toUpperCase() + this.selectedAttribute.slice(1)} Distribution and Medal Count`,
            },
          },
          scales: {
            x: {
              title: { display: true, text: `${this.selectedAttribute.charAt(0).toUpperCase() + this.selectedAttribute.slice(1)} Groups` },
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
      });
    },
    async drawOlympicCharts() {
      await this.$nextTick();

      this.filteredOlympicData.forEach((data) => {
        const canvasId = `combinedChart-${data.Year}`;
        const canvasContainer = document.getElementById(`canvas-container-${data.Year}`);

        if (!canvasContainer) {
          console.error(`Canvas container ${canvasId} not found!`);
          return;
        }

        let canvas = document.getElementById(canvasId);
        if (!canvas) {
          canvas = document.createElement("canvas");
          canvas.id = canvasId;
          canvasContainer.appendChild(canvas);
        }

        const ctx = canvas.getContext("2d");
        if (!ctx) {
          console.error("Canvas context is null!");
          return;
        }

        // Destroy existing chart instance if it exists
        if (this.chartInstances[canvasId]) {
          this.chartInstances[canvasId].destroy();
          delete this.chartInstances[canvasId];
        }

        // Create a new chart and store it in chartInstances
        this.chartInstances[canvasId] = new Chart(ctx, {
          type: "bar",
          data: {
            labels: this.attributeGroups,
            datasets: [
              {
                type: "bar",
                label: `Age Distribution (${data.Year})`,
                data: this.attributeGroups.map((group) => data[`${this.selectedAttribute}Groups`][group] || 0),
                backgroundColor: "rgba(100, 149, 237, 0.7)",
                borderColor: "rgba(100, 149, 237, 1)",
                borderWidth: 1,
              },
              {
                type: "line",
                label: `Medals (${data.Year})`,
                data: data.MedalsByGroup[this.selectedAttribute],
                borderColor: "rgba(220, 20, 60, 0.8)",
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
        });
      });
    },
    destroyCharts() {
      // Destroy main graph instance
      if (this.mainGraphInstance) {
        this.mainGraphInstance.destroy();
        this.mainGraphInstance = null;
      }

      // Destroy all Olympic chart instances
      Object.keys(this.chartInstances).forEach((canvasId) => {
        const chart = this.chartInstances[canvasId];
        if (chart) {
          chart.destroy();
        }
        delete this.chartInstances[canvasId];
      });
    },
    async toggleFullscreen() {
      this.isPanelOpen = !this.isPanelOpen;

      if (this.isPanelOpen) {
        this.destroyCharts();
        await this.$nextTick();
        await this.drawOlympicCharts();
      } else {
        this.destroyCharts();
        await this.$nextTick();
        this.updateMainGraph();
      }
    },
  },
  watch: {
    filteredOlympicData: {
      immediate: true,
      async handler() {
        if (!this.isPanelOpen) {
          this.destroyCharts();
          await this.$nextTick();
          this.updateMainGraph();
        }
      },
    },
    selectedAttribute: {
      immediate: true,
      async handler() {
        if (!this.isPanelOpen) {
          this.destroyCharts();
          await this.$nextTick();
          this.updateMainGraph();
        }
      },
    },
  },
  async mounted() {
    this.generateMockData();
    await this.$nextTick();
    this.updateMainGraph();
  },
};
</script>

<style scoped>
.layout-container {
  top: 0;
  left: 0;
  display: flex;
  flex-direction: column;
  width: 100%;
  align-items: center;
  margin: 0;
  padding: 0;
  z-index: 1000;
}

.menu-button {
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 2000;
}

.plus-icon {
  font-size: 32px;
  cursor: pointer;
  background: none;
  border: none;
}

.plus-icon:hover {
  transform: scale(1.2);
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

.graph-container {
  width: 100%;
  max-width: 1200px;
  margin-bottom: 20px;
}

#mainGraph {
  width: 100%;
  height: auto;
  display: block;
}

.fullscreen-panel {
  position: fixed;
  overflow-y: auto;
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
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
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
  display: flex;
  justify-content: center;
  align-items: center;
  width: 90%;
  height: 400px;
  margin: 20px 0;
}

.year-charts {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 40px;
}

canvas {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: contain;
}

.close-btn {
  position: fixed;
  top: 20px;
  left: 20px;
  background: none;
  border: none;
  color: black;
  font-size: 24px;
  cursor: pointer;
  z-index: 2000;
}

.close-btn:hover {
  color: #aaa;
}

.panel-content {
  text-align: center;
  width: 100%;
}

.panel-content h1 {
  font-size: 20px;
  margin-bottom: 10px;
}

.panel-content h2 {
  font-size: 18px;
}

.chart-container {
  width: 90%;
  height: 40%;
  margin: 20px 0;
}
</style>
