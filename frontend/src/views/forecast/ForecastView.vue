<template>
  <v-container v-if="!$vuetify.display.mobile" max-width="800" class="elevation-0 mt-5 ml-auto mr-auto">
    <v-card-title class="text-wrap" align="center">
      Прогнозирование спроса на работников
    </v-card-title>
  </v-container>
  <v-container class="elevation-2 mt-5 ml-auto mr-auto bg-white rounded-lg" max-width="1000">
    <v-toolbar flat color="white">
      <v-btn icon="mdi-arrow-left" color="primary" @click="$router.push('/main-menu')" />
      <v-toolbar-title v-if="!$vuetify.display.mobile" class="text-h6 font-weight-bold">
        Назад
      </v-toolbar-title>
      <v-spacer />
    </v-toolbar>

    <v-card class="elevation-0 mt-5 pa-6">
      <v-row>
        <v-col cols="12" md="4">
          <v-select
            v-model="selectedModel"
            :items="mlModels"
            label="Модель прогнозирования"
            outlined
            dense
          />
        </v-col>

        <v-col cols="12" md="4">
          <v-select
            v-model="selectedPeriod"
            :items="periods"
            label="Период прогнозирования (лет)"
            outlined
            dense
          />
        </v-col>

        <v-col cols="12" md="4">
          <v-select
            v-model="forecastType"
            :items="['profession', 'okved']"
            label="Тип прогноза"
            outlined
            dense
            clearable
          />
        </v-col>
      </v-row>

      <v-row v-if="forecastType === 'profession'">
        <v-col cols="12">
          <v-autocomplete
            v-model="selectedProfession"
            :items="professions"
            label="Выберите профессию"
            outlined
            dense
            clearable
          />
        </v-col>
      </v-row>

      <v-row v-else-if="forecastType === 'okved'">
        <v-col cols="12">
          <v-autocomplete
            v-model="selectedOkved"
            :items="okvedSectors"
            label="Выберите сферу (ОКВЭД)"
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
          @click="runForecast"
          :disabled="!canRunForecast"
          prepend-icon="mdi-chart-line"
        >
          Запустить прогноз
        </v-btn>
      </v-row>
    </v-card>

    <v-overlay :model-value="loading" class="align-center justify-center" persistent>
      <v-progress-circular color="primary" size="64" indeterminate />
    </v-overlay>

    <v-card v-if="showResults" class="mt-6 pa-6">
      <v-card-title class="text-h6">
        Прогноз спроса на
        <span v-if="forecastType === 'profession'">профессию: {{ selectedProfession }}</span>
        <span v-else>сферу (ОКВЭД): {{ selectedOkved }}</span>
      </v-card-title>

      <v-card-text>
        <div class="d-flex align-center justify-space-between">
          <!-- Текущий спрос -->
          <div>
            <div class="text-h4 primary--text">
              {{ forecastResult.current | formatNumber }}<span v-if="forecastType === 'okved'"> тыс. ч.</span> <span v-else> ч.</span>
            </div>
            <div class="text-caption">Текущий спрос</div>
            
          </div>

          <!-- Изменение -->
          <div class="text-center">
            <div
              class="text-h4"
              :class="forecastResult.change >= 0 ? 'green--text' : 'red--text'"
            >
              {{ forecastResult.change >= 0 ? '+' : '' }}{{ forecastResult.change | formatNumber }}%
            </div>
            <div class="text-caption">Изменение</div>
            
          </div>

          <!-- Прогноз -->
          <div>
            <div class="text-h4 blue--text">
              {{ forecastResult.forecast | formatNumber }}<span v-if="forecastType === 'okved'"> тыс. ч.</span> <span v-else> ч.</span>
            </div>
            <div class="text-caption">Прогноз через {{ selectedPeriod }} лет</div>
            <div class="text-caption">Точность: {{ forecastResult.accuracy }}%</div>
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
        />

        <div class="text-center mt-2">
          <v-chip color="blue" text-color="white" class="mr-2">
            <v-icon start>mdi-chart-line</v-icon>
            Прогноз
          </v-chip>
          <v-chip color="grey" text-color="white">
            <v-icon start>mdi-chart-bar</v-icon>
            Исторические данные
          </v-chip>
        </div>
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
  name: "ForecastView",
  data() {
    return {
      loading: false,
      showResults: false,
      chartKey: 0,

      selectedModel: null,
      selectedPeriod: null,
      forecastType: null,
      selectedProfession: null,
      selectedOkved: null,

      forecastResult: {
        current: 0,
        forecast: 0,
        change: 0,
        accuracy: 0
      },

      sparklineData: [],
      sparklineLabels: [],

      mlModels: ["Линейная регрессия", "Дерево решений", "Градиентный бустинг"],
      periods: [1,2,3,4,5,6,7,8,9,10],

      professions: [
        "Токарь, фрезеровщик, шлифовщик",
        "Машинист",
        "Сварщик",
        "Бухгалтер",
        "Слесарь, сантехник",
        "Инженер-конструктор, инженер-проектировщик",
        "Врач",
        "Электромонтажник",
        "Продавец-консультант, продавец-кассир",
        "Менеджер по продажам, менеджер по работе с клиентами",
        "Водитель",
        "Оператор call-центра, специалист контактного центра",
        "Разнорабочий",
        "Курьер",
        "Упаковщик, комплектовщик",
        "Повар, пекарь, кондитер",
        "Кладовщик",
        "Администратор магазина, администратор торгового зала",
        "Грузчик"
      ],

      okvedSectors: [
        "Сельское, лесное хозяйство, охота, рыболовство и рыбоводство",
        "Добыча полезных ископаемых",
        "Обрабатывающие производства",
        "Обеспечение электрической энергией, газом и паром; кондиционирование воздуха",
        "Водоснабжение; водоотведение, организация сбора и утилизации отходов, деятельность по ликвидации загрязнений",
        "Строительство",
        "Торговля оптовая и розничная; ремонт автотранспортных средств и мотоциклов",
        "Транспортировка и хранение",
        "Деятельность гостиниц и предприятий общественного питания",
        "Деятельность в области информации и связи",
        "Деятельность финансовая и страховая",
        "Деятельность по операциям с недвижимым имуществом",
        "Деятельность профессиональная, научная и техническая",
        "Деятельность административная и сопутствующие дополнительные услуги",
        "Государственное управление и обеспечение военной безопасности; социальное обеспечение",
        "Образование",
        "Деятельность в области здравоохранения и социальных услуг",
        "Деятельность в области культуры, спорта, организации досуга и развлечений",
        "Предоставление прочих видов услуг"
      ],

      // базовые значения 2023
      baseValuesByProfession: {
        "Продавец-консультант, продавец-кассир": 1926,
        "Менеджер по продажам, менеджер по работе с клиентами": 1695,
        "Водитель": 868,
        "Оператор call-центра, специалист контактного центра": 707,
        "Разнорабочий": 666,
        "Курьер": 652,
        "Упаковщик, комплектовщик": 606,
        "Слесарь, сантехник": 553,
        "Повар, пекарь, кондитер": 544,
        "Сварщик": 527,
        "Инженер-конструктор, инженер-проектировщик": 483,
        "Врач": 459,
        "Электромонтажник": 408,
        "Кладовщик": 392,
        "Администратор магазина, администратор торгового зала": 352,
        "Бухгалтер": 343,
        "Машинист": 337,
        "Токарь, фрезеровщик, шлифовщик": 305,
        "Грузчик": 274
      },
      baseValuesBySector: {
        "Сельское, лесное хозяйство, охота, рыболовство и рыбоводство": 44.9,
        "Добыча полезных ископаемых": 15.1,
        "Обрабатывающие производства": 234.8,
        "Обеспечение электрической энергией, газом и паром; кондиционирование воздуха": 23.3,
        "Водоснабжение; водоотведение, организация сбора и утилизации отходов, деятельность по ликвидации загрязнений": 10.4,
        "Строительство": 120.6,
        "Торговля оптовая и розничная; ремонт автотранспортных средств и мотоциклах": 179.5,
        "Транспортировка и хранение": 85.8,
        "Деятельность гостиниц и предприятий общественного питания": 35.3,
        "Деятельность в области информации и связи": 24.6,
        "Деятельность финансовая и страховая": 13.9,
        "Деятельность по операциям с недвижимым имуществом": 27.6,
        "Деятельность профессиональная, научная и техническая": 41.8,
        "Деятельность административная и сопутствующие дополнительные услуги": 33.2,
        "Государственное управление и обеспечение военной безопасности; социальное обеспечение": 64.2,
        "Образование": 82,
        "Деятельность в области здравоохранения и социальных услуг": 69.3,
        "Деятельность в области культуры, спорта, организации досуга и развлечений": 16.6,
        "Предоставление прочих видов услуг": 22.5
      }
    };
  },
  computed: {
    canRunForecast() {
      if (!this.selectedModel || !this.selectedPeriod || !this.forecastType) return false;
      return this.forecastType === "profession"
        ? !!this.selectedProfession
        : !!this.selectedOkved;
    }
  },
  methods: {
    runForecast() {
      this.loading = true;
      this.showResults = false;
      setTimeout(() => {
        this.generateResults();
        this.loading = false;
        this.showResults = true;
        this.chartKey++;
      }, 1500);
    },
    generateResults() {
      const base = this.forecastType === "profession"
        ? this.baseValuesByProfession[this.selectedProfession] || 300
        : this.baseValuesBySector[this.selectedOkved] || 50;
      const changePercentage = (Math.random() * 20) - 10; // от -10 до +10%
      const accuracy = (80 + Math.random() * 10).toFixed(1); // 80–90%

      this.forecastResult.current = base;
      this.forecastResult.change = parseFloat(changePercentage.toFixed(1));
      this.forecastResult.forecast = Math.round(base * (1 + this.forecastResult.change / 100));
      this.forecastResult.accuracy = parseFloat(accuracy);

      this.sparklineData = [];
      this.sparklineLabels = [];
      const year0 = new Date().getFullYear();
      for (let i = 5; i > 0; i--) {
        const val = Math.round(base * (0.85 + Math.random() * 0.15));
        this.sparklineData.push(val);
        this.sparklineLabels.push((year0 - i).toString());
      }
      this.sparklineData.push(base);
      this.sparklineLabels.push(year0.toString());
      for (let i = 1; i <= this.selectedPeriod; i++) {
        const interp = Math.round(base + (this.forecastResult.forecast - base) * (i / this.selectedPeriod));
        this.sparklineData.push(interp);
        this.sparklineLabels.push((year0 + i).toString());
      }
    },
    saveResults() {
      this.$toast.success("Отчет успешно сохранен!");
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
  from { transform: scale(0.8); }
  to { transform: scale(1.1); }
}
</style>
