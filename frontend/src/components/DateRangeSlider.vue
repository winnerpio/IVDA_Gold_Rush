<template>
  <div class="range-slider">
    <input
        type="number"
        class="input-box left-input"
        v-model.number="tempMinValue"
        @blur="updateSliderValue('min')"
        @keyup.enter="handleEnter('min', $event)"
    :min="minYear"
    :max="maxValue"
    />
    <div class="slider-container">
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
    </div>
    <input
        type="number"
        class="input-box right-input"
        v-model.number="tempMaxValue"
        @blur="updateSliderValue('max')"
        @keyup.enter="handleEnter('max', $event)"
    :min="minValue"
    :max="maxYear"
    />
  </div>
</template>

<script>
export default {
  props: {
    minYear: {
      type: Number,
      default: 1896,
    },
    maxYear: {
      type: Number,
      default: 2022,
    },
    initialRange: {
      type: Array,
      default: () => [1896, 2022],
      validator: (value) => value.length === 2 && value[0] <= value[1],
    },
  },
  data() {
    return {
      minValue: this.initialRange[0],
      maxValue: this.initialRange[1],
      tempMinValue: this.initialRange[0],
      tempMaxValue: this.initialRange[1],
      isDragging: false,
      draggingThumb: null,
      debounceTimer: null,
      debounceDelay: 300, // Time (ms) before emitting the update event
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
    handleEnter(type, event) {
      this.updateSliderValue(type);
      event.target.blur(); // Removes focus from the textbox
    },
    startDrag(thumb) {
      this.isDragging = true;
      this.draggingThumb = thumb;
      document.addEventListener("mousemove", this.handleDrag);
      document.addEventListener("mouseup", this.stopDrag);
    },
    handleDrag(event) {
      if (!this.isDragging) return;

      const slider = this.$el.querySelector(".slider-container").getBoundingClientRect();
      const percentage = ((event.clientX - slider.left) / slider.width) * 100;
      const yearValue =
          Math.round((percentage / 100) * (this.maxYear - this.minYear)) +
          this.minYear;

      if (this.draggingThumb === "min") {
        this.minValue = Math.min(
            Math.max(this.minYear, yearValue),
            this.maxValue
        );
        this.tempMinValue = this.minValue;
      } else if (this.draggingThumb === "max") {
        this.maxValue = Math.max(
            Math.min(this.maxYear, yearValue),
            this.minValue
        );
        this.tempMaxValue = this.maxValue;
      }

      this.debounceEmitRange();
    },
    stopDrag() {
      this.isDragging = false;
      this.draggingThumb = null;
      document.removeEventListener("mousemove", this.handleDrag);
      document.removeEventListener("mouseup", this.stopDrag);
    },
    updateSliderValue(type) {
      if (type === "min") {
        if (this.tempMinValue < this.minYear) {
          this.tempMinValue = this.minYear;
        } else if (this.tempMinValue > this.maxValue) {
          this.tempMinValue = this.maxValue;
        }
        this.minValue = this.tempMinValue;
      } else if (type === "max") {
        if (this.tempMaxValue > this.maxYear) {
          this.tempMaxValue = this.maxYear;
        } else if (this.tempMaxValue < this.minValue) {
          this.tempMaxValue = this.minValue;
        }
        this.maxValue = this.tempMaxValue;
      }
      this.debounceEmitRange();
    },
    debounceEmitRange() {
      clearTimeout(this.debounceTimer);
      this.debounceTimer = setTimeout(() => {
        this.emitRange();
      }, this.debounceDelay);
    },
    emitRange() {
      this.$emit("update:range", [this.minValue, this.maxValue]);
    },
  },
};
</script>


<style scoped>
.range-slider {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
}

.slider-container {
  flex: 1;
  position: relative;
  height: 50px;
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

.input-box {
  width: 80px;
  padding: 8px;
  font-size: 16px;
  text-align: center;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.left-input {
  margin-right: 10px;
}

.right-input {
  margin-left: 10px;
}
</style>
