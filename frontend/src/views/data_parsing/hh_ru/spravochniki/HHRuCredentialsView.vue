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
            v-if="editingCredential"
            v-model="form.HH_RU_ACCESS_TOKEN"
            label="Access Token"

            clearable
          />
          <v-text-field
            v-if="editingCredential"
            v-model="form.HH_RU_REFRESH_TOKEN"
            label="Refresh Token"

            clearable
          />
            <v-text-field
                v-model="form.HH_RU_REDIRECT_URI"
                label="Redirect URI"
                :rules="[rules.required]"
                clearable
            />

        </v-form>
        <v-col v-if="editingCredential">
            <v-row justify="center">
                <v-btn class="mr-5" color="primary" @click="getHHRuCode">получить code</v-btn>
                <v-btn class="ml-5" color="primary" @click="code_dialog=true">получить токены</v-btn>
            </v-row>
        </v-col>
        
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

  <!-- Dialog for entering code -->
    <v-dialog v-model="code_dialog" max-width="600px">
        <v-card>
        <v-card-title class="text-h5">Введите код</v-card-title>
        <v-card-text>
            <v-text-field
            v-model="code"
            label="Код"
            :rules="[rules.required]"
            clearable
            />
        </v-card-text>
        <v-card-actions>
            <v-spacer />
            <v-btn text @click="code_dialog = false">Отмена</v-btn>
            <v-btn color="primary" @click="getHHRuTokens(code)">Получить токены</v-btn>
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
        { title: "Access Token", key: "HH_RU_ACCESS_TOKEN" },
        { title: "Refresh Token", key: "HH_RU_REFRESH_TOKEN" },
        { title: "Client ID", key: "HH_RU_CLIENT_ID" },
        { title: "Client Secret", key: "HH_RU_CLIENT_SECRET" },
        { title: "Redirect URI", key: "HH_RU_REDIRECT_URI" },
        { title: "", key: "edit", sortable: false },
        { title: "", key: "delete", sortable: false },
      ],
      code: "",
      code_dialog: false,
      editDialog: false,
      confirmDeleteDialog: false,
      editingCredential: null,
      credentialToDelete: null,
      form: {
        HH_RU_CLIENT_ID: "",
        HH_RU_CLIENT_SECRET: "",
        HH_RU_ACCESS_TOKEN: "",
        HH_RU_REFRESH_TOKEN: "",
        HH_RU_REDIRECT_URI: "", 
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
    ...mapActions({
      getHhRuCredentials: "hh_ru_credentials/getHhRuCredentials",
      createHhRuCredentials: "hh_ru_credentials/createHhRuCredentials",
      updateHhRuCredentials: "hh_ru_credentials/updateHhRuCredentials",
      deleteHhRuCredentials: "hh_ru_credentials/deleteHhRuCredentials",
      requestHHRuTokens: "hh_ru_credentials/requestHHRuTokens",
    }),
    getHHRuCode() {
      const clientId = this.form.HH_RU_CLIENT_ID;
      const redirectUri = this.form.HH_RU_REDIRECT_URI;
      if (!clientId || !redirectUri) {
        this.$toast.error("Client ID и Redirect URI обязательны для получения кода.");
        return;
      }
      const url = `https://hh.ru/oauth/authorize?response_type=code&client_id=${clientId}&redirect_uri=${redirectUri}`;
      window.open(url, "_blank");
    },
    async getHHRuTokens(code) {
      const client_id = this.form.HH_RU_CLIENT_ID;
      const client_secret = this.form.HH_RU_CLIENT_SECRET;
      const redirect_uri = this.form.HH_RU_REDIRECT_URI;

      if (!client_id || !client_secret || !redirect_uri || !code) {
        this.$toast.error("Все поля обязательны для получения токенов.");
        return;
      }

      // Здесь вызов API для получения токенов
      console.log("Получение токенов с кодом:", code);
        const payload = {
            code,
            client_id,
            client_secret,
            redirect_uri,
        }
        const response = await this.requestHHRuTokens(payload)
        this.code_dialog = false;
        this.form.HH_RU_ACCESS_TOKEN = response.access_token;
        this.form.HH_RU_REFRESH_TOKEN = response.refresh_token;
        console.log("Response:", response);
    },
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
