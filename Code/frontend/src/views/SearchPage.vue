import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'

<template>
    <div>
      <div class="Navbar">
        <Navbar />
      </div>
      <div>
        <input v-model="userInput" type="text" class="searchInput" placeholder="search shows or venue" />
      </div>
      <div>
        <h2>Shows</h2>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Datetime</th>
              <th>Rating</th>
              <th>Description</th>
              <th>Tag</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="show in showResults" :key="show.id">
              <td>{{ show.name }}</td>
              <td>{{ show.datetime }}</td>
              <td>{{ show.rating }}</td>
              <td>{{ show.description }}</td>
              <td>{{ show.tag }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div>
        <h2>Venues</h2>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Location</th>
              <th>Capacity</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="venue in venueResults" :key="venue.id">
              <td>{{ venue.name }}</td>
              <td>{{ venue.location }}</td>
              <td>{{ venue.capacity }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="footer">
        <Footer />
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        userInput: '',
        showResults: [],
        venueResults: [],
      };
    },
    methods: {
      async searchAPI() {
        try {
          const response = await fetch(`http://localhost:8000/search?name=${this.userInput}`);
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          const data = await response.json();
          console.log('API Response:', data);
  
          if (data.result_type === "Mixed") {
            this.showResults = data.results.shows;
            this.venueResults = data.results.venues;
          } else if (data.result_type === "Show") {
            this.showResults = data.results;
            this.venueResults = [];
          } else if (data.result_type === "Venue") {
            this.showResults = [];
            this.venueResults = data.results;
          }
        } catch (error) {
          console.error('Error:', error);
        }
      },
    },
    watch: {
      userInput(newValue) {
        console.log('User input:', newValue);
        this.searchAPI();
      },
    },
  };
  </script>
  
  <style scoped>
  .searchInput {
    border-radius: 5px;
  }
  
  /* Add your CSS styles for tables here */
  table {
    border-collapse: collapse;
    width: 100%;
  }
  
  th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }
  
  th {
    background-color: #f2f2f2;
  }
  </style>
  