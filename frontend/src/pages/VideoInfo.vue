<template>
    <div>
        <v-container>
            <router-link to="/" class="headline">
                <v-icon class="pb-1"> mdi-chevron-left</v-icon> Home
            </router-link>

            <v-row
                class="fill-height youtube-player"
                align-content="center"
                justify="center"
            >
                <youtube 
                    :video-id="video.youtube_data.video_hash" 
                />
            </v-row>

            <v-row
                class="fill-height"
                align-content="center"
                justify="center"
            >
                <v-col
                    class="headline"
                    sm="12"
                    md="6"
                >
                    <v-row justify="center" class="display-1 black--text font-weight-medium">
                        YouTube Marks:
                    </v-row>

                    <v-row no-gutters>
                        <v-col col="12">
                            <v-card class="pa-2" outlined tile>
                                Positive marks: {{youtubeMarks.positive_mark_number}}
                            </v-card>
                        </v-col>
                    </v-row>
                    <v-row no-gutters>
                        <v-col col="12">
                            <v-card class="pa-2" outlined tile>
                                Negative marks: {{youtubeMarks.negative_mark_number}}
                            </v-card>
                        </v-col>
                    </v-row>
                    <v-row no-gutters>
                        <v-col col="12">
                            <v-card class="pa-2" outlined tile>
                                View Count: {{youtubeMarks.view_count}}
                            </v-card>
                        </v-col>
                    </v-row>
                    <v-row no-gutters>
                        <v-col col="12">
                            <v-card class="pa-2" outlined tile>
                                Comment count: {{youtubeMarks.comment_count}}
                            </v-card>
                        </v-col>
                    </v-row>
                </v-col>

                <v-col
                    class="headline"
                    sm="12"
                    md="6"
                >
                    <v-row justify="center" class="display-1 black--text font-weight-medium">
                        YouMed Marks:
                    </v-row>

                    <v-row no-gutters>
                        <v-col col="12">
                            <v-card class="pa-2" outlined tile>
                                Information quality: {{userMarks.information_quality}}
                            </v-card>
                        </v-col>
                    </v-row>
                    <v-row no-gutters>
                        <v-col col="12">
                            <v-card class="pa-2" outlined tile>
                                Medical practice quality: {{userMarks.medical_practice_quality}}
                            </v-card>
                        </v-col>
                    </v-row>
                    <v-row no-gutters>
                        <v-col col="12">
                            <v-card class="pa-2" outlined tile>
                                Description quality: {{userMarks.description_quality}}
                            </v-card>
                        </v-col>
                    </v-row>
                    <v-row no-gutters>
                        <v-col col="12">
                            <v-card class="pa-2" outlined tile>
                                Practical usage availability: {{userMarks.practical_usage_availability}}
                            </v-card>
                        </v-col>
                    </v-row>
                </v-col>
            </v-row>
            
            <v-divider color="grey" class="mb-3 mt-3"/>
            
            <v-row no-gutters class="pb-5">
                <v-col
                    class="display-1 black--text font-weight-medium"
                    sm="12"
                >
                Set your marks for this video:
                </v-col>
            </v-row>

            <v-row no-gutters class="headline">
                <v-col md="6">
                    Information quality: 
                    <v-rating
                        background-color="warning lighten-1"
                        color="warning"
    
                        half-increments
                        hover
                        :length="ratingMaxValue"
                        :size="ratingSize"
                        v-model="currentMark.information_quality"
                    />
                </v-col>
                <v-col sm="12">
                    Medical practice quality:
                    <v-rating
                        background-color="warning lighten-1"
                        color="warning"
    
                        half-increments
                        hover
                        :length="ratingMaxValue"
                        :size="ratingSize"
                        v-model="currentMark.medical_practice_quality"
                    />
                </v-col>
                <v-col sm="12">
                    Description quality:
                    <v-rating
                        background-color="warning lighten-1"
                        color="warning"
    
                        half-increments
                        hover
                        :length="ratingMaxValue"
                        :size="ratingSize"
                        v-model="currentMark.description_quality"
                    />
                </v-col>
                <v-col sm="12">
                    Practical usage availability:
                    <v-rating
                        background-color="warning lighten-1"
                        color="warning"
    
                        half-increments
                        hover
                        :length="ratingMaxValue"
                        :size="ratingSize"
                        v-model="currentMark.practical_usage_availability"
                    />
                </v-col>
                <v-col sm="12">
                    <ul>
                        <li class="red--text subheading" v-for="err in errors">
                            {{err[0]}}
                        </li>
                    </ul>
                </v-col>
                <v-col sm="12" class="pt-5">
                    <v-btn 
                        outlined
                        color="orange darken-2" 
                        width="200"
                        @click="clearData"
                        :disabled="isLoading"
                    >Discard marks</v-btn>
                    <v-btn 
                        outlined 
                        color="green darken-1" 
                        width="200"
                        @click="handleData"
                        :disabled="isLoading"
                    >Apply marks</v-btn>
                    <v-progress-circular
                        v-show="isLoading"
                        indeterminate
                        color="grey darken-2"
                    ></v-progress-circular>
                </v-col>
            </v-row>

        </v-container>
    </div>
