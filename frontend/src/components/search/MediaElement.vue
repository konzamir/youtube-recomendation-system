<template>
    <v-dialog
        v-model="dialog"
        content-class="youtube-player"
    >
        <v-card class="black">
            <v-card-title class="pb-2 pt-2 grey lighten-2">
                
                <div 
                    class="headline text-truncate ml-3 mr-4"   
                >
                    {{title}}
                </div> 
                <!-- <v-layout row justify-end> -->
                    <!-- <v-spacer /> -->
                <v-btn icon @click="close" class="mr-0 media-close-btn">
                    <v-icon color="grey darken-1" medium>clear</v-icon>
                </v-btn>
                <!-- </v-layout> -->
            </v-card-title>

        <youtube 
            :video-id="video_id" 
             />
        </v-card>
    </v-dialog>
</template>

<script>
    export default {
        data: () => {
            return {
                dialog: false,
                video_id: null,
                playing: false,
                title: ''
            }
        },
        methods: {
            close() {
                this.dialog = false;
                this.playing = false;
            },
            show: function(video_id) {
                this.dialog = !this.dialog;
                this.video_id = video_id;
            }
        }
    }
</script>
