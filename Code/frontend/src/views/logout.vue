
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'


<script>
export default {
  data() {
    return {
      searchQuery: "",
    };
  },
      methods: {
        redirectToLogin() {
            this.$router.push('/login');
        },
        
      },
   };
</script>

<template>
    <div class="Navbar">
        <Navbar />
    </div>
    <br><br><br><br><br><br><br><br><br><br><hr>
    <h1 style="text-align: center;">Logout Successful <br>Visit Again! <br>More movies coming soon <br>
    <a @click="redirectToLogin()" style="color: blue;">Login</a>
    </h1>
    <hr>
    
    <div class="footer">
        <Footer />
    </div>
</template>

<style scoped>
*{
    box-sizing: border-box;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
}
body{
    font-family: Helvetica;
    -webkit-font-smoothing: antialiased;
}


/* Table Styles */

.tableContainer{
    margin: 10px 70px 70px;
    box-shadow: 0px 35px 50px rgba( 0, 0, 0, 0.2 );
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
  font-size: 13px;
  transition: 0.3s;
}

button:hover {
  background-color: #293f50;
  color: white;
  box-shadow: 0 0 5px #293f50;
}
</style>

