<template>
    <v-container v-if="!$vuetify.display.mobile" max-width="800" class="elevation-0 mt-5 ml-auto mr-auto">
        <v-card-title class="text-wrap" align="center">
            Источники данных
        </v-card-title>
    </v-container>

    <v-container class="elevation-0 mt-5 ml-auto mr-auto" max-width="1200">
        <v-toolbar flat color="white">
            <v-btn icon="mdi-arrow-left" color="primary" @click="$router.push('/')" />
            <v-toolbar-title v-if="!$vuetify.display.mobile" class="text-subtitle-1 font-weight-bold">
                На главную
            </v-toolbar-title>
            <v-spacer />
        </v-toolbar>

        <v-card-text>
            <v-row>
                <v-col 
                    v-for="(source, index) in sources" 
                    :key="index"
                    cols="12" 
                    sm="6" 
                    md="4"
                >
                    <v-card 
                        class="pa-4 text-center rounded-lg d-flex flex-column"
                        elevation="3"
                        height="100%"
                        @click="selectSource(source)"
                    >
                        <v-icon 
                            size="64" 
                            color="blue-darken-2" 
                            class="mb-4"
                        >
                            {{ source.icon }}
                        </v-icon>
                        
                        <v-card-title class="text-subtitle-1 justify-center text-wrap">
                            {{ source.title }}
                        </v-card-title>
                        <v-card-text class="text-center flex-grow-1" height="100%">
                            <!-- Здесь можно добавить описание источника данных или инструкцию по его использованию. -->
                        </v-card-text>
                        <v-card-actions class="justify-center">
                            <v-btn 
                                color="primary" 
                                @click="selectSource(source)"
                                prepend-icon="mdi-download"
                            >
                                Выбрать источник
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                </v-col>
            </v-row>
        </v-card-text>
    </v-container>
</template>

<script>
    export default {
        name: "DataSourcesView",
        data() {
            return {
                sources: [
                    { title: "Кадровые агентства", id: "hh_ru/jobs", icon: "mdi-account-tie" },
                    { title: "Стратегический план развития региона", id: "regional-plan", icon: "mdi-map-legend" },
                    { title: "Национальная программа развития РФ", id: "national-plan", icon: "mdi-star-circle" },
                    { title: "ФГОС", id: "fgos", icon: "mdi-book-education" },
                    { title: "Профстандарты", id: "profstandards", icon: "mdi-certificate" },
                    { title: "Официальная статистика по количеству работников", id: "statistics", icon: "mdi-chart-bar" },
                    { title: "Контрольные цифры приема ВО, СПО", id: "kcp", icon: "mdi-school" },
                    { title: "Классификатор профессий", id: "prof-classificator", icon: "mdi-account-group" },
                    { title: "ОКВЭД", id: "okved", icon: "mdi-factory" }
                ]
            };
        },
        methods: {
            selectSource(source) {
                console.log("Сбор данных из источника:", source.title);
                
                this.$router.push(`/data-parsing/${source.id}`);
            }
        }
    };
</script>

<style scoped>
.v-card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.v-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.12) !important;
}
</style>