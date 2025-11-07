<template>
  <div class="font-size-block my-2 p-3">
    <div class="w-1/6 inline-block">
      <span
        aria-hidden="true"
        class="font-size-indicator font-size-indicator--small"
        >A</span
      >
    </div>
    <div class="w-2/3 inline-block">
      <el-slider
        v-model="fontSize"
        class="w-3/4"
        :min="sliderMin"
        :max="sliderMax"
        :format-tooltip="displayFontSize"
        @input="setFontSize"
      />
    </div>
    <div class="w-1/6 inline-block text-right">
      <span
        aria-hidden="true"
        class="font-size-indicator font-size-indicator--large"
        >A</span
      >
    </div>
  </div>
</template>

<script>
import { DynamicStorage } from '@/helpers/storage';

export default {
  name: 'FontSizer',
  components: {},
  props: {},
  data() {
    return {
      fontSize: 24,
      sliderMin: 10,
      sliderMax: 40,
    };
  },
  async mounted() {
    await this.resetFontSize();
  },
  methods: {
    async resetFontSize() {
      await this.$nextTick();
      this.fontSize = parseInt(
        (await DynamicStorage.getItem('fontSize')) || 24
      );
      await this.setFontSize(this.fontSize);
    },
    async setFontSize(value) {
      const main = document.getElementById('main');
      if (main) {
        main.style['font-size'] = `${value}px`;
        document
          .querySelectorAll(
            '#main h2, #main h3, #main p, .el-collapse-item__header, .el-collapse-item p'
          )
          .forEach((p) => {
            p.style['font-size'] = `${value}px`;
            p.style['line-height'] = `${value * 1.6}px`;
          });
      }
      await DynamicStorage.setItem('fontSize', this.fontSize);
      await DynamicStorage.getItem('fontSize');
    },
    displayFontSize(value) {
      return `${value}px`;
    },
  },
};
</script>

<style scoped>
.font-size-indicator {
  display: inline-block;
  font-weight: 600;
}

.font-size-indicator--small {
  font-size: 0.75rem;
}

.font-size-indicator--large {
  font-size: 1.25rem;
}
</style>
