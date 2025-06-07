<template>
  <v-container v-if="!$vuetify.display.mobile" max-width="800" class="elevation-0 mt-5 ml-auto mr-auto">
    <v-card-title class="text-wrap" align="center">
      Парсинг общероссийского классификатора профессий
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

    <v-data-table-server
      :headers="headers"
      :items="sources()"
      :loading="isLoading()"
      :items-per-page="-1"
      hide-default-footer
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
              @click="openEditDialog(item)"
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
              @click="confirmDelete(item)"
            >
              mdi-delete
            </v-icon>
          </template>
        </v-tooltip>
      </template>
    </v-data-table-server>
  </v-container>

  <!-- Диалог парсинга -->
  <v-dialog v-model="loadingDialog" persistent max-width="400">
    <v-card class="text-center pa-4">
      <v-card-title class="justify-center">Парсинг источника</v-card-title>
      <v-card-text>
        <v-progress-circular indeterminate size="64" />
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

  <!-- Create / Edit Dialog -->
  <v-dialog v-model="editDialog" max-width="450px">
    <v-card>
      <v-card-title class="text-h5">
        {{ editingSource ? "Редактировать источник" : "Создать источник" }}
      </v-card-title>
      <v-card-text>
        <v-form ref="formRef" v-model="valid" @submit.prevent="saveSource">
          <v-text-field
            v-model="form.name"
            label="Название источника"
            :rules="[rules.required]"
            clearable
          />
          <v-text-field
            v-model="form.link"
            label="Ссылка на источник"
            :rules="[rules.required]"
            clearable
          />
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="closeEditDialog">Отмена</v-btn>
        <v-btn color="primary" :disabled="!valid" @click="saveSource">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <!-- Delete Confirmation Dialog -->
  <v-dialog v-model="confirmDeleteDialog" max-width="400px">
    <v-card>
      <v-card-title class="text-h5">Подтвердите удаление</v-card-title>
      <v-card-text>
        Вы уверены, что хотите удалить источник
        «{{ sourceToDelete?.name }}»?
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="closeConfirmDialog">Отмена</v-btn>
        <v-btn color="red" @click="deleteConfirmed">Удалить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapActions } from "vuex";

export default {
  name: "ProfClassificatorParsingView",
  data() {
    return {
      sourceType: "prof_classificator",
      headers: [
        { title: "Название", key: "name" },
        { title: "Ссылка", key: "link" },
        { title: "Действия", key: "actions", sortable: false, width: "20%" },
      ],
      editDialog: false,
      confirmDeleteDialog: false,
      loadingDialog: false,
      successDialog: false,
      parseTimer: null,
      editingSource: null,
      sourceToDelete: null,
      form: { name: "", link: "" },
      valid: false,
      rules: {
        required: v => !!v || "Это поле обязательно",
      },
    };
  },

  methods: {
    sources() {
      return this.$store.state.data_sources.data || [];
    },
    isLoading() {
      return this.$store.state.data_sources.loading;
    },
    ...mapActions("data_sources", [
      "getDataSourcesByType",
      "createDataSource",
      "updateDataSource",
      "deleteDataSource",
    ]),

    truncateLink(link) {
      return link.length > 50 ? link.slice(0, 47) + "..." : link;
    },

    openCreateDialog() {
      this.editingSource = null;
      this.form = { name: "", link: "" };
      this.editDialog = true;
    },
    openEditDialog(item) {
      this.editingSource = item;
      this.form = { name: item.name, link: item.link };
      this.editDialog = true;
    },
    closeEditDialog() {
      this.editDialog = false;
      this.$nextTick(() => {
        this.form = { name: "", link: "" };
        this.editingSource = null;
      });
    },
    async saveSource() {
      const payload = { ...this.form, source_type: this.sourceType };
      if (this.editingSource) {
        await this.updateDataSource({ id: this.editingSource.id, payload });
      } else {
        await this.createDataSource(payload);
      }
      await this.getDataSourcesByType(this.sourceType);
      this.closeEditDialog();
    },

    confirmDelete(item) {
      this.sourceToDelete = item;
      this.confirmDeleteDialog = true;
    },
    closeConfirmDialog() {
      this.confirmDeleteDialog = false;
      this.sourceToDelete = null;
    },
    async deleteConfirmed() {
      if (!this.sourceToDelete) return;
      await this.deleteDataSource(this.sourceToDelete.id);
      await this.getDataSourcesByType(this.sourceType);
      this.closeConfirmDialog();
    },

    parseSource(item) {
      this.loadingDialog = true;
      this.successDialog = false;
      this.parseTimer = setTimeout(() => {
        this.loadingDialog = false;
        this.successDialog = true;
      }, 4000);
    },
    cancelParse() {
      clearTimeout(this.parseTimer);
      this.loadingDialog = false;
    },
    closeSuccess() {
      this.successDialog = false;
    },
  },
  async created() {
    await this.getDataSourcesByType(this.sourceType);
  },
};
</script>

<style scoped>
</style>
