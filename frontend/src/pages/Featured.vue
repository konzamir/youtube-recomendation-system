<template>
    <div>
        <v-container>
        <router-link to="/" class="headline">
            <v-icon class="pb-1"> mdi-chevron-left</v-icon> Home
        </router-link>
        <v-row no-gutters class="pb-5 pt-4">
            <v-col
                class="display-1 black--text font-weight-medium"
                sm="12"
            >
            Featured List:
            </v-col>
        </v-row>
        <v-divider color="grey" class="mb-3"/>
        <div>
            <v-layout row wrap v-if="this.videos.length > 0">
                <search-item 
                    v-for="video in this.videos" 
                    :key="video.video_id"
                    :video="video"
                />
            </v-layout>
            <v-layout row wrap justify-center v-else class="headline pt-2">
                No media were added into the featured!
            </v-layout>
        </div>
        
        </v-container>
    </div>
</template>
<script>
import SearchItem from '@/components/search/SearchItem';


export default {
    
    mounted() {
        this.$root.$children[0].$refs.bigProcess.show();
        this.$store.dispatch('getFeaturedList').then(res => {
            console.log(res.data)
            this.videos = res.data.data.videos;
            this.$root.$children[0].$refs.bigProcess.close();
        }).catch(err => {
            console.log(err);
            this.$root.$children[0].$refs.bigProcess.close();
        })
    },
    data: () => {
        return {
            videos: []
        }
    },
    components: {
        'search-item':      SearchItem,
    },
}
</script>