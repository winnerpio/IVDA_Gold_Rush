<template>
  <v-container>
    <v-row>
      <!-- Heatmap Display Panel -->
      <v-col cols="12" md="12">
        <v-card outlined class="pa-0" fill-height>
          <v-card-text class="pa-0">
            <div id="medal-map" style="width: 100%; height: 750px;"></div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import * as am5 from "@amcharts/amcharts5";
import * as am5map from "@amcharts/amcharts5/map";
import am5geodata_worldLow from "@amcharts/amcharts5-geodata/worldLow";
import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";

export default {
  name: "MedalSuccessMap",
  data(){
    return{
      chart: null,
      polygonSeries: null,
      selectedYearRange: [1896, 2022],
      selectedSport: null,
      selectedEvent: null,
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
      this.root = am5.Root.new("medal-map");
      this.root.setThemes([am5themes_Animated.new(this.root)]);

      let chart = this.root.container.children.push(
          am5map.MapChart.new(this.root, {
            projection: am5map.geoEqualEarth(),
            panX: "rotateX",
            panY: "none",
          })
      );

      let polygonSeries = chart.series.push(
          am5map.MapPolygonSeries.new(this.root, {
            geoJSON: am5geodata_worldLow,
            valueField: "value",
            calculateAggregates: true,
          })
      );

      this.polygonSeries = polygonSeries;

      let zoomControl = chart.set("zoomControl", am5map.ZoomControl.new(this.root, {}));
      zoomControl.homeButton.set("visible", true);

      chart.chartContainer.get("background").events.on("click", () => {
        chart.goHome();
      });

      polygonSeries.mapPolygons.template.adapters.add("tooltipText", function (text, target) {
        const value = target.dataItem?.dataContext.value;
        return value === undefined ? "{name}: NA" : "{name}: {value} medals";
      });

      polygonSeries.mapPolygons.template.events.on("click", (event) => {
        const polygon = event.target;
        const countryName = polygon._dataItem.dataContext.name;
        const countryCode = polygon._dataItem.dataContext.id;
        this.$emit("country-selected", { countryName, countryCode });
        polygonSeries.zoomToDataItem(polygon.dataItem);
      });

      polygonSeries.mapPolygons.template.set("interactive", true);

      polygonSeries.set("heatRules", [
        {
          target: polygonSeries.mapPolygons.template,
          dataField: "value",
          min: am5.color(0xb3d9ff),
          max: am5.color(0x8b0000),
          key: "fill",
        },
      ]);

      polygonSeries.mapPolygons.template.adapters.add("fill", function (fill, target) {
        return target.dataItem?.dataContext.value === undefined ? am5.color(0xCCCCCC) : fill;
      });

      this.updateData(this.selectedYearRange);

      chart.appear(1000, 100);

    },
    async fetchData(yearRange) {
      try {
        console.log(`Fetching data for year range: ${yearRange}`);
        return new Promise((resolve) => {
          setTimeout(() => {
            resolve([
              {id: "AF", value: Math.floor(Math.random() * 50)},
              {id: "AL", value: Math.floor(Math.random() * 50)},
              {id: "DZ", value: Math.floor(Math.random() * 50)},
              {id: "AD", value: Math.floor(Math.random() * 50)},
              {id: "AO", value: Math.floor(Math.random() * 50)},
              {id: "AG", value: Math.floor(Math.random() * 50)},
              {id: "AR", value: Math.floor(Math.random() * 50)},
              {id: "AM", value: Math.floor(Math.random() * 50)},
              {id: "AU", value: Math.floor(Math.random() * 50)},
              {id: "AT", value: Math.floor(Math.random() * 50)},
              {id: "AZ", value: Math.floor(Math.random() * 50)},
              {id: "BS", value: Math.floor(Math.random() * 50)},
              {id: "BH", value: Math.floor(Math.random() * 50)},
              {id: "BD", value: Math.floor(Math.random() * 50)},
              {id: "BB", value: Math.floor(Math.random() * 50)},
              {id: "BY", value: Math.floor(Math.random() * 50)},
              {id: "BE", value: Math.floor(Math.random() * 50)},
              {id: "BZ", value: Math.floor(Math.random() * 50)},
              {id: "BJ", value: Math.floor(Math.random() * 50)},
              {id: "BT", value: Math.floor(Math.random() * 50)},
              {id: "BO", value: Math.floor(Math.random() * 50)},
              {id: "BA", value: Math.floor(Math.random() * 50)},
              {id: "BW", value: Math.floor(Math.random() * 50)},
              {id: "BR", value: Math.floor(Math.random() * 50)},
              {id: "BN", value: Math.floor(Math.random() * 50)},
              {id: "BG", value: Math.floor(Math.random() * 50)},
              {id: "BF", value: Math.floor(Math.random() * 50)},
              {id: "BI", value: Math.floor(Math.random() * 50)},
              {id: "KH", value: Math.floor(Math.random() * 50)},
              {id: "CM", value: Math.floor(Math.random() * 50)},
              {id: "CA", value: Math.floor(Math.random() * 50)},
              {id: "CV", value: Math.floor(Math.random() * 50)},
              {id: "CF", value: Math.floor(Math.random() * 50)},
              {id: "TD", value: Math.floor(Math.random() * 50)},
              {id: "CL", value: Math.floor(Math.random() * 50)},
              {id: "CN", value: Math.floor(Math.random() * 50)},
              {id: "CO", value: Math.floor(Math.random() * 50)},
              {id: "KM", value: Math.floor(Math.random() * 50)},
              {id: "KP", value: Math.floor(Math.random() * 50)},
              {id: "CG", value: Math.floor(Math.random() * 50)},
              {id: "CD", value: Math.floor(Math.random() * 50)},
              {id: "CR", value: Math.floor(Math.random() * 50)},
              {id: "CI", value: Math.floor(Math.random() * 50)},
              {id: "HR", value: Math.floor(Math.random() * 50)},
              {id: "CU", value: Math.floor(Math.random() * 50)},
              {id: "CY", value: Math.floor(Math.random() * 50)},
              {id: "CZ", value: Math.floor(Math.random() * 50)},
              {id: "DK", value: Math.floor(Math.random() * 50)},
              {id: "DJ", value: Math.floor(Math.random() * 50)},
              {id: "DM", value: Math.floor(Math.random() * 50)},
              {id: "DO", value: Math.floor(Math.random() * 50)},
              {id: "EC", value: Math.floor(Math.random() * 50)},
              {id: "EG", value: Math.floor(Math.random() * 50)},
              {id: "SV", value: Math.floor(Math.random() * 50)},
              {id: "GQ", value: Math.floor(Math.random() * 50)},
              {id: "ER", value: Math.floor(Math.random() * 50)},
              {id: "EE", value: Math.floor(Math.random() * 50)},
              {id: "ET", value: Math.floor(Math.random() * 50)},
              {id: "FJ", value: Math.floor(Math.random() * 50)},
              {id: "FI", value: Math.floor(Math.random() * 50)},
              {id: "FR", value: Math.floor(Math.random() * 50)},
              {id: "GA", value: Math.floor(Math.random() * 50)},
              {id: "GM", value: Math.floor(Math.random() * 50)},
              {id: "GE", value: Math.floor(Math.random() * 50)},
              {id: "DE", value: Math.floor(Math.random() * 50)},
              {id: "GH", value: Math.floor(Math.random() * 50)},
              {id: "GR", value: Math.floor(Math.random() * 50)},
              {id: "GD", value: Math.floor(Math.random() * 50)},
              {id: "GT", value: Math.floor(Math.random() * 50)},
              {id: "GN", value: Math.floor(Math.random() * 50)},
              {id: "GW", value: Math.floor(Math.random() * 50)},
              {id: "GY", value: Math.floor(Math.random() * 50)},
              {id: "HT", value: Math.floor(Math.random() * 50)},
              {id: "HN", value: Math.floor(Math.random() * 50)},
              {id: "HU", value: Math.floor(Math.random() * 50)},
              {id: "IS", value: Math.floor(Math.random() * 50)},
              {id: "IN", value: Math.floor(Math.random() * 50)},
              {id: "ID", value: Math.floor(Math.random() * 50)},
              {id: "IR", value: Math.floor(Math.random() * 50)},
              {id: "IQ", value: Math.floor(Math.random() * 50)},
              {id: "IE", value: Math.floor(Math.random() * 50)},
              {id: "IL", value: Math.floor(Math.random() * 50)},
              {id: "IT", value: Math.floor(Math.random() * 50)},
              {id: "JM", value: Math.floor(Math.random() * 50)},
              {id: "JP", value: Math.floor(Math.random() * 50)},
              {id: "JO", value: Math.floor(Math.random() * 50)},
              {id: "KZ", value: Math.floor(Math.random() * 50)},
              {id: "KE", value: Math.floor(Math.random() * 50)},
              {id: "KI", value: Math.floor(Math.random() * 50)},
              {id: "KR", value: Math.floor(Math.random() * 50)},
              {id: "KW", value: Math.floor(Math.random() * 50)},
              {id: "KG", value: Math.floor(Math.random() * 50)},
              {id: "LA", value: Math.floor(Math.random() * 50)},
              {id: "LV", value: Math.floor(Math.random() * 50)},
              {id: "LB", value: Math.floor(Math.random() * 50)},
              {id: "LS", value: Math.floor(Math.random() * 50)},
              {id: "LR", value: Math.floor(Math.random() * 50)},
              {id: "LY", value: Math.floor(Math.random() * 50)},
              {id: "LT", value: Math.floor(Math.random() * 50)},
              {id: "LU", value: Math.floor(Math.random() * 50)},
              {id: "MG", value: Math.floor(Math.random() * 50)},
              {id: "MW", value: Math.floor(Math.random() * 50)},
              {id: "MY", value: Math.floor(Math.random() * 50)},
              {id: "MV", value: Math.floor(Math.random() * 50)},
              {id: "ML", value: Math.floor(Math.random() * 50)},
              {id: "MT", value: Math.floor(Math.random() * 50)},
              {id: "MR", value: Math.floor(Math.random() * 50)},
              {id: "MU", value: Math.floor(Math.random() * 50)},
              {id: "MX", value: Math.floor(Math.random() * 50)},
              {id: "MD", value: Math.floor(Math.random() * 50)},
              {id: "MN", value: Math.floor(Math.random() * 50)},
              {id: "ME", value: Math.floor(Math.random() * 50)},
              {id: "MA", value: Math.floor(Math.random() * 50)},
              {id: "MZ", value: Math.floor(Math.random() * 50)},
              {id: "MM", value: Math.floor(Math.random() * 50)},
              {id: "NA", value: Math.floor(Math.random() * 50)},
              {id: "NP", value: Math.floor(Math.random() * 50)},
              {id: "NL", value: Math.floor(Math.random() * 50)},
              {id: "NZ", value: Math.floor(Math.random() * 50)},
              {id: "NI", value: Math.floor(Math.random() * 50)},
              {id: "NE", value: Math.floor(Math.random() * 50)},
              {id: "NG", value: Math.floor(Math.random() * 50)},
              {id: "NO", value: Math.floor(Math.random() * 50)},
              {id: "OM", value: Math.floor(Math.random() * 50)},
              {id: "PK", value: Math.floor(Math.random() * 50)},
              {id: "PA", value: Math.floor(Math.random() * 50)},
              {id: "PG", value: Math.floor(Math.random() * 50)},
              {id: "PY", value: Math.floor(Math.random() * 50)},
              {id: "PE", value: Math.floor(Math.random() * 50)},
              {id: "PH", value: Math.floor(Math.random() * 50)},
              {id: "PL", value: Math.floor(Math.random() * 50)},
              {id: "PT", value: Math.floor(Math.random() * 50)},
              {id: "QA", value: Math.floor(Math.random() * 50)},
              {id: "RO", value: Math.floor(Math.random() * 50)},
              {id: "RU", value: Math.floor(Math.random() * 50)},
              {id: "RW", value: Math.floor(Math.random() * 50)},
              {id: "KN", value: Math.floor(Math.random() * 50)},
              {id: "LC", value: Math.floor(Math.random() * 50)},
              {id: "VC", value: Math.floor(Math.random() * 50)},
              {id: "WS", value: Math.floor(Math.random() * 50)},
              {id: "SM", value: Math.floor(Math.random() * 50)},
              {id: "ST", value: Math.floor(Math.random() * 50)},
              {id: "SA", value: Math.floor(Math.random() * 50)},
              {id: "SN", value: Math.floor(Math.random() * 50)},
              {id: "RS", value: Math.floor(Math.random() * 50)},
              {id: "SC", value: Math.floor(Math.random() * 50)},
              {id: "SL", value: Math.floor(Math.random() * 50)},
              {id: "SG", value: Math.floor(Math.random() * 50)},
              {id: "SK", value: Math.floor(Math.random() * 50)},
              {id: "SI", value: Math.floor(Math.random() * 50)},
              {id: "SB", value: Math.floor(Math.random() * 50)},
              {id: "SO", value: Math.floor(Math.random() * 50)},
              {id: "ZA", value: Math.floor(Math.random() * 50)},
              {id: "SS", value: Math.floor(Math.random() * 50)},
              {id: "ES", value: Math.floor(Math.random() * 50)},
              {id: "LK", value: Math.floor(Math.random() * 50)},
              {id: "SD", value: Math.floor(Math.random() * 50)},
              {id: "SR", value: Math.floor(Math.random() * 50)},
              {id: "SE", value: Math.floor(Math.random() * 50)},
              {id: "CH", value: Math.floor(Math.random() * 50)},
              {id: "SY", value: Math.floor(Math.random() * 50)},
              {id: "TJ", value: Math.floor(Math.random() * 50)},
              {id: "TZ", value: Math.floor(Math.random() * 50)},
              {id: "TH", value: Math.floor(Math.random() * 50)},
              {id: "TL", value: Math.floor(Math.random() * 50)},
              {id: "TW", value: Math.floor(Math.random() * 50)},
              {id: "TG", value: Math.floor(Math.random() * 50)},
              {id: "TO", value: Math.floor(Math.random() * 50)},
              {id: "TT", value: Math.floor(Math.random() * 50)},
              {id: "TN", value: Math.floor(Math.random() * 50)},
              {id: "TR", value: Math.floor(Math.random() * 50)},
              {id: "TM", value: Math.floor(Math.random() * 50)},
              {id: "UG", value: Math.floor(Math.random() * 50)},
              {id: "UA", value: Math.floor(Math.random() * 50)},
              {id: "AE", value: Math.floor(Math.random() * 50)},
              {id: "GB", value: Math.floor(Math.random() * 50)},
              {id: "US", value: Math.floor(Math.random() * 50)},
              {id: "UY", value: Math.floor(Math.random() * 50)},
              {id: "UZ", value: Math.floor(Math.random() * 50)},
              {id: "VU", value: Math.floor(Math.random() * 50)},
              {id: "VE", value: Math.floor(Math.random() * 50)},
              {id: "VN", value: Math.floor(Math.random() * 50)},
              {id: "YE", value: Math.floor(Math.random() * 50)},
              {id: "ZM", value: Math.floor(Math.random() * 50)},
              {id: "ZW", value: Math.floor(Math.random() * 50)},
            ]);
          }, 500);
        });
      } catch (error) {
        console.error("Error fetching data for year range:", error);
        return [];
      }
    },
    async updateData(yearRange) {
      console.log("inside updateDataForYearRane");
      const data = await this.fetchData(yearRange);
      if (this.polygonSeries) {
        this.polygonSeries.data.setAll(data);
      }
    },
  },
  props: {
    yearRange: {
      type: Array,
      required: true,
      default: () => [1896, 2022]
    },
    event: {
      type: String,
    },
    sport: {
      type: String,
    },
  },
  watch: {
    $props: {
      handler(newProps) {
        const { sport, event, yearRange } = newProps;
        if (sport && event && yearRange) {
          this.updateData(yearRange);
        }
      },
      deep: true,
    },
  },
};
</script>

<style scoped>
#medal-map {
  width: 100%;
  height: 100%;
}
</style>
