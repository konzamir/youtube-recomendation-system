<template>
    <v-dialog
        v-model="dialog"
        persistent
        content-class="big-process-dialog"
        class="big-process-dialog"
    >
    <v-card
        img
        color="transparent"
      >
        <v-layout justify-center
            align-center
            row
            fill-height
            class="big-process-layout"
            
        >
            <v-progress-circular
            :size="200"
            :width="12"
            color="white"
            indeterminate
        />
        
        </v-layout>
    </v-card>
    </v-dialog>
    
</template>

<script>
    export default {
        data() {
            return {
                dialog: false,
            }
        },
        methods: {
            show(){
                this.dialog = true;
            },
            close(){
                this.dialog = false;
            },
        }
    }
</script>
