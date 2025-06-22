<template>
      <v-container v-if="!$vuetify.display.mobile" max-width="800" class="elevation-0 mt-5 ml-auto mr-auto">
        <v-card-title class="text-wrap" align="center">
            Управление пользователями
        </v-card-title>
    </v-container>
    <v-container class="elevation-5 mt-5 ml-auto mr-auto pa-0" max-width="800">
        <v-toolbar flat>
            <v-btn icon="mdi-arrow-left" color="primary" @click="$router.push('/main-menu')" />
            <v-toolbar-title v-if="!$vuetify.display.mobile" class="text-h6 font-weight-bold">
                Назад
            </v-toolbar-title>
            <v-spacer />
            <v-btn v-if="!$vuetify.display.mobile" color="primary" prepend-icon="mdi-plus" @click="openCreateDialog">
                Добавить пользователя
            </v-btn>
            <v-btn v-else color="primary" icon="mdi-plus" @click="openCreateDialog">
            </v-btn>
        </v-toolbar>


      <v-data-table-server
        :headers="headers"
        :items="users()"
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

          <v-tooltip text="Пометить на удаление" location="top">
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
  <v-dialog v-model="editDialog" max-width="450px">
    <v-card>
      <v-card-title class="text-h5">
        {{ editingUser ? "Редактировать пользователя" : "Создать пользователя" }}
      </v-card-title>
      <v-card-text>
        <v-form ref="userFormRef" v-model="valid" @submit.prevent="saveUser">
          <v-text-field
            v-model="userForm.name"
            label="ФИО"
            :rules="[rules.required]"
            clearable
          />
          <v-text-field
            v-model="userForm.email"
            label="Email"
            :rules="[rules.required, rules.email]"
            clearable
          />
          <v-select
            v-model="userForm.role"
            :items="roles"
            label="Роль"
            :rules="[rules.required]"
            clearable
          />
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="closeEditDialog">Отмена</v-btn>
        <v-btn color="primary" :disabled="!valid" @click="saveUser">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <!-- Delete Confirmation Dialog -->
  <v-dialog v-model="confirmDeleteDialog" max-width="400px">
    <v-card>
      <v-card-title class="text-h5">Подтвердите удаление</v-card-title>
      <v-card-text>
        Вы уверены, что хотите удалить пользователя
        «{{ userToDelete?.name }}»?
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
  name: "UsersView",
  data() {
    return {
      headers: [
        { title: "ФИО", key: "name" },
        { title: "Email", key: "email" },
        { title: "Роль", key: "role" },
        { title: 'Действия', key: 'actions', sortable: false, width: '20%' }
      ],
      editDialog: false,
      confirmDeleteDialog: false,
      roles: ['admin', 'user'],
      editingUser: null,
      userToDelete: null,
      userForm: { name: "", email: "", role: "" },
      valid: false,
      rules: {
        required: v => !!v || "Это поле обязательно",
        email: v => /.+@.+\..+/.test(v) || "Неверный формат email",
      },
    };
  },
  computed: {
    
  },
  methods: {
    users() {
      return this.$store.state.users.data || [];
    },
    isLoading() {
      return this.$store.state.users.loading;
    },
    errorMessage() {
      return this.$store.state.users.error;
    },
    ...mapActions("users", [
      "getUsers",
      "createUser",
      "updateUser",
      "deleteUser",
    ]),

    openCreateDialog() {
      this.editingUser = null;
      this.userForm = { name: "", email: "", role: "" };
      this.editDialog = true;
    },
    openEditDialog(user) {
      this.editingUser = user;
      this.userForm = { ...user };
      this.editDialog = true;
    },
    closeEditDialog() {
      this.editDialog = false;
      this.userForm = { name: "", email: "", role: "" };
    },
    async saveUser() {
      const payload = { ...this.userForm };
      if (this.editingUser) {
        await this.updateUser({ id: this.editingUser.id, payload });
      } else {
        await this.createUser(payload);
      }
      await this.getUsers();
      this.closeEditDialog();
    },
    confirmDelete(user) {
      this.userToDelete = user;
      this.confirmDeleteDialog = true;
    },
    closeConfirmDialog() {
      this.confirmDeleteDialog = false;
      this.userToDelete = null;
    },
    async deleteConfirmed() {
      if (!this.userToDelete) return;
      await this.deleteUser(this.userToDelete.id);
      await this.getUsers();
      this.closeConfirmDialog();
    },
  },
  async created() {
    await this.getUsers();
  },
};
</script>
