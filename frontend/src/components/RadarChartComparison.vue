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
                      item-value="props"
                      item-text="title"
                      @change="fetchAthletes"
                  ></v-select>
                </v-col>
                <v-col cols="6">
                  <v-select
                      label="Select Athlete"
                      :items="athletes"
                      v-model="selectedAthlete"
                      item-value="props"
                      item-text="title"
                      :disabled="!selectedCountry || !sport || !event"
                      dense
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
import axios from "axios";

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
      countries: [],
      athletes: [],
      userData: {
        sex: null,
        height: null,
        weight: null,
        age: null,
        bmi: null,
        h2w: null,
      },
      isFetchingCountries: false,
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
                fontSize: "2px",
              })
            })
        );

        series.strokes.template.setAll({
          strokeWidth: 2
        });

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
    async fetchAthletes() {
      if (!this.selectedCountry || !this.sport || !this.event || this.yearRange.length !== 2) {
        console.warn("Missing required filters: country, sport, event, or year range.");
        return;
      }

      const params = {
        year_lower: this.yearRange[0],
        year_upper: this.yearRange[1],
        sport: this.sport,
        event: this.event,
        country_code: this.selectedCountry.code,
      };

      try {
        const response = await axios.get("http://127.0.0.1:5000/CountryAthletes", { params });
        const data = response.data;

        this.athletes = Object.entries(data).map(([key, athlete]) => {
          const yearMatch = key.match(/\d{4}$/);
          const year = yearMatch ? parseInt(yearMatch[0], 10) : null;

          return {
            title: athlete.name,
            props: {
              weight: athlete.weight,
              height: athlete.height,
              bmi: athlete.bmi,
              h2w: athlete.h2w,
              age: athlete.age,
              subtitle: year,
            },
          };
        });
      } catch (error) {
        console.error("Error fetching athletes:", error.message);
      }
    },
    updateChartData() {
      if (!this.selectedAthlete) return;

      const athleteData = toRaw(this.selectedAthlete);
      const labels = ["Height", "Weight", "Age", "BMI", "H2W"];
      const userDataset = [
        this.userData.height,
        this.userData.weight,
        this.userData.age,
        this.userData.bmi,
        this.userData.h2w,
      ];
      const athleteDataset = [
        athleteData.height,
        athleteData.weight,
        athleteData.age,
        athleteData.bmi,
        athleteData.h2w,
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
    },
    async fetchCountriesIfReady() {
      if (this.sport && this.event && this.yearRange.length === 2) {
        await this.fetchCountries();
      } else {
        console.warn("Missing required filters: sport, event, or year range.");
      }
    },
    async fetchCountries() {
      if (this.isFetchingCountries) return;

      this.isFetchingCountries = true;
      try {
        const response = await axios.get("http://127.0.0.1:5000/CC2CN", {
          params: {
            year_lower: this.yearRange[0],
            year_upper: this.yearRange[1],
            sport: this.sport,
            event: this.event,
          },
        });
        const data = response.data;
        this.countries = Object.entries(data).map(([code, name]) => ({
          title: name,
          props: {"code": code} ,
        }));
      } catch (error) {
        console.error("Failed to fetch countries:", error.message);
      } finally {
        this.isFetchingCountries = false;
      }
    },
    async fetchAthleteDetails(point) {
      try {
        const response = await axios.get("http://127.0.0.1:5000/athletes", {
          params: {
            name: point.name,
            country: point.country,
          },
        });
        const athleteData = response.data[0]; // Assuming the first result is relevant
        console.log("Fetched Athlete Data:", athleteData);
        this.updateRadarChart(athleteData);
      } catch (error) {
        console.error("Error fetching athlete details:", error.message);
      }
    },
    updateRadarChart(athleteData) {
      const labels = ["Height", "Weight", "Age", "BMI", "H2W"];
      const athleteDataset = [
        athleteData.height,
        athleteData.weight,
        athleteData.age,
        athleteData.bmi,
        athleteData.h2w,
      ];

      const userDataset = [
        this.userData.height,
        this.userData.weight,
        this.userData.age,
        this.userData.bmi,
        this.userData.h2w,
      ];

      const data = labels.map((label, i) => ({
        category: label,
        athlete: athleteDataset[i],
        user: userDataset[i],
      }));

      console.log("Radar Chart Data:", data);

      if (this.chart) {
        const xAxis = this.chart.xAxes.getIndex(0);
        if (xAxis) {
          xAxis.data.setAll(data);
        }

        this.series.user.data.setAll(data);
        this.series.athlete.data.setAll(data);
      }
    },
  },
  props: {
    sport: {
      type: [String, null],
      required: true,
    },
    event: {
      type: [String, null],
      required: true,
    },
    userDataForm: {
      type: [Object, null],
      required: true,
    },
    yearRange: {
      type: Array,
      default: () => [1896, 2022],
    },
    selectedPoint: {
      type: [Object, null],
      required: false, // Data of the clicked scatterplot point
    },
  },
  watch: {
    sport: "fetchCountriesIfReady",
    yearRange: {
      handler: "fetchCountriesIfReady",
      immediate: true,
    },
    selectedAthlete: "updateChartData",
    selectedCountry(newCountry) {
      if (newCountry) {
        this.selectedAthlete = null;
        this.selectedCountry = newCountry;
        this.fetchAthletes();
      }
    },
    userDataForm: {
      handler(newUserData) {
        this.userData = { ...newUserData };
        this.updateChartData();
      },
      deep: true,
    },
    event() {
      this.selectedAthlete = null;
      this.selectedCountry = null;
      this.fetchCountriesIfReady();
      this.series.athlete.data.setAll([]);
    },
    selectedPoint: {
      handler(newPoint) {
        if (newPoint) {
          this.fetchAthleteDetails(newPoint);
        }
      },
      immediate: true,
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
