<template>
  <v-container>
    <v-card outlined class="pa-5" fill-height>
      <v-card-title class="headline">
        {{ xAxis }} vs {{ yAxis }} Outlier Detection
      </v-card-title>
      <v-card-text>
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
            <div id="outlier-identification" style="width: 100%; height: 500px;"></div>
          </v-row>
        </v-container>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import * as am5 from "@amcharts/amcharts5";
import * as am5xy from "@amcharts/amcharts5/xy";
import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";

export default {
  name: "OutlierIdentification",
  data() {
    return {
      xAxis: null,
      yAxis: null,
      selectedSport: null,
      attributes: ["Attribute 1", "Attribute 2", "Attribute 3"],
      sports: ["Swimming", "Running", "Cycling"],
      chart: null,
      series: null,
      apiData: [],
    };
  },
  watch: {
    selectedSport(newSport) {
      this.updateChartData(newSport);
    },
  },
  mounted() {
    this.initChart();
    this.updateChartData(this.selectedSport);
  },
  beforeUnmount() {
    if (this.root) {
      this.root.dispose();
    }
  },
  methods: {
    initChart() {
      this.root = am5.Root.new("outlier-identification");
      this.root.setThemes([am5themes_Animated.new(this.root)]);

      const chart = this.root.container.children.push(
          am5xy.XYChart.new(this.root, {
            panX: true,
            panY: true,
            wheelY: "zoomXY",
            pinchZoomX: true,
            pinchZoomY: true,
          })
      );

      const xAxis = chart.xAxes.push(
          am5xy.ValueAxis.new(this.root, {
            renderer: am5xy.AxisRendererX.new(this.root, {}),
            // tooltip: am5.Tooltip.new(this.root, {}),
          })
      );

      const yAxis = chart.yAxes.push(
          am5xy.ValueAxis.new(this.root, {
            renderer: am5xy.AxisRendererY.new(this.root, {}),
            // tooltip: am5.Tooltip.new(this.root, {}),
          })
      );

      this.series = chart.series.push(
          am5xy.LineSeries.new(this.root, {
            xAxis: xAxis,
            yAxis: yAxis,
            valueXField: "ax",
            valueYField: "ay",
            tooltip: am5.Tooltip.new(this.root, {
              labelText: "x: {valueX}, y: {valueY}, medal: {medal}",
            }),
          })
      );

      this.series.bullets.push((root, series, dataItem) => {
        const medal = dataItem.dataContext.medal;
        let fill;

        if (medal === "gold") fill = am5.color(0xffd700); // Gold
        else if (medal === "silver") fill = am5.color(0xc0c0c0); // Silver
        else if (medal === "bronze") fill = am5.color(0xcd7f32); // Bronze
        else fill = am5.color(0x76bedf); // No medal (black)

        return am5.Bullet.new(root, {
          sprite: am5.Circle.new(root, {
            fill: fill,
            radius: 6,
            tooltipText: "x: {valueX}, y: {valueY}, medal: {medal}", // Tooltip text
          }),
        });
      });

      this.series.strokes.template.setAll({
        visible: false, // Hides the line connecting the points
      });

      // chart.set(
      //     "cursor",
      //     am5xy.XYCursor.new(this.root, {
      //       xAxis: xAxis,
      //       yAxis: yAxis,
      //     })
      // );

      chart.set(
          "scrollbarX",
          am5.Scrollbar.new(this.root, { orientation: "horizontal" })
      );
      chart.set(
          "scrollbarY",
          am5.Scrollbar.new(this.root, { orientation: "vertical" })
      );
    },
    async fetchData(sport) {
      const allData = [
        { "ax": 8.22, "ay": 2.10, "medal": "silver", "sport": "Swimming" },
        { "ax": 8.75, "ay": 1.29, "medal": "none", "sport": "Swimming" },
        { "ax": 5.43, "ay": 0.98, "medal": "gold", "sport": "Swimming" },
        { "ax": 6.99, "ay": 2.15, "medal": "gold", "sport": "Swimming" },
        { "ax": 3.73, "ay": 2.80, "medal": "bronze", "sport": "Swimming" },
        { "ax": 8.21, "ay": 3.44, "medal": "bronze", "sport": "Swimming" },
        { "ax": 7.26, "ay": 4.07, "medal": "gold", "sport": "Swimming" },
        { "ax": 3.03, "ay": 3.97, "medal": "none", "sport": "Swimming" },
        { "ax": 3.98, "ay": 3.06, "medal": "none", "sport": "Swimming" },
        { "ax": 5.54, "ay": 0.77, "medal": "bronze", "sport": "Swimming" },
        { "ax": 8.32, "ay": 2.17, "medal": "none", "sport": "Swimming" },
        { "ax": 8.43, "ay": 1.06, "medal": "bronze", "sport": "Swimming" },
        { "ax": 8.30, "ay": 4.05, "medal": "silver", "sport": "Swimming" },
        { "ax": 1.89, "ay": 0.60, "medal": "none", "sport": "Swimming" },
        { "ax": 2.33, "ay": 2.88, "medal": "gold", "sport": "Swimming" },
        { "ax": 4.36, "ay": 1.35, "medal": "silver", "sport": "Swimming" },
        { "ax": 6.56, "ay": 3.77, "medal": "none", "sport": "Swimming" },
        { "ax": 5.53, "ay": 0.96, "medal": "gold", "sport": "Swimming" },
        { "ax": 7.46, "ay": 4.24, "medal": "bronze", "sport": "Swimming" },
        { "ax": 7.18, "ay": 1.50, "medal": "none", "sport": "Swimming" },
        { "ax": 5.08, "ay": 4.19, "medal": "silver", "sport": "Running" },
        { "ax": 3.81, "ay": 3.69, "medal": "silver", "sport": "Running" },
        { "ax": 8.78, "ay": 0.69, "medal": "none", "sport": "Running" },
        { "ax": 6.89, "ay": 3.33, "medal": "gold", "sport": "Running" },
        { "ax": 3.66, "ay": 1.75, "medal": "none", "sport": "Running" },
        { "ax": 4.78, "ay": 4.13, "medal": "silver", "sport": "Running" },
        { "ax": 4.04, "ay": 2.19, "medal": "silver", "sport": "Running" },
        { "ax": 7.63, "ay": 2.69, "medal": "silver", "sport": "Running" },
        { "ax": 6.93, "ay": 1.37, "medal": "gold", "sport": "Running" },
        { "ax": 3.60, "ay": 2.84, "medal": "silver", "sport": "Running" },
        { "ax": 9.48, "ay": 0.81, "medal": "none", "sport": "Running" },
        { "ax": 9.72, "ay": 3.95, "medal": "none", "sport": "Running" },
        { "ax": 1.77, "ay": 2.84, "medal": "silver", "sport": "Running" },
        { "ax": 1.61, "ay": 1.45, "medal": "gold", "sport": "Running" },
        { "ax": 6.90, "ay": 3.73, "medal": "bronze", "sport": "Running" },
        { "ax": 3.06, "ay": 3.50, "medal": "bronze", "sport": "Running" },
        { "ax": 2.73, "ay": 4.22, "medal": "gold", "sport": "Running" },
        { "ax": 1.10, "ay": 3.09, "medal": "none", "sport": "Running" },
        { "ax": 8.68, "ay": 1.97, "medal": "none", "sport": "Running" },
        { "ax": 5.65, "ay": 4.61, "medal": "silver", "sport": "Running" },
        { "ax": 3.20, "ay": 0.81, "medal": "silver", "sport": "Cycling" },
        { "ax": 6.79, "ay": 3.45, "medal": "none", "sport": "Cycling" },
        { "ax": 7.23, "ay": 0.95, "medal": "none", "sport": "Cycling" },
        { "ax": 2.51, "ay": 0.76, "medal": "gold", "sport": "Cycling" },
        { "ax": 5.47, "ay": 2.46, "medal": "silver", "sport": "Cycling" },
        { "ax": 5.86, "ay": 2.27, "medal": "silver", "sport": "Cycling" },
        { "ax": 3.88, "ay": 1.24, "medal": "gold", "sport": "Cycling" },
        { "ax": 9.97, "ay": 1.50, "medal": "none", "sport": "Cycling" },
        { "ax": 8.50, "ay": 2.82, "medal": "none", "sport": "Cycling" },
        { "ax": 6.96, "ay": 3.70, "medal": "silver", "sport": "Cycling" },
        { "ax": 5.84, "ay": 4.90, "medal": "none", "sport": "Cycling" },
        { "ax": 5.50, "ay": 2.64, "medal": "silver", "sport": "Cycling" },
        { "ax": 9.65, "ay": 3.01, "medal": "none", "sport": "Cycling" },
        { "ax": 5.90, "ay": 0.65, "medal": "none", "sport": "Cycling" },
        { "ax": 1.25, "ay": 1.80, "medal": "gold", "sport": "Cycling" },
        { "ax": 9.63, "ay": 3.26, "medal": "silver", "sport": "Cycling" },
        { "ax": 8.90, "ay": 3.21, "medal": "bronze", "sport": "Cycling" },
        { "ax": 9.43, "ay": 4.07, "medal": "silver", "sport": "Cycling" },
        { "ax": 5.17, "ay": 4.66, "medal": "gold", "sport": "Cycling" },
        { "ax": 2.11, "ay": 3.35, "medal": "none", "sport": "Cycling" }
      ]

      return allData.filter((d) => d.sport === sport);
    },
    async updateChartData(newSport) {
      if (!newSport) {
        console.warn("Chart data will not update because no sport is selected.");
        return;
      }

      const data = await this.fetchData(newSport);
      if (data.length > 0 && this.series) {
        this.series.data.setAll(data);
      } else {
        console.warn(`No data found for the selected sport: ${newSport}`);
      }
    },
  },
};
</script>

<style scoped>
</style>
