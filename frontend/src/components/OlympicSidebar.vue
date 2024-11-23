<template>
  <aside :class="{ 'is-expanded': isExpanded }">
    <!-- Logo Section -->
    <div class="logo">
      <img :src="logoURL" alt="Olympic Rings" />
    </div>

    <!-- Menu Toggle Button -->
    <div class="menu-toggle-wrap">
      <button class="menu-toggle" @click="toggleMenu">
        <span class="material-icons">
          {{ isExpanded ? "keyboard_double_arrow_left" : "keyboard_double_arrow_right" }}
        </span>
      </button>
    </div>

    <!-- Menu Items -->
    <div class="menu">
      <!-- Olympic Data Menu -->
      <div class="menu-item" @click="expandMenu">
        <template v-if="isExpanded">
          <OlympicDataTopMenu @update-sport-event="handleSportEventUpdate" />
        </template>
        <template v-else>
          <span class="material-icons" title="Select Sport and Event">sports</span>
        </template>
      </div>

      <!-- User Control Menu -->
      <div class="menu-item" @click="expandMenu">
        <template v-if="isExpanded">
          <UserControlHub @update-attributes="handleAttributesUpdate" />
        </template>
        <template v-else>
          <span class="material-icons" title="User Attributes">person</span>
        </template>
      </div>

      <!-- Date Range Slider -->
      <div class="menu-item" @click="expandMenu">
        <template v-if="isExpanded">
          <DateRangeSlider
              :minYear="1896"
              :maxYear="2022"
              :initialRange="[1920, 2005]"
              @update:range="updateYearRange"
          />
        </template>
        <template v-else>
          <span class="material-icons" title="Select Date Range">calendar_today</span>
        </template>
      </div>
    </div>
  </aside>
</template>

<script>
import { ref } from "vue";
import logoURL from "../assets/olympic_rings.png";
import UserControlHub from "./UserControlHub.vue";
import OlympicDataTopMenu from "./OlympicDataTopMenu.vue";
import DateRangeSlider from "./DateRangeSlider.vue";

export default {
  name: "OlympicSidebar",
  components: {
    UserControlHub,
    OlympicDataTopMenu,
    DateRangeSlider,
  },
  emits: ["update:modelValue", "update-sport-event", "update-user-data"],
  setup(_, { emit }) {
    const isExpanded = ref(localStorage.getItem("is_expanded") === "true");

    const toggleMenu = () => {
      isExpanded.value = !isExpanded.value;
      const menuElement = document.querySelector('.menu');
      if (menuElement) {
        if (isExpanded.value) {
          menuElement.classList.add('translate-up');
        } else {
          menuElement.classList.remove('translate-up');
        }
      }
      localStorage.setItem("is_expanded", isExpanded.value);
    };


    const expandMenu = () => {
      if (!isExpanded.value) {
        toggleMenu();
      }
    };

    const updateYearRange = (newRange) => {
      emit("update:range", newRange);
    };

    const handleSportEventUpdate = (data) => {
      emit("update-sport-event", data);
    };

    const handleAttributesUpdate = (attributes) => {
      emit("update-user-data", attributes);
    };

    return {
      isExpanded,
      toggleMenu,
      expandMenu,
      updateYearRange,
      handleSportEventUpdate,
      handleAttributesUpdate,
      logoURL,
    };
  },
};
</script>

<style lang="scss" scoped>
aside {
  display: flex;
  flex-direction: column;
  background-color: #f8f8f8;
  color: #333;
  width: calc(2rem + 32px);
  overflow: hidden;
  min-height: 100vh;
  padding: 1rem;
  transition: width 0.2s ease-in-out;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1;

  .logo {
    margin-bottom: 1rem;

    img {
      width: 2rem;
    }
  }

  .menu-toggle-wrap {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 1rem;

    /* Ensure it remains in the top-right corner */
    position: relative;
    top: 0;

    transition: 0.2s ease-in-out;


    .menu-toggle {
      transition: 0.2s ease-in-out;

      .material-icons {
        font-size: 2rem;
        cursor: pointer;
        color: #666;
        transition: transform 0.2s ease-in-out, color 0.2s ease-in-out;

        &:hover {
          color: #333;
          transform: translateX(0.5rem);

        }
      }
    }
  }

  .menu {
    margin: 0;
    transition: transform 0.3s ease-in-out;

    &.translate-up {
      transform: translateY(-4rem);
    }

    .menu-item {
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 1rem;
      padding: 0.5rem;
      cursor: pointer;

      .material-icons {
        font-size: 2rem;
        color: #999;
        transition: transform 0.2s ease-in-out, color 0.2s ease-in-out;

        &:hover {
          color: #333;
          transform: scale(1.2);
        }
      }
    }
  }

  &.is-expanded {
    width: 350px;

    .menu-toggle-wrap {
      top: -3rem; /* Keep it near the top of the expanded sidebar */

    }

    h3, .button .text {
      opacity: 1;
    }

    .button {
      .material-icons {
        margin-right: 1rem;
      }
    }

    .footer {
      opacity: 0;
    }

    .menu-item {
      justify-content: flex-start;
      padding-left: 1rem;

      .material-icons {
        margin-right: 1rem;
        font-size: 1.5rem;
      }
    }
  }
}

</style>