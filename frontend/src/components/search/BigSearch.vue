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
                label="Input text phrase to search"
                type="text"
                @click:append-outer="sendMessage"
                @click:clear="clearMessage"
            ></v-text-field>
        </v-layout>

        <v-layout justify-center row>
            <v-autocomplete
                class="ma-1"
                label="Choose sources"
                chips
                clearable
                deletable-chips
                multiple
                v-model="sources.model"
                :items="sourceItems"
                :loading="sources.isLoading"
                :search-input.sync="sources.search"
                hide-no-data
                hide-selected
                :item-text="itemText"
                :item-value="itemValue"
                return-object
            ></v-autocomplete>
        </v-layout>
        <v-layout justify-center row>
            <v-autocomplete
                class="ma-1"
                label="Choose tags"
                chips
                clearable
                deletable-chips
                multiple
                v-model="tags.model"
                :items="tagItems"
                :loading="tags.isLoading"
                :search-input.sync="tags.search"
                hide-no-data
                hide-selected
                :item-text="itemText"
                :item-value="itemValue"
                return-object
            ></v-autocomplete>
        </v-layout>
        <v-layout justify-center row>
            <v-autocomplete
                class="ma-1"
                label="Choose categories"
                chips
                clearable
                deletable-chips
                multiple
                v-model="categories.model"
                :items="categoryItems"
                :loading="categories.isLoading"
                :search-input.sync="categories.search"
                hide-no-data
                hide-selected
                :item-text="itemText"
                :item-value="itemValue"
                return-object
            ></v-autocomplete>
        </v-layout>
        

    </v-container>
    </v-form>
</template>

<script>
    export default {
        data: () => {
            return {
                message: '',
                descriptionLimit: 60,
                itemText: 'Description',
                itemValue: 'API',

                sources: {
                    entries: [],
                    isLoading: false,
                    model: null,
                    search: null,
                },
                tags: {
                    entries: [],
                    isLoading: false,
                    model: null,
                    search: null,
                },
                categories: {
                    entries: [],
                    isLoading: false,
                    model: null,
                    search: null,
                }
            }
        },
        computed: {
            sourceItems () {
                return this.sources.entries.map(entry => {
                    const Description = entry.Description.length > this.descriptionLimit
                    ? entry.Description.slice(0, this.descriptionLimit) + '...'
                    : entry.Description

                    return Object.assign({}, entry, { Description })
                })
            },
            tagItems () {
                return this.tags.entries.map(entry => {
                    const Description = entry.Description.length > this.descriptionLimit
                    ? entry.Description.slice(0, this.descriptionLimit) + '...'
                    : entry.Description

                    return Object.assign({}, entry, { Description })
                })
            },
            categoryItems () {
                return this.categories.entries.map(entry => {
                    const Description = entry.Description.length > this.descriptionLimit
                    ? entry.Description.slice(0, this.descriptionLimit) + '...'
                    : entry.Description

                    return Object.assign({}, entry, { Description })
                })
            },
        },

        watch: {
            'sources.search' (val) {
                if (this.sources.isLoading) return
                this.sources.isLoading = true

                fetch('https://api.publicapis.org/entries')
                    .then(res => res.json())
                    .then(res => {
                        const { count, entries } = res
                        this.sources.entries = entries
                    })
                    .catch(err => {
                        console.log(err)
                    })
                    .finally(() => (this.sources.isLoading = false))
            },
            'tags.search' (val) {
                if (this.tags.isLoading) return
                this.tags.isLoading = true

                fetch('https://api.publicapis.org/entries')
                    .then(res => res.json())
                    .then(res => {
                        const { count, entries } = res
                        this.tags.entries = entries
                    })
                    .catch(err => {
                        console.log(err)
                    })
                    .finally(() => (this.tags.isLoading = false))
            },
            'categories.search' (val) {
                if (this.categories.isLoading) return
                this.categories.isLoading = true

                fetch('https://api.publicapis.org/entries')
                    .then(res => res.json())
                    .then(res => {
                        const { count, entries } = res
                        this.categories.entries = entries
                    })
                    .catch(err => {
                        console.log(err)
                    })
                    .finally(() => (this.categories.isLoading = false))
            },
            
        },
        methods: {
            submitForm(e){
                this.sendMessage();
                e.preventDefault();
            },
            sendMessage() {
                if (this.message != ''){
                    this.$emit('startSearch', {
                        process: {
                            search_data: this.message
                        },
                        tags: this.tags.model,
                        sources: this.sources.model,
                        categories: this.categories.model
                    });
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
