<template>
  <div class="olympic-data-top-menu">
    <h1>
      The Olympic Data of
      <v-select
          :items="sports"
          v-model="selectedSport"
          label="Select Sport"
          persistent-placeholder
          outlined
          dense
          class="flexible-dropdown"
      />
      <v-select
          :items="filteredEvents"
          v-model="selectedEvent"
          label="Select Event"
          :disabled="!selectedSport"
          persistent-placeholder
          outlined
          dense
          class="flexible-dropdown"
      />
    </h1>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue';
import axios from 'axios';

export default {
  name: 'OlympicDataTopMenu',
  data() {
    return {
      selectedYearRange: [1896, 2022],
    };
  },
  setup(_, { emit }) {
    const selectedSport = ref(null);
    const selectedEvent = ref(null);
    const sports = ref([]); // All available sports
    const events = ref([]); // All available events
    const filteredEvents = computed(() =>
      events.value
        .filter((event) => event.sport === selectedSport.value)
        .map((event) => event.event)
    );

    // Fetch sports and events using the SportEventList API
    const fetchSportsAndEvents = async (yearRange) => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/SportEventList', {
          params: {
            year_lower: yearRange[0],
            year_upper: yearRange[1],
          },
        });

        console.log(yearRange[0]);
        console.log(yearRange[1]);
        const data = response.data;

        // Extract sports and events from the API response
        sports.value = Object.keys(data);
        events.value = Object.entries(data).flatMap(([sport, eventList]) =>
          eventList.map((event) => ({ sport, event }))
        );
      } catch (error) {
        console.error('Error fetching sports and events:', error);
      }
    };

    // Emit sport and event whenever the event changes
    watch(selectedEvent, (newEvent) => {
      if (newEvent) {
        emit('update-sport-event', { sport: selectedSport.value, event: newEvent });
      }
    });

    // Reset the event selection when the sport changes
    watch(selectedSport, () => {
      selectedEvent.value = null; // Reset the event
    });

    // Fetch data on mount
    onMounted(() => {
      fetchSportsAndEvents([1896, 2022]);
    });

    return {
      selectedSport,
      selectedEvent,
      sports,
      filteredEvents,
    };
  },
  props: {
    yearRange: {
      type: Array,
      required: true,
      default: () => [1896, 2022],
    },
  },
};
</script>

<style scoped>
.olympic-data-top-menu {
  padding: 10px;
  background: #f5f5f5;
  border-bottom: 1px solid #ddd;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}

h1 {
  display: flex;
  align-items: center;
  font-size: 1.5rem;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: center;
}

.flexible-dropdown {
  min-width: 200px;
  max-width: 30%;
  flex: 1 1 auto;
  white-space: nowrap;
}
</style>
