<template>
    <v-container v-if="!$vuetify.display.mobile" max-width="800" class="elevation-0 mt-5 ml-auto mr-auto">
        <v-card-title class="text-wrap" align="center">
            Управление пользователями
        </v-card-title>
    </v-container>
    <v-container class="elevation-5 mt-5 ml-auto mr-auto pa-0" max-width="800">
        <v-toolbar flat>
            <v-btn icon="mdi-arrow-left" color="primary" @click="$router.push('/')" />
            <v-toolbar-title v-if="!$vuetify.display.mobile" class="text-h6 font-weight-bold">
                На главную
            </v-toolbar-title>
            <v-spacer />
            <v-btn v-if="!$vuetify.display.mobile" color="primary" prepend-icon="mdi-plus" @click="openCreateDialog">
                Добавить пользователя
            </v-btn>
            <v-btn v-else color="primary" icon="mdi-plus" @click="openCreateDialog">
            </v-btn>
        </v-toolbar>

        <v-container class="pa-0">
            <v-data-table
                :headers="headers"
                :items="users"
                :items-per-page="10"
                class="elevation-1"
            >
                <template v-slot:item.actions="{ item }">
                    <v-icon
                        size="small"
                        class="me-2"
                        @click="editUser(item)"
                    >
                        mdi-pencil
                    </v-icon>
                    <v-icon
                        size="small"
                        @click="deleteUser(item)"
                    >
                        mdi-delete
                    </v-icon>
                </template>
            </v-data-table>
        </v-container>

        <!-- Диалог создания/редактирования -->
        <v-dialog v-model="dialog" max-width="500">
            <v-card>
                <v-card-title>
                    <span class="text-h5">{{ formTitle }}</span>
                </v-card-title>

                <v-card-text>
                    <v-container>
                        <v-row>
                            <v-col cols="12">
                                <v-text-field
                                    v-model="editedItem.fullName"
                                    label="ФИО"
                                    required
                                ></v-text-field>
                            </v-col>
                            <v-col cols="12">
                                <v-select
                                    v-model="editedItem.role"
                                    :items="roles"
                                    label="Роль"
                                    required
                                ></v-select>
                            </v-col>
                        </v-row>
                    </v-container>
                </v-card-text>

                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue-darken-1" variant="text" @click="close">
                        Отмена
                    </v-btn>
                    <v-btn color="blue-darken-1" variant="text" @click="save">
                        Сохранить
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <!-- Диалог подтверждения удаления -->
        <v-dialog v-model="deleteDialog" max-width="500">
            <v-card>
                <v-card-title class="text-h5">Вы уверены?</v-card-title>
                <v-card-text>
                    Вы собираетесь удалить пользователя: <strong>{{ editedItem.fullName }}</strong>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue-darken-1" variant="text" @click="deleteDialog = false">
                        Отмена
                    </v-btn>
                    <v-btn color="red" variant="text" @click="confirmDelete">
                        Удалить
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-container>
</template>

<script>
    export default {
        name: "UserManagementView",
        data: () => ({
            dialog: false,
            deleteDialog: false,
            headers: [
                { title: 'ID', key: 'id', width: '80px' },
                { title: 'ФИО', key: 'fullName' },
                { title: 'Роль', key: 'role' },
                { title: 'Действия', key: 'actions', sortable: false, width: '100px' }
            ],
            users: [
                { id: 1, fullName: 'Иванов Иван Иванович', role: 'Администратор' },
                { id: 2, fullName: 'Петрова Светлана Викторовна', role: 'Редактор' },
                { id: 3, fullName: 'Сидоров Алексей Петрович', role: 'Аналитик' },
                { id: 4, fullName: 'Кузнецова Ольга Сергеевна', role: 'Пользователь' },
            ],
            roles: ['Администратор', 'Редактор', 'Аналитик', 'Пользователь'],
            editedIndex: -1,
            editedItem: {
                id: 0,
                fullName: '',
                role: ''
            },
            defaultItem: {
                id: 0,
                fullName: '',
                role: ''
            }
        }),
        computed: {
            formTitle() {
                return this.editedIndex === -1 ? 'Новый пользователь' : 'Редактирование пользователя';
            }
        },
        methods: {
            openCreateDialog() {
                this.editedItem = Object.assign({}, this.defaultItem);
                this.editedIndex = -1;
                this.dialog = true;
            },
            
            editUser(item) {
                this.editedIndex = this.users.indexOf(item);
                this.editedItem = Object.assign({}, item);
                this.dialog = true;
            },
            
            deleteUser(item) {
                this.editedIndex = this.users.indexOf(item);
                this.editedItem = Object.assign({}, item);
                this.deleteDialog = true;
            },
            
            confirmDelete() {
                this.users.splice(this.editedIndex, 1);
                this.closeDelete();
            },
            
            close() {
                this.dialog = false;
                this.$nextTick(() => {
                    this.editedItem = Object.assign({}, this.defaultItem);
                    this.editedIndex = -1;
                });
            },
            
            closeDelete() {
                this.deleteDialog = false;
                this.$nextTick(() => {
                    this.editedItem = Object.assign({}, this.defaultItem);
                    this.editedIndex = -1;
                });
            },
            
            save() {
                if (this.editedIndex > -1) {
                    // Обновление существующего пользователя
                    Object.assign(this.users[this.editedIndex], this.editedItem);
                } else {
                    // Создание нового пользователя
                    const newId = Math.max(...this.users.map(u => u.id)) + 1;
                    this.editedItem.id = newId;
                    this.users.push(this.editedItem);
                }
                this.close();
            }
        }
    };
</script>

<style scoped>
/* .v-data-table {
    border-radius: 8px;
    overflow: hidden;
} */
</style>