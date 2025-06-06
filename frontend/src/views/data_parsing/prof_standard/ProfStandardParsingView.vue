<template>
  <v-container v-if="!$vuetify.display.mobile" max-width="1200" class="elevation-0 mt-5 ml-auto mr-auto">
    <v-card-title class="text-wrap" align="center">
      Парсинг реестра профессиональных стандартов
    </v-card-title>
  </v-container>

  <v-container class="elevation-5 mt-5 ml-auto mr-auto pa-0" max-width="800">
    <v-toolbar flat>
      <v-btn icon="mdi-arrow-left" color="primary" @click="$router.go(-1)" />
      <v-toolbar-title v-if="!$vuetify.display.mobile" class="text-h6 font-weight-bold">
        Назад
      </v-toolbar-title>
      <v-spacer />
      <v-btn v-if="!$vuetify.display.mobile" color="primary" prepend-icon="mdi-plus" @click="openCreateDialog">
        Добавить документ
      </v-btn>
      <v-btn v-else color="primary" icon="mdi-plus" @click="openCreateDialog"></v-btn>
    </v-toolbar>

    <v-container class="pa-0">
      <v-data-table
        :headers="headers"
        :items="documents"
        :items-per-page="10"
        class="elevation-1"
        item-value="id"
      >
        <template v-slot:item.link="{ item }">
          <a :href="item.link" target="_blank" class="text-primary">{{ truncateLink(item.link) }}</a>
        </template>

        <template v-slot:item.actions="{ item }">
          <v-tooltip text="Запустить парсинг" location="top">
            <template v-slot:activator="{ props }">
              <v-icon
                v-bind="props"
                size="small"
                class="me-2"
                color="green"
                @click="parseDocument(item)"
              >
                mdi-cog-play
              </v-icon>
            </template>
          </v-tooltip>

          <v-tooltip text="Редактировать" location="top">
            <template v-slot:activator="{ props }">
              <v-icon
                v-bind="props"
                size="small"
                class="me-2"
                @click="editDocument(item)"
              >
                mdi-pencil
              </v-icon>
            </template>
          </v-tooltip>

          <v-tooltip text="Удалить" location="top">
            <template v-slot:activator="{ props }">
              <v-icon
                v-bind="props"
                size="small"
                @click="deleteDocument(item)"
              >
                mdi-delete
              </v-icon>
            </template>
          </v-tooltip>
        </template>
      </v-data-table>
    </v-container>

    <!-- Диалоговая карточка с индикатором загрузки -->
    <v-dialog v-model="loading" persistent max-width="400">
      <v-card class="text-center pa-4">
        <v-card-title class="justify-center">Парсинг документа</v-card-title>
        <v-card-text>
          <v-progress-circular indeterminate size="64" color="primary" />
          <div class="mt-4">Идет парсинг документа...</div>
        </v-card-text>
        <v-card-actions class="justify-center">
          <v-btn color="red" @click="cancelParse">Отменить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог успешного формирования датасета -->
    <v-dialog v-model="successDialog" max-width="400">
      <v-card>
        <v-card-title class="text-h5">Парсинг завершен</v-card-title>
        <v-card-text>Датасет был сформирован успешно.</v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="primary" text @click="closeSuccess">ОК</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог создания/редактирования -->
    <v-dialog v-model="dialog" max-width="600">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ formTitle }}</span>
        </v-card-title>

        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="editedItem.name"
                  label="Название документа"
                  required
                  clearable
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="editedItem.link"
                  label="Ссылка на документ"
                  required
                  clearable
                  hint="Пример: https://profstandart.rosmintrud.ru/.../document.xlsx"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue-darken-1" text @click="close">Отмена</v-btn>
          <v-btn color="blue-darken-1" text @click="save">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог подтверждения удаления -->
    <v-dialog v-model="deleteDialog" max-width="500">
      <v-card>
        <v-card-title class="text-h5">Подтвердите удаление</v-card-title>
        <v-card-text>
          Вы уверены, что хотите удалить документ: <strong>{{ editedItem.name }}</strong>?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue-darken-1" text @click="deleteDialog = false">Отмена</v-btn>
          <v-btn color="red" text @click="confirmDelete">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
export default {
  name: "ProfStandardsView",
  data: () => ({
    dialog: false,
    deleteDialog: false,
    successDialog: false,
    loading: false,
    parseTimer: null,
    headers: [
      { title: 'Название документа', key: 'name', width: '40%' },
      { title: 'Ссылка на документ', key: 'link', width: '40%' },
      { title: 'Действия', key: 'actions', sortable: false, width: '20%' }
    ],
    documents: [
      { 
        id: 1, 
        name: 'Реестр профессиональных стандартов', 
        link: 'https://profstandart.rosmintrud.ru/upload/iblock/d4a/...02.06.2025.xlsx'
      }
    ],
    editedIndex: -1,
    editedItem: { id: 0, name: '', link: '' },
    defaultItem: { id: 0, name: '', link: '' }
  }),
  computed: {
    formTitle() {
      return this.editedIndex === -1 ? 'Новый документ' : 'Редактирование документа';
    }
  },
  methods: {
    truncateLink(link) {
      return link.length > 50 ? link.substring(0, 47) + '...' : link;
    },
    openCreateDialog() {
      this.editedItem = Object.assign({}, this.defaultItem);
      this.editedIndex = -1;
      this.dialog = true;
    },
    editDocument(item) {
      this.editedIndex = this.documents.findIndex(d => d.id === item.id);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },
    parseDocument(item) {
      this.loading = true;
      this.successDialog = false;
      this.parseTimer = setTimeout(() => {
        this.loading = false;
        this.successDialog = true;
      }, 2000);
    },
    cancelParse() {
      clearTimeout(this.parseTimer);
      this.loading = false;
    },
    closeSuccess() {
      this.successDialog = false;
    },
    deleteDocument(item) {
      this.editedIndex = this.documents.findIndex(d => d.id === item.id);
      this.editedItem = Object.assign({}, item);
      this.deleteDialog = true;
    },
    confirmDelete() {
      if (this.editedIndex !== -1) this.documents.splice(this.editedIndex, 1);
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
        Object.assign(this.documents[this.editedIndex], this.editedItem);
      } else {
        const newId = this.documents.length > 0 
          ? Math.max(...this.documents.map(d => d.id)) + 1 
          : 1;
        this.editedItem.id = newId;
        this.documents.push(this.editedItem);
      }
      this.close();
    }
  }
};
</script>

<style scoped>
.v-progress-circular {
  animation: grow 1.5s infinite alternate;
}
@keyframes grow {
  from { transform: scale(0.8); }
  to { transform: scale(1.1); }
}
</style>
