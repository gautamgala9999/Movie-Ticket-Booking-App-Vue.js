<template>
    <div class="Navbar">
        <Navbar />
    </div>
    <h1></h1>
    <div class="formContainer">
        <h1  style="text-align: center; color: white;">
      Create Show
    </h1>
        <form @submit.prevent="submitForm">
            <div class="form-group">
                <label for="name">Name</label>
                <input type="text" v-model="formData.name" required>
            </div>
            <div class="form-group">
                <label for="description">Description</label>
                <input type="text" v-model="formData.description" required>
            </div>
            <div class="form-group">
                <label for="rating">Rating</label>
                <input type="text" v-model="formData.rating" required>
            </div>
            <div class="form-group">
                <label for="tag">Tag</label>
                <input type="text" v-model="formData.tag" required>
            </div>
            <div class="form-group">
                <label for="datetime">Date - Time</label>
                <input type="datetime-local" v-model="formData.datetime" required>
            </div>
            <div class="form-group">
                <label for="venue_id">Venue Name</label>
                <select v-model="formData.venue_id" required style="width: 220px;text-align: center">
                <option v-for="venue in venues" :key="venue.id" :value="venue.id">
                    {{ venue.name }}
                </option>
                </select>
            </div><br>
      <button type="submit">Submit</button>
    </form>
  </div>
  <div class="footer">
    <Footer />
  </div>
</template>

<script>
import Navbar from '../components/NavBar.vue';
import Footer from '../components/Footer.vue';

export default {
  components: {
    Navbar,
    Footer,
  },
  data() {
    return {
      formData: {
        name: '',
        description: '',
        rating:'',
        tag:'',
        datetime:'',
        venue_id: '',
      },
      venues: [],
    };
  },
  created() {
    this.fetchVenues();
  },
  methods: {
    fetchVenues() {
      fetch('http://localhost:8000/show_venue')
        .then(response => response.json())
        .then(data => {
          this.venues = data; 
        })
        .catch(error => {
          console.error('An error occurred while fetching venues:', error);
        });
    },
    submitForm() {
      const user_data = JSON.parse(localStorage.getItem("user"));
      const requestOptions = {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${user_data?.token}`, 'Content-Type': 'application/json' },
        body: JSON.stringify(this.formData),
      };
      fetch('http://localhost:8000/create_shows', requestOptions)
        .then(response => response.json())
        .then(data => {
          console.log(data);
          if (!data.error) {
            this.$router.push('/shows/');
          }
        })
        .catch(error => {
          console.error('An error occurred:', error);
        });
    },
  },
};
</script>
<style scoped>
.formContainer{

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
input,select{
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
