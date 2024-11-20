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

export default {
  name: 'OlympicDataTopMenu',
  setup(_, { emit }) {
    const selectedSport = ref(null);
    const selectedEvent = ref(null);
    const sports = ref([]); // All available sports
    const events = ref([]); // All available events
    const filteredEvents = computed(() =>
        events.value
            .filter((event) => event.subtitle === selectedSport.value)
            .map((event) => event.title)
    );

    // Mock fetch function, replace with actual API or logic
    const fetchSports = async () => {
      sports.value = ['Athletics', 'Swimming', 'Gymnastics'];
    };

    const fetchEvents = async () => {
      events.value = [
        { subtitle: 'Athletics', title: '100m' },
        { subtitle: 'Athletics', title: '200m' },
        { subtitle: 'Swimming', title: '100m Freestyle' },
        { subtitle: 'Swimming', title: '200m Freestyle' },
        { subtitle: 'Gymnastics', title: 'Floor Exercise' },
      ];
    };

    // Emit sport and event whenever the event changes
    watch(selectedEvent, (newEvent) => {
      if (newEvent) {
        emit('update-sport-event', {sport: selectedSport.value, event: newEvent});
      }
    });

    // Reset the event selection when the sport changes
    watch(selectedSport, () => {
      selectedEvent.value = null; // Reset the event
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
