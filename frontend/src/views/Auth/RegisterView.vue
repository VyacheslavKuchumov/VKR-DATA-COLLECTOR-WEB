<template>
  <v-container class="home" fluid>
    <v-card-title>Зарегистрироваться</v-card-title>
    <v-form @submit.prevent="go_register" ref="registerForm" v-model="valid" lazy-validation>
      <v-text-field
        label="Введите email"
        v-model="email"
        :rules="emailRules"
        required
        type="email"
      ></v-text-field>

      <v-text-field
        label="Введите ФИО"
        v-model="name"
        :rules="nameRules"
        required
        type="text"
      ></v-text-field>

      <v-text-field
        label="Введите пароль"
        v-model="password"
        :rules="passwordRules"
        required
        type="password"
      ></v-text-field>

      <v-text-field
        label="Повторите пароль"
        v-model="repeat_password"
        :rules="repeatPasswordRules"
        required
        type="password"
      ></v-text-field>

      <!-- Согласие на обработку персональных данных -->
      <v-checkbox
        v-model="agree"
        :rules="agreeRules"
        label="Я согласен на обработку персональных данных"
        required
      ></v-checkbox>

      <v-btn
        type="submit"
        :disabled="!valid || !agree"
        class="form-btn"
        color="primary"
      >
        Регистрация
      </v-btn>

      <v-btn class="mt-5" variant="plain" text to="/login">
        Уже есть аккаунт?
      </v-btn>
    </v-form>
  </v-container>
</template>

<script>
import { mapActions } from "vuex";

export default {
  name: "register",
  data() {
    return {
      email: "",
      password: "",
      repeat_password: "",
      name: "",
      agree: false,
      valid: false,
      emailRules: [
        v => !!v || "Email обязателен",
        v => /.+@.+\..+/.test(v) || "Email должен быть действительным"
      ],
      passwordRules: [
        v => !!v || "Пароль обязателен"
      ],
      repeatPasswordRules: [
        v => !!v || "Повторение пароля обязательно",
        v => v === this.password || "Пароли должны совпадать"
      ],
      nameRules: [
        v => !!v || "Имя обязательно"
      ],
      agreeRules: [
        v => v || "Необходимо согласие на обработку персональных данных"
      ],
    };
  },
  methods: {
    ...mapActions({
      register: "auth/register",
    }),
    go_register() {
      if (this.$refs.registerForm.validate()) {
        const formData = {
          email: this.email,
          password: this.password,
          name: this.name,
          agree: this.agree,
        };
        this.register(formData);
      }
    }
  }
};
</script>

<style>
.home {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
.v-form {
  max-width: 400px;
  width: 100%;
}
.form-btn {
  width: 100%;
}
</style>
