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
                                Practical usage availability: {{video.practical_usage_availability || "Not chosen yet"}}
                            </v-card>
                        </v-col>
                    </v-row>
                </v-col>
            </v-row>
            
        </v-container>
    </div>
</template>

<script>
    export default {
        mounted() {
            this.$root.$children[0].$refs.bigProcess.show();

            this.$store.dispatch('getVideo', this.$route.params.id)
                .then(response => {
                    this.video = response.data.data.video;
                    this.userMarks = response.data.data.user_marks;
                    this.youtubeMarks = response.data.data.youtube_marks;
                    this.currentMark = response.data.data.current_mark;

                    this.$root.$children[0].$refs.bigProcess.close();
                })
                .catch(err => console.log(err));
        },
        data: () => {
            return {
                video: {
                    youtube_data: {}
                },
                currentMark: {},
                userMarks: {},
                youtubeMarks: {},
                errors: []
            }
        }
    }
</script>
