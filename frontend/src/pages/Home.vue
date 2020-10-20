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
                fetched:                    false
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
            startSearch(payload){
                this.$root.$children[0].$refs.bigProcess.show();
                
                this.$store.dispatch('startProcess', payload)
                .then((response) => {
                    this.$root.$children[0].$refs.bigProcess.close();

                    console.log(response.data)
                    // this.process = response.data.data.process;
                    this.fetched = true;
                })
                .catch((err) => {
                    this.$root.$children[0].$refs.bigProcess.close();
                    this.errors = err.response.data.errors;
                    this.fetched = true;
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
        }
    }
</script>
