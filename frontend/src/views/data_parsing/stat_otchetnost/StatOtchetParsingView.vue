<template>
  <v-container v-if="!$vuetify.display.mobile" max-width="1200" class="elevation-0 mt-5 ml-auto mr-auto">
    <v-card-title class="text-wrap" align="center">
      Парсинг отчетов министерства статистики
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
        Добавить источник
      </v-btn>
      <v-btn v-else color="primary" icon="mdi-plus" @click="openCreateDialog"></v-btn>
    </v-toolbar>

    <v-container class="pa-0">
      <v-data-table
        :headers="headers"
        :items="sources"
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
                @click="parseSource(item)"
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
                @click="editSource(item)"
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
                @click="deleteSource(item)"
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
        <v-card-title class="justify-center">Парсинг источника</v-card-title>
        <v-card-text>
          <v-progress-circular indeterminate size="64" color="primary" />
          <div class="mt-4">Идет парсинг источника...</div>
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
                  v-model="editedSource.name"
                  label="Название источника"
                  required
                  clearable
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="editedSource.link"
                  label="Ссылка на источник"
                  required
                  clearable
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue-darken-1" text @click="closeDialog">Отмена</v-btn>
          <v-btn color="blue-darken-1" text @click="saveSource">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог подтверждения удаления -->
    <v-dialog v-model="deleteDialog" max-width="500">
      <v-card>
        <v-card-title class="text-h5">Подтвердите удаление</v-card-title>
        <v-card-text>
          Вы уверены, что хотите удалить источник: <strong>{{ editedSource.name }}</strong>?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue-darken-1" text @click="cancelDelete">Отмена</v-btn>
          <v-btn color="red" text @click="confirmDelete">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
export default {
  name: "StatOtchetParsingView",
  data: () => ({
    dialog: false,
    deleteDialog: false,
    successDialog: false,
    loading: false,
    parseTimer: null,
    headers: [
      { title: 'Название источника', key: 'name', width: '40%' },
      { title: 'Ссылка на источник', key: 'link', width: '40%' },
      { title: 'Действия', key: 'actions', sortable: false, width: '20%' }
    ],
    sources: [
      { 
        id: 1, 
        name: 'Среднегодовая численность занятых по видам деятельности в Пермском крае в 2010-2016, 2017-2023 гг.', 
        link: 'https://59.rosstat.gov.ru/storage/mediabank/%D0%A1%D1%80%D0%B5%D0%B4%D0%BD%D0%B5%D0%B3%D0%BE%D0%B4%D0%BE%D0%B2%D0%B0%D1%8F%20%D1%87%D0%B8%D1%81%D0%BB%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D1%8C%20%D0%B7%D0%B0%D0%BD%D1%8F%D1%82%D1%8B%D1%85%20%D0%BF%D0%BE%20%D0%B2%D0%B8%D0%B4%D0%B0%D0%BC%20%D0%B4%D0%B5%D1%8F%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%BE%D1%81%D1%82%D0%B8%20%D0%B2%20%D0%9F%D0%B5%D1%80%D0%BC%D1%81%D0%BA%D0%BE%D0%BC%20%D0%BA%D1%80%D0%B0%D0%B5%20%D0%B2%202010-2016,%202017-2023%20%D0%B3%D0%B3..xlsx'
      }
    ],
    editedSource: { id: 0, name: '', link: '' },
    defaultSource: { id: 0, name: '', link: '' },
    editedIndex: -1
  }),
  computed: {
    formTitle() {
      return this.editedIndex === -1 ? 'Новый источник' : 'Редактирование источника';
    }
  },
  methods: {
    truncateLink(link) {
      return link.length > 50 ? link.substring(0, 47) + '...' : link;
    },
    openCreateDialog() {
      this.editedSource = Object.assign({}, this.defaultSource);
      this.editedIndex = -1;
      this.dialog = true;
    },
    editSource(item) {
      this.editedIndex = this.sources.findIndex(s => s.id === item.id);
      this.editedSource = Object.assign({}, item);
      this.dialog = true;
    },
    parseSource(item) {
      this.loading = true;
      this.successDialog = false;
      this.parseTimer = setTimeout(() => {
        this.loading = false;
        this.successDialog = true;
      }, 4000);
    },
    cancelParse() {
      clearTimeout(this.parseTimer);
      this.loading = false;
    },
    closeSuccess() {
      this.successDialog = false;
    },
    deleteSource(item) {
      this.editedIndex = this.sources.findIndex(s => s.id === item.id);
      this.editedSource = Object.assign({}, item);
      this.deleteDialog = true;
    },
    confirmDelete() {
      if (this.editedIndex !== -1) this.sources.splice(this.editedIndex, 1);
      this.cancelDelete();
    },
    cancelDelete() {
      this.deleteDialog = false;
      this.$nextTick(() => {
        this.editedSource = Object.assign({}, this.defaultSource);
        this.editedIndex = -1;
      });
    },
    closeDialog() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedSource = Object.assign({}, this.defaultSource);
        this.editedIndex = -1;
      });
    },
    saveSource() {
      if (this.editedIndex > -1) {
        Object.assign(this.sources[this.editedIndex], this.editedSource);
      } else {
        const newId = this.sources.length > 0 
          ? Math.max(...this.sources.map(s => s.id)) + 1 
          : 1;
        this.editedSource.id = newId;
        this.sources.push(this.editedSource);
      }
      this.closeDialog();
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