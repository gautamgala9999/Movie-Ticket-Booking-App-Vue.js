
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'

<script setup>
import { ref } from 'vue';
const venues = ref(null);
fetch(`http://localhost:8000/show_venue`)
    .then(response => response.json())
    .then(data => {
        venues.value = data;
    });
</script>

<template>
    <div class="Navbar">
        <Navbar />
    </div>
    <div class="headerContainer">
        <button  v-if="isAdmin"  @click="downloadCSV()">Download Venues</button>
        <hr><h1 style="text-align: center;">Venues</h1><hr>
        <button  v-if="isAdmin"  @click="CreateVenue()">Create a new Venue</button>
    </div>
    <div id="tableContainer">
        <table class="tableDisplay">
            <thead>
                <tr>
                    <!-- <th>ID</th> -->
                    <th>Name</th>
                    <th>Location</th>
                    <th>Capacity</th>
                    <th  v-if="isAdmin" >Update</th>
                    <th  v-if="isAdmin" >Delete</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="venue in venues" :key="venue.id">
                    <!-- <td>{{ venue.id }}</td> -->
                <td>{{ venue.name }}</td>
                <td>{{ venue.location }}</td>
                <td>{{ venue.capacity }}</td>
                <td  v-if="isAdmin" ><button @click="update_venue(venue.id)">Update {{ venue.name }} </button></td>
                <td  v-if="isAdmin" ><button @click="delete_venue(venue.id)">Delete {{ venue.name }} </button></td>
                    
                </tr>
            </tbody>
        </table>
    </div>
    <div class="footer">
        <Footer />
    </div>
</template>

<style scoped>
*{
    box-sizing: border-box;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    /* font-family: 'Times New Roman', Times, serif; */
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

<script>
export default {
    computed: {
    isLoggedIn() {
      const user = JSON.parse(localStorage.getItem('user'));
      return user !== null;
    },
    isAdmin() {
        const user = JSON.parse(localStorage.getItem('user'));
      console.log(user);
      return user !== null && user.role === 'admin';
    },
  },
      methods: {
        CreateVenue() {
            this.$router.push('/create_venue');
        },
        update_venue(id){
            this.$router.push('/update_venue/'+id);
        },
        delete_venue(id)
        {
            fetch(`http://localhost:8000/delete_venue/${id}`, {
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
         this.$router.push('/csv_venue');
        
        },

        
  
      },
   };
   
</script>

