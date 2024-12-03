<template>
  <div class="layout-container">
    <div>
      <h2 v-if="computedSelectedCountry && computedSelectedCountry.name">
        {{ computedSelectedCountry.name }} Athlete Attribute Distribution
      </h2>
      <h2 v-else>Athlete Attribute Distribution</h2>
    </div>
    <!-- Attribute Selection -->
    <div class="attribute-selection">
      <label v-for="attribute in attributes" :key="attribute.value">
        <input
          type="radio"
          :value="attribute.value"
          v-model="selectedAttribute"
        />
        {{ attribute.label }}
      </label>
    </div>

    <!-- Main Graph -->
    <div class="graph-container" ref="chartDiv"></div>
  </div>
</template>

<script>
import * as am5 from "@amcharts/amcharts5";
import * as am5xy from "@amcharts/amcharts5/xy";
import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";
import { onMounted, onBeforeUnmount, ref, watch, computed } from "vue";

export default {
  name: "AthleteAttributeDistribution",
  props: {
    dateRange: {
      type: Array,
      default: () => [1896, 2023],
    },
    distributionData: {
      type: Object,
      required: true,
    },
    selectedCountry: {
      type: Object,
      default: () => ({}),
    },
    selectedDistVariable: {
      type: String,
      required: true,
    },
  },
  setup(props, { emit }) {
    const chartDiv = ref(null);
    let chartRoot = null;
    let chart = null;
    let xAxis = null;
    let yAxisAthletes = null;
    let yAxisMedals = null;
    let isChartInitialized = false;

    const attributes = [
      { value: "age", label: "Age" },
      { value: "weight", label: "Weight" },
      { value: "height", label: "Height" },
      { value: "bmi", label: "BMI" },
      { value: "h2w", label: "Height-to-Weight Ratio" },
    ];

    const selectedAttribute = ref(props.selectedDistVariable);

    // Watch for changes in props.selectedDistVariable
    watch(
      () => props.selectedDistVariable,
      (newVal) => {
        selectedAttribute.value = newVal;
      }
    );

    // Emit changes when the selected attribute changes
    watch(selectedAttribute, (newVal) => {
      emit("update:distVariable", newVal);
    });

    watch(
      () => props.selectedCountry,
      () => {
        if (isChartInitialized) {
          updateChartData();
        }
      },
      { immediate: true }
    );

    // Update chart when distribution data changes
    watch(
      () => props.distributionData,
      () => {
        if (isChartInitialized) {
          updateChartData();
        }
      },
      { immediate: true, deep: true }
    );

    const createChart = () => {
      if (isChartInitialized) return;
      if (!chartDiv.value) {
        console.error("Chart container element not found!");
        return;
      }
      chartRoot = am5.Root.new(chartDiv.value);
      chartRoot.setThemes([am5themes_Animated.new(chartRoot)]);

      chart = chartRoot.container.children.push(
        am5xy.XYChart.new(chartRoot, {
          panX: false,
          panY: false,
          wheelX: "none",
          wheelY: "none",
        })
      );

      // Create X-axis
      xAxis = chart.xAxes.push(
        am5xy.CategoryAxis.new(chartRoot, {
          categoryField: "group",
          renderer: am5xy.AxisRendererX.new(chartRoot, {
            minGridDistance: 30,
          }),
          tooltip: am5.Tooltip.new(chartRoot, {}),
        })
      );

      // Create Y-axes
      yAxisAthletes = chart.yAxes.push(
        am5xy.ValueAxis.new(chartRoot, {
          renderer: am5xy.AxisRendererY.new(chartRoot, {}),
          min: 0,
          extraMax: 0.1,
          tooltip: am5.Tooltip.new(chartRoot, {}),
        })
      );

      yAxisMedals = chart.yAxes.push(
        am5xy.ValueAxis.new(chartRoot, {
          renderer: am5xy.AxisRendererY.new(chartRoot, { opposite: true }),
          min: 0,
          extraMax: 0.1,
          syncWithAxis: yAxisAthletes,
          tooltip: am5.Tooltip.new(chartRoot, {}),
        })
      );

      // Create histogram series for athlete counts
      chart.series.push(
        am5xy.ColumnSeries.new(chartRoot, {
          name: "Number of Athletes",
          xAxis: xAxis,
          yAxis: yAxisAthletes,
          valueYField: "athlete_count",
          categoryXField: "group",
          tooltip: am5.Tooltip.new(chartRoot, {
            labelText: "{name}\n{categoryX}: {valueY}",
          }),
        })
      );

      // Create line series for medal counts
      const medalSeries = chart.series.push(
        am5xy.LineSeries.new(chartRoot, {
          name: "Medal Count",
          xAxis: xAxis,
          yAxis: yAxisMedals,
          valueYField: "medal_count",
          categoryXField: "group",
          stroke: am5.color(0xff0000),
          tooltip: am5.Tooltip.new(chartRoot, {
            labelText: "{name}\n{categoryX}: {valueY}",
          }),
        })
      );

      medalSeries.strokes.template.setAll({ strokeWidth: 2 });
      medalSeries.bullets.push(() =>
        am5.Bullet.new(chartRoot, {
          sprite: am5.Circle.new(chartRoot, {
            radius: 5,
            fill: medalSeries.get("fill"),
          }),
        })
      );

      // Add legend
      chart.children.push(
        am5.Legend.new(chartRoot, {
          centerX: am5.percent(50),
          x: am5.percent(50),
        })
      );

      // Add cursor
      chart.set("cursor", am5xy.XYCursor.new(chartRoot, {}));

      isChartInitialized = true;
    };

    const updateChartData = () => {
      if (!isChartInitialized || !chart) return;

      const data = computeChartData();

      if (xAxis) {
        xAxis.data.setAll(data);
      }

      chart.series.each((series) => {
        series.data.setAll(data);
      });
    };

    const computeChartData = () => {
      const attributeGroups = Object.keys(props.distributionData || {});
      return attributeGroups.map((group) => {
        const groupData = props.distributionData[group] || {};
        return {
          group,
          athlete_count: groupData.athlete_count || 0,
          medal_count: groupData.medal_count || 0,
        };
      });
    };

    onMounted(() => {
      watch(
        () => chartDiv.value,
        (newVal) => {
          console.log("chartDiv.value changed:", newVal);
          if (newVal) {
            createChart();
            updateChartData();
          }
        },
        { immediate: true }
      );
    });

    onBeforeUnmount(() => {
      if (chartRoot) {
        chartRoot.dispose();
        chartRoot = null;
        isChartInitialized = false;
      }
    });

    return {
      chartDiv,
      attributes,
      selectedAttribute,
      computedSelectedCountry: computed(() => props.selectedCountry),
    };
  },
};
</script>

<style scoped>
.layout-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
}

.layout-container > div > h2 {
  text-align: center;
  margin-bottom: 20px;
}

.attribute-selection {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}

.attribute-selection label {
  font-size: 18px;
  margin-right: 15px;
}

.graph-container {
  flex: 1;
  min-height: 400px;
}
</style>
