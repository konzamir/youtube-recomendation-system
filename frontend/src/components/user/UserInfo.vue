<template>
    <v-dialog
        v-model="dialog"
        content-class="form-style"
        :persistent="isLoading"
        width="400"
    >
        <v-card class="elevation-12">
                <v-toolbar color="grey lighten-2">
                <v-toolbar-title>User info</v-toolbar-title>
                <v-spacer />
                <v-btn 
                    icon 
                    @click="close" 
                    class="user-close-btn"
                    :disabled="isLoading">
                    <v-icon color="grey darken-1" medium>clear</v-icon>
                </v-btn>
                </v-toolbar>
                <v-card-text class="pb-0">
                    <blockquote class="blockquote pl-0 ">
                        <v-layout justify-center row>
                        <v-parallax
                            dark
                            src="https://cdn.vuetifyjs.com/images/parallax/material.jpg"
                            class="user-parallax-picture"
                        >
                            <v-layout
                            align-center
                            column
                            justify-center
                            >
                            <h1 class="display-3 text-capitalize">{{username[0]}}</h1>
                            </v-layout>
                        </v-parallax>
                        </v-layout>
                    </blockquote>
                    <blockquote class="blockquote">
                        <b>Email:</b> {{email}}
                    </blockquote>
                    <blockquote class="blockquote">
                        <b>Username:</b> {{username}}
                    </blockquote>
                    <blockquote class="blockquote">
                        <a @click.stop="getFeatured"> Get featured list ({{featuredCount}}) </a>
                    </blockquote>
                    <!-- <blockquote class="blockquote"> -->
                        <ul>
                        <li class="red--text subheading" v-for="err in errors">
                            {{err}}
                        </li>
                        </ul>
                    <!-- </blockquote> -->
                
                </v-card-text>
                <v-card-actions class="pb-2">
                    <v-spacer />
                    <v-btn
                        flat 
                        color="primary" 
                        @click="logout"
                        :disabled="isLoading"
                    ><b>Log out</b></v-btn>
                    <v-progress-circular
                    v-show="isLoading"
                    indeterminate
                    color="grey darken-2"
                    ></v-progress-circular>
                    <v-spacer />
                </v-card-actions>
            </v-card>
        <confirmation 
            v-on:confirm="confirmLogoutF"
            ref="confirmation"
        />
    </v-dialog>
</template>

<script>
    import LogoutConfirmation from '@/components/dialogs/LogoutConfirmation';
    export default {
        data: () => {
            return {
                errors: [],
                username: "",
                dialog: false,
                email: "",
            }
        },
        computed:{
            isLoading(){
                return this.$store.state.isLoading;
            },
            featuredCount() {
                return this.$store.state.user.links.length;
            }
        },
        methods: {
            getFeatured (){
                this.$parent.getFeatured();
                this.close();
            },
            confirmLogoutF(confirmed){
                if (confirmed) {
                    this.$store.dispatch('logoutAction')
                    .then((response) => {
                        this.$store.commit('removeUser', false);
                        this.$store.commit('setLoadingStatus', false);
                        this.close();
                        this.$parent.$refs.successDialog.show('Logout successful!');
                    })
                    .catch((err) => {
                        this.errors = error.response.data.errors;
                        this.$store.commit('setLoadingStatus', false);
                    })
                }
            },
            close() {
                this.dialog = false;
            },
            logout() {
                this.$refs.confirmation.show();
            },
            show() {
                let user = this.$store.state.user;
                this.username = user.username;
                this.email = user.email;
                this.dialog = !this.dialog;

            },
        },
        components: {
            'confirmation': LogoutConfirmation
        }
    }
</script>
