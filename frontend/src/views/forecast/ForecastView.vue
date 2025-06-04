<template>
    <v-container v-if="!$vuetify.display.mobile" max-width="800" class="elevation-0 mt-5 ml-auto mr-auto">
        <v-card-title class="text-wrap" align="center">
            Прогнозирование спроса на работников
        </v-card-title>
    </v-container>
    <v-container class="elevation-0 mt-5 ml-auto mr-auto" max-width="1000">
        <v-toolbar flat color="white">
            <v-btn icon="mdi-arrow-left" color="primary" @click="$router.push('/')" />
            <v-toolbar-title v-if="!$vuetify.display.mobile" class="text-h6 font-weight-bold">
                На главную
            </v-toolbar-title>
            <v-spacer />
        </v-toolbar>

        <v-card class="mt-5 pa-6">
            <v-row>
                <v-col cols="12" md="4">
                    <v-select
                        v-model="selectedModel"
                        :items="mlModels"
                        label="Модель прогнозирования"
                        outlined
                        dense
                    ></v-select>
                </v-col>
                
                <v-col cols="12" md="4">
                    <v-select
                        v-model="selectedPeriod"
                        :items="periods"
                        label="Период прогнозирования"
                        outlined
                        dense
                    ></v-select>
                </v-col>
                
                <v-col cols="12" md="4">
                    <v-select
                        v-model="forecastType"
                        :items="forecastTypes"
                        label="Тип прогноза"
                        outlined
                        dense
                        item-title="text"
                        item-value="value"
                        return-object
                        clearable
                    ></v-select>
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
                    ></v-autocomplete>
                </v-col>
            </v-row>
            
            <v-row v-else>
                <v-col cols="12">
                    <v-autocomplete
                        v-model="selectedSector"
                        :items="economicSectors"
                        label="Выберите сферу экономики (ОКВЭД)"
                        outlined
                        dense
                        clearable
                    ></v-autocomplete>
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

        <!-- Индикатор загрузки -->
        <v-overlay 
            :model-value="loading" 
            class="align-center justify-center"
            persistent
        >
            <v-progress-circular 
                color="primary" 
                size="64" 
                indeterminate
            >
            </v-progress-circular>
        </v-overlay>

        <!-- Результаты прогноза -->
        <v-card v-if="showResults" class="mt-6 pa-6">
            <v-card-title class="text-h6">
                Прогноз спроса на 
                <span v-if="forecastType === 'profession'">профессию: {{ selectedProfession }}</span>
                <span v-else>сферу: {{ selectedSector }}</span>
            </v-card-title>
            
            <v-card-subtitle>
                Модель: {{ selectedModel }}, Период: {{ selectedPeriod }} лет
            </v-card-subtitle>
            
            <v-card-text>
                <div class="d-flex align-center justify-space-between">
                    <div>
                        <div class="text-h4 primary--text">{{ forecastResult.current | formatNumber }}</div>
                        <div class="text-caption">Текущий спрос</div>
                    </div>
                    
                    <div class="text-center">
                        <div class="text-h4" :class="forecastResult.change >= 0 ? 'green--text' : 'red--text'">
                            {{ forecastResult.change >= 0 ? '+' : '' }}{{ forecastResult.change | formatNumber }}%
                        </div>
                        <div class="text-caption">Изменение</div>
                    </div>
                    
                    <div>
                        <div class="text-h4 blue--text">{{ forecastResult.forecast | formatNumber }}</div>
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
                <v-spacer></v-spacer>
                <v-btn color="primary" @click="saveResults" prepend-icon="mdi-content-save">
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
            
            // Параметры выбора
            selectedModel: null,
            selectedPeriod: null,
            forecastType: 'profession',
            selectedProfession: null,
            selectedSector: null,
            
            // Результаты прогноза
            forecastResult: {
                current: 0,
                forecast: 0,
                change: 0
            },
            
            // Данные для графика
            sparklineData: [],
            sparklineLabels: [],
            
            // Списки для выбора
            mlModels: [
                'Линейная регрессия',
                'ARIMA',
                'Prophet',
                'LSTM нейросеть',
                'Градиентный бустинг'
            ],
            
            periods: [1, 3, 5, 10],
            
            forecastTypes: [
                { text: 'По профессии', value: 'profession' },
                { text: 'По сфере экономики (ОКВЭД)', value: 'sector' }
            ],
            
            professions: [
                'Программист',
                'Инженер-конструктор',
                'Врач-терапевт',
                'Учитель математики',
                'Аналитик данных',
                'Маркетолог',
                'Бухгалтер',
                'Электрик',
                'Повар',
                'Водитель'
            ],
            
            economicSectors: [
                'IT и коммуникации',
                'Производство',
                'Здравоохранение',
                'Образование',
                'Финансы и страхование',
                'Торговля',
                'Транспорт и логистика',
                'Строительство',
                'Гостиничный бизнес',
                'Сельское хозяйство'
            ]
        };
    },
    computed: {
        canRunForecast() {
            if (!this.selectedModel || !this.selectedPeriod) return false;
            
            if (this.forecastType === 'profession') {
                return !!this.selectedProfession;
            } else {
                return !!this.selectedSector;
            }
        }
    },
    methods: {
        runForecast() {
            // Показать индикатор загрузки
            this.loading = true;
            this.showResults = false;
            
            // Имитация работы модели (2 секунды)
            setTimeout(() => {
                this.generateResults();
                this.loading = false;
                this.showResults = true;
                this.chartKey++; // Принудительное обновление графика
            }, 2000);
        },
        
        generateResults() {
            // Генерация случайных данных для демонстрации
            const baseValue = Math.floor(Math.random() * 500) + 100;
            const changePercentage = (Math.random() * 30) - 10; // От -10% до +20%
            
            this.forecastResult = {
                current: baseValue,
                forecast: Math.round(baseValue * (1 + changePercentage / 100)),
                change: parseFloat(changePercentage.toFixed(1))
            };
            
            // Генерация данных для графика
            this.sparklineData = [];
            this.sparklineLabels = [];
            
            // Исторические данные (5 лет назад - текущий год)
            for (let i = 5; i > 0; i--) {
                const year = new Date().getFullYear() - i;
                const value = Math.round(baseValue * (0.8 + Math.random() * 0.4));
                
                this.sparklineData.push(value);
                this.sparklineLabels.push(year.toString());
            }
            
            // Текущий год
            this.sparklineData.push(this.forecastResult.current);
            this.sparklineLabels.push(new Date().getFullYear().toString());
            
            // Прогноз на выбранный период
            const period = parseInt(this.selectedPeriod);
            for (let i = 1; i <= period; i++) {
                const year = new Date().getFullYear() + i;
                const progress = i / period;
                const value = Math.round(
                    this.forecastResult.current + 
                    (this.forecastResult.forecast - this.forecastResult.current) * progress
                );
                
                this.sparklineData.push(value);
                this.sparklineLabels.push(year.toString());
            }
        },
        
        saveResults() {
            // В реальном приложении здесь будет сохранение отчета
            console.log("Сохранение результатов прогноза");
            this.$toast.success('Отчет успешно сохранен!');
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