<template>
    <v-dialog
        v-model="dialog"
        content-class="form-style"
        persistent 
    >
        <v-card class="elevation-12">
              <v-toolbar color="grey lighten-2">
                <v-toolbar-title>Login form</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <v-form
                  ref="form" 
                  v-model="valid"
                  lazy-validation>

                  <v-text-field 
                  v-model="username"
                  prepend-icon="person" 
                  name="username" 
                  label="Username"
                  :rules="usernameRules"
                  type="text"/>

                  <v-text-field
                  v-model="password"
                  prepend-icon="lock" 
                  name="password" 
                  label="Password" 
                  id="password"
                  :rules="passwordRules"
                  type="password" />
                </v-form>
                <ul>
                  <li class="red--text subheading" v-for="err in errors">
                    {{err}}
                  </li>
                </ul>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn 
                  flat 
                  color="red darken-2" 
                  @click="close"
                  :disabled="isLoading"
                >Dismiss</v-btn>
                <v-btn 
                  flat 
                  color="green darken-1" 
                  @click="handleData"
                  :disabled="!valid || isLoading"
                >Login</v-btn>
                <v-progress-circular
                  v-show="isLoading"
                  indeterminate
                  color="grey darken-2"
                ></v-progress-circular>
              </v-card-actions>
            </v-card>
    </v-dialog>
</template>

<script>
    export default {
      data: () => {
          return {
            errors: [],
            username: "",
            password: "",
            valid: true,
            dialog: false,
            passwordRules: [
              value => !!value || 'Required.',
              value => {
                if (value)
                  return value.length >= 8 || 'Min length is 8 symbols.'
                return true
              }
            ],
            usernameRules: [
              v => !!v || 'Required.'
            ]
        }
      },
      computed:{
        isLoading(){
          return this.$store.state.isLoading;
        }
      },
      watch: {
        '$store.state.errors.loginErrors': (o, n) => {
          if (n.length > 0){
            this.errors = n;
          }
        }
      },
      methods: {
        close() {
          this.$refs.form.resetValidation();
          this.errors = [];
          this.dialog = false;
        },
        show() {
            this.dialog = !this.dialog;
        },
        handleData() {
          if (this.$refs.form.validate()){
            this.$store.dispatch('loginAction', {
              username: this.username,
              password: this.password
            })
            .then((response) => {
                this.$store.commit("setUser", response.data.data);
                this.$store.commit('setLoadingStatus', false);
                this.close()

                this.$parent.$refs.successDialog.show('User logined!');
            })
            .catch((error) => {
                this.errors = error.response.data.errors;
                this.$store.commit('setLoadingStatus', false);
            })
            
          }
            // this.isLoading = true;
        }
      }
    }
</script>
