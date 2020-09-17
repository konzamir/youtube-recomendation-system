<template>
    <v-dialog
        v-model="dialog"
        content-class="form-style"
        width="300"
    >
        <v-card class="elevation-12">
              <v-toolbar color="green">
                <v-toolbar-title>
                    Success!
                </v-toolbar-title>
              </v-toolbar>
              <v-card-text class="subheading">
                  {{detail}}
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn 
                    flat 
                    color="green darken-1" 
                    @click="close" 
                    icon
                >
                <v-icon>check</v-icon>
                </v-btn>
              </v-card-actions>
            </v-card>

    </v-dialog>
</template>

<script>
    export default {
        data(){
            return {
                dialog: false,
                detail: ''
            }
        },
        methods: {
            close() {
                this.dialog = false;
            },
            show(detail) {
                this.detail = detail;
                this.dialog = true;
            },
        }
    }
</script>