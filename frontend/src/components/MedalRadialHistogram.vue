<template>
  <v-container>
    <v-col cols="12">
      <v-card outlined class="pa-0" fill-height>
        <v-card-title>{{ country.name }} Medal History </v-card-title>
        <v-card-text class="pa-0">
          <div id="chartdiv" style="width: 100%; height: 300px;"></div>
        </v-card-text>
      </v-card>
    </v-col>
  </v-container>
</template>

<script>
import * as am5radar from "@amcharts/amcharts5/radar";
import * as am5 from "@amcharts/amcharts5";
import * as am5xy from "@amcharts/amcharts5/xy";
import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";
import {toRaw} from "vue";

export default {
  name: "MedalRadialHistogram",
  data() {
    return {
      chart: null,
      series: {
        gold: null,
        silver: null,
        bronze: null,
      },
    };
  },
  mounted() {
    this.initChart();
  },
  beforeUnmount() {
    if (this.chart) {
      this.chart.dispose();
    }
  },
  methods: {
    initChart() {
      this.root = am5.Root.new("chartdiv");

      this.root.setThemes([am5themes_Animated.new(this.root)]);

      const chart = this.root.container.children.push(
          am5radar.RadarChart.new(this.root, {
            panX: false,
            panY: false,
            wheelX: "none",
            wheelY: "none",
            startAngle: -84,
            endAngle: 264,
            innerRadius: am5.percent(40),
          })
      );

      const cursor = chart.set(
          "cursor",
          am5radar.RadarCursor.new(this.root, {
            behavior: "zoomX",
          })
      );
      cursor.lineY.set("forceHidden", true);

      const xRenderer = am5radar.AxisRendererCircular.new(this.root, {
        minGridDistance: 30,
      });
      xRenderer.grid.template.set("forceHidden", true);

      const xAxis = chart.xAxes.push(
          am5xy.CategoryAxis.new(this.root, {
            maxDeviation: 0,
            categoryField: "date",
            renderer: xRenderer,
          })
      );

      const yRenderer = am5radar.AxisRendererRadial.new(this.root, {});
      yRenderer.labels.template.set("centerX", am5.p50);

      const yAxis = chart.yAxes.push(
          am5xy.ValueAxis.new(this.root, {
            maxDeviation: 0.3,
            min: 0,
            renderer: yRenderer,
          })
      );

      const createSeries = (name, color) => {
        const series = chart.series.push(
            am5radar.RadarColumnSeries.new(this.root, {
              name: name,
              xAxis: xAxis,
              yAxis: yAxis,
              valueYField: "value",
              categoryXField: "category",
            })
        );

        series.columns.template.setAll({
          cornerRadius: 5,
          tooltipText: `{categoryX}: {valueY} ${name}`,
          fill: am5.color(color),
          stroke: am5.color(color),
        });

        return series;
      };

      this.series.gold = createSeries("Gold", "#FFD700");
      this.series.silver = createSeries("Silver", "#C0C0C0");
      this.series.bronze = createSeries("Bronze", "#CD7F32");

      this.chart = chart;
      this.updateChartData();
      chart.appear(1000, 100);
    },
    async updateChartData() {
      const filteredData = this.getFilteredData();

      if (filteredData.length > 0) {
        const uniqueYears = filteredData.map((d) => d.year.toString());
        this.chart.xAxes.getIndex(0).data.setAll(uniqueYears.map((year) => ({ date: year })));

        const goldData = filteredData.map((d) => ({ category: d.year.toString(), value: d.gold }));
        const silverData = filteredData.map((d) => ({ category: d.year.toString(), value: d.silver }));
        const bronzeData = filteredData.map((d) => ({ category: d.year.toString(), value: d.bronze }));

        this.series.gold.data.setAll(goldData);
        this.series.silver.data.setAll(silverData);
        this.series.bronze.data.setAll(bronzeData);
      } else {
        console.warn("No data available for the selected filters.");
        this.series.gold.data.setAll([]);
        this.series.silver.data.setAll([]);
        this.series.bronze.data.setAll([]);
      }
    },
    getFilteredData() {
      const { data, country, dateRange } = this;
      const [startYear, endYear] = dateRange;

      const rawData = toRaw(data);

      if (!rawData || !rawData[country.code]) {
        console.warn(`No data found for country: ${country.name}`);
        return [];
      }

      return Object.entries(rawData[country.code])
        .filter(([year]) => year !== "all" && +year >= startYear && +year <= endYear)
        .map(([year]) => ({
          year: +year,
          gold: rawData[country.code][year]?.gold || 0,
          silver: rawData[country.code][year]?.silver || 0,
          bronze: rawData[country.code][year]?.bronze || 0,
        }));
    }
  },
  props: {
    event: {
      type: [String, null],
      required: true,
    },
    sport: {
      type: [String, null],
      required: true,
    },
    country: {
      type: Object,
      required: true,
    },
    dateRange: {
      type: Array,
      default: () => [1896, 2022],
    },
    data: {
      type: [Object, null],
      required: true,
    },
  },
  watch: {
    $props: {
      handler() {
        this.updateChartData();
      },
      deep: true,
    },
  },
};
</script>

<style scoped>
#chartdiv {
  width: 100%;
  height: 100%;
}
</style>
