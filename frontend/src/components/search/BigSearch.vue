<template>
    <v-form ref="form" 
    lazy-validation
    @submit="submitForm"
    >
    <v-container >
        <v-layout justify-center row>
            <v-text-field
                class="search-field headline"
                v-model="message"
                autofocus
                append-outer-icon="send"
                prepend-icon="search"
                

                clear-icon="clear"
                clearable
                label="What do you want to found?"
                type="text"
                @click:append-outer="sendMessage"
                @click:clear="clearMessage"
            ></v-text-field>
        </v-layout>
    </v-container>
    </v-form>
</template>

<script>
    export default {
        data: () => {
            return {
                show: false,
                message: '',
            }
        },

        computed: {
        },

        methods: {
            submitForm(e){
                this.sendMessage();
                e.preventDefault();
            },
            sendMessage() {
                // this.clearMessage();
                if (this.message != ''){
                    this.$emit('startSearch', this.message);
                }
            },
            clearMessage(){
                this.message = ''
            },
            setMessage(m) {
                this.message = m;
            }
        }
    }
</script>
