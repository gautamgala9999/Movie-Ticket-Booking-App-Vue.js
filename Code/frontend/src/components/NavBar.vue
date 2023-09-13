<template>
    <header>
    <div class="container">

      <nav>
        <ul>
          <li><a @click="redirectToHome()">nJOY</a></li>
          <li><a @click="redirectToShows()">Shows</a></li>
          <li><a @click="redirectToVenues()">Venues</a></li>
          <li class="searchBar"><input v-model="searchQuery" placeholder="search show or venue" @keyup.enter="" /></li>
          <!-- search() put this in enter="" above -->
          <li v-if="!isLoggedIn"><a @click="redirectToLogin()">SignIn</a></li>
          <li v-if="!isLoggedIn"><a @click="redirectToSignup()">SignUp</a></li>
          <li v-if="isLoggedIn"><a @click="redirectToProfile()">Profile</a></li>
          <li v-if="isLoggedIn"><a @click="redirectToLogout()">Logout</a></li>
          
        </ul>
      </nav>
    </div>
  </header>
  <hr>
</template>


<script>
export default {
  data() {
    return {
      searchQuery: "",
    };
  },
  computed: {
    isLoggedIn() {
      const user = JSON.parse(localStorage.getItem('user'));
      return user !== null;
    },
  },
      methods: {
        redirectToLogin() {
            this.$router.push('/login');
        },
        redirectToSignup() {
            this.$router.push('/signup');
        },
        redirectToHome() {
            this.$router.push('/');
        },
        redirectToShows() {
            this.$router.push('/shows');
        },
        redirectToVenues() {
            this.$router.push('/venues');
        },
        search() {
          const trimmedQuery = this.searchQuery.trim();
          if (trimmedQuery) {
            this.$router.push(`/search?q=${encodeURIComponent(trimmedQuery)}`);
          }
        },
        redirectToLogout(){
          localStorage.removeItem('user');
            this.$router.push('/logout');
        },
        redirectToProfile(){
            this.$router.push('/profile');
        },
      },
   };
</script>

<style scoped>
body {
	margin: 0;
	background: black;
	font-family: 'Times New Roman', Times, serif;
	font-weight: 800;
  width: 100%;
  background: #55d6aa;
 
}
.searchBar {
  margin-left: 20px;
}

.searchBar input {
  border: none;
  border-radius: 4px;
  padding: 8px 12px;
  font-size: 14px;
  transition: box-shadow 0.3s, border-color 0.3s;
  background-color: #f5f5f5;
  width: 200px; 
}

.searchBar input:focus {
  outline: none;
  box-shadow: 0 0 5px black;
  border-color: black;
}

.container {
	width: 80%;
	margin: 0 auto;
  background: #55d6aa;

}

header {
  background: #55d6aa;
  width: 100%;

}

header::after {
  content: '';
  display: table;
  clear: both;
}

.logo {
  float: left;
  /* padding: 10px 0; */
}

nav {
  float: left;
  background: #55d6aa;

}

nav li {
  display: inline-block;
  margin-left: 100px;
  padding-top: 12px;
  padding-bottom: 12px;
  padding-left: 12px;
  padding-right: 1px;
  background: #55d6aa;

  position: relative;
}
nav ul {
  margin: 0;
  padding: 0;
  list-style: none;
  background: #55d6aa;

}


nav a {
  color: black;
  text-decoration: none;
  /* text-transform: uppercase; */
  font-size: 24px;
  background: #55d6aa;

}



nav a::before {
  content: '';
  display: block;
  height: 5px;
  background-color: #444;

  position: absolute;
  top: 0;
  width: 0%;

  transition: all ease-in-out 250ms;
}

nav a:hover::before {
  width: 100%;
}


</style>