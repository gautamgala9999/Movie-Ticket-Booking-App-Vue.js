
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'

<script setup>
import { ref } from 'vue';
const shows = ref(null);
const venues = ref(null);
// const user_data = JSON.parse(localStorage.getItem("user"));
// const requestOptions = {
//     method: 'GET', // or 'POST' or other HTTP methods
//     headers: {
//         'Authorization': `Bearer ${user_data?.token}`, // Add the token to the "Authorization" header
//         'Content-Type': 'application/json', // Adjust the content type as needed
//     },
// };

fetch('http://localhost:8000/show_shows')
    .then(response => response.json())
    .then(data => {
        shows.value = data;
    });
fetch(`http://localhost:8000/show_venue`)
    .then(response => response.json())
    .then(data => {
        venues.value = data;
        
    });

    // const getVenueName = (venueId) => {
    //     const venue = venues.value.find(venue => venue.id === venueId);
    //     return venue ? venue.name : 'Unknown Venue';
    // };
    
    
</script>

<template>
    <div class="Navbar">
        <Navbar />
    </div>
    <div class="headerContainer">
        <button v-if="isAdmin" class="buttoncss" @click="downloadCSV()">Download Shows</button>
        <hr><h1 style="text-align: center;">Shows</h1><hr>
        <button v-if="isAdmin" class="buttoncss" @click="CreateShow()">Create a new show</button>
    </div>  
    <div id="tableContainer">
        
        <table class="tableDisplay">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Description</th>
                    <th>Rating</th>
                    <th>Tag</th>
                    <th>Date and Time</th>
                    <th>Venue Name</th>
                    <th  v-if="isAdmin" >Update</th>
                    <th  v-if="isAdmin" >Delete</th>
                    <th v-if="isLoggedIn">Grab Tickets</th>
                    
                </tr>
            </thead>
            <tbody>
                <tr v-for="show in shows" :key="show.id">
                    <td>{{ show.name }}</td>
                    <td>{{ show.description }}</td>
                    <td>{{ show.rating }}</td>
                    <td>{{ show.tag }}</td>
                    <td>{{ show.datetime }}</td>
                    <td>{{ (show.venue_id) }}</td>
                    <td  v-if="isAdmin" ><button @click="update_shows(show.id)">Update {{ show.name }} </button></td>
                    <td  v-if="isAdmin" ><button @click="delete_shows(show.id)">Delete {{ show.name }} </button></td>
                    <td v-if="isLoggedIn"> <button  @click="BuyTicket(show.id)">Grab</button></td>
                </tr>
            </tbody>
        </table>
    </div>
    <div class="footer">
        <Footer />
    </div>
</template>

<script>

export default {
    computed: {
    isLoggedIn() {
      const user = JSON.parse(localStorage.getItem('user'));
    //   console.log(user);
      return user !== null;
    },
    isAdmin() {
        const user = JSON.parse(localStorage.getItem('user'));
    //   console.log(user);
      return user !== null && user.role === 'admin';
    },
  },
    
      methods: {
        BuyTicket(id) {
            this.$router.push('/book_show/' + id);
        },
        CreateShow() {
            this.$router.push('/create_show');
        
        },
        update_shows(id)
        {
            this.$router.push('/update_shows/'+id);
        },
        delete_shows(id)
        {
        fetch(`http://localhost:8000/delete_shows/${id}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
        })
        .then(response => response.json())
        .then(data => {
          console.log(data);
          if ( !data.error) {
            location.reload();
          }
        })
        .catch(error => {
          console.error('An error occurred:', error);
        });
        },
        downloadCSV(){
         this.$router.push('/csv_shows');
        
        },

      },
   };

   
</script>



<style scoped>
*{
    box-sizing: border-box;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
}
body{
    font-family: 'Times New Roman', Times, serif;
    -webkit-font-smoothing: antialiased;
}
h2{
    text-align: center;
    font-size: 18px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: white;
    padding: 30px 0;
}

/* Table Styles */

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

/* Responsive */

@media (max-width: 767px) {
    .tableDisplay {
        display: block;
        width: 100%;
    }
    .tableContainer:before{
        content: "Scroll horizontally >";
        display: block;
        text-align: right;
        font-size: 11px;
        color: white;
        padding: 0 0 10px;
    }
    .tableDisplay thead, .tableDisplay tbody, .tableDisplay thead th {
        display: block;
    }
    .tableDisplay thead th:last-child{
        border-bottom: none;
    }
    .tableDisplay thead {
        float: left;
    }
    .tableDisplay tbody {
        width: auto;
        position: relative;
        overflow-x: auto;
    }
    .tableDisplay td, .tableDisplay th {
        padding: 20px .625em .625em .625em;
        height: 60px;
        vertical-align: middle;
        box-sizing: border-box;
        overflow-x: hidden;
        overflow-y: auto;
        width: 120px;
        font-size: 13px;
        text-overflow: ellipsis;
    }
    .tableDisplay thead th {
        text-align: left;
        border-bottom: 1px solid #f7f7f9;
    }
    .tableDisplay tbody tr {
        display: table-cell;
    }
    .tableDisplay tbody tr:nth-child(odd) {
        background: none;
    }
    .tableDisplay tr:nth-child(even) {
        background: transparent;
    }
    .tableDisplay tr td:nth-child(odd) {
        background: #F8F8F8;
        border-right: 1px solid #E6E4E4;
    }
    .tableDisplay tr td:nth-child(even) {
        border-right: 1px solid #E6E4E4;
    }
    .tableDisplay tbody td {
        display: block;
        text-align: center;
    }
}

.headerContainer {
    display: flex;
    justify-content: flex-end;
    padding: 10px;
    background-color: white;
}

button {
  background-color: #55d6aa;
  color: black;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 15px;
  transition: 0.3s;
}

button:hover {
  background-color: #293f50;
  color: white;
  box-shadow: 0 0 5px #293f50;
}
</style>