<template>
  <v-container v-if="!$vuetify.display.mobile" max-width="800" class="elevation-0 mt-5 ml-auto mr-auto">
    <v-card-title class="text-wrap" align="center">
      Управление профессиональными стандартами
    </v-card-title>
  </v-container>

  <v-container class="elevation-5 mt-5 ml-auto mr-auto pa-0" max-width="1100">
    <v-toolbar flat>
      <v-btn icon="mdi-arrow-left" color="primary" @click="$router.push('/datasets')" />
      <v-toolbar-title v-if="!$vuetify.display.mobile" class="text-h6 font-weight-bold">
        Назад
      </v-toolbar-title>
      <v-spacer />
      <v-btn v-if="!$vuetify.display.mobile" color="primary" prepend-icon="mdi-plus" @click="openCreateDialog">
        Добавить стандарт
      </v-btn>
      <v-btn v-else color="primary" icon="mdi-plus" @click="openCreateDialog" />
    </v-toolbar>

    <v-data-table-server
      :headers="headers"
      :items="datasets()"
      :loading="isLoading()"
      :items-per-page="-1"
      hide-default-footer
    >
      <template v-slot:item.actions="{ item }">
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

  <!-- Create / Edit Dialog -->
  <v-dialog v-model="editDialog" max-width="600px">
    <v-card>
      <v-card-title class="text-h5">
        {{ editing ? "Редактировать стандарт" : "Добавить стандарт" }}
      </v-card-title>
      <v-card-text>
        <v-form ref="formRef" v-model="valid" @submit.prevent="save">
          <v-text-field
            v-model="form.prof_standard_code"
            label="Код стандарта"
            :rules="[rules.required]"
            clearable
          />
          <v-text-field
            v-model="form.prof_standard_sphere"
            label="Сфера деятельности"
            :rules="[rules.required]"
            clearable
          />
          <v-text-field
            v-model="form.prof_standard_type"
            label="Тип деятельности"
            :rules="[rules.required]"
            clearable
          />
          <v-textarea
            v-model="form.prof_standard_name"
            label="Наименование стандарта"
            :rules="[rules.required]"
            auto-grow
            clearable
          />
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="closeEditDialog">Отмена</v-btn>
        <v-btn color="primary" :disabled="!valid" @click="save">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <!-- Confirm Delete -->
  <v-dialog v-model="confirmDeleteDialog" max-width="400px">
    <v-card>
      <v-card-title class="text-h5">Удалить стандарт</v-card-title>
      <v-card-text>
        Вы уверены, что хотите удалить запись «{{ datasetToDelete?.prof_standard_code }} — {{ datasetToDelete?.prof_standard_name }}»?
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
  name: "ProfStandardView",
  data() {
    return {
      headers: [
        { title: "Код", key: "prof_standard_code" },
        { title: "Сфера", key: "prof_standard_sphere" },
        { title: "Тип", key: "prof_standard_type" },
        { title: "Наименование", key: "prof_standard_name" },
        { title: "Действия", key: "actions", sortable: false}
      ],
      form: {
        prof_standard_code: "",
        prof_standard_sphere: "",
        prof_standard_type: "",
        prof_standard_name: "",
      },
      editingDataset: null,
      datasetToDelete: null,
      editDialog: false,
      confirmDeleteDialog: false,
      valid: false,
      rules: {
        required: v => !!v || "Обязательное поле",
      },
    };
  },
  methods: {
    datasets() {
      return this.$store.state.prof_standard_dataset.data || [];
    },
    isLoading() {
      return this.$store.state.prof_standard_dataset.loading;
    },
    ...mapActions({
      getDatasets: "prof_standard_dataset/getProfStandardDatasets",
      createDataset: "prof_standard_dataset/createProfStandardDataset",
      updateDataset: "prof_standard_dataset/updateProfStandardDataset",
      deleteDataset: "prof_standard_dataset/deleteProfStandardDataset",
    }),
    openCreateDialog() {
      this.editingDataset = null;
      this.form = {
        prof_standard_code: "",
        prof_standard_sphere: "",
        prof_standard_type: "",
        prof_standard_name: "",
      };
      this.editDialog = true;
    },
    openEditDialog(item) {
      this.editingDataset = item;
      this.form = { ...item };
      this.editDialog = true;
    },
    closeEditDialog() {
      this.editDialog = false;
    },
    async save() {
      const payload = { ...this.form };
      if (this.editingDataset) {
        await this.updateDataset({ id: this.editingDataset.id, payload });
      } else {
        await this.createDataset(payload);
      }
      await this.getDatasets();
      this.closeEditDialog();
    },
    confirmDelete(item) {
      this.datasetToDelete = item;
      this.confirmDeleteDialog = true;
    },
    closeConfirmDialog() {
      this.confirmDeleteDialog = false;
    },
    async deleteConfirmed() {
      if (!this.datasetToDelete) return;
      await this.deleteDataset(this.datasetToDelete.id);
      await this.getDatasets();
      this.closeConfirmDialog();
    },
  },
  async created() {
    await this.getDatasets();
  },
};
</script>
