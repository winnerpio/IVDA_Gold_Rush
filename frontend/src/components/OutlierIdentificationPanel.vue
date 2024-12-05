<template>
  <v-container outlined class="pa-4" fluid>
    <v-row>
      <v-col cols="12" class="d-flex justify-end pb-6">
        <!-- Help Button -->
        <v-btn
            icon
            density="compact"
            @click="openHelpDialog"
            aria-label="Help"
            style="font-size: 14px; padding: 4px;"
        >
          <v-icon>mdi-help-circle</v-icon>
        </v-btn>
      </v-col>
    </v-row>
    <v-card outlined>
      <v-card-title class="text-center justify-center">
        {{ xAxis || 'X-Axis' }} vs {{ yAxis || 'Y-Axis' }} Outlier Detection
      </v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12" sm="4">
              <v-select
                  v-model="xAxis"
                  :items="attributes"
                  label="X-Axis Attribute"
                  @change="updateChart"
              ></v-select>
            </v-col>
            <v-col cols="12" sm="4">
              <v-select
                  v-model="yAxis"
                  :items="attributes"
                  label="Y-Axis Attribute"
                  @change="updateChart"
              ></v-select>
            </v-col>
            <v-col cols="12" sm="4">
              <v-select
                  label="Select Country"
                  :items="countries"
                  v-model="selectedCountry"
                  item-value="props"
                  item-text="title"
                  @change="updateChart"
                  :disabled="!sport || !event"
              ></v-select>
            </v-col>
          </v-row>
          <v-row>
            <div ref="outlierChart" style="width: 100%; height: 500px;"></div>
          </v-row>
        </v-container>
      </v-card-text>
    </v-card>
  </v-container>

  <v-dialog v-model="athleteDialog" max-width="600px">
    <v-card>
      <v-card-title class="headline">
        {{ athleteDetails.name }}
      </v-card-title>
      <v-card-text>
        <div v-if="loading" class="d-flex justify-center pa-3">
          <v-progress-linear
              indeterminate
              color="primary"
          ></v-progress-linear>
        </div>
        <p v-else>{{ athleteDetails.info }}</p>
      </v-card-text>
      <v-card-actions>
        <v-btn text @click="athleteDialog = false">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>


  <v-dialog v-model="helpDialog" max-width="600px">
    <v-card>
      <v-card-title class="headline">How to Use the Graph</v-card-title>
      <v-card-text>
        <p class="dialog-paragraph">
          This graph displays outliers for the selected X and Y axis attributes.
          Each data point represents an athlete, with the X and Y values corresponding to the chosen attributes (e.g., Age, Height, Weight).
        </p>
        <li>
          <strong>X-Axis:</strong> Choose the attribute to display on the X-axis (e.g., Age, Height).
        </li>
        <li>
          <strong>Y-Axis:</strong> Choose the attribute to display on the Y-axis (e.g., Weight, BMI).
        </li>
        <li>
          <strong>Outliers:</strong> Athletes who fall outside the expected range for the selected attributes are marked as outliers (with larger circles).
        </li>
        <li>
          <strong>Year Filter:</strong> Changing the year range dynamically updates the data across all visualizations, including available sports, events, countries and athletes.
        </li>
        <li>
          <strong>Important:</strong> You <strong>must</strong> select both a <strong>sport</strong> and an <strong>event</strong> for the <strong>country</strong> options to appear and to see the data.
        </li>
      </v-card-text>
      <v-card-actions>
        <v-btn text @click="helpDialog = false">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>


</template>


<script>
import * as am5 from "@amcharts/amcharts5";
import * as am5xy from "@amcharts/amcharts5/xy";
import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";
import axios from "axios";
import OpenAI from "openai";

