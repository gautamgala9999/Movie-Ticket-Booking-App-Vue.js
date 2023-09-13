<script setup>
import { ref } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();

const formData = ref({
  name: "",
  description: "",
  rating: "",
  tag: "",
  datetime: "",
  venue_id: "",
});
const user_data = JSON.parse(localStorage.getItem("user"));
const requestOptions = {
    method: 'GET', // or 'POST' or other HTTP methods
    headers: {
        'Authorization': `Bearer ${user_data?.token}`, // Add the token to the "Authorization" header
        'Content-Type': 'application/json', // Adjust the content type as needed
    },
};
fetch(`http://localhost:8000/show_shows/${route.params.id}`,requestOptions)
  .then((response) => response.json())
  .then((data) => {
    formData.value.name = data.name;
    formData.value.description = data.description;
    formData.value.rating = data.rating;
    formData.value.tag = data.tag;
    formData.value.datetime = data.datetime;
    formData.value.venue_id = data.venue_id;
    console.log(formData);
  });

function submitForm() {
  console.log(JSON.parse(JSON.stringify(formData.value)));
  const requestBody = JSON.parse(JSON.stringify(formData.value));

  const requestOptions = {
    method: "POST",
    headers: { 'Content-Type': 'application/json','Authorization': `Bearer ${user_data?.token}` },
    body: JSON.stringify(requestBody),
  };
  fetch(`http://localhost:8000/update_shows/${route.params.id}`, requestOptions)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      if (!data.error) {
        window.location.href = "http://localhost:5173/shows"
      }
    });
}
</script>

import Navbar from '../components/Navbar.vue' import Footer from
'../components/Footer.vue'
<template>
  <div class="Navbar">
    <Navbar />
  </div>
  <h1></h1>
  <div class="formContainer">
    <h1 style="text-align: center; color: white">Update Show</h1>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="name">Name</label>
        <input type="text" id="name" v-model="formData.name" required />
      </div>
      <div class="form-group">
        <label for="description">Description</label>
        <input type="text" v-model="formData.description" required />
      </div>
      <div class="form-group">
        <label for="rating">Rating</label>
        <input type="text" v-model="formData.rating" required />
      </div>
      <div class="form-group">
        <label for="tag">Tag</label>
        <input type="text" v-model="formData.tag" required />
      </div>
      <div class="form-group">
        <label for="tag">Tag</label>
        <input type="datetime-local" v-model="formData.datetime" required />
      </div>
      <div class="form-group">
        <label for="venue_id">Venue ID</label>
        <input type="text" v-model="formData.venue_id" required />
      </div>
      <br />
      <button type="submit">Submit</button>
    </form>
  </div>
  <div class="footer">
    <Footer />
  </div>
</template>

<style scoped>
.formContainer {
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
  margin-left: 35%;
}
input {
  background-color: white;
  padding: 10px;
  border-radius: 10px;
  margin-top: 8px;
  margin-bottom: 5px;
  text-align: center;
  align-self: center;
  width: 50%;
  width: 200px;
}
label {
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