</template>

<script>
    export default {
        mounted() {
            if (!this.$store.state.user.token) {
                this.$root.$children[0].$refs.errorDialog.show('You must be authorized to perform this action!');
                this.$router.push('/');
                return
            }
            this.$root.$children[0].$refs.bigProcess.show();

            this.$store.dispatch('getVideo', this.$route.params.id)
                .then(response => {
                    this.video = response.data.data.video;
                    this.userMarks = response.data.data.user_marks;
                    this.youtubeMarks = response.data.data.youtube_marks;
                    this.loadedMark = response.data.data.current_mark;

                    this.setCurrentMarkFromLoaded();

                    this.$root.$children[0].$refs.bigProcess.close();
                })
                .catch(err => console.log(err));
        },
        data: () => {
            return {
                video: {
                    youtube_data: {}
                },
                currentMark: {
                    id: null,
                    information_quality: 0,
                    medical_practice_quality: 0,
                    description_quality: 0,
                    practical_usage_availability: 0
                },
                loadedMark: {},
                userMarks: {},
                youtubeMarks: {},
                errors: [],

                ratingSize: 40,
                ratingMaxValue: 5,

                isLoading: false
            }
        },
        computed: {
            marksUpdated() {
                return (this.currentMark.information_quality !== this.loadedMark.information_quality || 
                this.currentMark.medical_practice_quality !== this.loadedMark.medical_practice_quality ||
                this.currentMark.description_quality !== this.loadedMark.description_quality || 
                this.currentMark.practical_usage_availability !== this.loadedMark.practical_usage_availability);
            }
        },
        methods: {
            setCurrentMarkFromLoaded() {
                const defaultValue = 0;

                this.currentMark.id = this.loadedMark.id || null;
                this.currentMark.information_quality = this.loadedMark.information_quality || defaultValue;
                this.currentMark.medical_practice_quality = this.loadedMark.medical_practice_quality || defaultValue;
                this.currentMark.description_quality = this.loadedMark.description_quality || defaultValue;
                this.currentMark.practical_usage_availability = this.loadedMark.practical_usage_availability || defaultValue;
            },
            clearData() {
                this.setCurrentMarkFromLoaded();
            },
            handleData() {
                if (this.marksUpdated){
                    this.isLoading = true;
                    this.$store.dispatch('markVideo', {
                        videoId: this.video.id,
                        userMarks: this.currentMark
                    }).then(response => {
                        this.loadedMark = response.data.data.updated_mark;
                        this.setCurrentMarkFromLoaded();
                        this.userMarks = response.data.data.user_marks;
                        this.isLoading = false;
                    }).catch(err => {
                        this.errors = error.response.data.errors;
                        this.isLoading = false;
                    })
                }
                
            }
        }
    }
</script>
