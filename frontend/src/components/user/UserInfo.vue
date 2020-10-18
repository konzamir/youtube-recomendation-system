<template>
    <v-dialog
        v-model="dialog"
        content-class="form-style"
        persistent
        :width="editEnabled ? 500 : 400"
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

                    <div v-if="!editEnabled">
                        <blockquote class="blockquote">
                            <b>Email:</b> {{email}}
                        </blockquote>
                        <blockquote class="blockquote">
                            <b>Username:</b> {{username}}
                        </blockquote>
                        <blockquote class="blockquote">
                            <a @click.stop="getFeatured"> Get featured list ({{featuredCount}}) </a>
                        </blockquote>
                    </div>
                    <div v-else>
                        <v-form
                            ref="form" 
                            v-model="editFormValid"
                            lazy-validation>
                            <blockquote class="blockquote">
                                <b>New email:</b>
                                <v-text-field 
                                    v-model="editableData.email"
                                    prepend-icon="alternate_email" 
                                    name="email" 
                                    label="Email"
                                    type="email"
                                    :rules="emailRules"
                                />
                            </blockquote>
                            <blockquote class="blockquote">
                                <b>New username:</b> 
                                <v-text-field 
                                    v-model="editableData.username"
                                    prepend-icon="person" 
                                    name="username" 
                                    label="Username"
                                    type="text"/>
                            </blockquote>
                            <blockquote class="blockquote" >
                                <b>New password:</b> <v-text-field
                                    v-model="editableData.password"
                                    prepend-icon="lock" 
                                    name="password" 
                                    label="Password" 
                                    :rules="passwordRules"
                                    type="password" />
                            </blockquote>
                        </v-form>
                    </div>

                    <blockquote class="blockquote" v-show="errors.length > 0">
                        <ul>
                        <li class="red--text subheading" v-for="err in errors">
                            {{err}}
                        </li>
                        </ul>
                    </blockquote>
                
                </v-card-text>
                <v-card-actions class="pb-2">
                    <v-spacer />
                    <div v-if="!editEnabled">
                    <v-btn
                        flat 
                        color="green darken-2" 
                        @click="edit"
                        :disabled="isLoading"
                    >
                        <b>Edit</b>
                    </v-btn>
                    <v-btn
                        flat 
                        color="primary" 
                        @click="logout"
                        :disabled="isLoading"
                    >
                        <b>Log out</b>
                    </v-btn>
                    </div>
                    <div v-else>
                        <v-btn
                            flat 
                            color="green darken-2" 
                            @click="confirmUpdate"
                            :disabled="isLoading"
                        >
                            <b>Confirm</b>
                        </v-btn>
                        <v-btn
                            flat 
                            color="red darken-2" 
                            @click="edit"
                            :disabled="isLoading"
                        >
                            <b>Cancel</b>
                        </v-btn>
                    </div>
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
                dialog: false,
                editEnabled: false,
                editFormValid: true,
                editableData: {
                    username: "",
                    email: "",
                    password: ""
                },
                passwordRules: [
                    v => v == "" || v.length >= 8 || 'Min length is 8 symbols.'
                ],
                emailRules: [
                    v => v == "" ||  /.+@.+/.test(v) || 'E-mail must be valid'
                ],
            }
        },
        computed:{
            isLoading(){
                return this.$store.state.isLoading;
            },
            featuredCount() {
                return this.$store.state.user.links.length;
            },
            username() {
                return this.$store.state.user.username;
            },
            email() {
                return this.$store.state.user.email;
            }
        },
        methods: {
            getFeatured (){
                // TODO:::find a better solution to always get 
                // featured list
                this.$router.push({
                    name: 'main',
                }, () => {});
                this.$router.push({
                    name: 'main',
                    query: {
                        q: this.$store.state.gettingFeaturedKeyPhrase
                    }
                }, () => {});
                this.close();
            },
            confirmLogoutF(confirmed){
                if (confirmed) {
                    this.$store.dispatch('logoutAction')
                    .then((response) => {
                        this.$store.commit('removeUser', false);
                        this.$store.commit('setLoadingStatus', false);
                        this.close();
                        this.$parent.$parent.$refs.successDialog.show('Logout successful!');
                    })
                    .catch((err) => {
                        this.errors = error.response.data.errors;
                        this.$store.commit('setLoadingStatus', false);
                    })
                }
            },
            close() {
                this.dialog = false;
                this.$store.state.userInfoModal = false;
            },
            logout() {
                this.$refs.confirmation.show();
            },
            edit() {
                this.editEnabled = !this.editEnabled;
                Object.keys(this.editableData).forEach(key => {
                    this.editableData[key] = "";
                });
            },
            confirmUpdate() {
                this.errors = [];
                if (this.$refs.form.validate()) {
                    let payload = {}
                    Object.keys(this.editableData).forEach(key => {
                        if (this.editableData[key] != "" && this.editableData[key] != this[key]){
                            payload[key] = this.editableData[key];
                        }
                    });
                    this.$store.commit('setLoadingStatus', true);
                    this.$store.dispatch('updateUser', payload).then(response => {
                        this.$store.commit('setLoadingStatus', false);
                        this.$store.commit("updateUser", response.data.data);
                        this.editEnabled = false;
                    }).catch(err => {
                        let errors = err.response.data.errors;
                        Object.keys(errors).forEach(key => {
                            this.errors.push(`${key} - ${errors[key][0]}`)
                        })
                    })
                }
            },
            show() {
                this.dialog = !this.dialog;
            },
        },
        components: {
            'confirmation': LogoutConfirmation
        }
    }
</script>
