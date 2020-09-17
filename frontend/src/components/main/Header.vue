<template>
  <v-toolbar>
    <v-toolbar-title class="toolbar-title">YouPlayer</v-toolbar-title>
    <v-spacer></v-spacer>
    <v-toolbar-items>
      <v-btn v-show="!logined" flat @click.stop="showLoginForm">Login</v-btn>
      <v-btn v-show="!logined" flat @click.stop="showRegisterForm">Register</v-btn>
      <v-btn v-show="logined" flat color="primary" @click.stop="showUserInfo">
        <v-icon>person</v-icon> {{username}}
      </v-btn>
    </v-toolbar-items>
  </v-toolbar>
</template>

<script>

  export default {
    data: () => {
      return {
        username: ""
      }
    },
    computed: {
      logined() {
        if (this.$store.state.user.token) {
          this.username = this.$store.state.user.username
          return true;
        }
        return false;
      }
    },
    methods: {
      showLoginForm() {
        this.$parent.$refs.loginForm.show();
      },
      showRegisterForm() {
        this.$parent.$refs.registerForm.show();
      },
      showUserInfo() {
        this.$parent.$refs.userInfo.show();
      }
    },
    components: {
      
    }
  }
</script>