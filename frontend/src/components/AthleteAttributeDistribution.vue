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
      <label class="custom-radio">
        <input
          type="radio"
          value="bmi"
          v-model="selectedAttribute"
        />
        <span class="radio-btn"></span>
        BMI
      </label>
      <label class="custom-radio">
        <input
          type="radio"
          value="h2w"
          v-model="selectedAttribute"
        />
        <span class="radio-btn"></span>
        Height-to-Weight Ratio
      </label>
    </div>

    <!-- Main Graph -->
    <div v-if="!isPanelOpen" class="graph-container">
      <canvas id="mainGraph"></canvas>
    </div>

    <!-- Detailed Panel -->
    <div v-if="isPanelOpen" class="fullscreen-panel">
      <button class="close-btn" @click="toggleFullscreen">X</button>
      <div class="panel-content">
        <h1>{{ dynamicPanelTitle }}</h1>
        <div class="year-charts">
          <div
            class="chart-container"
            v-for="(year, index) in sortedYears"
            :key="index"
          >
            <h2>Year {{ year }}</h2>
            <canvas :id="`combinedChart-${year}`"></canvas>
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
    distributionData: {
      type: Object,
      required: false,
      default: () => ({}),
    },
    detailedDistributionData: {
      type: Object,
      required: false,
      default: () => ({}),
    },
  },
  data() {
    return {
      selectedAttribute: "age",
      mainGraphInstance: null,
      chartInstances: {},
      isPanelOpen: false,
    };
  },
  computed: {
    hasData() {
      return this.attributeGroups.length > 0;
    },
    dynamicPanelTitle() {
      const capitalizedAttribute =
        this.selectedAttribute.charAt(0).toUpperCase() +
        this.selectedAttribute.slice(1);
      return `${capitalizedAttribute} Distribution during Selected Years`;
    },
    attributeGroups() {
      return Object.keys(this.distributionData || {});
    },
  },
  methods: {
    async updateMainGraph() {
      console.log("Updating main graph with data:", this.distributionData);
      const { athleteData, medalData } = this.computeAttributeDistribution();
      const labels = this.attributeGroups;

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

      // Loop over the years in detailedDistributionData
      Object.keys(this.detailedDistributionData).forEach((year) => {
        const dataForYear = this.detailedDistributionData[year];

        const canvasId = `combinedChart-${year}`;
        const canvasContainerId = `canvas-container-${year}`;
        let canvasContainer = document.getElementById(canvasContainerId);

        // Create a container if it doesn't exist
        if (!canvasContainer) {
          canvasContainer = document.createElement('div');
          canvasContainer.id = canvasContainerId;
          canvasContainer.classList.add('chart-container');
          document.querySelector('.year-charts').appendChild(canvasContainer);
        }

        // Create canvas
        let canvas = document.getElementById(canvasId);
        if (!canvas) {
          canvas = document.createElement('canvas');
          canvas.id = canvasId;
          canvasContainer.appendChild(canvas);
        }

        canvas.removeAttribute('width');
        canvas.removeAttribute('height');

        canvas.style.width = '';
        canvas.style.height = '';

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

        const labels = Object.keys(dataForYear);

        const athleteData = labels.map(label => dataForYear[label].athlete_count || 0);
        const medalData = labels.map(label => dataForYear[label].medal_count || 0);

        // Create a new chart and store it in chartInstances
        this.chartInstances[canvasId] = new Chart(ctx, {
          type: "bar",
          data: {
            labels: labels,
            datasets: [
              {
                type: "bar",
                label: `${this.selectedAttribute.charAt(0).toUpperCase() + this.selectedAttribute.slice(1)} Distribution (${year})`,
                data: athleteData,
                backgroundColor: "rgba(100, 149, 237, 0.7)",
                borderColor: "rgba(100, 149, 237, 1)",
                borderWidth: 1,
              },
              {
                type: "line",
                label: `Medals (${year})`,
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
              title: { display: true, text: `${this.selectedAttribute.charAt(0).toUpperCase() + this.selectedAttribute.slice(1)} Distribution and Medal Count for ${year}` },
            },
            resizeDelay: 0,
            scales: {
              x: { title: { display: true, text: `${this.selectedAttribute.charAt(0).toUpperCase() + this.selectedAttribute.slice(1)} Groups` } },
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
            resize: false,
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
        this.$emit('fetch-detailed-distribution'); // Emit event to parent to fetch data
      } else {
        this.destroyCharts();
        await this.$nextTick();
        this.updateMainGraph();
      }
    },
    computeAttributeDistribution() {
      const attributeGroups = this.attributeGroups;
      const athleteData = [];
      const medalData = [];

      attributeGroups.forEach((group) => {
        const groupData = this.distributionData[group];
        athleteData.push(groupData.athlete_count || 0);
        medalData.push(groupData.medal_count || 0);
      });

      return { athleteData, medalData };
    },
  },
  watch: {
    selectedAttribute: {
    immediate: true,
      handler(newVal) {
        // Emit the selected attribute to the parent component
        this.$emit('update:distVariable', newVal);

        // If panel is open, fetch detailed distribution
        if (this.isPanelOpen) {
          this.$emit('fetch-detailed-distribution');
        }
      },
    },
    distributionData: {
      immediate: true,
      handler() {
        if (this.hasData) {
          this.destroyCharts();
          this.updateMainGraph();
        } else {
          this.destroyCharts();
        }
      },
    },
    detailedDistributionData: {
      immediate: false,
      handler() {
        if (this.isPanelOpen && this.detailedDistributionData) {
          this.destroyCharts();
          this.drawOlympicCharts();
        }
      },
    },
  },
};
</script>

<style>
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
  padding: 20px;
  z-index: 1000;
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
}

.chart-container {
  width: 100%;
  max-width: 800px;
  margin-bottom: 20px;
  height: 500px;
}

canvas {
  width: 100% !important;
  height: 100% !important;
  display: block;
}

.year-charts {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.panel-content {
  width: 100%;
  height: 100%;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.close-btn {
  position: fixed;
  top: 20px;
  right: 20px;
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

.panel-content h1 {
  font-size: 20px;
  margin-bottom: 10px;
}

.panel-content h2 {
  font-size: 18px;
}
</style>
