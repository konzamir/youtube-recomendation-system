<template>
<div>
    <v-container  >
        <big-search v-on:startSearch="startSearch" ref="bigSearch" />
        <ul>
            <li class="red--text subheading" v-for="err in errors">
                {{err}}
            </li>
        </ul>
        <div v-if="this.fetched">
            <v-layout flex class="pt-0">
                <div class="headline pt-2">
                    Results:
                </div>
                <v-spacer />
                <div class="pt-2">
                    <v-btn icon class="ma-0" :disabled="prevPage == null" @click="sendRequest(prevPage)">
                        <v-icon color="grey darken-1" medium>keyboard_arrow_left</v-icon>
                    </v-btn>
                    <v-btn icon class="ma-0" :disabled="nextPage == null" @click="sendRequest(nextPage)">
                        <v-icon color="grey darken-1" medium>keyboard_arrow_right</v-icon>
                    </v-btn>
                </div>
            </v-layout>
            
            <v-divider color="grey" class="mb-2"/>

            <v-layout row wrap v-scroll="onScroll" v-if="this.items.length > 0">
                <search-item v-for="item in this.items" :key="item.video_id"
                    :item="item"/>    
            </v-layout>
            <v-layout row wrap justify-center v-scroll="onScroll" v-else class="display-1 pt-2">
                No media were found!
            </v-layout>    
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
        </div>
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
                displayReturnButtonValue:   200,
                displayReturnButton:        false,
                offsetTop:                  0,
                items:                      [],
                errors:                     [],
                query:                      "",
                fetched:                    false,
                currPage:                   null,
                nextPage:                   null,
                prevPage:                   null,
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
            sendGettingFeatureRequest(){
                this.$root.$children[0].$refs.bigProcess.show();
                this.$store.dispatch('getFeaturedList')
                .then((response) => {
                    this.$root.$children[0].$refs.bigProcess.close()
                    this.items = response.data.data.links;
                    this.nextPage = null;
                    this.prevPage = null;
                    this.currPage = null;

                    this.fetched = true;
                })
                .catch((err) => {
                    console.log(err)
                    this.$root.$children[0].$refs.bigProcess.close()
                    this.errors = err.response.data.errors;
                    this.fetched = true;
                });
            },
            sendRequest(pageToken){
                let payload = {
                    q: this.query
                }
                if (pageToken){
                    payload['page_token'] = pageToken;
                    this.$router.push({
                        path: '/',
                        query: {
                            q: this.query,
                            p: pageToken
                        }
                    }, () => {})
                } else {
                    this.$router.push({
                        path: '/',
                        query: {
                            q: this.query
                        }
                    }, () => {})
                }
                this.$root.$children[0].$refs.bigProcess.show();
                
                this.$store.dispatch('getMedia', payload)
                .then((response) => {
                    this.$root.$children[0].$refs.bigProcess.close();

                    this.currPage = response.data.data.request_data.curr_page;
                    this.prevPage = response.data.data.request_data.prev_page;
                    this.nextPage = response.data.data.request_data.next_page;
                    
                    this.items = response.data.data.links;

                    this.fetched = true;
                })
                .catch((err) => {
                    this.$root.$children[0].$refs.bigProcess.close();
                    this.errors = err.response.data.errors;
                    this.fetched = true;
                })
            },
            startSearch(payload) {
                console.log(payload);
                // this.query = q;
                // if (q == this.$store.state.gettingFeaturedKeyPhrase){
                //     this.sendGettingFeatureRequest();
                // } else {
                //     this.sendRequest(null);
                // }
            },
            pageLoad() {
                if (this.$route.query.q) {
                    this.query = this.$route.query.q;
                    this.$refs.bigSearch.setMessage(this.query);

                    if (this.query == this.$store.state.gettingFeaturedKeyPhrase){
                        this.$refs.bigSearch.setMessage(this.query);
                        this.sendGettingFeatureRequest();
                    } else {
                        this.sendRequest(this.$route.query.p);
                    }
                }
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
        beforeRouteUpdate(to, from, next) {
            this.pageLoad();
            next();
        },
        mounted() {
            this.pageLoad();
        }
    }
</script>
