<template>
    <v-container v-if="!$vuetify.display.mobile" max-width="800" class="elevation-0 mt-5 ml-auto mr-auto">
        <v-card-title class="text-wrap" align="center">
            НСИ Датасеты
        </v-card-title>
    </v-container>

    <v-container class="elevation-2 mt-5 ml-auto mr-auto bg-white rounded-lg" max-width="1200">
        <v-toolbar flat color="white">
            <v-btn icon="mdi-arrow-left" color="primary" @click="$router.push('/main-menu')" />
            <v-toolbar-title v-if="!$vuetify.display.mobile" class="text-subtitle-1 font-weight-bold">
                Назад
            </v-toolbar-title>
            <v-spacer />
        </v-toolbar>

        <v-card-text>
            <v-row>
                <v-col 
                    v-for="(dataset, index) in datasets" 
                    :key="index"
                    cols="12" 
                    sm="6" 
                    md="4"
                >
                    <v-card 
                        class="pa-4 text-center rounded-lg d-flex flex-column"
                        elevation="3"
                        height="100%"
                        @click="selectDataset(dataset)"
                    >
                        <v-icon 
                            size="64" 
                            color="blue-darken-2" 
                            class="mb-4"
                        >
                            {{ dataset.icon }}
                        </v-icon>
                        
                        <v-card-title class="text-subtitle-1 justify-center text-wrap">
                            {{ dataset.title }}
                        </v-card-title>
                         <v-card-text class="text-center flex-grow-1" height="100%">
                            <!-- Здесь можно добавить описание источника данных или инструкцию по его использованию. -->
                        </v-card-text>
                        <v-card-actions class="justify-center">
                            <v-btn 
                                color="primary" 
                                @click="selectDataset(dataset)"
                                prepend-icon="mdi-arrow-right"
                            >
                                Перейти
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
        name: "DatasetsView",
        data() {
            return {
                datasets: [
                    { title: "Кадровые агентства", id: "hh-ru", icon: "mdi-account-tie" },
                    { title: "Стратегический план развития региона", id: "region-plan", icon: "mdi-map-legend" },
                    { title: "Национальная программа развития РФ", id: "national-program", icon: "mdi-star-circle" },
                    { title: "Перечень ФГОС", id: "fgos", icon: "mdi-book-education" },
                    { title: "Профстандарты", id: "prof-standard", icon: "mdi-certificate" },
                    { title: "Официальная статистика по количеству работников", id: "stat-otchet", icon: "mdi-chart-bar" },
                    { title: "Контрольные цифры приема ВО, СПО", id: "kcp", icon: "mdi-school" },
                    { title: "Классификатор профессий", id: "classificator-prof", icon: "mdi-account-group" },
                    { title: "ОКВЭД", id: "okved", icon: "mdi-factory" }
                ]
            };
        },
        methods: {
            selectDataset(dataset) {
                console.log("Переход к датасету:", dataset.title);
                // Реальная логика перехода:
                this.$router.push(`/datasets/${dataset.id}`);
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