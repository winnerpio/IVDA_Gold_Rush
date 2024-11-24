<template>
  <v-container>
    <v-col cols="12">
      <v-card outlined class="pa-0" fill-height>
        <v-card-title>{{ country.name }} Performance Evolution </v-card-title>
        <v-card-text class="pa-0">
          <div id="country-performance-evolution" style="width: 100%; height: 250px;"></div>
        </v-card-text>
      </v-card>
    </v-col>
  </v-container>
</template>

<script>
import * as am5 from '@amcharts/amcharts5';
import * as am5xy from '@amcharts/amcharts5/xy';
import am5themes_Animated from '@amcharts/amcharts5/themes/Animated';
import { toRaw } from "vue";

export default {
  name: 'CountryPerformanceEvolution',
  props: {
    country: {
      type: Object,
      required: true,
    },
    data: {
      type: [Object, null],
      required: true,
    },
    dateRange: {
      type: Array,
      default: () => [1896, 2022],
    },
  },
  data() {
    return {
      chart: null,
      series: null,
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
      this.root = am5.Root.new("country-performance-evolution");
      this.root.setThemes([am5themes_Animated.new(this.root)]);

      let chart = this.root.container.children.push(
        am5xy.XYChart.new(this.root, {
          panX: false,
          panY: false,
          wheelX: "panX",
          wheelY: "zoomX",
          pinchZoomX: true,
          paddingLeft: 0,
          maxTooltipDistance: 2,
        })
      );

      let cursor = chart.set("cursor", am5xy.XYCursor.new(this.root, {
        behavior: "none",
      }));
      cursor.lineY.set("visible", true);
      cursor.lineX.set("visible", true);

      this.xAxis = chart.xAxes.push(am5xy.DateAxis.new(this.root, {
        maxDeviation: 0.2,
        baseInterval: {
          timeUnit: "year",
          count: 1,
        },
        min: new Date(this.dateRange[0], 0, 1).getTime(),
        max: new Date(this.dateRange[1], 11, 31).getTime(),
        renderer: am5xy.AxisRendererX.new(this.root, {
          minorGridEnabled: true,
        }),
        tooltip: am5.Tooltip.new(this.root, {}),
      }));

      this.yAxis = chart.yAxes.push(am5xy.ValueAxis.new(this.root, {
        renderer: am5xy.AxisRendererY.new(this.root, {
          pan: "zoom",
        }),
        min: 0,
      }));

      this.series = chart.series.push(am5xy.LineSeries.new(this.root, {
        name: `${this.country.name} performance`,
        xAxis: this.xAxis,
        yAxis: this.yAxis,
        valueYField: "value",
        valueXField: "date",
        strokeWidth: 3,
        tooltip: am5.Tooltip.new(this.root, {
          labelText: "{valueY}",
        }),
      }));

      this.averageSeries = chart.series.push(am5xy.LineSeries.new(this.root, {
        name: "Average Performance",
        xAxis: this.xAxis,
        yAxis: this.yAxis,
        valueYField: "avgValue",
        valueXField: "date",
        stroke: am5.color(0x808080),
        strokeWidth: 3,
        strokeDasharray: [4, 4],
        tooltip: am5.Tooltip.new(this.root, {
          labelText: "Avg: {avgValue}",
        }),
      }));

      chart.set("cursor", am5xy.XYCursor.new(this.root, {
        behavior: "zoomX",
      }));

      this.chart = chart;

      this.updateChartData();
    },

    async updateChartData() {
      if (!this.country || !this.data || Object.keys(this.data).length === 0 || !this.dateRange || this.dateRange.length !== 2) {
        console.warn("Chart data will not update. Missing required fields or data is empty.");
        return;
      }

      const [startYear, endYear] = toRaw(this.dateRange);

      if (this.xAxis) {
        this.xAxis.set("min", new Date(startYear, 0, 1).getTime());
        this.xAxis.set("max", new Date(endYear, 11, 31).getTime());
      }

      const performanceData = this.getPerformanceData();
      const averagePerformanceData = this.getAveragePerformanceData();

      if (performanceData.length > 0 && this.series) {
        this.series.data.setAll(performanceData);
      } else {
        console.warn("No data found for the selected filters.");
      }

      if (averagePerformanceData.length > 0 && this.averageSeries) {
        this.averageSeries.data.setAll(averagePerformanceData);
      } else {
        console.warn("No average data found for the selected filters.");
      }
    },
    getPerformanceData() {
      const { country, data, dateRange } = this;
      const [startYear, endYear] = dateRange;

      const rawData = toRaw(data);
      if (!rawData || !rawData[country.code]) {
        console.warn(`No data found for country: ${country.name}`);
        return [];
      }

      const countryData = rawData[country.code];
      const filteredData = [];

      for (const year in countryData) {
        const yearNumber = parseInt(year, 10);
        if (yearNumber >= startYear && yearNumber <= endYear) {
          const yearData = countryData[year];
          const value = yearData
            ? yearData.gold * 1 + yearData.silver * 0.7 + yearData.bronze * 0.5
            : 0;
          filteredData.push({
            date: new Date(yearNumber, 0, 1).getTime(),
            value,
          });
        }
      }

      return filteredData;
    },
    getAveragePerformanceData() {
      const { data, dateRange } = this;
      const [startYear, endYear] = dateRange;

      const rawData = toRaw(data);
      if (!rawData) {
        console.warn("No data available to calculate averages.");
        return [];
      }

      const yearTotals = {};
      const yearCounts = {};

      for (const countryCode in rawData) {
        const countryData = rawData[countryCode];
        for (const year in countryData) {
          const yearNumber = parseInt(year, 10);
          if (yearNumber >= startYear && yearNumber <= endYear) {
            const yearData = countryData[year];
            const value = yearData
              ? yearData.gold * 1 + yearData.silver * 0.7 + yearData.bronze * 0.5
              : 0;

            if (!yearTotals[yearNumber]) {
              yearTotals[yearNumber] = 0;
              yearCounts[yearNumber] = 0;
            }

            yearTotals[yearNumber] += value;
            yearCounts[yearNumber] += 1;
          }
        }
      }

      return Object.keys(yearTotals).map(year => ({
        date: new Date(parseInt(year, 10), 0, 1).getTime(),
        avgValue: yearTotals[year] / yearCounts[year],
      }));
    },
  },
  watch: {
    country: {
      handler: "updateChartData",
      deep: true,
    },
    dateRange: {
      handler: "updateChartData",
      deep: true,
    },
    data: {
      handler: "updateChartData",
      deep: true,
    },
  },

};
</script>

<style scoped>
#country-performance-evolution {
  width: 100%;
  height: 100%;
}
</style>
