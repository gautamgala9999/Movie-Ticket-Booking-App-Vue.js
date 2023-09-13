<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router'

const route = useRoute()
console.log(route.params)
const showData = ref(null);
const user_data = JSON.parse(localStorage.getItem("user"));
const requestOptions = {
    method: 'GET', // or 'POST' or other HTTP methods
    headers: {
        'Authorization': `Bearer ${user_data?.token}`, // Add the token to the "Authorization" header
        'Content-Type': 'application/json', // Adjust the content type as needed
    },
};
fetch(`http://localhost:8000/book_tickets/${route.params.id}`,requestOptions)
    .then(response => response.json())
    .then(data => {
        showData.value = data;
    });
</script>


import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'

<template>
    <div class="Navbar">
      <Navbar />
    </div>

    <h1>
    </h1>
    <div class="showInfo">
      <h1  style="text-align: center; color: white;">
        Book Tickets
    </h1>
      <form @submit.prevent="bookTickets">
        <label for="ShowName">Movie Name</label>
        <input type="text" id="ShowName" name="ShowName" v-model="showData.name" disabled/>
        <br>
        <label for="ShowTime">Show Time</label>
        <input type="text" id="ShowTime" name="ShowTime" v-model="showData.datetime" disabled/>
        <br>
        <label for="venue">Venue</label>
        <input type="number" id="venue" name="venue" v-model="showData.venue_id" disabled/>
        <br>
        
        <label for="ShowDescription">Description</label>
        <input type="text" id="ShowDescription" name="ShowDescription" v-model="showData.description" disabled/>
        <br>
        <label for="ShowRating">Rating</label>
        <input type="text" id="ShowRating" name="ShowRating" v-model="showData.rating" disabled/>
        <br>
        <label for="ShowTickets">Grab Tickets</label>
        <input type="number" id="ShowTickets" name="ShowTickets" v-model="numTickets"  />
        <br>
        <br>
        <button v-if="isLoggedIn" type="submit">Grab Now !</button>
      </form>
    </div>
    <div class="footer">
      <Footer />
    </div>
  </template>

<script>
import { useRoute } from 'vue-router'
export default {
  data() {
    return {
      showData: {
        name: '',
        datetime: '',
        description: '',
        rating: '',
        venue_id: '',
      },
      numTickets: 0,
    };
  },
  computed: {
    isLoggedIn() {
      const user = JSON.parse(localStorage.getItem('user'));
      console.log(user);
      return user !== null;
    },
  },
  methods: {
    bookTickets() {
      const route = useRoute()
      const formData = {
        email : JSON.parse(localStorage.getItem('user')).email,
        numTickets: this.numTickets,
      };
      console.log(formData);
        fetch(`http://localhost:8000/book_tickets/${route.params.id}`, {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        })
            .then(response => response.json())
            .then(data => {
              console.log(data);
              if(!data.error){
                alert("Tickets Booked Successfully")
                this.$router.push("/")
              }
              else{
                
                alert(data.error)
                this.$router.push("/login")
              }
            });
  },
}
}
</script>


<style scoped>
.showInfo{
  display: flex;
  flex-direction: column;
  width: 21%;
  text-align: right;
  justify-self: right;
  align-self: right;
  padding: 1% 1%;
  border-radius: 10px;
  border-color: black;
  background-color: black;
  margin-left:35%;
}
input{
  background-color: white;
  padding: 10px;
  border-radius: 10px;
  margin-top:8px;
  margin-bottom:5px;
  text-align: center;
  align-self: center;
  width: 50%;
  width: 200px;

}
label{
  color: white;
  padding: 5px;
}
button {
background-color: #55d6aa;
color: black;
padding: 10px 15px;
border-radius: 5px;
cursor: pointer;
font-size: 16px;
transition: 0.3s;
}

button:hover {
background-color: #293f50;
color: white;
box-shadow: 0 0 5px #293f50;
}
</style>
