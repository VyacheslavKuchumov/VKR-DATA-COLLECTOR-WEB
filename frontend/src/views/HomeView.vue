<template>
    <v-container max-width="800" class="elevation-0 mt-5 ml-auto mr-auto">
        <v-card-title class="text-wrap text-center justify-center">
            <h1 class="text-h4">Система анализа и прогнозирования кадрового потенциала</h1>
        </v-card-title>
    </v-container>

    <v-container class="elevation-5 mt-5 ml-auto mr-auto" max-width="1000">
        <v-card-text>
            <v-row>
                <v-col 
                    v-for="(section, index) in sections" 
                    :key="index"
                    cols="12" 
                    sm="6" 
                    md="6"
                >
                    <v-card 
                        class="pa-4 rounded-lg d-flex flex-column"
                        elevation="3"
                        height="100%"
                        :color="section.color"
                        @click="selectSection(section)"
                    >
                        <div class="d-flex align-center">
                            <v-icon 
                                size="64" 
                                :color="section.iconColor"
                                class="mr-4"
                            >
                                {{ section.icon }}
                            </v-icon>
                            
                            <v-card-title class="text-h6 font-weight-bold text-wrap">
                                {{ section.title }}
                            </v-card-title>
                        </div>

                        <v-card-text class="mt-2 flex-grow-1">
                            {{ section.description }}
                        </v-card-text>
                        
                        <v-card-actions class="justify-end">
                            <v-btn 
                                color="white"
                                variant="outlined"
                                @click.stop="selectSection(section)"
                                append-icon="mdi-arrow-right"
                                size="large"
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
        name: "HomeView",
        data() {
            return {
                sections: [
                    { 
                        title: "Управление пользователями", 
                        id: "users", 
                        icon: "mdi-account-cog", 
                        description: "Управление учетными записями, ролями и правами доступа пользователей системы",
                        color: "blue-lighten-4",
                        iconColor: "blue-darken-2"
                    },
                    { 
                        title: "НСИ датасеты", 
                        id: "datasets", 
                        icon: "mdi-datasets", 
                        description: "Просмотр и управление нормативно-справочной информацией",
                        color: "green-lighten-4",
                        iconColor: "green-darken-2"
                    },
                    { 
                        title: "Сбор данных", 
                        id: "data-parsing", 
                        icon: "mdi-cloud-download", 
                        description: "Интеграция данных из внешних источников и систем",
                        color: "orange-lighten-4",
                        iconColor: "orange-darken-2"
                    },
                    { 
                        title: "Прогнозы", 
                        id: "forecasts", 
                        icon: "mdi-chart-line", 
                        description: "Аналитические отчеты и прогнозные модели",
                        color: "purple-lighten-4",
                        iconColor: "purple-darken-2"
                    }
                ]
            };
        },
        methods: {
            selectSection(section) {
                console.log("Переход в раздел:", section.title);
                this.$router.push(`/${section.id}`);
            }
        }
    };
</script>

<style scoped>

.text-h6 {
    font-size: 1.25rem;
    line-height: 1.6;
}
</style>