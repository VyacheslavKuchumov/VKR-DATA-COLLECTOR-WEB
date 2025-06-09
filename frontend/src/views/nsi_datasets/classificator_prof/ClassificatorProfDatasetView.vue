<template>
  <v-container v-if="!$vuetify.display.mobile" max-width="800" class="elevation-0 mt-5 ml-auto mr-auto">
    <v-card-title class="text-wrap" align="center">
      Управление профессиями
    </v-card-title>
  </v-container>

  <v-container class="elevation-5 mt-5 ml-auto mr-auto pa-0" max-width="800">
    <v-toolbar flat>
      <v-btn icon="mdi-arrow-left" color="primary" @click="$router.push('/datasets')" />
      <v-toolbar-title v-if="!$vuetify.display.mobile" class="text-h6 font-weight-bold">
        Назад
      </v-toolbar-title>
      <v-spacer />
      <v-btn v-if="!$vuetify.display.mobile" color="primary" prepend-icon="mdi-plus" @click="openCreateDialog">
        Добавить профессию
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
        {{ editing ? "Редактировать профессию" : "Добавить профессию" }}
      </v-card-title>
      <v-card-text>
        <v-form ref="formRef" v-model="valid" @submit.prevent="save">
          <v-text-field
            v-model="form.prof_code"
            label="Код профессии"
            :rules="[rules.required]"
            clearable
          />
          <v-text-field
            v-model="form.prof_name"
            label="Название профессии"
            :rules="[rules.required]"
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

  <!-- Confirm Delete Dialog -->
  <v-dialog v-model="confirmDeleteDialog" max-width="400px">
    <v-card>
      <v-card-title class="text-h5">Удалить профессию</v-card-title>
      <v-card-text>
        Вы уверены, что хотите удалить запись «{{ datasetToDelete?.prof_code }} — {{ datasetToDelete?.prof_name }}»?
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
  name: "ClassificatorProfDatasetView",
  data() {
    return {
      headers: [
        { title: "Код", key: "prof_code" },
        { title: "Название", key: "prof_name" },
        { title: "Действия", key: "actions", sortable: false, width: '20%' },
      ],
      form: {
        prof_code: "",
        prof_name: "",
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
  computed: {
    
  },
  methods: {
    datasets() {
      return this.$store.state.classificator_prof_dataset.data || [];
    },
    isLoading() {
      return this.$store.state.classificator_prof_dataset.loading;
    },
    ...mapActions({
      getProfDatasets: "classificator_prof_dataset/getProfDatasets",
      createProfDataset: "classificator_prof_dataset/createProfDataset",
      updateProfDataset: "classificator_prof_dataset/updateProfDataset",
      deleteProfDataset: "classificator_prof_dataset/deleteProfDataset",
    }),

    openCreateDialog() {
      this.editingDataset = null;
      this.form = {
        prof_code: "",
        prof_name: "",
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
        await this.updateProfDataset({ id: this.editingDataset.id, payload });
      } else {
        await this.createProfDataset(payload);
      }
      await this.getProfDatasets();
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
      await this.deleteProfDataset(this.datasetToDelete.id);
      await this.getProfDatasets();
      this.closeConfirmDialog();
    },
  },
  async created() {
    await this.getProfDatasets();
  },
};
</script>
