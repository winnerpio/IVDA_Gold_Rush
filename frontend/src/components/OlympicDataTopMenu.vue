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
import { ref, computed, onMounted, watch } from "vue";

export default {
  name: "OlympicDataTopMenu",
  setup(_, { emit }) {
    const selectedSport = ref(null);
    const selectedEvent = ref(null);
    const sports = ref([]);
    const events = ref([]);

    const filteredEvents = computed(() =>
        events.value
            .filter((event) => event.subtitle === selectedSport.value)
            .map((event) => event.title)
    );

    const fetchSports = async () => {
      sports.value = ["Athletics", "Swimming", "Gymnastics"];
    };

    const fetchEvents = async () => {
      events.value = [
        { subtitle: "Athletics", title: "100m" },
        { subtitle: "Athletics", title: "200m" },
        { subtitle: "Swimming", title: "100m Freestyle" },
        { subtitle: "Swimming", title: "200m Freestyle" },
        { subtitle: "Gymnastics", title: "Floor Exercise" },
      ];
    };

    watch(selectedEvent, (newEvent) => {
      if (newEvent) {
        emit("update-sport-event", { sport: selectedSport.value, event: newEvent });
      }
    });

    watch(selectedSport, () => {
      selectedEvent.value = null;
    });

    onMounted(() => {
      fetchSports();
      fetchEvents();
    });

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
