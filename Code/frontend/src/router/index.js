import { createRouter, createWebHistory } from 'vue-router'
import HomePage from "../views/HomePage.vue"
import Login from "../views/Login.vue"
import Signup from "../views/Signup.vue"
import BookShow from "../views/BookShow.vue"
import Shows from "../views/Shows.vue"
import Venues from "../views/Venues.vue"
import CreateShow from "../views/CreateShow.vue"
import CreateVenue from "../views/CreateVenue.vue"
import UpdateShow from "../views/UpdateShow.vue"
import UpdateVenue from "../views/UpdateVenue.vue"
import csv_venue from "../views/csv_venue.vue"
import csv_shows from "../views/csv_shows.vue"
import profile from "../views/profile.vue"
import logout from "../views/logout.vue"
import SearchPage from '../views/SearchPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage
    },
    {
      path : "/login",
      name: "login",
      component : Login
    },
    {
      path : "/signup",
      name: "signup",
      component : Signup
    },
    {
      path: '/shows',
      name: "shows",
      component: Shows
    },
    {
      path: '/venues',
      name: "venues",
      component: Venues
    },
    {
      path: '/book_show/:id',
      name: "book_show",
      component: BookShow
    },
    {
      path: '/create_show',
      name: 'create_show',
      component: CreateShow
    },
    {
      path: '/create_venue',
      name: 'create_venue',
      component: CreateVenue
    },
    {
      path: '/update_shows/:id',
      name: 'update_shows',
      component: UpdateShow
    },
    {
      path: '/update_venue/:id',
      name: 'update_venue',
      component: UpdateVenue
    },
    {
      path: '/csv_venue',
      name: 'csv_venue',
      component: csv_venue
    },
    {
      path: '/csv_shows',
      name: 'csv_shows',
      component: csv_shows
    },
    {
      path: '/profile',
      name: ' profile',
      component: profile
    },
    {
      path: '/logout',
      name: 'logout',
      component: logout
    },
    {
      path: '/search',
      name: 'search',
      component: SearchPage
    }
  ]
})

export default router
