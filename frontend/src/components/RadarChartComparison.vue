<template>
  <v-container class="container" fluid>
    <v-row>
      <v-col cols="12" md="12">
        <div class="dropdown-container">
          <v-card>
            <v-container>
              <!-- Dropdowns -->
              <v-row>
                <v-col cols="6">
                  <v-select
                      label="Select Country"
                      :items="countries"
                      v-model="selectedCountry"
                  ></v-select>
                </v-col>
                <v-col cols="6">
                  <v-select
                      label="Select Athlete"
                      :items="filteredAthletes"
                      v-model="selectedAthlete"
                      item-value="props"
                      item-text="title"
                      :disabled="!selectedCountry || !sport || !event"
                  ></v-select>
                </v-col>
              </v-row>
              <!-- Radar Chart -->
              <v-row>
                <v-col cols="12">
                  <div ref="radarChart" style="width: 100%; height: 400px;"></div>
                </v-col>
              </v-row>
            </v-container>
          </v-card>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import * as am5 from "@amcharts/amcharts5";
import * as am5radar from "@amcharts/amcharts5/radar";
import * as am5xy from "@amcharts/amcharts5/xy";
import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";
import {toRaw} from "vue";

export default {
  data() {
    return {
      chart: null,
      series: {
        user: null,
        athlete: null,
      },
      selectedCountry: null,
      selectedAthlete: null,
      countries: ["USA", "China", "Germany", "Canada"], // Example countries
      filteredAthletes: [], // Athletes filtered by selectedCountry, sport, and event
      userData: {
        sex: '',
        height: 175,
        weight: 70,
        age: 25,
        medals: 10,
        performance: 179,
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
      if (this.chart) {
        this.chart.dispose();
      }

      this.root = am5.Root.new(this.$refs.radarChart);
      this.root.setThemes([am5themes_Animated.new(this.root)]);

      let chart = this.root.container.children.push(
          am5radar.RadarChart.new(this.root, {
            startAngle: -90,
            endAngle: 270,
          })
      );

      // Add cursor for better interactivity
      let cursor = chart.set("cursor", am5radar.RadarCursor.new(this.root, {
        behavior: "zoomX"
      }));
      cursor.lineY.set("visible", false);

      let xRenderer = am5radar.AxisRendererCircular.new(this.root, {});
      let yRenderer = am5radar.AxisRendererRadial.new(this.root, {});

      let xAxis = chart.xAxes.push(
          am5xy.CategoryAxis.new(this.root, {
            renderer: xRenderer,
            categoryField: "category",
          })
      );

      let yAxis = chart.yAxes.push(
          am5xy.ValueAxis.new(this.root, {
            renderer: yRenderer,
            min: 0,
          })
      );

      let createSeries = (name, field, color) => {
        const series = chart.series.push(
            am5radar.RadarLineSeries.new(this.root, {
              name,
              xAxis,
              yAxis,
              valueYField: field,
              categoryXField: "category",
              stroke: color,
              fill: color,
              fillOpacity: 0.4,
              tooltip: am5.Tooltip.new(this.root, {
                labelText: `{name}: {valueY}`,
                fontSize: "2px", // Smaller font size for tooltips
              })
            })
        );

        series.strokes.template.setAll({
          strokeWidth: 2
        });

        // Add bullets for better visibility of points
        series.bullets.push(() => {
          return am5.Bullet.new(this.root, {
            sprite: am5.Circle.new(this.root, {
              radius: 5,
              fill: series.get("fill"),
            })
          });
        });

        return series;
      };

      this.series.user = createSeries("Your Data", "user", am5.color(0x36a2eb));
      this.series.athlete = createSeries("Athlete Data", "athlete", am5.color(0xff6384));

      chart.set(
          "legend",
          am5.Legend.new(this.root, {
            centerX: am5.p50,
            x: am5.p50,
          })
      );

      this.chart = chart;
      this.updateChartData();
      chart.appear(1000, 100);
    },
    async fetchAthletesByCriteria(country, sport, event) {
      // Simulate an API call
      await new Promise((resolve) => setTimeout(resolve, 500));

      // Mock data
      const allAthletes = [
        {
          name: "Athlete A",
          id: 1,
          country: "USA",
          sport: "Swimming",
          event: "200m Freestyle",
          height: 180,
          weight: 75,
          age: 26,
          medals: 8,
          performance: 200,
        },
        {
          name: "Athlete B",
          id: 2,
          country: "China",
          sport: "Running",
          event: "100m",
          height: 170,
          weight: 65,
          age: 24,
          medals: 12,
          performance: 220,
        },
        {
          name: "Athlete C",
          id: 3,
          country: "USA",
          sport: "Swimming",
          event: "200m Freestyle",
          height: 185,
          weight: 80,
          age: 28,
          medals: 6,
          performance: 190,
        },
        {
          name: "Athlete D",
          id: 4,
          country: "Germany",
          sport: "Cycling",
          event: "Road Race",
          height: 178,
          weight: 72,
          age: 27,
          medals: 9,
          performance: 210,
        },
        {
          name: "Athlete E",
          id: 5,
          country: "Canada",
          sport: "Running",
          event: "200m",
          height: 172,
          weight: 68,
          age: 23,
          medals: 15,
          performance: 230,
        },
      ];

      const filteredAthletes = allAthletes.filter(
          (athlete) =>
              athlete.country === country &&
              athlete.sport === sport &&
              athlete.event === event
      );

      return filteredAthletes.map((athlete) => ({
        title: athlete.name,
        props: {
          id: athlete.id,
          country: athlete.country,
          sport: athlete.sport,
          event: athlete.event,
          height: athlete.height,
          weight: athlete.weight,
          age: athlete.age,
          medals: athlete.medals,
          performance: athlete.performance,
        },
      }));
    },
    async updateAthletesList() {
      if (!this.selectedCountry || !this.sport || !this.event) {
        console.warn("Cannot fetch athletes. Ensure country, sport, and event are selected.");
        return;
      }

      this.filteredAthletes = await this.fetchAthletesByCriteria(this.selectedCountry, this.sport, this.event);
    },
    async updateChartData() {
      if (!this.selectedAthlete) {
        console.warn("No athlete selected. Chart data will not update.");
        return;
      }

      const athleteData = toRaw(this.selectedAthlete);

      if (athleteData) {
        // Update chart with new data
        const labels = ["Height", "Weight", "Age", "Number of Medals", "Performance"];
        const userDataset = [
          this.userData.height,
          this.userData.weight,
          this.userData.age,
          this.userData.medals,
          this.userData.performance,
        ];
        const athleteDataset = [
          athleteData.height,
          athleteData.weight,
          athleteData.age,
          athleteData.medals,
          athleteData.performance,
        ];

        const data = labels.map((label, i) => ({
          category: label,
          user: userDataset[i],
          athlete: athleteDataset[i],
        }));

        if (this.chart) {
          const xAxis = this.chart.xAxes.getIndex(0);
          if (xAxis) {
            xAxis.data.setAll(data);
          }

          this.series.user.data.setAll(data);
          this.series.athlete.data.setAll(data);
        }
      } else {
        console.warn("No data available for the selected athlete.");
      }
    }
  },
  props: {
    sport: {
      type: String,
      required: true,
    },
    event: {
      type: String,
      required: true,
    },
    userDataForm: {
      type: Object,
      required: true,
    },
  },
  watch: {
    selectedCountry: "updateAthletesList",
    sport: "updateAthletesList",
    event: "updateAthletesList",
    selectedAthlete() {
      this.updateAthletesList();
      this.updateChartData();
    },
    userDataForm: {
      handler(newUserData) {
        console.log(newUserData);
        this.userData = { ...newUserData };
        this.updateChartData();
      },
      deep: true,
    },

  }
}
</script>

<style scoped>
.dropdown-container {
  width: 100%;
  height: auto;
  min-height: 300px;
  max-width: 100%;
}
</style>
