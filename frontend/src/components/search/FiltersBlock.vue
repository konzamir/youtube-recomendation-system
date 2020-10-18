<template>
    <v-form ref="form" 
    lazy-validation
    @submit="submitForm"
    >
    <v-container >
        <v-layout justify-center row>
            <v-autocomplete
                class="ma-1"
                label="Choose source"
                chips
                clearable
                deletable-chips
                multiple

                v-model="model"
                :items="items"
                :loading="isLoading"
                :search-input.sync="search"
                hide-no-data
                hide-selected
                item-text="Description"
                item-value="API"
                return-object
            ></v-autocomplete>
        </v-layout>
        <v-layout justify-center row>
            <v-autocomplete
                class="ma-1"
                label="Choose tag"
                chips
                clearable
                deletable-chips
                multiple
            ></v-autocomplete>
        </v-layout>
        <v-layout justify-center row>
            <v-autocomplete
                class="ma-1"
                label="Choose category"
                chips
                clearable
                deletable-chips
                multiple
            ></v-autocomplete>
            
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

                descriptionLimit: 60,
                entries: [],
                isLoading: false,
                model: null,
                search: null,
            }
        },
        computed: {
            items () {
                return this.entries.map(entry => {
                    const Description = entry.Description.length > this.descriptionLimit
                    ? entry.Description.slice(0, this.descriptionLimit) + '...'
                    : entry.Description

                    return Object.assign({}, entry, { Description })
                })
            },
        },

        watch: {
            search (val) {
            // Items have already been requested
            if (this.isLoading) return

            this.isLoading = true

            // Lazily load input items
            fetch('https://api.publicapis.org/entries')
                .then(res => res.json())
                .then(res => {
                    const { count, entries } = res
                    this.count = count
                    this.entries = entries
                })
                .catch(err => {
                    console.log(err)
                })
                .finally(() => (this.isLoading = false))
            },
        },
        methods: {
            submitForm(e){
                this.sendMessage();
                e.preventDefault();
            },
            sendMessage() {
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
