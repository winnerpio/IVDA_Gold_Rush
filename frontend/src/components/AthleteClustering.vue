<template>
  <v-container>
    <v-card outlined class="pa-5" fill-height>
      <v-card-title>Similar Athlete Clusters</v-card-title>
      <v-card-subtitle>Select attributes to visualize athlete clusters</v-card-subtitle>
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
        <v-row class="chart-row">
          <v-col cols="12">
            <div id="athlete-clusters" style="width: 100%; height: 500px;"></div>
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

export default {
  name: "AthleteClustering",
  data() {
    return {
      xAttribute: "Height",
      yAttribute: "Age",
      attributes: ["Height", "Age", "Weight"],
      chart: null,
      series: null,
      colors: ["#4bc0c0", "#ff6384", "#36a2eb"],
    };
  },
  methods: {
    async fetchData() {
      // Mock API data
      const allData = [
        { x: 190, y: 22, cluster: 0 },
        { x: 188, y: 23, cluster: 0 },
        { x: 192, y: 24, cluster: 0 },
        { x: 189, y: 25, cluster: 0 },
        { x: 191, y: 21, cluster: 0 },
        { x: 193, y: 22, cluster: 0 },
        { x: 190, y: 24, cluster: 0 },
        { x: 194, y: 23, cluster: 0 },
        { x: 189, y: 20, cluster: 0},
        {x: 192, y: 21, cluster: 0},
        {x: 180, y: 28, cluster: 1},
        {x: 178, y: 29, cluster: 1},
        {x: 181, y: 30, cluster: 1},
        {x: 179, y: 27, cluster: 1},
        {x: 182, y: 31, cluster: 1},
        {x: 180, y: 29, cluster: 1},
        {x: 183, y: 28, cluster: 1},
        {x: 181, y: 30, cluster: 1},
        {x: 178, y: 27, cluster: 1},
        {x: 182, y: 32, cluster: 1},
        {x: 170, y: 33, cluster: 2},
        {x: 172, y: 34, cluster: 2},
        {x: 173, y: 35, cluster: 2},
        {x: 171, y: 32, cluster: 2},
        {x: 174, y: 36, cluster: 2},
        {x: 172, y: 34, cluster: 2},
        {x: 175, y: 35, cluster: 2},
        {x: 170, y: 33, cluster: 2},
        {x: 173, y: 34, cluster: 2},
        {x: 171, y: 32, cluster: 2},
      ];

      // Filter based on sport
      return allData;
    },
    async updateChartData() {

      const data = await this.fetchData();
      if (data.length > 0 && this.series) {
        this.series.data.setAll(data);
      }
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

      // Add horizontal scrollbar
      chart.set(
          "scrollbarX",
          am5.Scrollbar.new(this.root, { orientation: "horizontal" })
      );

      // Add vertical scrollbar
      chart.set(
          "scrollbarY",
          am5.Scrollbar.new(this.root, { orientation: "vertical" })
      );

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
        const color = am5.color(this.colors[cluster]);

        const bullet = am5.Bullet.new(root, {
          sprite: am5.Circle.new(root, {
            fill: color,
            radius: 6,
            tooltipText: "Cluster: {cluster}\nX: {valueX}\nY: {valueY}",
          }),
        });

        return bullet;
      });

      series.strokes.template.setAll({
        visible: false,
      });

      this.chart = chart;
      this.series = series;

      this.updateChartData();
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
