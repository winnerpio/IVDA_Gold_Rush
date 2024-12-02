<template>
    <aside class="sidebar">
      <!-- Menu Items -->
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
        <div class="menu-item">
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
    </aside>
  </template>
  
  <script>
  import axios from 'axios';
  import { ref, computed, watch, onMounted } from 'vue';
  
  export default {
    name: 'OlympicSidebar',
    emits: ['update:yearRange', 'update-sport-event', 'update-user-data'],
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
        filteredEvents,
        rangeLeft,
        rangeRight,
        rangeWidth,
        handleEnter,
        startDrag,
        handleDrag,
        stopDrag,
        updateSliderValue,
      };
    },
  };
  </script>
  