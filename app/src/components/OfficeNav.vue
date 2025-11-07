<template>
  <el-row
    v-if="currentServiceType == 'office'"
    :gutter="5"
    class="mt-6 text-xs mx-auto"
  >
    <el-col :span="12" class="text-left"> Full Daily Office mode </el-col>
    <el-col :span="12" class="text-right">
      <a href="" @click.stop.prevent="toggleServiceType"
        >Switch to Family Prayer</a
      >
    </el-col>
  </el-row>
  <el-row v-else :gutter="5" class="mt-6 text-xs mx-auto">
    <el-col :span="12" class="text-left"> Shorter Family Prayer mode </el-col>
    <el-col :span="12" class="text-right">
      <a href="" @click.stop.prevent="toggleServiceType"
        >Switch to full Daily Office</a
      >
    </el-col>
  </el-row>
  <el-row :gutter="5" class="mt-2 text-center text-xs sm:text-sm mx-auto">
    <el-col v-for="link in links" :key="link.name" :span="6">
      <div class="grid-content bg-purple">
        <router-link :to="link.to">
          <el-card
            :class="selectedClass(link.name)"
            :shadow="hoverClass(link.name)"
          >
            <p class="text-xs sm:text-sm" v-html="link.text" />
          </el-card>
        </router-link>
      </div>
    </el-col>
  </el-row>
  <el-row :gutter="5" class="mt-2 text-center">
    <el-col :span="24">
      <div class="grid-content bg-purple">
        <router-link :to="readingsLink.to">
          <el-card
            :class="selectedClass(readingsLink.name)"
            :shadow="hoverClass(readingsLink.name)"
          >
            <p class="text-xs sm:text-sm">
              <span v-html="readingsLink.text" />
            </p>
          </el-card>
        </router-link>
      </div>
    </el-col>
  </el-row>
  <el-row :gutter="5" class="mt-2 text-center">
    <el-col v-for="link in dayLinks" :key="link.text" :span="8">
      <div class="grid-content bg-purple">
        <router-link :to="link.to" :v-on:click="scrollToTop">
          <el-card
            :class="link.selected ? 'selected' : ''"
            shadow="hover"
            class="text-xs sm:text-sm"
          >
            <span
              v-if="link.icon == 'left'"
              aria-hidden="true"
              class="nav-arrow"
              >&lt;</span
            >
            {{ link.text }}
            <span
              v-if="link.icon == 'right'"
              aria-hidden="true"
              class="nav-arrow"
              >&gt;</span
            >
          </el-card>
        </router-link>
      </div>
    </el-col>
  </el-row>
</template>

<script>
import { DynamicStorage } from '@/helpers/storage';

