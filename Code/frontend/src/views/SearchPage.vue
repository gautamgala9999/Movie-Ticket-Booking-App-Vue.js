import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'
<template>
  <div>
    <div class="Navbar">
      <Navbar />
    </div>
    <div style="display: flex; justify-content: center; align-items: center;">
      <input
        v-model="userInput"
        type="text"
        class="searchInput"
        placeholder="search shows or venue"
        style="width: 100%; height: 100%; border: 2px solid #55d6aa; padding: 10px; box-sizing: border-box;"
      />
    </div>
    <div v-if="resultType === 'Mixed'">
      <hr /><h1 style="text-align: center;">Shows</h1><hr />
      <table class="tableDisplay">
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

      <hr /><h1 style="text-align: center;">Venues</h1><hr />
      <table class="tableDisplay">
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
    <div v-else-if="resultType === 'Show'">
      <hr /><h1 style="text-align: center;">Shows</h1><hr />
      <table class="tableDisplay">
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
    <div v-else-if="resultType === 'Venue'">
      <hr /><h1 style="text-align: center;">Venues</h1><hr />
      <table class="tableDisplay">
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
    <div v-else>
      <br><br><br>
      <h1 style="text-align: center;">(⊙ˍ⊙)</h1>
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
      resultType: '', 
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

        this.resultType = data.result_type; 

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

#tableContainer{
    margin: 10px 70px 70px;
    box-shadow: 0px 35px 50px #55d6aa;
}

.tableDisplay {
    border-radius: 5px;
    font-size: 15px;
    font-weight: normal;
    border: none;
    border-collapse: collapse;
    width: 100%;
    max-width: 100%;
    white-space: nowrap;
    background-color: white;
}

.tableDisplay td, .tableDisplay th {
    text-align: center;
    padding: 8px;
}

.tableDisplay td {
    border-right: 1px solid #f8f8f8;
    font-size: 15px;
}

.tableDisplay thead th {
    color: #ffffff;
    background: #55d6aa;
}


.tableDisplay thead th:nth-child(odd) {
    color: #ffffff;
    background: black;
}

.tableDisplay tr:nth-child(even) {
    background: #F8F8F8;
}

  </style>
  