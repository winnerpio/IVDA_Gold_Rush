<template>
  <v-container>
    <v-col cols="12">
      <v-card outlined class="pa-0" fill-height>
        <v-card-title>{{ country }} Medal History </v-card-title>
        <v-card-text class="pa-0">
          <div id="chartdiv" style="width: 100%; height: 700px;"></div>
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
      series: null,
    }
  },
  mounted() {
    this.root = am5.Root.new("chartdiv");

    this.root.setThemes([
      am5themes_Animated.new(this.root)
    ]);



    let chart = this.root.container.children.push(am5radar.RadarChart.new(this.root, {
      panX: false,
      panY: false,
      wheelX: "none",
      wheelY: "none",
      startAngle: -84,
      endAngle: 264,
      innerRadius: am5.percent(40)
    }));



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
      categoryField: "category",
      renderer: xRenderer
    }));

    let yRenderer = am5radar.AxisRendererRadial.new(this.root, {});
    yRenderer.labels.template.set("centerX", am5.p50);

    let yAxis = chart.yAxes.push(am5xy.ValueAxis.new(this.root, {
      maxDeviation: 0.3,
      min: 0,
      renderer: yRenderer
    }));

    let series = chart.series.push(am5radar.RadarColumnSeries.new(this.root, {
      name: "Series 1",
      sequencedInterpolation: true,
      xAxis: xAxis,
      yAxis: yAxis,
      valueYField: "value",
      categoryXField: "category"
    }));

    series.columns.template.setAll({
      cornerRadius: 5,
      tooltipText: "{categoryX}: {valueY}"
    });

    series.columns.template.adapters.add("fill", function (fill, target) {
      return chart.get("colors").getIndex(series.columns.indexOf(target));
    });

    series.columns.template.adapters.add("stroke", function (stroke, target) {
      return chart.get("colors").getIndex(series.columns.indexOf(target));
    });


    let data = [];

    for (let i = 1; i < 21; i++) {
      data.push({ category: i, value: Math.round(Math.random() * 100) });
    }

    xAxis.data.setAll(data);
    series.data.setAll(data);

    series.appear(1000);
    chart.appear(1000, 100);
  },
  beforeUnmount() {
    if (this.chart) {
      this.chart.dispose();
    }
  },
};
</script>

<style scoped>

</style>