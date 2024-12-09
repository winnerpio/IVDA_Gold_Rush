<template>
  <div class="layout-container" style="width: 100%; height: 35vh;">
    <!-- Header -->
    <div class="header" style="text-align: center; margin-bottom: 8px;">
      <h2>Medal Map</h2>
    </div>

    <div class="graph-container" style="width: 100%; height: calc(100% - 48px);">
      <div id="medal-map" style="width: 100%; height: 100%;"></div>
    </div>
  </div>
</template>

<script>
import * as am5 from "@amcharts/amcharts5";
import * as am5map from "@amcharts/amcharts5/map";
import am5geodata_worldLow from "@amcharts/amcharts5-geodata/worldLow";
import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";

export default {
  name: "MedalSuccessMap",
  data() {
    return {
      chart: null,
      polygonSeries: null,
    };
  },
  mounted() {
    this.initChart();
    this.updateChartData();
  },
  beforeUnmount() {
    if (this.root) {
      this.root.dispose();
    }
  },
  methods: {
    initChart() {
      if (this.root) return;

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

      chart.appear(1000, 100);
    },
    updateChartData() {
      const filteredData = this.getFilteredData();
      if (this.polygonSeries) {
        this.polygonSeries.data.setAll(filteredData);
      } else {
        console.warn("Polygon series not initialized yet.");
      }
    },
    getFilteredData() {
      const rawData = this.data;

      if (!rawData || typeof rawData !== "object") {
        console.warn("Invalid or missing data.");
        return [];
      }

      return Object.entries(rawData).map(([countryCode, data]) => ({
        id: countryCode,
        value: data.all?.total || 0,
      }));
    },
  },
  props: {
    data: {
      type: Object,
      default: () => ({}),
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
#medal-map {
  width: 100%;
  height: 100%;
}

.fill-height {
  height: 100%;
}
</style>