export default {
  name: "OutlierIdentificationPanel",
  data() {
    return {
      xAxis: null,
      yAxis: null,
      selectedEvent: null,
      attributes: ["Age", "Height", "Weight", "BMI", "H2W"],
      sports: [],
      chart: null,
      series: null,
      apiData: [],
      countries: [],
      selectedCountry: null,
      xAxisLabel: null,
      yAxisLabel: null,
      helpDialog: false,
      athleteDialog: false,
      athleteDetails: {
        name: "",
        info: "",
      },
      loading: false,
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
      if (!this.$refs.outlierChart) {
        console.warn("Chart container not found");
        return;
      }
      this.root = am5.Root.new(this.$refs.outlierChart);
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
            tooltip: am5.Tooltip.new(this.root, {})

          })
      );

      this.xAxisLabel = am5.Label.new(this.root, {
        text: "X-Axis",
        x: am5.p50,
        centerX: am5.p50,
      });
      xAxis.children.moveValue(this.xAxisLabel, xAxis.children.length - 1);

      const yAxis = chart.yAxes.push(
          am5xy.ValueAxis.new(this.root, {
            renderer: am5xy.AxisRendererY.new(this.root, {}),
            tooltip: am5.Tooltip.new(this.root, {})

          })
      );

      this.yAxisLabel = am5.Label.new(this.root, {
        rotation: -90,
        text: "Y-Axis",
        y: am5.p50,
        centerX: am5.p50,
      });
      yAxis.children.moveValue(this.yAxisLabel, 0);


      this.series = chart.series.push(
          am5xy.LineSeries.new(this.root, {
            xAxis: xAxis,
            yAxis: yAxis,
            valueXField: "x",
            valueYField: "y",
            seriesTooltipTarget: "bullet",
          })
      );

      this.series.strokes.template.set("visible", false);

      this.series.bullets.push((root, series, dataItem) => {
        const { outlier } = dataItem.dataContext;
        const fill = dataItem.dataContext.fill;

        let bullet = am5.Bullet.new(root, {
          sprite: am5.Circle.new(root, {
            radius: outlier ? 10 : 6,
            fill: fill,
            tooltipText: `[bold]Athlete[/]: {name}\n[bold]Year[/]: {year}\n[bold]${this.xAxis || "X"}[/]: {x}\n[bold]${this.yAxis || "Y"}[/]: {y}\n[bold]Medal[/]: {medal}\n[bold]Outlier[/]: ${outlier ? "Yes" : "No"}`,
            tooltipY: 0,
          }),
        });

        bullet.get("sprite").events.on("click", () => {
          this.fetchAthleteDetails(dataItem.dataContext);
        });

        return bullet;


      });

      this.series.strokes.template.setAll({
        visible: false,
      });

      chart.set(
          "scrollbarX",
          am5.Scrollbar.new(this.root, { orientation: "horizontal" })
      );
      chart.set(
          "scrollbarY",
          am5.Scrollbar.new(this.root, { orientation: "vertical" })
      );

      chart.set(
          "cursor",
          am5xy.XYCursor.new(this.root, {
            xAxis: xAxis,
            yAxis: yAxis,
            snapToSeries: [this.series]
          })
      );


      this.chart = chart;

    },
    updateAxisLabels() {
      if (this.xAxisLabel && this.xAxis) {
        this.xAxisLabel.set("text", this.xAxis);
      }
      if (this.yAxisLabel && this.yAxis) {
        this.yAxisLabel.set("text", this.yAxis);
      }
    },
    async fetchData() {
      if (!this.xAxis || !this.yAxis || !this.selectedCountry || !this.sport || !this.event || this.yearRange.length !== 2) {
        console.warn("Missing parameters for fetching data.");
        return;
      }

      try {
        const response = await axios.get("http://127.0.0.1:5000/GetOutliers", {
          params: {
            year_lower: this.yearRange[0],
            year_upper: this.yearRange[1],
            x_axis_variable: this.xAxis.toLowerCase(),
            y_axis_variable: this.yAxis.toLowerCase(),
            sport: this.sport,
            event: this.event,
            country_code: this.selectedCountry.code,
          },
        });

        const data = response.data;

        let object = Object.entries(data).map(([key, value]) => {
          const athleteData = value.data;

          const yearMatch = key.match(/\b\d{4}\b/);
          const year = yearMatch ? yearMatch[0] : null;

          let medal;
          if (typeof athleteData.highest_medal === "number") {
            medal = athleteData.highest_medal === 3
                ? "Gold"
                : athleteData.highest_medal === 2
                    ? "Silver"
                    : athleteData.highest_medal === 1
                        ? "Bronze"
                        : "None";
          } else {
            medal = athleteData.highest_medal;
          }

          return {
            year: year,
            x: athleteData.x_axis_variable_value,
            y: athleteData.y_axis_variable_value,
            name: athleteData.name,
            medal: medal,
            outlier: athleteData.outlier || false,
          };
        });

        return object;

      } catch (error) {
        console.error("Failed to fetch data:", error.message);
        return [];
      }
    },
    async updateChart() {
      this.updateAxisLabels();
      const data = await this.fetchData();
      if (data && data.length > 0) {
        this.series.data.setAll(
            data.map((item) => ({
              x: item.x,
              y: item.y,
              name: item.name,
              year: item.year,
              country: this.selectedCountry.code,
              sport: this.sport,
              event: this.event,
              medal: item.medal,
              outlier: item.outlier,
              fill: item.medal === "Gold"
                      ? am5.color(0xffd700)
                      : item.medal === "Silver"
                          ? am5.color(0xc0c0c0)
                          : item.medal === "Bronze"
                              ? am5.color(0xcd7f32)
                              : am5.color(0x76bedf),
            }))
        );
      } else {
        console.warn("No data available for the selected parameters.");
      }
    },
    async fetchCountriesIfReady() {
      this.clearChartAndCountry();
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
    clearChartAndCountry() {
      if (this.series && this.series.data) {
        this.series.data.setAll([]);
        this.selectedCountry = null;
      }
    },
    openHelpDialog() {
      this.helpDialog = true;
    },
    async fetchAthleteDetails(athleteData) {
      const { name, year, country, sport, event } = athleteData;

      this.athleteDetails.name = "";
      this.athleteDetails.info = "";

      this.athleteDialog = true;
      this.loading = true;

      const openai = new OpenAI({
        apiKey: process.env.VUE_APP_OPENAI_API_KEY,
        dangerouslyAllowBrowser: true
      });

      try {
        const prompt = `
          Provide information about the athlete "${name}" who competed in the year "${year}"
          representing the country with this country code "${country}" in the sport "${sport}"
          for the event "${event}". The response must follow this format exactly:

          1. Performance: [Brief description of how they performed in that Olympics].
          2. Funny Fact: [A single, lighthearted or interesting fact about the athlete].

          Keep the response under 200 words and maintain the format.
        `

        const response = await openai.chat.completions.create({
          model: "gpt-4o",
          messages: [
            { role: "system", content: "You are a helpful assistant." },
            { role: "user", content: prompt },
          ],
        });

        const info = response.choices[0]?.message?.content || "Details not available.";

        this.athleteDetails.name = name;
        this.athleteDetails.info = info;
        this.athleteDialog = true;
      } catch (error) {
        console.error("Failed to fetch athlete details:", error.message);
        this.athleteDetails.name = "Error";
        this.athleteDetails.info = "Unable to retrieve details at the moment.";
        this.athleteDialog = true;
      } finally {
        this.loading = false;
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
    yearRange: {
      type: Array,
      default: () => [1896, 2022],
    },
  },
  watch: {
    sport: "fetchCountriesIfReady",
    event: "fetchCountriesIfReady",
    yearRange: {
      handler: "fetchCountriesIfReady",
      immediate: true,
    },
    selectedCountry(newCountry) {
      if (newCountry) {
        this.selectedCountry = newCountry;
        this.updateChart();
      }
    },
    xAxis(newAttribute) {
      if (newAttribute) {
        this.xAxis = newAttribute;
        this.updateChart();
      }
    },
    yAxis(newAttribute) {
      if (newAttribute) {
        this.yAxis = newAttribute;
        this.updateChart();
      }
    },
  }
};
</script>

<style scoped>
.dialog-paragraph {
  margin-bottom: 12px;
}
</style>