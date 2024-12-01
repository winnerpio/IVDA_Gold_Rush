<template>
  <v-container class="fill-height" style="height: 100%;">
    <v-col cols="12" class="fill-height" style="height: 100%;">
      <v-card outlined class="pa-0 fill-height" style="height: 100%;">
        <v-card-title>{{ country.name }} Medal History</v-card-title>
        <v-card-text class="pa-0 fill-height" style="height: calc(100% - 48px);">
          <!-- Adjust height for card-text to exclude title height -->
          <div id="chartdiv" style="width: 100%; height: 100%;"></div>
        </v-card-text>
      </v-card>
    </v-col>
  </v-container>
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
    if (this.chart) {
      this.chart.dispose();
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

      // const cursor = chart.set(
      //     "cursor",
      //     am5radar.RadarCursor.new(this.root, {
      //       behavior: "zoomX",
      //     })
      // );
      // cursor.lineY.set("forceHidden", true);

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
      this.generateRandomData();
      // this.updateChartData();
      chart.appear(1000, 100);
    },
    generateRandomData() {
      const years = Array.from({ length: 126 }, (_, i) => 1896 + i); // Generate years from 2000 to 2009
      console.log(years);
      const randomData = years.map((year) => ({
        date: year.toString(), // Matches "date" for yAxis data
        gold: Math.floor(Math.random() * 10),
        silver: Math.floor(Math.random() * 10),
        bronze: Math.floor(Math.random() * 10),
      }));

      // Set data for Y-Axis
      this.chart.yAxes.getIndex(0).data.setAll(
          randomData.map((d) => ({ date: d.date }))
      );

      // Set data for each series
      this.series.gold.data.setAll(
          randomData.map((d) => ({ category: d.date, value: d.gold }))
      );
      this.series.silver.data.setAll(
          randomData.map((d) => ({ category: d.date, value: d.silver }))
      );
      this.series.bronze.data.setAll(
          randomData.map((d) => ({ category: d.date, value: d.bronze }))
      );
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

.fill-height {
  height: 100%;
}
</style>
