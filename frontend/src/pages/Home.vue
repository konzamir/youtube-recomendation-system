<template>
<div>
    <v-container  >
        <big-search v-on:startSearch="startSearch" ref="bigSearch" />
        <ul>
            <li class="red--text subheading" v-for="err in errors">
                {{err}}
            </li>
        </ul>

        <v-container v-show="process.status != undefined">
            <v-layout flex class="pt-0">
                <div class="headline pt-2">
                    Results:
                </div>
                <v-spacer />
                <v-btn 
                    icon color="primary" 
                    :disabled="process.prev_process == undefined" 
                    @click="getOtherProcess(process.prev_process)"
                >
                    <v-icon>mdi-arrow-left</v-icon>
                </v-btn>
                <v-btn 
                    icon color="primary" 
                    :disabled="process.next_process == undefined" 
                    @click="getOtherProcess(process.next_process)"
                >
                    <v-icon>mdi-arrow-right</v-icon>
                </v-btn>
                
            </v-layout>
            <v-divider color="grey" class="mb-2"/>

            <v-row
                class="fill-height"
                align-content="center"
                justify="center"
                v-show="successStatuses.indexOf(process.status) == -1"
            >
                <v-col
                    class="headline text-center"
                    cols="12"
                >
                    {{processStatusesLabels[process.status]}}
                </v-col>
                <v-col cols="6">
                <v-progress-linear
                    color="deep-purple accent-4"
                    indeterminate
                    rounded
                    height="6"
                ></v-progress-linear>
                </v-col>
            </v-row>

            <div v-show="successStatuses.indexOf(process.status) > -1">
                <v-layout row wrap v-scroll="onScroll" v-if="this.items.length > 0">
                    <search-item v-for="item in this.items" :key="item.video_id"
                        :item="item"/>    
                </v-layout>
                <v-layout row wrap justify-center v-scroll="onScroll" v-else class="headline pt-2">
                    No media were found for current group!
                </v-layout>

                <v-layout row wrap justify-center v-scroll="onScroll" class="pt-2">
                    <v-btn dark color="primary lighten-1">Get next group</v-btn>
                </v-layout>
            </div>

            <v-btn
                v-show="displayReturnButton"
                fixed
                dark
                fab
                bottom
                right
                color="grey lighten-1"
                @click="returnToTop"
            >
                <v-icon color="black" large>keyboard_arrow_up</v-icon>
            </v-btn>

        </v-container>
    </v-container>
    <media-element ref="media"/>
    

  </div>  
</template>

<script>
    import BigSearch from '@/components/search/BigSearch';
    import SearchItem from '@/components/search/SearchItem';
    import MediaElement from '@/components/search/MediaElement';
    import FiltersBlock from '@/components/search/FiltersBlock';

    export default {
        data: () => {
            return {
                displayReturnButtonValue: 200,
                displayReturnButton: false,
                offsetTop: 0,
                items: [],
                errors: [],

                pollingInterval: 2000,

                process: {
                    "id": 1,
                    "status": 3,
                    "youtube_video_group": null,
                    "active": true,
                    "search_data": "Test search§",
                    "invalid_msg": null,
                    "next_process": 2,
                    "prev_process": null,
                    "updated_at": "2020-10-20T19:46:24.159578Z",
                    "created_at": "2020-10-11T19:34:52.138086Z",
                    "user": 1
                },
                processStatusesLabels: {
                    0: "Waiting for fetching base data...",
                    1: "Waiting for fetching full data...",
                    2: "Waiting for filtering...",
                    3: "Success!",
                    4: "Failed!"
                },
                successStatuses: [3, 4]
            }
        },
        methods: {
            showAlert(d) {
                this.$root.$children[0].$refs.successAlert.show()
            },
            onScroll (e) {
                this.offsetTop = window.pageYOffset || document.documentElement.scrollTop
            },
            returnToTop() {
                this.$vuetify.goTo(0, {
                    duration: 200,
                    offset: 0,
                    easing: 'linear'
                });
            },
            getOtherProcess(process_id) {
                this.$store.dispatch('getProcess', this.process.id)
                    .then(response => {
                        this.process = response.data.data.process;
                        
                        if (this.successStatuses.indexOf(this.process.status) == -1) {
                            this.executePolling();
                        }
                    })
                    .catch(err => {
                        this.process = {}
                        this.errors = err.response.data.errors;
                    });
            },
            executePolling() {
                setTimeout(() => {
                    this.$store.dispatch('getProcess', this.process.id)
                        .then(response => {
                            this.process = response.data.data.process;
                            
                            if (this.successStatuses.indexOf(this.process.status) == -1) {
                                this.executePolling();
                            }
                        })
                        .catch(err => {
                            this.process = {}
                            this.errors = err.response.data.errors;
                        });
                }, this.pollingInterval);
            },
            startSearch(payload){
                this.$root.$children[0].$refs.bigProcess.show();
                
                this.$store.dispatch('startProcess', payload)
                .then((response) => {
                    this.$root.$children[0].$refs.bigProcess.close();
                    this.process = response.data.data.process;
                    this.executePolling();
                })
                .catch((err) => {
                    this.$root.$children[0].$refs.bigProcess.close();

                    this.errors = err.response.data.errors;
                })
            }
        },
        watch:{
            offsetTop (o, n) {
                if (n >= this.displayReturnButtonValue) {
                    this.displayReturnButton = true;
                } else {
                    this.displayReturnButton = false;
                }
            }
        },
        components: {
            'big-search':       BigSearch,
            'search-item':      SearchItem,
            'media-element':    MediaElement,
            'filters-block':    FiltersBlock
        },
        mounted() {
            console.log(this.successStatuses)
        }
    }
</script>
