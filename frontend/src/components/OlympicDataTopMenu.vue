<template>
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
</template>

<script>
import { ref, computed, watch } from "vue";
import axios from 'axios';

export default {
  name: "OlympicDataTopMenu",
  props: {
    yearRange: {
      type: Array,
      required: true,
      default: () => [1896, 2022],
    },
  },
  setup(props, { emit }) {
    const selectedSport = ref(null);
    const selectedEvent = ref(null);
    const sports = ref([]);
    const events = ref([]);

    const filteredEvents = computed(() =>
      events.value
        .filter((event) => event.sport === selectedSport.value)
        .map((event) => event.event)
    );

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

    watch(selectedEvent, (newEvent) => {
      if (newEvent) {
        emit('update-sport-event', { sport: selectedSport.value, event: newEvent });
      }
    });

    watch(selectedSport, () => {
      selectedEvent.value = null;
    });

    watch(() => props.yearRange, (newYearRange) => {
      fetchSportsAndEvents(newYearRange);
    }, {immediate: true});

    return {
      selectedSport,
      selectedEvent,
      sports,
      filteredEvents,
    };
  },
};
</script>

<style scoped>
.olympic-data-top-menu {
  display: flex;
  flex-direction: column;
  padding: 15px;
  background-color: #f8f8f8;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%; /* Dynamically resize with the sidebar width */
  box-sizing: border-box; /* Ensure padding is included in the width */
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
  width: 100%; /* Expand dropdown to fit parent container */
}

.dropdown:last-child {
  margin-bottom: 0; /* Remove margin for the last dropdown */
}

@media (max-width: 600px) {
  .olympic-data-top-menu {
    padding: 10px; /* Adjust padding for smaller screens */
  }

  h2 {
    font-size: 1rem; /* Adjust heading size for smaller screens */
  }
}
</style>
