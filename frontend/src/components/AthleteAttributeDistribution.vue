<template>
  <div class="layout-container" style="width: 100%; height: 40vh;">
    <div>
      <h2>{{ selectedCountry.name }} Athlete Attribute Distribution</h2>
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
    <div class="graph-container">
      <canvas id="mainGraph" ref="mainGraph"></canvas>
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
    selectedCountry: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      selectedAttribute: "age",
      mainGraphInstance: null,
      isMounted: false,
    };
  },
  computed: {
    hasData() {
      return this.attributeGroups.length > 0;
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

      const canvas = this.$refs.mainGraph;
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
    destroyCharts() {
      // Destroy main graph instance
      if (this.mainGraphInstance) {
        this.mainGraphInstance.destroy();
        this.mainGraphInstance = null;
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
      },
    },
    distributionData: {
      immediate: true,
      handler() {
        if (!this.isMounted) return;
        if (this.hasData) {
          this.destroyCharts();
          this.updateMainGraph();
        } else {
          this.destroyCharts();
        }
      },
    },
  },
  mounted() {
    this.isMounted = true;
  },
  beforeUnmount() {
    this.isMounted = false;
    this.destroyCharts(); // Clean up the chart instance
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
</style>