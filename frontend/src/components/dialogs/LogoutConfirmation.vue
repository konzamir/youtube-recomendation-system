<template>
    <v-dialog
        v-model="dialog"
        content-class="form-style"
        width="300"
        persistent 
    >
        <v-card class="elevation-12">
              <v-toolbar color="grey lighten-2">
                <v-toolbar-title>Are you sure to logout?</v-toolbar-title>
              </v-toolbar>
              <v-card-text>

              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn 
                    flat 
                    color="red darken-2" 
                    @click="close"  
                >Dismiss</v-btn>
                <v-btn 
                    flat 
                    color="primary" 
                    @click="confirm" 
                >Log out</v-btn>
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>

    </v-dialog>
</template>

<script>
    export default {
        data: () => {
            return {
                confirmLogout: false,
                isLoading: false,
                username: "",
                dialog: false,
                email: "",
                featuredCount: 29,
            }
        },
        watchers: {
            confirmLogout(o, n) {
                if (n) {
                    this.isLoading = true;
                }
            }
        },
        methods: {
          close() {
            this.dialog = false;
            this.$emit('confirm', false);
          },
          confirm() {
              this.dialog = false;
              this.$emit('confirm', true);
          },
          show() {
              this.dialog = true;
          },
        },
    }
</script>
