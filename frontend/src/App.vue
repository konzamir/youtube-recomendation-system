<template>
  <v-app>
    <main-header/>
    <v-main>
      <router-view />
    </v-main>

    <big-process ref="bigProcess" />
    <login-form ref="loginForm" />
    <register-form ref="registerForm" />
    <user-info ref="userInfo" />
    <error-dialog ref="errorDialog" />
    <success-dialog ref="successDialog" />

    <main-footer/>
  </v-app>
</template>

<script>
import Header from '@/components/main/Header';
import Footer from '@/components/main/Footer';
import LoginForm from "@/components/user/LoginForm";
import RegisterForm from "@/components/user/RegisterForm";
import UserInfo from "@/components/user/UserInfo";
import BigProcess from "@/components/progress/BigProcess";
import ErrorDialog from '@/components/dialogs/ErrorDialog';
import SuccessDialog from '@/components/dialogs/SuccessDialog';

export default {
  
  name: "app",
  components: {
    'main-footer':      Footer,
    'main-header':      Header,
    'login-form':       LoginForm,
    'register-form':    RegisterForm,
    'user-info':        UserInfo,
    'big-process':      BigProcess,
    'error-dialog':     ErrorDialog,
    'success-dialog':   SuccessDialog
  },
}
</script>
