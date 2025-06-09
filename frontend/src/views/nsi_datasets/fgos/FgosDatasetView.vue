<template>
  <v-container v-if="!$vuetify.display.mobile" max-width="800" class="elevation-0 mt-5 ml-auto mr-auto">
    <v-card-title class="text-wrap" align="center">
      Управление записями ФГОС
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
        Добавить ФГОС
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
        {{ editing ? "Редактировать ФГОС" : "Добавить ФГОС" }}
      </v-card-title>
      <v-card-text>
        <v-form ref="formRef" v-model="valid" @submit.prevent="save">
          <v-text-field
            v-model="form.fgos_code"
            label="Код ФГОС"
            :rules="[rules.required]"
            clearable
          />
          <v-text-field
            v-model="form.fgos_name"
            label="Название программы"
            :rules="[rules.required]"
            clearable
          />
          <v-textarea
            v-model="form.fgos_prikaz"
            label="Приказ"
            :rules="[rules.required]"
            rows="3"
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
      <v-card-title class="text-h5">Удалить ФГОС</v-card-title>
      <v-card-text>
        Вы уверены, что хотите удалить запись «{{ datasetToDelete?.fgos_code }} — {{ datasetToDelete?.fgos_name }}»?
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
  name: "FgosDatasetView",
  data() {
    return {
      headers: [
        { title: "Код", key: "fgos_code" },
        { title: "Название", key: "fgos_name" },
        { title: "Приказ", key: "fgos_prikaz" },
        { title: "Действия", key: "actions", sortable: false, width: '20%' }
      ],
      form: {
        fgos_code: "",
        fgos_name: "",
        fgos_prikaz: "",
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
      return this.$store.state.fgos_dataset.data || [];
    },
    isLoading() {
      return this.$store.state.fgos_dataset.loading;
    },
    ...mapActions({
        getFgosDatasets: "fgos_dataset/getFgosDatasets",
        createFgosDataset: "fgos_dataset/createFgosDataset",
        updateFgosDataset: "fgos_dataset/updateFgosDataset",
        deleteFgosDataset: "fgos_dataset/deleteFgosDataset",
    }),
    openCreateDialog() {
      this.editingDataset = null;
      this.form = {
        fgos_code: "",
        fgos_name: "",
        fgos_prikaz: "",
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
        await this.updateFgosDataset({ id: this.editingDataset.id, payload });
      } else {
        await this.createFgosDataset(payload);
      }
      await this.getFgosDatasets();
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
      await this.deleteFgosDataset(this.datasetToDelete.id);
      await this.getFgosDatasets();
      this.closeConfirmDialog();
    },
  },
  async created() {
    await this.getFgosDatasets();
  },
};
</script>
