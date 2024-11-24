<template>
  <div class="range-slider">
    <h2>Select Year Range</h2>
    <!-- Min Year Input -->
    <input
        type="number"
        class="input-box"
        v-model.number="tempMinValue"
        @blur="updateSliderValue('min')"
        @keyup.enter="handleEnter('min', $event)"
        :min="minYear"
        :max="maxValue"
        placeholder="Start Year"
    />

    <!-- Slider -->
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

    <!-- Max Year Input -->
    <input
        type="number"
        class="input-box"
        v-model.number="tempMaxValue"
        @blur="updateSliderValue('max')"
        @keyup.enter="handleEnter('max', $event)"
        :min="minValue"
        :max="maxYear"
        placeholder="End Year"
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
      debounceDelay: 300,
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
      event.target.blur();
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
          Math.round((percentage / 100) * (this.maxYear - this.minYear)) + this.minYear;

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
  flex-direction: column;
  align-items: flex-start;
  padding: 15px;
  gap: 15px;
  background-color: #f8f8f8;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%; /* Dynamically resize with the sidebar */
  box-sizing: border-box;
}

h2 {
  font-size: 1.2rem;
  font-weight: 500;
  margin: 0;
  color: #333;
}

.slider-container {
  position: relative;
  height: 10px;
  width: 100%; /* Full width for responsiveness */
  background-color: #ddd;
  border-radius: 5px;
  overflow: hidden;
}

.slider-track {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #ddd;
}

.slider-range {
  position: absolute;
  top: 0;
  height: 100%;
  background-color: #2196f3;
  border-radius: 5px;
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
  width: 100%; /* Full width for sidebar compatibility */
  padding: 8px;
  font-size: 14px;
  text-align: center;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

@media (max-width: 600px) {
  .range-slider {
    padding: 10px; /* Reduce padding for smaller screens */
  }

  h2 {
    font-size: 1rem; /* Adjust heading size for smaller screens */
  }
}
</style>
