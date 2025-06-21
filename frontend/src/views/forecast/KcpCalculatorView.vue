<template>
  <v-container v-if="!$vuetify.display.mobile" max-width="800" class="elevation-0 mt-5 ml-auto mr-auto">
    <v-card-title class="text-wrap" align="center">
      Расчет контрольных цифр приема (КЦП)
    </v-card-title>
  </v-container>

  <v-container class="elevation-2 mt-5 ml-auto mr-auto bg-white rounded-lg" max-width="1000">
    <v-toolbar flat color="white">
      <v-btn icon="mdi-arrow-left" color="primary" @click="$router.go(-1)" />
      <v-toolbar-title v-if="!$vuetify.display.mobile" class="text-h6 font-weight-bold">
        На главную
      </v-toolbar-title>
      <v-spacer />
    </v-toolbar>

    <v-card class="elevation-0 mt-5 pa-6">
      <v-row>
        <v-col cols="12" md="6">
          <v-select
            v-model="selectedPeriod"
            :items="periods"
            label="Выберите период, лет"
            outlined
            dense
          />
        </v-col>

        <v-col cols="12" md="6">
          <v-autocomplete
            v-model="selectedDirection"
            :items="directions"
            label="Направление подготовки / специальность"
            outlined
            dense
            clearable
          />
        </v-col>
      </v-row>

      <v-row justify="center" class="mt-6">
        <v-btn
          color="primary"
          size="large"
          @click="calculateKCP"
          :disabled="!canCalculate"
          prepend-icon="mdi-calculator"
        >
          Рассчитать КЦП
        </v-btn>
      </v-row>
    </v-card>

    <v-overlay :model-value="loading" class="align-center justify-center" persistent>
      <v-progress-circular color="primary" size="64" indeterminate />
    </v-overlay>

    <v-card v-if="showResults" class="mt-6 pa-6">
      <v-card-title class="text-h6">
        Результаты расчета КЦП по направлению: {{ selectedDirection }}
      </v-card-title>

      <v-card-subtitle>Период: {{ selectedPeriod }} лет</v-card-subtitle>

      <v-card-text>
        <div class="d-flex align-center justify-space-between">
          <div>
            <div class="text-h4 primary--text">{{ result.current | formatNumber }}</div>
            <div class="text-caption">Текущее значение</div>
          </div>

          <div class="text-center">
            <div class="text-h4" :class="result.change >= 0 ? 'green--text' : 'red--text'">
              {{ result.change >= 0 ? '+' : '' }}{{ result.change | formatNumber }}%
            </div>
            <div class="text-caption">Изменение</div>
          </div>

          <div>
            <div class="text-h4 blue--text">{{ result.forecast | formatNumber }}</div>
            <div class="text-caption">Прогноз через {{ selectedPeriod }} лет</div>
          </div>
        </div>

        <v-sparkline
          :key="chartKey"
          :model-value="sparklineData"
          :labels="sparklineLabels"
          :smooth="16"
          :gradient="['#1976D2', '#2196F3', '#64B5F6']"
          :line-width="3"
          padding="24"
          auto-draw
          auto-draw-duration="2000"
          auto-draw-easing="cubic-bezier(0.4, 0.0, 0.2, 1)"
          class="mt-8"
        >
          <template v-slot:label="item">
            {{ item.value }}
          </template>
        </v-sparkline>
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn disabled color="primary" @click="saveResults" prepend-icon="mdi-content-save">
          Сохранить отчет
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: 'KCPView',
  data() {
    return {
      loading: false,
      showResults: false,
      chartKey: 0,

      selectedPeriod: null,
      selectedDirection: null,

      result: {
        current: 0,
        forecast: 0,
        change: 0
      },

      sparklineData: [],
      sparklineLabels: [],

      periods: [1, 2, 3, 4, 5],
      directions: [
        '08.02.01 Строительство и эксплуатация зданий и сооружений',
        '08.02.03 Производство неметаллических строительных изделий и конструкций',
        '08.02.04 Водоснабжение и водоотведение',
        '08.02.05 Строительство и эксплуатация автомобильных дорог и аэродромов',
        '08.02.07 Монтаж и эксплуатация внутренних сантехнических устройств, кондиционирования воздуха и вентиляции',
        '08.02.08 Монтаж и эксплуатация оборудования и систем газоснабжения',
        '08.02.09 Монтаж, наладка и эксплуатация электрооборудования промышленных и гражданских зданий',
        '08.02.10 Строительство железных дорог, путь и путевое хозяйство',
        '09.02.01 Компьютерные системы и комплексы',
        '09.01.03 Оператор информационных систем и ресурсов',
        '09.02.06 Сетевое и системное администрирование',
        '09.02.07 Информационные системы и программирование',
        '10.02.01 Организация и технология защиты информации',
        '10.02.04 Обеспечение информационной безопасности телекоммуникационных систем',
        '10.02.05 Обеспечение информационной безопасности автоматизированных систем',
        '11.02.15 Инфокоммуникационные сети и системы связи',
        '44.02.01 Дошкольное образование',
        '44.02.02 Преподавание в начальных классах',
        '44.02.03 Педагогика дополнительного образования',
        '44.02.04 Специальное дошкольное образование',
        '44.02.05 Коррекционная педагогика в начальном образовании',
        '44.02.06 Профессиональное обучение (по отраслям)'
      ],

      baseKCP: {
        '08.02.01 Строительство и эксплуатация зданий и сооружений': 295,
        '08.02.03 Производство неметаллических строительных изделий и конструкций': 25,
        '08.02.04 Водоснабжение и водоотведение': 25,
        '08.02.05 Строительство и эксплуатация автомобильных дорог и аэродромов': 0,
        '08.02.07 Монтаж и эксплуатация внутренних сантехнических устройств, кондиционирования воздуха и вентиляции': 0,
        '08.02.08 Монтаж и эксплуатация оборудования и систем газоснабжения': 25,
        '08.02.09 Монтаж, наладка и эксплуатация электрооборудования промышленных и гражданских зданий': 25,
        '08.02.10 Строительство железных дорог, путь и путевое хозяйство': 50,
        '09.02.01 Компьютерные системы и комплексы': 200,
        '09.01.03 Оператор информационных систем и ресурсов': 70,
        '09.02.06 Сетевое и системное администрирование': 200,
        '09.02.07 Информационные системы и программирование': 100,
        '10.02.01 Организация и технология защиты информации': 0,
        '10.02.04 Обеспечение информационной безопасности телекоммуникационных систем': 25,
        '10.02.05 Обеспечение информационной безопасности автоматизированных систем': 75,
        '11.02.15 Инфокоммуникационные сети и системы связи': 50,
        '44.02.01 Дошкольное образование': 330,
        '44.02.02 Преподавание в начальных классах': 270,
        '44.02.03 Педагогика дополнительного образования': 100,
        '44.02.04 Специальное дошкольное образование': 50,
        '44.02.05 Коррекционная педагогика в начальном образовании': 125,
        '44.02.06 Профессиональное обучение (по отраслям)': 100
      }
    };
  },
  computed: {
    canCalculate() {
      return this.selectedPeriod && this.selectedDirection;
    }
  },
  methods: {
    calculateKCP() {
      this.loading = true;
      this.showResults = false;

      setTimeout(() => {
        this.generateKCP();
        this.loading = false;
        this.showResults = true;
        this.chartKey++;
      }, 1500);
    },
    generateKCP() {
      const base = this.baseKCP[this.selectedDirection] || 100;
      const changePercent = (Math.random() * 20 - 5).toFixed(1);
      const forecast = Math.round(base * (1 + changePercent / 100));

      this.result = {
        current: base,
        forecast,
        change: parseFloat(changePercent)
      };

      this.sparklineData = [];
      this.sparklineLabels = [];

      for (let i = 5; i > 0; i--) {
        const year = new Date().getFullYear() - i;
        const val = Math.round(base * (0.85 + Math.random() * 0.15));
        this.sparklineData.push(val);
        this.sparklineLabels.push(year.toString());
      }

      this.sparklineData.push(base);
      this.sparklineLabels.push(new Date().getFullYear().toString());

      for (let i = 1; i <= this.selectedPeriod; i++) {
        const year = new Date().getFullYear() + i;
        const val = Math.round(base + (forecast - base) * (i / this.selectedPeriod));
        this.sparklineData.push(val);
        this.sparklineLabels.push(year.toString());
      }
    },
    saveResults() {
      this.$toast.success('Отчет сохранен!');
    }
  },
  filters: {
    formatNumber(value) {
      return value.toLocaleString();
    }
  }
};
</script>

<style scoped>
.v-sparkline {
  height: 300px;
}
.v-progress-circular {
  animation: grow 1.5s infinite alternate;
}
@keyframes grow {
  from {
    transform: scale(0.8);
  }
  to {
    transform: scale(1.1);
  }
}
</style>
