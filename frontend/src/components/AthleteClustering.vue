<template>
  <v-container>
    <v-card outlined class="pa-5" fill-height>
      <v-container fluid>
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
        <v-row>
          <v-col cols="12" md="4">
            <v-select
                :items="sports"
                label="Sport 1"
                v-model="selectedSport1"
                outlined
            ></v-select>
          </v-col>
          <v-col cols="12" md="4">
            <v-select
                :items="sports"
                label="Sport 2"
                v-model="selectedSport2"
                outlined
            ></v-select>
          </v-col>
          <v-col cols="12" md="4">
            <v-select
                :items="sports"
                label="Sport 3"
                v-model="selectedSport3"
                outlined
            ></v-select>
          </v-col>
        </v-row>
        <v-row class="chart-row" justify="center" align="center" style="position: relative;">
          <!-- Chart Container -->
          <v-col cols="12">
            <div id="athlete-clusters" style="width: 100%; height: 500px;"></div>
          </v-col>
          <!-- Loading Spinner -->
          <v-col
              cols="12"
              v-if="loading"
              class="d-flex justify-center align-center"
              style="position: absolute; top: 0; bottom: 0; left: 0; right: 0; background: rgba(255, 255, 255, 0.8); z-index: 10;"
          >
            <!-- Loading spinner or content -->
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
          </v-col>
        </v-row>
      </v-container>
    </v-card>
  </v-container>
</template>




<script>
import * as am5 from "@amcharts/amcharts5";
import * as am5xy from "@amcharts/amcharts5/xy";
import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";
import axios from "axios";

