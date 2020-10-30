<template>
    <v-dialog
        v-model="dialog"
        content-class="form-style"
        persistent 
    >
        <v-card class="elevation-12">
              <v-toolbar color="grey lighten-2">
                <v-toolbar-title>Register form</v-toolbar-title>
              </v-toolbar>
              <v-card-text class="pt-5 pb-0">
                To register on the platform you should send the request to <a href = "mailto: administration@youmed.com">administration@youmed.com</a>. <br />
                In the mail's body you should place documents, that will tell us, that you are a professional employee.
              </v-card-text>
              <v-card-actions class="pb-4 pr-5">
                <v-spacer></v-spacer>
                <v-btn 
                    outlined
                    width="200"
                    color="green darken-1"
                    @click="close"
                    
                    :disabled="isLoading"    
                >Understand</v-btn>
              </v-card-actions>
            </v-card>
    </v-dialog>
</template>

<script>
    export default {
        data: () => {
          return {
              dialog: false,
          }
        },
        methods: {
            close() {
              this.dialog = false;
            },
            show() {
              this.dialog = true;
            }
        }
    }
</script>
