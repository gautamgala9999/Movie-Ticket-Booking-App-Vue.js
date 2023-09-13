
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'


<script setup>
import { ref, computed } from 'vue';


const ticketData = ref([]);
fetch('http://localhost:8000/bookings')
.then(response => response.json())
.then(data => {
    ticketData.value = data.ticket_data;
    console.log(data);
});

const shows = ref([]);
fetch(`http://localhost:8000/show_shows`)
    .then(response => response.json())
    .then(data => {
        shows.value = data;
    });

const gusers = JSON.parse(localStorage.getItem('user'));
// console.log(gusers);

const defaultUser = {
    id: 'null',
    name: 'Please Login',
    email: 'Please Login'
};

const users = ref(gusers ? [gusers] : [defaultUser]);

const getShowName = (showId) => {
    const show = shows.value.find(show => show.id === showId);
    return show ? show.name : 'Unknown Show';
};

const getShowTime = (showId) => {
    const show = shows.value.find(show => show.id === showId);
    return show ? show.datetime : 'error';
};

const filteredTicketData = computed(() => {
    if (users.value[0].id === 'null') {
        return [];
    }
    return ticketData.value.filter(ticket => ticket.user_id === users.value[0].id);
});
</script>

<template>
    <div class="Navbar">
        <Navbar />
    </div>
    <div id="tableContainer"><hr>
    <h1 style="text-align: center;">Profile</h1><hr>
    <table class="tableDisplay">
        <tbody>
            <tr v-for="user in users" :key="user.id">
                <th>User ID</th>
                <td>:</td>
                <td>U{{ user.id }}</td><hr><hr><hr><hr>
               
                <th>User Name</th>
                <td>:</td>
                <td>{{ user.name }}</td><hr><hr><hr><hr>
                
                <th>Email ID</th>
                <td>:</td>
                <td>{{ user.email }}</td>    
            </tr>
            
        </tbody>
    </table>
    <hr>
</div>
    <div id="tableContainer">
        <hr>
        <h1 style="text-align: center;">Bookings</h1>
        <hr>
        <table class="tableDisplay">
            <thead>
                <tr>
                    <th>Ticket ID</th>
                    <!-- <th>User ID <sub>remove this</sub></th> -->
                    <th>Show Name</th>
                    <th>Show Time</th>
                    <th>Date Time</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="ticket in filteredTicketData" :key="ticket.id">
                <td>T{{ ticket.id }}</td>
                <!-- <td>{{ ticket.user_id }}</td> -->
                <td>{{ getShowName(ticket.show_id) }}</td>
                <td>{{ getShowTime(ticket.show_id) }}</td>
                
                <td>{{ ticket.date_purchased }}</td>                    
                </tr>
            </tbody>
        </table>
        <hr>
    </div>
    <div class="footer">
        <Footer />
    </div>
</template>



<script>
export default {
  data() {
    return {
      searchQuery: "",
    };
  },
      methods: {
        redirecttoLogin() {
            this.$router.push('/login');
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
    margin: 15px 390px 70px;
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
    justify-content: flex-start;
    padding: 50px;
    
    background-color: white;
}

button {
  background-color: #55d6aa;
  color: black;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 13px;
  transition: 0.3s;
}

button:hover {
  background-color: #293f50;
  color: white;
  box-shadow: 0 0 5px #293f50;
}
</style>
