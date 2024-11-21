<template>
  <v-container>
    <v-col cols="12">
      <v-card outlined class="pa-0" fill-height>
        <v-card-title>{{ country }} Performance Evolution </v-card-title>
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

export default {
  name: 'CountryPerformanceEvolution',
  data() {
    return {
      chart: null,
      series: null,
    }
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
            panX: true,
            panY: true,
            wheelX: "panX",
            wheelY: "zoomX",
            pinchZoomX:true,
            paddingLeft: 0
          })
      );

      let cursor = chart.set("cursor", am5xy.XYCursor.new(this.root, {
        behavior: "none"
      }));
      cursor.lineY.set("visible", false)

      let xAxis = chart.xAxes.push(am5xy.DateAxis.new(this.root, {
        maxDeviation: 0.2,
        baseInterval: {
          timeUnit: "year",
          count: 1
        },
        renderer: am5xy.AxisRendererX.new(this.root, {
          minorGridEnabled: true,
        }),
        tooltip: am5.Tooltip.new(this.root, {})
      }));

      let yAxis = chart.yAxes.push(am5xy.ValueAxis.new(this.root, {
        renderer: am5xy.AxisRendererY.new(this.root, {
          pan:"zoom"
        })
      }));

      this.series = chart.series.push(am5xy.LineSeries.new(this.root, {
        name: "Series",
        xAxis: xAxis,
        yAxis: yAxis,
        valueYField: "value",
        valueXField: "date",
        tooltip: am5.Tooltip.new(this.root, {
          labelText: "{valueY}"
        })
      }));

      this.updateChartData()
    },

    async fetchPerformanceData() {
      const { country, sport, event, dateRange} = this;
      const [startYear, endYear] = dateRange;

      const allData = [
        { country: "United States", sport: "Swimming", event: "200m Freestyle", year: 2000, performance: 100 },
        { country: "United States", sport: "Swimming", event: "200m Freestyle", year: 2004, performance: 98 },
        { country: "United States", sport: "Swimming", event: "200m Freestyle", year: 2008, performance: 96 },
        { country: "United States", sport: "Swimming", event: "200m Freestyle", year: 2012, performance: 94 },
        { country: "United States", sport: "Swimming", event: "200m Freestyle", year: 2016, performance: 92 },
        { country: "United States", sport: "Swimming", event: "200m Freestyle", year: 2020, performance: 90 },
      ];

      return allData.filter(
          (d) =>
              d.country === country &&
              d.sport === sport &&
              d.event === event &&
              d.year >= startYear &&
              d.year <= endYear
      );
    },

    async updateChartData() {
      if (!this.country || !this.sport || !this.event) {
        let missingFields = [];
        if (!this.country) missingFields.push('Country');
        if (!this.sport) missingFields.push('Sport');
        if (!this.event) missingFields.push('Event');

        console.warn(`Performance chart data will not update because the following fields are missing: ${missingFields.join(', ')}`);
        return;
      }

      const data = await this.fetchPerformanceData();
      if (data.length > 0 && this.series) {
        let chartData = data.map((d) => ({
          date: new Date(d.year, 0, 1).getTime(),
          value: d.performance,
        }))
        this.series.data.setAll(chartData);
      } else {
        console.warn("No data found for the selected filters.");
      }
    },
  },
  props: {
    event: {
      type: String,
    },
    sport: {
      type: String,
    },
    country: {
      type: String,
    },
    dateRange: {
      type: Array,
      default: () => [2000, 2020]
    }
  },
  watch: {
    $props: {
      handler(newProps) {
        const { country, sport, event, dateRange } = newProps;
        if (country && sport && event && dateRange) {
          this.updateChartData();
        }
      },
      deep: true,
    },
  },
}
</script>

<style scoped>

</style>
