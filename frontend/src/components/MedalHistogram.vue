<template>
  <div class="layout-container">
    <!-- Header -->
    <div>
      <h2>{{ country.name }} Medal History</h2>
    </div>

    <!-- Chart Container -->
    <div class="graph-container" style="width: 100%; height: 85vh">
      <div id="chartdiv" ></div>
    </div>
  </div>
</template>


<script>
import * as am5 from "@amcharts/amcharts5";
import * as am5xy from "@amcharts/amcharts5/xy";
import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";
import {toRaw} from "vue";

export default {
  name: "MedalHistogram",
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
    if (this.root) {
      this.root.dispose();
    }
  },
  methods: {
    initChart() {
      this.root = am5.Root.new("chartdiv");

      const myTheme = am5.Theme.new(this.root);
      myTheme.rule("Grid", ["base"]).setAll({
        strokeOpacity: 0.1,
      });

      this.root.setThemes([
          am5themes_Animated.new(this.root),
          myTheme
      ]);

      const chart = this.root.container.children.push(
          am5xy.XYChart.new(this.root, {
            panX: false,
            panY: false,
            wheelX: "panY",
            wheelY: "zoomY",
            paddingLeft: 0,
            layout: this.root.verticalLayout,
          })
      );

      chart.set(
          "scrollbarY",
          am5.Scrollbar.new(this.root, {
            orientation: "vertical",
          })
      );

      const xRenderer = am5xy.AxisRendererX.new(this.root, {
        minGridDistance: 40,
        strokeOpacity: 0.1,
      });

      const xAxis = chart.xAxes.push(
          am5xy.ValueAxis.new(this.root, {
            min: 0,
            maxPrecision: 0,
            // categoryField: "date",
            renderer: xRenderer,
          })
      );

      const yRenderer = am5xy.AxisRendererY.new(this.root, {});

      const yAxis = chart.yAxes.push(
          am5xy.CategoryAxis.new(this.root, {
            categoryField: "date",
            renderer: yRenderer,
          })
      );

      const legend = chart.children.push(
          am5.Legend.new(this.root, {
            centerX: am5.p50,
            x: am5.p50
          })
      );

      const createSeries = (name, color) => {
        const series = chart.series.push(
            am5xy.ColumnSeries.new(this.root, {
              name: name,
              stacked: true,
              xAxis: xAxis,
              yAxis: yAxis,
              valueXField: "value",
              categoryYField: "category",
            })
        );

        series.columns.template.setAll({
          tooltipText: `{categoryY}: {valueX} ${name}`,
          fill: am5.color(color),
          stroke: am5.color(color),
        });

        series.bullets.push(() => {
          return am5.Bullet.new(this.root, {
            sprite: am5.Label.new(this.root, {
              text: "{valueX}",
              fill: this.root.interfaceColors.get("alternativeText"),
              centerX: am5.p50,
              centerY: am5.p50,
              populateText: true,
              forceHidden: "{valueX} === 0",
            }),
          });
        });

        legend.data.push(series);

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
        this.chart.yAxes.getIndex(0).data.setAll(uniqueYears.map((year) => ({ date: year })));

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

.fill-height {
  height: 100%;
}
</style>
