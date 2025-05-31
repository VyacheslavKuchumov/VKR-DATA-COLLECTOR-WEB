<template>
  <v-card max-width="800" class="elevation-0 mt-5 ml-auto mr-auto">
    <v-card-title class="text-wrap" align="center">
      Управление секретами hh.ru
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
        :items="credentials()"
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
  <v-dialog v-model="editDialog" max-width="600px">
    <v-card>
      <v-card-title class="text-h5">
        {{ editingCredential ? "Редактировать Credential" : "Создать Credential" }}
      </v-card-title>
      <v-card-text>
        <v-form ref="form" v-model="valid" @submit.prevent="saveCredential">
          <v-text-field
            v-model="form.HH_RU_CLIENT_ID"
            label="Client ID"
            :rules="[rules.required]"
            clearable
          />
          <v-text-field
            v-model="form.HH_RU_CLIENT_SECRET"
            label="Client Secret"
            :rules="[rules.required]"
            clearable
          />
          <v-text-field
            v-model="form.HH_RU_ACCESS_TOKEN"
            label="Access Token"
            :rules="[rules.required]"
            clearable
          />
          <v-text-field
            v-model="form.HH_RU_REFRESH_TOKEN"
            label="Refresh Token"
            :rules="[rules.required]"
            clearable
          />
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="closeEditDialog">Отмена</v-btn>
        <v-btn color="primary" :disabled="!valid" @click="saveCredential">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <!-- Delete Confirmation Dialog -->
  <v-dialog v-model="confirmDeleteDialog" max-width="400px">
    <v-card>
      <v-card-title class="text-h5">Подтвердите удаление</v-card-title>
      <v-card-text>
        Вы уверены, что хотите удалить Credential
        «{{ credentialToDelete?.HH_RU_CLIENT_ID }}»?
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
  name: "HHRuCredentialsView",
  data() {
    return {
      headers: [
        { title: "Client ID", key: "HH_RU_CLIENT_ID" },
        { title: "Client Secret", key: "HH_RU_CLIENT_SECRET" },
        { title: "Access Token", key: "HH_RU_ACCESS_TOKEN" },
        { title: "Refresh Token", key: "HH_RU_REFRESH_TOKEN" },
        { title: "", key: "edit", sortable: false },
        { title: "", key: "delete", sortable: false },
      ],
      editDialog: false,
      confirmDeleteDialog: false,
      editingCredential: null,
      credentialToDelete: null,
      form: {
        HH_RU_CLIENT_ID: "",
        HH_RU_CLIENT_SECRET: "",
        HH_RU_ACCESS_TOKEN: "",
        HH_RU_REFRESH_TOKEN: "",
      },
      valid: false,
      rules: {
        required: (v) => !!v || "Это поле обязательно",
      },
    };
  },
  methods: {
    credentials() {
      return this.$store.state.hh_ru_credentials.data || [];
    },
    isLoading() {
      return this.$store.state.hh_ru_credentials.loading;
    },
    errorMessage() {
      return this.$store.state.hh_ru_credentials.error;
    },
    ...mapActions("hh_ru_credentials", [
      "getHhRuCredentials",
      "createHhRuCredentials",
      "updateHhRuCredentials",
      "deleteHhRuCredentials",
    ]),
    openCreateDialog() {
      this.editingCredential = null;
      this.form = {
        HH_RU_CLIENT_ID: "",
        HH_RU_CLIENT_SECRET: "",
        HH_RU_ACCESS_TOKEN: "",
        HH_RU_REFRESH_TOKEN: "",
      };
      this.editDialog = true;
    },
    openEditDialog(item) {
      this.editingCredential = item;
      this.form = { ...item };
      this.editDialog = true;
    },
    closeEditDialog() {
      this.editDialog = false;
      this.valid = false;
    },
    async saveCredential() {
      const payload = { ...this.form };
      if (this.editingCredential) {
        await this.updateHhRuCredentials({ id: this.editingCredential.id, payload });
      } else {
        await this.createHhRuCredentials(payload);
      }
      await this.getHhRuCredentials();
      this.closeEditDialog();
    },
    confirmDelete(item) {
      this.credentialToDelete = item;
      this.confirmDeleteDialog = true;
    },
    closeConfirmDialog() {
      this.confirmDeleteDialog = false;
      this.credentialToDelete = null;
    },
    async deleteConfirmed() {
      if (!this.credentialToDelete) return;
      await this.deleteHhRuCredentials(this.credentialToDelete.id);
      await this.getHhRuCredentials();
      this.closeConfirmDialog();
    },
  },
  async created() {
    await this.getHhRuCredentials();
  },
};
</script>
