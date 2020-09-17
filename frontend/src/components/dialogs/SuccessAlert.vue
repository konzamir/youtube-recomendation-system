<template>
    <div>
        <v-alert
        v-model="alert"
        dismissible
        type="success"
      >
        {{data}}
      </v-alert>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                alert:  false,
                data:   "",
            }
        },
        methods: {
            show(d){
                this.data = d;
                this.alert = true;
                setTimeout(() =>{
                    this.close()
                }, 1000);
            },
            close() {
                this.alert = false;
            }
        }
    }
</script>