<template>
<div>
    <main-header/>
    <v-container  >
        <big-search v-on:startSearch="startSearch" ref="bigSearch"/>
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
    <big-process ref="bigProcess" />
    <login-form ref="loginForm" />
    <register-form ref="registerForm" />
    <user-info ref="userInfo" />
    <error-dialog ref="errorDialog" />
    <success-dialog ref="successDialog" />
    <success-alert ref="successAlert" />

  </div>  
</template>

<script>
    import BigSearch from '@/components/search/BigSearch';
    import SearchItem from '@/components/search/SearchItem';
    import MediaElement from '@/components/search/MediaElement';
    import Header from '@/components/main/Header';
    import LoginForm from "@/components/user/LoginForm";
    import RegisterForm from "@/components/user/RegisterForm";
    import UserInfo from "@/components/user/UserInfo";
    import BigProcess from "@/components/progress/BigProcess";
    import ErrorDialog from '@/components/dialogs/ErrorDialog';
    import SuccessDialog from '@/components/dialogs/SuccessDialog';
    import SuccessAlert from '@/components/dialogs/SuccessAlert';

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
                gettingFeaturedKeyPhrase:   "#featured-media"
            }
        },
        methods: {
            showAlert(d) {
                this.$refs.successAlert.show(d);
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
            getFeatured() {
                this.query = this.gettingFeaturedKeyPhrase;
                this.$refs.bigSearch.setMessage(this.query);

                this.$router.push({
                    path: '/',
                    query: {
                        q: this.query
                    }
                });

                this.sendGettingFeatureRequest();
            },
            sendGettingFeatureRequest(){
                this.$refs.bigProcess.show();
                this.$store.dispatch('getFeaturedList')
                .then((response) => {
                    this.$refs.bigProcess.close();
                    this.items = response.data.data.links;
                    this.nextPage = null;
                    this.prevPage = null;
                    this.currPage = null;

                    this.fetched = true;
                })
                .catch((err) => {
                    this.$refs.bigProcess.close();
                    this.errors = error.response.data.errors;
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
                    })
                } else {
                    this.$router.push({
                        path: '/',
                        query: {
                            q: this.query
                        }
                    })
                }
                this.$refs.bigProcess.show();
                
                this.$store.dispatch('getMedia', payload)
                .then((response) => {
                    this.$refs.bigProcess.close();

                    this.currPage = response.data.data.request_data.curr_page;
                    this.prevPage = response.data.data.request_data.prev_page;
                    this.nextPage = response.data.data.request_data.next_page;
                    
                    this.items = response.data.data.links;

                    this.fetched = true;
                })
                .catch((err) => {
                    this.$refs.bigProcess.close();
                    this.errors = error.response.data.errors;
                    this.fetched = true;
                })
            },
            startSearch(q) {
                this.query = q;
                if (q == this.gettingFeaturedKeyPhrase){
                    this.sendGettingFeatureRequest();
                } else {
                    this.sendRequest(null);
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
            },
        },
        components: {
            'big-search':       BigSearch,
            'search-item':      SearchItem,
            'media-element':    MediaElement,
            'login-form':       LoginForm,
            'register-form':    RegisterForm,
            'user-info':        UserInfo,
            'main-header':      Header,
            'big-process':      BigProcess,
            'error-dialog':     ErrorDialog,
            'success-dialog':   SuccessDialog,
            'success-alert':    SuccessAlert,
        },
        mounted() {
            if (this.$route.query.q) {
                this.query = this.$route.query.q;
                this.$refs.bigSearch.setMessage(this.query);

                if (this.query == this.gettingFeaturedKeyPhrase){
                    this.sendGettingFeatureRequest();
                } else {
                    this.sendRequest(this.$route.query.p);
                }
            }
        },
        beforeMount() {
            this.$store.dispatch('initial');
        }
    }
</script>
