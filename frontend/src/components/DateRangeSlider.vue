<template>
  <div class="range-slider">
    <div class="slider-track"></div>
    <div
        class="slider-range"
        :style="{ left: rangeLeft + '%', width: rangeWidth + '%' }"
    ></div>
    <div
        class="slider-thumb left"
        :style="{ left: rangeLeft + '%' }"
        @mousedown="startDrag('min')"
    ></div>
    <div
        class="slider-thumb right"
        :style="{ left: rangeRight + '%' }"
        @mousedown="startDrag('max')"
    ></div>
    <div class="slider-labels">
      <span class="label-left" :style="{ left: rangeLeft + '%' }">
        {{ minValue }}
      </span>
      <span class="label-right" :style="{ left: rangeRight + '%' }">
        {{ maxValue }}
      </span>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    minYear: {
      type: Number,
      default: 1900,
    },
    maxYear: {
      type: Number,
      default: 2023,
    },
    initialRange: {
      type: Array,
      default: () => [1900, 2023],
    },
  },
  data() {
    return {
      minValue: this.initialRange[0],
      maxValue: this.initialRange[1],
      isDragging: false,
      draggingThumb: null,
    };
  },
  computed: {
    rangeLeft() {
      return ((this.minValue - this.minYear) / (this.maxYear - this.minYear)) * 100;
    },
    rangeRight() {
      return ((this.maxValue - this.minYear) / (this.maxYear - this.minYear)) * 100;
    },
    rangeWidth() {
      return this.rangeRight - this.rangeLeft;
    },
  },
  methods: {
    startDrag(thumb) {
      this.isDragging = true;
      this.draggingThumb = thumb;
      document.addEventListener('mousemove', this.handleDrag);
      document.addEventListener('mouseup', this.stopDrag);
    },
    handleDrag(event) {
      if (!this.isDragging) return;

      const slider = this.$el.getBoundingClientRect();
      const percentage = ((event.clientX - slider.left) / slider.width) * 100;
      const yearValue =
          Math.round((percentage / 100) * (this.maxYear - this.minYear)) + this.minYear;

      if (this.draggingThumb === 'min') {
        this.minValue = Math.min(
            Math.max(this.minYear, yearValue),
            this.maxValue
        );
      } else if (this.draggingThumb === 'max') {
        this.maxValue = Math.max(
            Math.min(this.maxYear, yearValue),
            this.minValue
        );
      }

      this.$emit('update:range', [this.minValue, this.maxValue]);
    },
    stopDrag() {
      this.isDragging = false;
      this.draggingThumb = null;
      document.removeEventListener('mousemove', this.handleDrag);
      document.removeEventListener('mouseup', this.stopDrag);
    },
  },
};
</script>

<style scoped>
.range-slider {
  position: relative;
  width: 100%;
  height: 50px;
  margin: 20px 0;
}
.slider-track {
  position: absolute;
  top: 50%;
  left: 0;
  width: 100%;
  height: 4px;
  background-color: #ddd;
  transform: translateY(-50%);
}
.slider-range {
  position: absolute;
  top: 50%;
  height: 4px;
  background-color: #2196f3;
  transform: translateY(-50%);
}
.slider-thumb {
  position: absolute;
  top: 50%;
  width: 16px;
  height: 16px;
  background-color: #2196f3;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  cursor: pointer;
}
.slider-labels {
  position: relative;
  margin-top: 10px;
}

.label-right, .label-left {
  position: absolute;
  top: 35px;
  transform: translateX(-50%);
  white-space: nowrap;
  font-size: 12px;
  color: #333;
}

.label-left {
  left: 0;
}

.label-right {
  left: calc(100% - 16px);
  transform: translateX(-50%);
}
</style>
