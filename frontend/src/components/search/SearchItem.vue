<template>
    <v-flex xs12 sm6 md4 lg3 class="pa-1">
        <v-hover>
        <v-card 
            slot-scope="{ hover }"
            :class="`elevation-${hover ? 12 : 2}`"
            class="search-card-item mx-auto"
        >
            <v-img
                class="white--text search-item-img"
                height="200px"
                :src="$props.video.youtube_data.image_preview.link"
                @click="showInfoPage"
                >
                <v-container fluid pt-1 pr-4>
                    <v-layout justify-end row>
                        <v-btn 
                            fab
                            elevation="5" 
                            @click.stop="addFeatured"
                            width="45"
                            height="45"
                        >
                            <v-icon 
                                :color="featured ? 'red' : 'grey lighten-1'" 
                                x-large 
                            >favorite</v-icon>
                        </v-btn>
                    </v-layout>
                </v-container>
            </v-img>
            <v-card-title>
                <div>
                    <span class="font-weight-regular" :class="titleClass"> 
                        <a @click="showInfoPage">{{sliceStr($props.video.title)}}</a>
                    </span>
                    <br>
                    <span class="grey--text">{{sliceStr($props.video.description)}}</span><br>
                </div>
            </v-card-title>
        </v-card>
        </v-hover>

    </v-flex>    
</template>

<script>
    export default {
        beforeMount(){
            const videoId = this.$props.video.id;
            const feturedList = this.$store.state.user.links;
            this.featured = feturedList.includes(videoId);
        },
        props: ['video'],
        data: () => {
            return {
                dialog: false,
                featured: false,
                interval: null,
                sendingRequestDelay: 1000,
                descriptionLimit: 45
            }
        },
        computed: {
            titleClass(){
                const titleLength = this.$props.video.title.length;

                if (titleLength > 30) {
                    return 'subheading';
                } else if (titleLength > 15) {
                    return 'title';
                }
                return 'headline';
            }
        },
        components: {
        },
        methods: {
            sliceStr(textData) {
                return textData.length > this.descriptionLimit
                    ? textData.slice(0, this.descriptionLimit) + '...'
                    : textData
            },
            showInfoPage() {
                this.$router.push({
                        name: 'videoInfo',
                        params: {
                            id: this.$props.video.id
                        }
                    }
                )
            },
            sendFeaturedRequest(){
                const videoId = this.$props.video.id;

                if (this.featured){
                    if (!this.$store.state.user.links.includes(videoId))
                    {
                        this.$store.dispatch('addFeatured', videoId)
                        .catch((err) => {
                            this.featured = !this.featured;
                            console.log(err);
                        });
                    }
                } else {
                    var arr = this.$store.state.user.links;
                    var index = arr.indexOf(videoId);
                    
                    if (index > -1) {
                        this.$store.dispatch('removeFeatured', videoId)
                        .catch((err) => {
                            this.featured = !this.featured;
                            console.log(err);
                        });
                    }
                }
            },
            addFeatured(){
                if (this.$store.state.user.token){
                    this.featured = !this.featured;
                    const videoId = this.$props.video.video_id;

                    if (this.featured) {
                        this.$store.commit("addFeatured", videoId);
                    } else {
                        this.$store.commit("removeFeatured", videoId);
                    }

                    clearInterval(this.interval);
                    this.interval = setInterval(() => {
                        this.sendFeaturedRequest();
                        clearInterval(this.interval);
                    }, this.sendingRequestDelay);
                } else {
                    this.sendErrorMessage("You must be logined to add media to favourites!");
                }
                
            },
            sendErrorMessage(detail){
                this.$parent.$refs.errorDialog.show(detail);
            }
        }
    }
</script>