export default {
  name: "AthleteClustering",
  data() {
    return {
      xAttribute: null,
      yAttribute: null,
      attributes: ["Age", "Height", "Weight", "BMI", "H2W"],
      chart: null,
      series: null,
      colors: ["#4bc0c0", "#ff6384", "#36a2eb"],
      sports: [],
      selectedSport1: null,
      selectedSport2: null,
      selectedSport3: null,
      loading: false,
      userData: {
        sex:'',
        height: null,
        weight: null,
        age: null,
        bmi: null,
        h2w: null,
      },
      xAxisLabel: null,
      yAxisLabel: null,
    };
  },
  watch: {
    yearRange: {
      handler(newRange) {
        this.selectedSport1 = null;
        this.selectedSport2 = null;
        this.selectedSport3 = null;
        this.fetchSports(newRange);
      },
      immediate: true,
    },
    xAttribute: "updateChartData",
    yAttribute: "updateChartData",
    selectedSport1: "updateChartData",
    selectedSport2: "updateChartData",
    selectedSport3: "updateChartData",
    userDataForm: {
      handler(newUserData) {
        console.log(newUserData);
        this.userData = { ...newUserData };
        this.updateChartData();
      },
      deep: true,
    },
  },
  props: {
    yearRange: {
      type: Array,
      required: true,
      default: () => [1896, 2022],
    },
    userDataForm: {
      type: [Object, null],
      required: true,
    }
  },
  methods: {
    async fetchSports(range) {
      this.clearChart();
      try {
        const response = await axios.get("http://127.0.0.1:5000/SportEventList", {
          params: {
            year_lower: range[0],
            year_upper: range[1],
          },
        });
        this.sports = Object.keys(response.data);
      } catch (error) {
        console.error("Error fetching sports data:", error.message);
      }
    },
    async fetchData() {
      if (!this.validateInputs()) {
        console.warn("Missing parameters for fetching data.");
        return;
      }

      this.loading = true;

      try {
        const response = await axios.get("http://127.0.0.1:5000/GetClustering", {
          params: {
            year_lower: this.yearRange[0],
            year_upper: this.yearRange[1],
            x_axis_variable: this.xAttribute?.toLowerCase(),
            y_axis_variable: this.yAttribute?.toLowerCase(),
            sport1: this.selectedSport1,
            sport2: this.selectedSport2,
            sport3: this.selectedSport3,
            user_age: this.userData.age,
            user_bmi: this.userData.bmi,
            user_height: this.userData.height,
            user_weight: this.userData.weight,
            user_h2w: this.userData.h2w,
          },
        });
        return response.data.map((athlete) => ({
          x: athlete.x_axis_value,
          y: athlete.y_axis_value,
          cluster: athlete.cluster,
          name: athlete.name,
          country: athlete.country,
          sport: athlete.sport,
          event: athlete.event,
        }));
      } catch (error) {
        console.error("Error fetching clustering data:", error.message);
        return [];
      } finally {
        this.loading = false;
      }
    },
    async updateChartData() {
      this.clearChart();
      this.updateAxisLabels();
      if (!this.xAttribute || !this.yAttribute || !this.selectedSport1) {
        return;
      }

      const data = await this.fetchData();
      if (data){
        if (data.length > 0 && this.series) {
          this.series.data.setAll(data);
        }
      }
    },
    validateInputs() {
      const missingFields = [];

      Object.entries(this.userData).forEach(([key, value]) => {
        if (value === null || value === undefined) {
          missingFields.push(`User Data: ${key}`);
        }
      });

      if (!this.xAttribute) missingFields.push("X-Axis Attribute");
      if (!this.yAttribute) missingFields.push("Y-Axis Attribute");
      if (!this.selectedSport1) missingFields.push("Selected Sport 1");
      if (!this.selectedSport2) missingFields.push("Selected Sport 2");
      if (!this.selectedSport3) missingFields.push("Selected Sport 3");

      if (missingFields.length > 0) {
        console.warn("Missing inputs:", missingFields.join(", "));
        return false;
      }

      return true;
    },
    initChart() {
      this.root = am5.Root.new("athlete-clusters");
      this.root.setThemes([am5themes_Animated.new(this.root)]);

      const chart = this.root.container.children.push(
          am5xy.XYChart.new(this.root, {
            panX: true,
            panY: true,
            wheelX: "zoomX",
            wheelY: "zoomY",
          })
      );

      chart.set("scrollbarX", am5.Scrollbar.new(this.root, { orientation: "horizontal" }));
      chart.set("scrollbarY", am5.Scrollbar.new(this.root, { orientation: "vertical" }));

      const xAxis = chart.xAxes.push(
          am5xy.ValueAxis.new(this.root, {
            renderer: am5xy.AxisRendererX.new(this.root, {}),
            tooltip: am5.Tooltip.new(this.root, {}),
          })
      );

      const yAxis = chart.yAxes.push(
          am5xy.ValueAxis.new(this.root, {
            renderer: am5xy.AxisRendererY.new(this.root, {}),
            tooltip: am5.Tooltip.new(this.root, {}),
          })
      );

      this.xAxisLabel = am5.Label.new(this.root, {
        text: this.xAttribute || "X-Axis",
        x: am5.p50,
        centerX: am5.p50,
      });
      xAxis.children.moveValue(this.xAxisLabel, xAxis.children.length - 1);

      this.yAxisLabel = am5.Label.new(this.root, {
        rotation: -90,
        text: this.yAttribute || "Y-Axis",
        y: am5.p50,
        centerX: am5.p50,
      });
      yAxis.children.moveValue(this.yAxisLabel, 0);

      const series = chart.series.push(
          am5xy.LineSeries.new(this.root, {
            xAxis: xAxis,
            yAxis: yAxis,
            valueXField: "x",
            valueYField: "y",
            tooltip: am5.Tooltip.new(this.root, {
              labelText: "Cluster: {cluster}\nX: {valueX}\nY: {valueY}",
            }),
          })
      );

      series.bullets.push((root, series, dataItem) => {
        const cluster = dataItem.dataContext.cluster;
        const name = dataItem.dataContext.name;
        const color = am5.color(this.colors[cluster]);

        if (name === "User") {
          return am5.Bullet.new(root, {
            sprite: am5.Rectangle.new(root, {
              width: 10,
              height: 10,
              fill: color,
              tooltipText: `[bold]Cluster[/]: {cluster}\n[bold]${this.xAttribute || "X"}[/]: {valueX}\n[bold]${this.yAttribute || "Y"}[/]: {valueY}\n[bold]Athlete[/]: {name}\n[bold]Country[/]: {country}\n[bold]Sport[/]: {sport}\n[bold]Event[/]: {event}`,
            }),
          });
        } else {
          return am5.Bullet.new(root, {
            sprite: am5.Circle.new(root, {
              fill: color,
              radius: 6,
              tooltipText: `[bold]Cluster[/]: {cluster}\n[bold]${this.xAttribute || "X"}[/]: {valueX}\n[bold]${this.yAttribute || "Y"}[/]: {valueY}\n[bold]Athlete[/]: {name}\n[bold]Country[/]: {country}\n[bold]Sport[/]: {sport}\n[bold]Event[/]: {event}`,
            }),
          });
        }
      });


      series.strokes.template.setAll({ visible: false });

      this.chart = chart;
      this.series = series;

      this.updateChartData();
    },
    clearChart() {
      if (this.series && this.series.data) {
        this.series.data.setAll([]);
      }
    },
    updateAxisLabels() {
      if (this.xAxisLabel && this.xAttribute) {
        this.xAxisLabel.set("text", this.xAttribute);
      }
      if (this.yAxisLabel && this.yAttribute) {
        this.yAxisLabel.set("text", this.yAttribute);
      }
    },
  },
  mounted() {
    this.initChart();
  },
  beforeUnmount() {
    if (this.root) {
      this.root.dispose();
    }
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

</style>