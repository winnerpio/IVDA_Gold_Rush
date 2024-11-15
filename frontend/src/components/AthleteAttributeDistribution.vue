<template>
  <v-container>
    <!-- Attribute Selection Card -->
    <v-card outlined class="mb-4">
      <v-card-title>Select Attribute for Correlation</v-card-title>
      <v-card-text>
        <v-radio-group v-model="internalSelectedAttribute" @change="updateCorrelationData" inline>
          <v-radio label="Age" value="Age" />
          <v-radio label="Weight" value="Weight" />
          <v-radio label="Height" value="Height" />
        </v-radio-group>
      </v-card-text>
    </v-card>

    <!-- Charts Row -->
    <v-row>
      <v-col cols="12" md="6">
        <v-card outlined>
          <v-card-title>{{ internalSelectedAttribute }} Distribution in {{ internalSelectedSport }}</v-card-title>
          <v-card-text class="chart-container">
            <Bar :data="distributionData" :options="chartOptions" />
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card outlined>
          <v-card-title>Correlation of {{ internalSelectedAttribute }} and Medal Count in {{ internalSelectedSport }}</v-card-title>
          <v-card-text class="chart-container">
            <Line :data="correlationData" :options="chartOptions" />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { Bar, Line } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  LineElement,
  PointElement,
} from "chart.js";

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, LineElement, PointElement);

export default {
  name: "AthleteAttributeDistribution",
  components: { Bar, Line },

  props: {
    userDataForm: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      internalSelectedSport: this.selectedSport,
      internalSelectedAttribute: 'Age',
      distributionData: {
        labels: ["140-150", "150-160", "160-170", "170-180", "180-190"],
        datasets: [
          {
            data: [15, 25, 40, 30, 10],
            backgroundColor: "#42A5F5",
            borderWidth: 1,
            barPercentage: 1,
            categoryPercentage: 1,
            borderRadius: 5,
          },
        ],
      },
      correlationData: {
        labels: ["150", "160", "170", "180", "190"],
        datasets: [
          {
            label: "Height vs. Weight Correlation",
            borderColor: "#66BB6A",
            data: [60, 65, 70, 75, 80],
            fill: false,
            tension: 0.4,
          },
        ],
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
      },
    };
  },

  methods: {
    updateCorrelationData() {
      console.log("Correlation data updated for attribute:", this.internalSelectedAttribute);
      // Placeholder logic for updating correlation data based on selected attribute
    },
  },

  watch: {
    internalSelectedAttribute() {
      this.updateCorrelationData();
    },
    userDataForm: {
      handler(newInformation){
        console.log("This is in Athlete Attribute", newInformation);
        this.internalSelectedSport = newInformation.sport;
        this.updateCorrelationData();
      },
      deep: true,
    },
  },

  mounted() {
    this.updateCorrelationData();
  },
};
</script>

<style scoped>
.chart-container {
  height: 400px;
}
.mb-4 {
  margin-bottom: 16px;
}
</style>
