<template>
  <v-container>
    <v-col cols="12">
      <v-card outlined class="pa-0" fill-height>
        <v-card-title>{{ country }} Medal History </v-card-title>
        <v-card-text class="pa-0">
          <div id="chartdiv" style="width: 100%; height: 380px;"></div>
        </v-card-text>
      </v-card>
    </v-col>
  </v-container>
</template>

<script>
import * as am5radar from "@amcharts/amcharts5/radar";
import * as am5 from '@amcharts/amcharts5';
import * as am5xy from '@amcharts/amcharts5/xy';
import am5themes_Animated from '@amcharts/amcharts5/themes/Animated';


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
    }
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

      this.root.setThemes([
        am5themes_Animated.new(this.root)
      ]);

      let chart = this.root.container.children.push(
          am5radar.RadarChart.new(this.root, {
            panX: false,
            panY: false,
            wheelX: "none",
            wheelY: "none",
            startAngle: -84,
            endAngle: 264,
            innerRadius: am5.percent(40)
          })
      );

      const cursor = chart.set("cursor", am5radar.RadarCursor.new(this.root, {
        behavior: "zoomX"
      }));
      cursor.lineY.set("forceHidden", true);

      chart.set("scrollbarX", am5.Scrollbar.new(this.root, {
        orientation: "horizontal",
        exportable: false
      }));

      let xRenderer = am5radar.AxisRendererCircular.new(this.root, {
        minGridDistance: 30
      });

      xRenderer.grid.template.set("forceHidden", true);

      let xAxis = chart.xAxes.push(am5xy.CategoryAxis.new(this.root, {
        maxDeviation: 0,
        categoryField: "date",
        renderer: xRenderer
      }));

      let yRenderer = am5radar.AxisRendererRadial.new(this.root, {});
      yRenderer.labels.template.set("centerX", am5.p50);

      let yAxis = chart.yAxes.push(am5xy.ValueAxis.new(this.root, {
        maxDeviation: 0.3,
        min: 0,
        renderer: yRenderer
      }));

      let createSeries = (name, color) => {
        let series = chart.series.push(
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

      this.series.gold = createSeries("Gold", '#FFD700');
      this.series.silver = createSeries("Silver", '#C0C0C0');
      this.series.bronze = createSeries("Bronze", '#CD7F32');

      this.chart = chart;
      this.updateChartData();
      chart.appear(1000, 100);
    },

    async fetchMedalData() {
      const { country, sport, event, dateRange } = this;
      const [startYear, endYear] = dateRange;

      country
      sport
      event

      // Mock Data
      const mockData = [
        { year: 2000, gold: 5, silver: 3, bronze: 2 },
        { year: 2004, gold: 6, silver: 2, bronze: 3 },
        { year: 2008, gold: 8, silver: 4, bronze: 1 },
        { year: 2012, gold: 7, silver: 5, bronze: 2 },
        { year: 2016, gold: 9, silver: 6, bronze: 3 },
        { year: 2020, gold: 4, silver: 7, bronze: 6 },
      ];

      return mockData.filter(
          (d) =>
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

        console.warn(`Medal Radial Chart data will not update because the following fields are missing: ${missingFields.join(', ')}`);
        return;
      }

      const data = await this.fetchMedalData();

      if (data.length > 0) {

        const yearsInData = data.map((d) => d.year.toString());
        const uniqueYears = [...new Set(yearsInData)].sort();

        this.chart.xAxes.getIndex(0).data.setAll(uniqueYears.map(year => ({ date: year })));

        const goldData = data.map((d) => ({ category: d.year.toString(), value: d.gold }));
        const silverData = data.map((d) => ({ category: d.year.toString(), value: d.silver }));
        const bronzeData = data.map((d) => ({ category: d.year.toString(), value: d.bronze }));

        this.series.gold.data.setAll(goldData);
        this.series.silver.data.setAll(silverData);
        this.series.bronze.data.setAll(bronzeData);

      } else {
        console.warn("No data available for the selected filters.")
      }
    }
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
};
</script>

<style scoped>

</style>