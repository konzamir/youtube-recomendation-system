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
                itemText: 'name',
                itemValue: 'id',

                sources: {
                    entries: [],
                    isLoading: false,
                    model: [],
                    search: null,
                },
                tags: {
                    entries: [],
                    isLoading: false,
                    model: [],
                    search: null,
                },
                categories: {
                    entries: [],
                    isLoading: false,
                    model: [],
                    search: null,
                }
            }
        },
        computed: {
            sourceItems () {
                return this.getItems(this.sources);
            },
            tagItems () {
                return this.getItems(this.tags);
            },
            categoryItems () {
                return this.getItems(this.categories);
            },
        },

        watch: {
            'sources.search' (val) {
                if (this.sources.isLoading || !val) return
                this.sources.isLoading = true

                this.$store.dispatch('getSources', val)
                    .then(res => res.data)
                    .then(res => {
                        this.sources.entries = res.data
                    })
                    .catch(err => {
                        console.log(err)
                    })
                    .finally(() => (this.sources.isLoading = false))
            },
            'tags.search' (val) {
                if (this.tags.isLoading || !val) return
                this.tags.isLoading = true

                this.$store.dispatch('getTags', val)
                    .then(res => res.data)
                    .then(res => {
                        this.tags.entries = res.data
                    })
                    .catch(err => {
                        console.log(err)
                    })
                    .finally(() => (this.tags.isLoading = false))
            },
            'categories.search' (val) {
                if (this.categories.isLoading || !val) return
                this.categories.isLoading = true

                this.$store.dispatch('getCategories', val)
                    .then(res => res.data)
                    .then(res => {
                        this.categories.entries = res.data
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
            getItems(obj) {
                return obj.entries.concat(obj.model).map(entry => {
                    const name = entry.name.length > this.descriptionLimit
                    ? entry.name.slice(0, this.descriptionLimit) + '...'
                    : entry.name

                    return Object.assign({}, entry, { name })
                })
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
