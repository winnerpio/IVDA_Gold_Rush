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
    </div>
  </v-navigation-drawer>
</template>

<script>
import { ref, computed, watch, onMounted } from "vue";
import axios from "axios";
import logoURL from "../assets/olympic_rings.png";

export default {
  name: "OlympicSidebar",
  emits: ["update:yearRange", "update-sport-event"],
  props: {
    minYear: {
      type: Number,
      default: 1896,
    },
    maxYear: {
      type: Number,
      default: 2022,
    },
    yearRange: {
      type: Array,
      default: () => [1896, 2022],
    },
  },
  setup(props, { emit }) {
    // Sidebar State
    const isExpanded = ref(localStorage.getItem("is_expanded") === "true" || false);

    const toggleMenu = () => {
      isExpanded.value = !isExpanded.value;
      const menuElement = document.querySelector(".menu");
      if (menuElement) {
        if (isExpanded.value) {
          menuElement.classList.add("translate-up");
        } else {
          menuElement.classList.remove("translate-up");
        }
      }
      localStorage.setItem("is_expanded", isExpanded.value);
    };

    const expandMenu = () => {
      if (!isExpanded.value) {
        toggleMenu();
      }
    };

    // Sport and Event Selection Data
    const selectedSport = ref(null);
    const selectedEvent = ref(null);
    const sports = ref([]);
    const events = ref([]);

    // Date Range Slider Data
    const minValue = ref(props.yearRange[0]);
    const maxValue = ref(props.yearRange[1]);
    const tempMinValue = ref(props.yearRange[0]);
    const tempMaxValue = ref(props.yearRange[1]);
    const isDragging = ref(false);
    const draggingThumb = ref(null);
    const debounceTimer = ref(null);
    const debounceDelay = 300;

    // Computed Properties for Sport and Event
    const filteredEvents = computed(() =>
      events.value
        .filter((event) => event.sport === selectedSport.value)
        .map((event) => event.event)
    );

    // Computed Properties for Date Range Slider
    const rangeLeft = computed(() => {
      return ((minValue.value - props.minYear) / (props.maxYear - props.minYear)) * 100;
    });

    const rangeRight = computed(() => {
      return ((maxValue.value - props.minYear) / (props.maxYear - props.minYear)) * 100;
    });

    const rangeWidth = computed(() => {
      return rangeRight.value - rangeLeft.value;
    });

    // Methods for Sport and Event Selection
    const fetchSportsAndEvents = async (yearRange) => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/SportEventList", {
          params: {
            year_lower: yearRange[0],
            year_upper: yearRange[1],
          },
        });
        const data = response.data;

        sports.value = Object.keys(data);
        events.value = Object.entries(data).flatMap(([sport, eventList]) =>
          eventList.map((event) => ({ sport, event }))
        );
      } catch (error) {
        console.error("Error fetching sports and events:", error);
      }
    };

    // Watchers for Sport and Event Selection
    watch(selectedEvent, (newEvent) => {
      if (newEvent) {
        emit("update-sport-event", { sport: selectedSport.value, event: newEvent });
      }
    });

    watch(selectedSport, () => {
      selectedEvent.value = null;
    });

    // Methods for Date Range Slider
    const handleEnter = (type, event) => {
      updateSliderValue(type);
      event.target.blur();
    };

    const startDrag = (thumb) => {
      isDragging.value = true;
      draggingThumb.value = thumb;
      document.addEventListener("mousemove", handleDrag);
      document.addEventListener("mouseup", stopDrag);
    };

    const handleDrag = (event) => {
      if (!isDragging.value) return;

      const slider = document.querySelector(".slider-container").getBoundingClientRect();
      const percentage = ((event.clientX - slider.left) / slider.width) * 100;
      const yearValue = Math.round((percentage / 100) * (props.maxYear - props.minYear)) + props.minYear;

      if (draggingThumb.value === "min") {
        minValue.value = Math.min(Math.max(props.minYear, yearValue), maxValue.value);
        tempMinValue.value = minValue.value;
      } else if (draggingThumb.value === "max") {
        maxValue.value = Math.max(Math.min(props.maxYear, yearValue), minValue.value);
        tempMaxValue.value = maxValue.value;
      }

      debounceEmitRange();
    };

    const stopDrag = () => {
      isDragging.value = false;
      draggingThumb.value = null;
      document.removeEventListener("mousemove", handleDrag);
      document.removeEventListener("mouseup", stopDrag);
    };

    const updateSliderValue = (type) => {
      if (type === "min") {
        if (tempMinValue.value < props.minYear) {
          tempMinValue.value = props.minYear;
        } else if (tempMinValue.value > maxValue.value) {
          tempMinValue.value = maxValue.value;
        }
        minValue.value = tempMinValue.value;
      } else if (type === "max") {
        if (tempMaxValue.value > props.maxYear) {
          tempMaxValue.value = props.maxYear;
        } else if (tempMaxValue.value < minValue.value) {
          tempMaxValue.value = minValue.value;
        }
        maxValue.value = tempMaxValue.value;
      }
      debounceEmitRange();
    };

    const debounceEmitRange = () => {
      clearTimeout(debounceTimer.value);
      debounceTimer.value = setTimeout(() => {
        emitRange();
      }, debounceDelay);
    };

    const emitRange = () => {
      emit("update:yearRange", [minValue.value, maxValue.value]);
    };

    // Watcher for Date Range Slider
    watch(
      [minValue, maxValue],
      ([newMin, newMax]) => {
        fetchSportsAndEvents([newMin, newMax]);
        emitRange();
      },
      { immediate: true }
    );

    // Initial Fetch
    onMounted(() => {
      fetchSportsAndEvents([minValue.value, maxValue.value]);
    });

    return {
      isExpanded,
      toggleMenu,
      expandMenu,
      logoURL,
      // Sport and Event Data
      selectedSport,
      selectedEvent,
      sports,
      filteredEvents,
      // Date Range Slider Data
      minValue,
      maxValue,
      tempMinValue,
      tempMaxValue,
      rangeLeft,
      rangeRight,
      rangeWidth,
      isDragging,
      draggingThumb,
      handleEnter,
      startDrag,
      handleDrag,
      stopDrag,
      updateSliderValue,
    };
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