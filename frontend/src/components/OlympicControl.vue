<template>
  <div class="controls">
    <!-- Olympic Data Top Menu (Sport and Event Selection) -->
    <div class="olympic-data-top-menu">
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
    <div class="date-range-slider">
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
</template>

<script>
import axios from 'axios';
import { ref, computed, watch, onMounted } from 'vue';

export default {
  name: 'OlympicControl',
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
    // Data for Sport and Event Selection
    const selectedSport = ref(null);
    const selectedEvent = ref(null);
    const sports = ref([]);
    const events = ref([]);

    // Data for Date Range Slider
    const minValue = ref(props.yearRange[0]);
    const maxValue = ref(props.yearRange[1]);
    const tempMinValue = ref(props.yearRange[0]);
    const tempMaxValue = ref(props.yearRange[1]);
    const isDragging = ref(false);
    const draggingThumb = ref(null);
    const debounceTimer = ref(null);
    const debounceDelay = 300;

    // Computed Properties
    const filteredEvents = computed(() =>
      events.value
        .filter((event) => event.sport === selectedSport.value)
        .map((event) => event.event)
    );

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
        const response = await axios.get('http://127.0.0.1:5000/SportEventList', {
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
        console.error('Error fetching sports and events:', error);
      }
    };

    // Methods for Date Range Slider
    const handleEnter = (type, event) => {
      updateSliderValue(type);
      event.target.blur();
    };

    const startDrag = (thumb) => {
      isDragging.value = true;
      draggingThumb.value = thumb;
      document.addEventListener('mousemove', handleDrag);
      document.addEventListener('mouseup', stopDrag);
    };

    const handleDrag = (event) => {
      if (!isDragging.value) return;

      const slider = document.querySelector('.slider-container').getBoundingClientRect();
      const percentage = ((event.clientX - slider.left) / slider.width) * 100;
      const yearValue =
        Math.round((percentage / 100) * (props.maxYear - props.minYear)) + props.minYear;

      if (draggingThumb.value === 'min') {
        minValue.value = Math.min(Math.max(props.minYear, yearValue), maxValue.value);
        tempMinValue.value = minValue.value;
      } else if (draggingThumb.value === 'max') {
        maxValue.value = Math.max(Math.min(props.maxYear, yearValue), minValue.value);
        tempMaxValue.value = maxValue.value;
      }

      debounceEmitRange();
    };

    const stopDrag = () => {
      isDragging.value = false;
      draggingThumb.value = null;
      document.removeEventListener('mousemove', handleDrag);
      document.removeEventListener('mouseup', stopDrag);
    };

    const updateSliderValue = (type) => {
      if (type === 'min') {
        if (tempMinValue.value < props.minYear) {
          tempMinValue.value = props.minYear;
        } else if (tempMinValue.value > maxValue.value) {
          tempMinValue.value = maxValue.value;
        }
        minValue.value = tempMinValue.value;
      } else if (type === 'max') {
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
      emit('update:yearRange', [minValue.value, maxValue.value]);
    };

    // Watchers
    watch(selectedEvent, (newEvent) => {
      if (newEvent) {
        emit('update-sport-event', { sport: selectedSport.value, event: newEvent });
      }
    });

    watch(selectedSport, () => {
      selectedEvent.value = null;
    });

    watch([minValue, maxValue], ([newMin, newMax]) => {
      fetchSportsAndEvents([newMin, newMax]);
    });

    // Initial Fetch
    onMounted(() => {
      fetchSportsAndEvents([minValue.value, maxValue.value]);
    });

    return {
      // Data
      selectedSport,
      selectedEvent,
      sports,
      events,
      tempMinValue,
      tempMaxValue,
      minValue,
      maxValue,
      isDragging,
      draggingThumb,
      debounceTimer,
      // Computed
      filteredEvents,
      rangeLeft,
      rangeRight,
      rangeWidth,
      // Methods
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
.controls {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Styles from OlympicDataTopMenu.vue */
.olympic-data-top-menu {
  display: flex;
  flex-direction: column;
  padding: 15px;
  background-color: #f8f8f8;
  border-radius: 8px;
  box-sizing: border-box;
}

h2 {
  font-size: 1.2rem;
  font-weight: 500;
  margin-bottom: 15px;
  color: #333;
  text-align: center;
}

.dropdown {
  margin-bottom: 15px;
  width: 100%;
}

.dropdown:last-child {
  margin-bottom: 0;
}

/* Styles from DateRangeSlider.vue */
.date-range-slider {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 15px;
  gap: 15px;
  background-color: #f8f8f8;
  border-radius: 8px;
  box-sizing: border-box;
}

.slider-container {
  position: relative;
  height: 10px;
  width: 100%;
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
  width: 100%;
  padding: 8px;
  font-size: 14px;
  text-align: center;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

@media (max-width: 600px) {
  .olympic-data-top-menu,
  .date-range-slider {
    padding: 10px;
  }

  h2 {
    font-size: 1rem;
  }
}
</style>
