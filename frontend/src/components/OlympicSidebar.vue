<template>
  <v-navigation-drawer app permanent width="300">
    <!-- Sidebar content -->
    <div class="menu">
      <!-- Sport and Event Selection -->
      <div class="menu-item">
        <h2>Select Sport and Event</h2>
        <v-select
          :items="sports"
          v-model="selectedSport"
          label="Sport"
          persistent-placeholder
          dense
          outlined
          hide-details
          class="dropdown"
        />
        <v-select
          :items="filteredEvents"
          v-model="selectedEvent"
          label="Event"
          :disabled="!selectedSport"
          persistent-placeholder
          dense
          outlined
          hide-details
          class="dropdown"
        />
      </div>

      <!-- Date Range Slider -->
      <div class="menu-item range-slider">
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
        <div class="slider-container" ref="sliderContainer">
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
    </div>
  </v-navigation-drawer>
</template>

<script>
import axios from "axios";

export default {
  name: "OlympicSidebar",
  props: {
    minYear: { type: Number, default: 1896 },
    maxYear: { type: Number, default: 2022 },
    yearRange: { type: Array, default: () => [1896, 2022] },
  },
  data() {
    return {
      selectedSport: null,
      selectedEvent: null,
      sports: [],
      events: [],
      minValue: this.yearRange[0],
      maxValue: this.yearRange[1],
      tempMinValue: this.yearRange[0],
      tempMaxValue: this.yearRange[1],
      isDragging: false,
      draggingThumb: null,
      debounceTimer: null,
      debounceDelay: 300,
    };
  },
  computed: {
    filteredEvents() {
      return this.events
          .filter((event) => event.sport === this.selectedSport)
          .map((event) => event.event);
    },
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
    async fetchSportsAndEvents(yearRange) {
      try {
        const response = await axios.get("http://127.0.0.1:5000/SportEventList", {
          params: { year_lower: yearRange[0], year_upper: yearRange[1] },
        });
        const data = response.data;
        this.sports = Object.keys(data);
        this.events = Object.entries(data).flatMap(([sport, eventList]) =>
            eventList.map((event) => ({ sport, event }))
        );
      } catch (error) {
        console.error("Error fetching sports and events:", error);
      }
    },
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

      const slider = this.$refs.sliderContainer.getBoundingClientRect();
      const percentage = ((event.clientX - slider.left) / slider.width) * 100;
      const yearValue =
          Math.round((percentage / 100) * (this.maxYear - this.minYear)) + this.minYear;

      if (this.draggingThumb === "min") {
        this.minValue = Math.min(Math.max(this.minYear, yearValue), this.maxValue);
        this.tempMinValue = this.minValue;
      } else if (this.draggingThumb === "max") {
        this.maxValue = Math.max(Math.min(this.maxYear, yearValue), this.minValue);
        this.tempMaxValue = this.maxValue;
      }
    },
    stopDrag() {
      this.isDragging = false;
      this.draggingThumb = null;
      document.removeEventListener("mousemove", this.handleDrag);
      document.removeEventListener("mouseup", this.stopDrag);
      this.emitRange();
    },
    updateSliderValue(type) {
      if (type === "min") {
        this.tempMinValue = Math.max(this.minYear, Math.min(this.tempMinValue, this.maxValue));
        this.minValue = this.tempMinValue;
      } else if (type === "max") {
        this.tempMaxValue = Math.min(this.maxYear, Math.max(this.tempMaxValue, this.minValue));
        this.maxValue = this.tempMaxValue;
      }
      this.debounceEmitRange();
    },
    emitRange() {
      this.$emit("update:yearRange", [this.minValue, this.maxValue]);
    },
  },
  watch: {
    selectedSport(newSport) {
      if (newSport) {
        this.selectedEvent = null;
      }
    },
    selectedEvent(newEvent) {
      if (newEvent) {
        this.$emit("update-sport-event", { sport: this.selectedSport, event: newEvent });
      }
    },
    yearRange: {
      handler(newRange) {
        this.fetchSportsAndEvents(newRange);
      },
      immediate: true,
    },
  },
  mounted() {
    this.fetchSportsAndEvents([this.minValue, this.maxValue]);
  },
};
</script>

<style scoped>
.menu {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
}

.menu-item {
  margin-bottom: 20px;
}

h2 {
  font-size: 1.2rem;
  font-weight: 500;
  margin-bottom: 15px;
  color: #333;
  text-align: center;
}

/* Styles for the custom range slider */
.range-slider {
  width: 100%;
}

.slider-container {
  position: relative;
  height: 10px;
  width: 100%;
  background-color: #ddd;
  border-radius: 5px;
  overflow: hidden;
  margin: 10px 0;
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
  background-color: #000;
  border-radius: 5px;
}

.slider-thumb {
  position: absolute;
  top: 50%;
  width: 16px;
  height: 16px;
  background-color: #000;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  cursor: pointer;
}

.input-box {
  width: 100%;
  padding: 8px;
  font-size: 14px;
  text-align: center;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

@media (max-width: 600px) {
  .menu {
    padding: 10px;
  }

  h2 {
    font-size: 1rem;
  }
}
</style>