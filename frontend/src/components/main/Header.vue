<template>
  <v-card>
    <v-toolbar>
      <v-toolbar-title class="toolbar-title">
        <router-link to="/" class="black--text font-weight-medium">YouMed</router-link>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items>
        <v-btn v-show="!logined" text @click.stop="showLoginForm">Login</v-btn>
        <v-btn v-show="!logined" text @click.stop="showRegisterForm">Register</v-btn>
        <v-btn v-show="logined" text color="primary" @click.stop="showUserInfo">
          <v-icon>person</v-icon> {{username}}
        </v-btn>
      </v-toolbar-items>
    </v-toolbar>
  </v-card>
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
        this.$parent.$parent.$refs.loginForm.show();
      },
      showRegisterForm() {
        this.$parent.$parent.$refs.registerForm.show();
      },
      showUserInfo() {
        this.$parent.$parent.$refs.userInfo.show();
      }
    },
    components: {
      
    }
  }
</script>