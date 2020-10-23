<template>
<div>
    <v-container>
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
                v-show="!successStatuses.includes(process.status)"
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

            <div v-show="successStatuses.includes(process.status)">
                <v-layout row wrap v-if="this.videos.length > 0">
                    <search-item v-for="video in this.videos" :key="video.video_id"
                        :video="video"/>    
                </v-layout>
                <v-layout row wrap justify-center v-else class="headline pt-2">
                    No media were found!
                </v-layout>
            </div>

        </v-container>
    </v-container>
  </div>  
</template>

<script>
    import BigSearch from '@/components/search/BigSearch';
    import SearchItem from '@/components/search/SearchItem';

    export default {
        data: () => {
            return {
                videos: [],
                errors: [],

                pollingInterval: 2000, // 2 seconds

                process: {},
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
            setProcessFromAPI(process_id) {
                this.$store.dispatch('getProcess', process_id)
                    .then(response => {
                        this.process = response.data.data.process;
                        this.$store.commit('setProcess', this.process);

                        this.videos = response.data.data.videos;

                        if (!this.process.active) {
                            this.$store.dispatch('setProcessActive', process_id)
                                .catch(err => {
                                    this.process = {}
                                    this.errors = err.response.data.errors;
                                });
                        }
                        
                        if (!this.successStatuses.includes(this.process.status)) {
                            this.executePolling();
                        } else if (this.videos.length == 0 && this.process.next_process != undefined) {
                            this.getOtherProcess(this.process.next_process);
                        }
                    })
                    .catch(err => {
                        this.process = {}
                        this.errors = err.response.data.errors;
                    });
            },
            getOtherProcess(process_id) {
                this.setProcessFromAPI(process_id);
            },
            executePolling() {
                setTimeout(() => {
                    this.setProcessFromAPI(this.process.id)
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
        components: {
            'big-search':       BigSearch,
            'search-item':      SearchItem,
        },
        mounted() {
            this.process = this.$store.state.process;

            if (!this.successStatuses.includes(this.process.status)) {
                this.executePolling();
            } else if (this.videos.length == 0) {
                this.getOtherProcess(this.process.id);
            } else if (this.videos.length == 0 && this.process.next_process != undefined) {
                this.getOtherProcess(this.process.next_process);
            }
        }
    }
</script>
