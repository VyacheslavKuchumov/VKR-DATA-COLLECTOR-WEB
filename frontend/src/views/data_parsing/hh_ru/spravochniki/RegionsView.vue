<template>
  <v-card max-width="800" class="elevation-0 mt-5 ml-auto mr-auto">
    <v-card-title class="text-wrap" align="center">
      Управление регионами для скрэйпинга
    </v-card-title>
  </v-card>

  <v-card class="elevation-5 mt-5 ml-auto mr-auto" max-width="800">
    <v-toolbar flat>
      <v-spacer />
      <v-btn icon="mdi-plus" color="primary" @click="openCreateDialog" />
    </v-toolbar>

    <v-container>
      <v-data-table-server
        :headers="headers"
        :items="regions()"
        :loading="isLoading()"
        :items-per-page="-1"
        hide-default-footer
      >
        <template #item.edit="{ item }">
          <v-btn size="small" color="primary" class="mr-2" @click="openEditDialog(item)">
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
        </template>

        <template #item.delete="{ item }">
          <v-btn size="small" color="red" @click="confirmDelete(item)">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </template>
      </v-data-table-server>

    </v-container>
  </v-card>

  <!-- Create / Edit Dialog -->
  <v-dialog v-model="editDialog" max-width="450px">
    <v-card>
      <v-card-title class="text-h5">
        {{ editingRegion ? "Редактировать регион" : "Создать регион" }}
      </v-card-title>
      <v-card-text>
        <v-form ref="regionForm" v-model="valid" @submit.prevent="saveRegion">
          <v-text-field
            v-model="regionForm.region_name"
            label="Название региона"
            :rules="[rules.required]"
            clearable
          />
          <v-text-field
            v-model="regionForm.country"
            label="Страна"
            :rules="[rules.required]"
            clearable
          />
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="closeEditDialog">Отмена</v-btn>
        <v-btn color="primary" :disabled="!valid" @click="saveRegion">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <!-- Delete Confirmation Dialog -->
  <v-dialog v-model="confirmDeleteDialog" max-width="400px">
    <v-card>
      <v-card-title class="text-h5">Подтвердите удаление</v-card-title>
      <v-card-text>
        Вы уверены, что хотите удалить регион
        «{{ regionToDelete?.region_name }}»?
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
  name: "RegionsView",
  data() {
    return {
      headers: [
        { title: "Регион", key: "region_name" },
        { title: "Страна", key: "country" },
        { title: "", key: "edit", sortable: false },
        { title: "", key: "delete", sortable: false },
      ],
      editDialog: false,
      confirmDeleteDialog: false,
      editingRegion: null,
      regionToDelete: null,
      regionForm: { region_name: "", country: "" },
      valid: false,
      rules: {
        required: (v) => !!v || "Это поле обязательно",
      },
    };
  },
  computed: {

  },
  methods: {
    regions() {
      return this.$store.state.regions.data || [];
    },
    isLoading() {
      return this.$store.state.regions.isLoading;
    },
    errorMessage() {
      return this.$store.state.regions.errorMessage;
    },
    ...mapActions({
      fetchData: "regions/getRegions",
      createRegion: "regions/createRegion",
      updateRegion: "regions/updateRegion",
      deleteRegion: "regions/deleteRegion",
    }),

    openCreateDialog() {
      this.editingRegion = null;
      this.regionForm = { region_name: "", country: "" };
      this.editDialog = true;
    },
    openEditDialog(region) {
      this.editingRegion = region;
      this.regionForm = { ...region };
      this.editDialog = true;
    },
    closeEditDialog() {
      this.editDialog = false;
      this.regionForm = { region_name: "", country: "" };
    },
    async saveRegion() {
      const payload = { ...this.regionForm };
      if (this.editingRegion) {
        await this.updateRegion({ id: this.editingRegion.id, payload });
      } else {
        await this.createRegion(payload);
      }
      await this.fetchData();
      this.closeEditDialog();
    },
    confirmDelete(region) {
      this.regionToDelete = region;
      this.confirmDeleteDialog = true;
    },
    closeConfirmDialog() {
      this.confirmDeleteDialog = false;
      this.regionToDelete = null;
    },
    async deleteConfirmed() {
      if (!this.regionToDelete) return;
      await this.deleteRegion(this.regionToDelete.id);
      await this.fetchData();
      this.closeConfirmDialog();
    },
  },
  async created() {
    await this.fetchData();
  },
};
</script>