export default {
  name: 'OfficeNav',
  components: {},
  props: {
    calendarDate: {
      type: Date,
    },
    selectedOffice: {
      type: String,
    },
    serviceType: {
      default: 'office',
      type: String,
    },
  },
  data() {
    return {
      links: null,
      dayLink: null,
      currentServiceType: this.serviceType,
    };
  },
  async created() {
    const tomorrow = new Date(this.calendarDate);
    tomorrow.setDate(this.calendarDate.getDate() + 1);
    const yesterday = new Date(this.calendarDate);
    yesterday.setDate(this.calendarDate.getDate() - 1);
    this.dailyLinks = [
      {
        to: `/morning_prayer/${this.calendarDate.getFullYear()}/${
          this.calendarDate.getMonth() + 1
        }/${this.calendarDate.getDate()}`,
        text: 'Morning<br>Prayer',
        name: 'morning_prayer',
      },
      {
        to: `/midday_prayer/${this.calendarDate.getFullYear()}/${
          this.calendarDate.getMonth() + 1
        }/${this.calendarDate.getDate()}`,
        text: 'Midday<br>Prayer',
        name: 'midday_prayer',
      },
      {
        to: `/evening_prayer/${this.calendarDate.getFullYear()}/${
          this.calendarDate.getMonth() + 1
        }/${this.calendarDate.getDate()}`,
        text: 'Evening<br>Prayer',
        name: 'evening_prayer',
      },
      {
        to: `/compline/${this.calendarDate.getFullYear()}/${
          this.calendarDate.getMonth() + 1
        }/${this.calendarDate.getDate()}`,
        text: 'Compline<br>(Bedtime)',
        name: 'compline',
      },
    ];
    this.readingsLink = {
      to: `/readings/${this.calendarDate.getFullYear()}/${
        this.calendarDate.getMonth() + 1
      }/${this.calendarDate.getDate()}`,
      text: "Day's Readings",
      name: 'readings',
    };
    this.familyLinks = [
      {
        to: `/family/morning_prayer/${this.calendarDate.getFullYear()}/${
          this.calendarDate.getMonth() + 1
        }/${this.calendarDate.getDate()}`,
        text: 'Morning',
        name: 'morning_prayer',
      },
      {
        to: `/family/midday_prayer/${this.calendarDate.getFullYear()}/${
          this.calendarDate.getMonth() + 1
        }/${this.calendarDate.getDate()}`,
        text: 'Midday',
        name: 'midday_prayer',
      },
      {
        to: `/family/early_evening_prayer/${this.calendarDate.getFullYear()}/${
          this.calendarDate.getMonth() + 1
        }/${this.calendarDate.getDate()}`,
        text: 'Early Evening',
        name: 'early_evening_prayer',
      },
      {
        to: `/family/close_of_day_prayer/${this.calendarDate.getFullYear()}/${
          this.calendarDate.getMonth() + 1
        }/${this.calendarDate.getDate()}`,
        text: 'Close of Day',
        name: 'close_of_day_prayer',
      },
    ];
    if (this.currentServiceType == 'family') {
      this.links = this.familyLinks;
    } else {
      this.links = this.dailyLinks;
    }
    const servicePart =
      this.currentServiceType == 'family' ? `/${this.currentServiceType}` : '';
    this.dayLinks = [
      {
        to: `${servicePart}/${this.selectedOffice}/${yesterday.getFullYear()}/${
          yesterday.getMonth() + 1
        }/${yesterday.getDate()}`,
        icon: 'left',
        text: yesterday.toLocaleDateString('en-us', { weekday: 'long' }),
      },
      {
        to: `${servicePart}/${this.selectedOffice}/${this.calendarDate.getFullYear()}/${
          this.calendarDate.getMonth() + 1
        }/${this.calendarDate.getDate()}`,
        text: this.calendarDate.toLocaleDateString('en-us', {
          weekday: 'long',
        }),
        selected: true,
      },
      {
        to: `${servicePart}/${this.selectedOffice}/${tomorrow.getFullYear()}/${
          tomorrow.getMonth() + 1
        }/${tomorrow.getDate()}`,
        icon: 'right',
        text: tomorrow.toLocaleDateString('en-us', { weekday: 'long' }),
      },
    ];
  },
  methods: {
    scrollToTop() {
      window.scrollTo(0, 0);
    },
    hoverClass(name) {
      return name == this.selectedOffice ? 'always' : 'hover';
    },
    selectedClass(name) {
      return name == this.selectedOffice ? 'selected' : '';
    },
    redirectToDaily() {
      if (this.selectedOffice) {
        const lookup = {
          morning_prayer: 'morning_prayer',
          midday_prayer: 'midday_prayer',
          early_evening_prayer: 'evening_prayer',
          close_of_day_prayer: 'compline',
        };
        const new_office = lookup[this.selectedOffice];
        if (new_office) {
          this.$router.push(
            `/office/${new_office}/${this.calendarDate.getFullYear()}/${
              this.calendarDate.getMonth() + 1
            }/${this.calendarDate.getDate()}`
          );
        }
      }
    },
    redirectToFamily() {
      if (this.selectedOffice) {
        const lookup = {
          morning_prayer: 'morning_prayer',
          midday_prayer: 'midday_prayer',
          evening_prayer: 'early_evening_prayer',
          compline: 'close_of_day_prayer',
        };
        const new_office = lookup[this.selectedOffice];
        if (new_office) {
          this.$router.push(
            `/family/${new_office}/${this.calendarDate.getFullYear()}/${
              this.calendarDate.getMonth() + 1
            }/${this.calendarDate.getDate()}`
          );
        }
      }
    },
    async toggleServiceType() {
      if (this.currentServiceType == 'family') {
        this.currentServiceType = 'office';
        this.links = this.dailyLinks;
        await DynamicStorage.setItem('serviceType', 'office');
        this.redirectToDaily();
      } else {
        this.currentServiceType = 'family';
        await DynamicStorage.setItem('serviceType', 'family');
        this.links = this.familyLinks;
        this.redirectToFamily();
      }
    },
  },
};
</script>

<style scoped>
.selected {
  background-color: rgb(229, 231, 235);
  border-color: rgb(44, 62, 80);
  color: var(--font-on-white-background);
}

.el-card {
  --el-card-padding: 10px;
  height: 100%;
}

.el-card__body {
  padding: 5px !important;
}

.nav-arrow {
  display: inline-block;
  margin: 0 0.25rem;
}
</style>
