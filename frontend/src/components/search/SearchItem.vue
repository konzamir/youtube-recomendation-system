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
                :src="$props.item.preview_url"
                @click.stop="showDialog"
                >
                <v-container fluid pt-1 pr-1>
                    <v-layout justify-end row>
                        
                        <v-btn icon dark @click.stop="addFeatured">
                            <v-icon :color="featured ? 'red' : 'white'" medium>favorite</v-icon>
                        </v-btn>
                    </v-layout>
                </v-container>
            </v-img>
            <v-card-title>
                <div>
                    <span class="font-weight-regular" :class="titleClass"> 
                        <a @click.stop="showDialog">{{$props.item.title}}</a>
                    </span>
                    <br>
                    <span class="grey--text">Number 10</span><br>
                </div>
            </v-card-title>
        </v-card>
        </v-hover>

    </v-flex>    
</template>

<script>
    export default {
        beforeMount(){
            const videoId = this.$props.item.video_id;
            const feturedList = this.$store.state.user.links;
            this.featured = feturedList.includes(videoId);
        },
        props: ['item'],
        data: () => {
            return {
                dialog:                 false,
                featured:               false,
                interval:               null,
                sendingRequestDelay:    1000
            }
        },
        computed: {
            titleClass(){
                const titleLength = this.$props.item.title.length;

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
            showDialog() {
                this.$parent.$refs.media.title=this.$props.item.title;
                this.$parent.$refs.media.show(this.$props.item.video_id);
            },
            sendFeaturedRequest(){
                const videoId = this.$props.item.video_id;
                const payload = {
                    video_id: videoId
                };

                if (this.featured){
                    if (!this.$store.state.user.links.includes(videoId))
                    {
                        this.$store.commit('addFeatured', videoId);
                        this.$store.dispatch('addFeatured', payload)
                        .catch((err) => {
                            this.featured = !this.featured;
                            console.log(err);
                            this.sendErrorMessage(err.response.data.errors[0]);
                        });
                    }
                } else {
                    var arr = this.$store.state.user.links;
                    var index = arr.indexOf(videoId);
                    
                    if (index > -1) {
                        this.$store.commit('removeFeatured', videoId);
                        this.$store.dispatch('removeFeatured', payload)
                        .catch((err) => {
                            this.featured = !this.featured;
                            console.log(err);
                            this.sendErrorMessage(err.response.data.errors[0]);
                        });
                    }
                }
            },
            addFeatured(){
                if (this.$store.state.user.token){
                    this.featured = !this.featured;
                    const videoId = this.$props.item.video_id;

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
