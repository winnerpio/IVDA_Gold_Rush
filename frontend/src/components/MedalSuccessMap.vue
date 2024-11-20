<template>
  <v-container>
    <v-row>
      <!-- Heatmap Display Panel -->
      <v-col cols="12" md="12">
        <v-card outlined class="pa-0" fill-height>
          <v-card-title>Medal Success Map</v-card-title>
          <v-card-text class="pa-0">
            <div id="medal-map" style="width: 100%; height: 700px;"></div>
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
  mounted() {
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
          calculateAggregates: true
        })
    );

    polygonSeries.mapPolygons.template.adapters.add("tooltipText", function (text, target) {
      const value = target.dataItem?.dataContext.value;
      return value === undefined ? "{name}: NA" : "{name}: {value} medals";
    });

    polygonSeries.mapPolygons.template.events.on("click", (event) => {
      const polygon = event.target;
      const countryName = polygon._dataItem.dataContext.name;
      const countryCode = polygon._dataItem.dataContext.id;
      this.$emit("country-selected", { countryName, countryCode });
    });


    polygonSeries.mapPolygons.template.set("interactive", true);

    // Define heat rules
    polygonSeries.set("heatRules", [
      {
        target: polygonSeries.mapPolygons.template,
        dataField: "value",
        min: am5.color(0xb3d9ff),
        max: am5.color(0x8b0000),
        key: "fill",
      },
    ]);

    polygonSeries.data.setAll([
      {id: "AF", value: 10},
      {id: "AL", value: 12},
      {id: "DZ", value: 25},
      {id: "AD", value: 5},
      {id: "AO", value: 8},
      {id: "AG", value: 2},
      {id: "AR", value: 60},
      {id: "AM", value: 15},
      {id: "AU", value: 75},
      {id: "AT", value: 35},
      {id: "AZ", value: 20},
      {id: "BS", value: 10},
      {id: "BH", value: 5},
      {id: "BD", value: 18},
      {id: "BB", value: 3},
      {id: "BY", value: 28},
      {id: "BE", value: 42},
      {id: "BZ", value: 7},
      {id: "BJ", value: 6},
      {id: "BT", value: 1},
      {id: "BO", value: 9},
      {id: "BA", value: 13},
      {id: "BW", value: 4},
      {id: "BR", value: 70},
      {id: "BN", value: 3},
      {id: "BG", value: 32},
      {id: "BF", value: 5},
      {id: "BI", value: 4},
      {id: "KH", value: 8},
      {id: "CM", value: 14},
      {id: "CA", value: 110},
      {id: "CV", value: 2},
      {id: "CF", value: 1},
      {id: "TD", value: 6},
      {id: "CL", value: 23},
      {id: "CN", value: 178},
      {id: "CO", value: 47},
      {id: "KM", value: 1},
      {id: "KP", value: 3},
      {id: "CG", value: 6},
      {id: "CD", value: 12},
      {id: "CR", value: 5},
      {id: "CI", value: 9},
      {id: "HR", value: 34},
      {id: "CU", value: 29},
      {id: "CY", value: 8},
      {id: "CZ", value: 45},
      {id: "DK", value: 40},
      {id: "DJ", value: 2},
      {id: "DM", value: 1},
      {id: "DO", value: 16},
      {id: "EC", value: 18},
      {id: "EG", value: 50},
      {id: "SV", value: 7},
      {id: "GQ", value: 2},
      {id: "ER", value: 3},
      {id: "EE", value: 20},
      {id: "ET", value: 15},
      {id: "FJ", value: 4},
      {id: "FI", value: 35},
      {id: "FR", value: 140},
      {id: "GA", value: 6},
      {id: "GM", value: 1},
      {id: "GE", value: 12},
      {id: "DE", value: 150},
      {id: "GH", value: 18},
      {id: "GR", value: 55},
      {id: "GD", value: 2},
      {id: "GT", value: 9},
      {id: "GN", value: 5},
      {id: "GW", value: 2},
      {id: "GY", value: 3},
      {id: "HT", value: 4},
      {id: "HN", value: 7},
      {id: "HU", value: 48},
      {id: "IS", value: 6},
      {id: "IN", value: 130},
      {id: "ID", value: 60},
      {id: "IR", value: 65},
      {id: "IQ", value: 20},
      {id: "IE", value: 25},
      {id: "IL", value: 30},
      {id: "IT", value: 120},
      {id: "JM", value: 12},
      {id: "JP", value: 97},
      {id: "JO", value: 5},
      {id: "KZ", value: 22},
      {id: "KE", value: 45},
      {id: "KI", value: 1},
      {id: "KR", value: 45},
      {id: "KW", value: 8},
      {id: "KG", value: 7},
      {id: "LA", value: 3},
      {id: "LV", value: 18},
      {id: "LB", value: 10},
      {id: "LS", value: 2},
      {id: "LR", value: 2},
      {id: "LY", value: 6},
      {id: "LT", value: 21},
      {id: "LU", value: 4},
      {id: "MG", value: 3},
      {id: "MW", value: 2},
      {id: "MY", value: 32},
      {id: "MV", value: 1},
      {id: "ML", value: 3},
      {id: "MT", value: 4},
      {id: "MR", value: 2},
      {id: "MU", value: 3},
      {id: "MX", value: 55},
      {id: "MD", value: 8},
      {id: "MN", value: 6},
      {id: "ME", value: 4},
      {id: "MA", value: 30},
      {id: "MZ", value: 3},
      {id: "MM", value: 5},
      {id: "NA", value: 2},
      {id: "NP", value: 5},
      {id: "NL", value: 85},
      {id: "NZ", value: 35},
      {id: "NI", value: 3},
      {id: "NE", value: 2},
      {id: "NG", value: 45},
      {id: "NO", value: 33},
      {id: "OM", value: 5},
      {id: "PK", value: 40},
      {id: "PA", value: 7},
      {id: "PG", value: 2},
      {id: "PY", value: 6},
      {id: "PE", value: 17},
      {id: "PH", value: 32},
      {id: "PL", value: 53},
      {id: "PT", value: 25},
      {id: "QA", value: 4},
      {id: "RO", value: 40},
      {id: "RU", value: 160},
      {id: "RW", value: 2},
      {id: "KN", value: 1},
      {id: "LC", value: 1},
      {id: "VC", value: 1},
      {id: "WS", value: 2},
      {id: "SM", value: 3},
      {id: "ST", value: 1},
      {id: "SA", value: 20},
      {id: "SN", value: 10},
      {id: "RS", value: 20},
      {id: "SC", value: 1},
      {id: "SL", value: 3},
      {id: "SG", value: 12},
      {id: "SK", value: 22},
      {id: "SI", value: 18},
      {id: "SB", value: 1},
      {id: "SO", value: 1},
      {id: "ZA", value: 50},
      {id: "SS", value: 1},
      {id: "ES", value: 90},
      {id: "LK", value: 10},
      {id: "SD", value: 3},
      {id: "SR", value: 1},
      {id: "SE", value: 60},
      {id: "CH", value: 33},
      {id: "SY", value: 8},
      {id: "TJ", value: 2},
      {id: "TZ", value: 5},
      {id: "TH", value: 45},
      {id: "TL", value: 1},
      {id: "TW", value: 15},
      {id: "TG", value: 2},
      {id: "TO", value: 1},
      {id: "TT", value: 9},
      {id: "TN", value: 12},
      {id: "TR", value: 85},
      {id: "TM", value: 3},
      {id: "UG", value: 7},
      {id: "UA", value: 52},
      {id: "AE", value: 10},
      {id: "GB", value: 140},
      {id: "US", value: 200},
      {id: "UY", value: 15},
      {id: "UZ", value: 25},
      {id: "VU", value: 1},
      {id: "VE", value: 25},
      {id: "VN", value: 35},
      {id: "YE", value: 1},
      {id: "ZM", value: 6},
      {id: "ZW", value: 8},
    ]);

    polygonSeries.mapPolygons.template.adapters.add("fill", function (fill, target) {
      return target.dataItem?.dataContext.value === undefined ? am5.color(0xCCCCCC) : fill;
    });
  },
  beforeUnmount() {
    if (this.root) {
      this.root.dispose();
    }
  },
};
</script>

<style scoped>
#medal-map {
  width: 100%;
  height: 100%;
}
</style>
