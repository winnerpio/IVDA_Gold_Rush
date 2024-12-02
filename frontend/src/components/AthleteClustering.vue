<template>
  <div ref="athleteClusters" style="width: 100%; height: 500px;">
    <v-container>
      <v-card outlined class="pa-5" fill-height>
        <v-container fluid>
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
  </div>
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
      attributes: ["Age", "Height", "Weight", "BMI", "H2W"],
      chart: null,
      series: null,
      colors: ["#4bc0c0", "#ff6384", "#36a2eb"],
      sports: [],
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
      chartInitialized: false,
    };
  },
  watch: {
    attributeSelection: {
      handler(newVal) {
        if (newVal) {
          if (!this.chartInitialized) {
            this.initChart();
            this.chartInitialized = true;
          }
          this.updateChartData();
        }
      },
      deep: true,
      immediate: true,
    },
    userDataForm: {
      handler(newUserData) {
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
      type: Object,
      required: true,
    },
    attributeSelection: {
      type: Object,
      required: true,
    },
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
        this.$emit('update-sports', this.sports);
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
            x_axis_variable: this.attributeSelection.xAttribute?.toLowerCase(),
            y_axis_variable: this.attributeSelection.yAttribute?.toLowerCase(),
            sport1: this.attributeSelection.selectedSport1,
            sport2: this.attributeSelection.selectedSport2,
            sport3: this.attributeSelection.selectedSport3,
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
      if (!this.attributeSelection) {
        console.warn('attributeSelection is undefined in updateChartData');
        return;
      }

      this.clearChart();
      this.updateAxisLabels();

      const {
        xAttribute,
        yAttribute,
        selectedSport1,
        selectedSport2,
        selectedSport3,
      } = this.attributeSelection;

      if (!xAttribute || !yAttribute || !selectedSport1 || !selectedSport2 || !selectedSport3) {
        return;
      }

      const data = await this.fetchData();
      if (data && data.length > 0 && this.series) {
        this.series.data.setAll(data);
      }
    },
    validateInputs() {
      if (!this.attributeSelection) {
        console.warn('attributeSelection is undefined in validateInputs');
        return false;
      }

      const missingFields = [];

      Object.entries(this.userData).forEach(([key, value]) => {
        if (value === null || value === undefined) {
          missingFields.push(`User Data: ${key}`);
        }
      });

      const {
        xAttribute,
        yAttribute,
        selectedSport1,
        selectedSport2,
        selectedSport3,
      } = this.attributeSelection;

      if (!xAttribute) missingFields.push("X-Axis Attribute");
      if (!yAttribute) missingFields.push("Y-Axis Attribute");
      if (!selectedSport1) missingFields.push("Selected Sport 1");
      if (!selectedSport2) missingFields.push("Selected Sport 2");
      if (!selectedSport3) missingFields.push("Selected Sport 3");

      if (missingFields.length > 0) {
        console.warn("Missing inputs:", missingFields.join(", "));
        return false;
      }

      return true;
    },
    initChart() {
      if (!this.$refs.athleteClusters) {
        console.warn('attributeSelection is undefined in initChart');
        return;
      }

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

      const xAttrLabel = this.attributeSelection?.xAttribute || "X-Axis";
      this.xAxisLabel = am5.Label.new(this.root, {
        text: xAttrLabel,
        x: am5.p50,
        centerX: am5.p50,
      });
      xAxis.children.moveValue(this.xAxisLabel, xAxis.children.length - 1);

      const yAttrLabel = this.attributeSelection?.yAttribute || "Y-Axis";
      this.yAxisLabel = am5.Label.new(this.root, {
        rotation: -90,
        text: yAttrLabel,
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

        const xAttr = this.attributeSelection?.xAttribute || "X";
        const yAttr = this.attributeSelection?.yAttribute || "Y";

        const tooltipText = `[bold]Cluster[/]: {cluster}\n[bold]${xAttr}[/]: {valueX}\n[bold]${yAttr}[/]: {valueY}\n[bold]Athlete[/]: {name}\n[bold]Country[/]: {country}\n[bold]Sport[/]: {sport}\n[bold]Event[/]: {event}`;

        if (name === "User") {
          return am5.Bullet.new(root, {
            sprite: am5.Rectangle.new(root, {
              width: 10,
              height: 10,
              fill: color,
              tooltipText,
            }),
          });
        } else {
          return am5.Bullet.new(root, {
            sprite: am5.Circle.new(root, {
              fill: color,
              radius: 6,
              tooltipText,
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
      if (this.xAxisLabel && this.attributeSelection?.xAttribute) {
        this.xAxisLabel.set("text", this.attributeSelection.xAttribute);
      }
      if (this.yAxisLabel && this.attributeSelection?.yAttribute) {
        this.yAxisLabel.set("text", this.attributeSelection.yAttribute);
      }
    },
  },
  mounted() {
    this.$nextTick(() => {
      if (this.attributeSelection) {
        this.initChart();
        this.chartInitialized = true;
      } else {
        console.warn('attributeSelection is undefined in mounted hook');
      }
    });
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
