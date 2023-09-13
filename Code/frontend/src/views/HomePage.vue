
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'

<template>
    <div class="Navbar">
        <Navbar />
    </div>
    <div>
        <div class="heading">
            <div class="wrapper four">
        <div class="type">
            <h3 class="typing">It's Show Time !</h3>
        </div>
    </div>
    </div>
    <div class="buttondiv">
        <button class="buttoncss" @click="redirectToShows()">
            Shows
        </button>
        <button class="buttoncss" 
        @click="redirectToVenues()">
            Venues
        </button>
    </div>
    </div>
    <div class="footer">
        <Footer />
    </div>
</template>


<script>
export default {
      methods: {
        redirectToShows() {
            this.$router.push('/shows');
         },
        redirectToVenues() {
            this.$router.push('/venues');
         },
      },
   };
</script>

<style scoped>
        @import url('https://fonts.googleapis.com/css2?family=Play&display=swap');
*{
    background-color: 324960;
}
        h1{
    padding: 3%;
}
button {
  background-color: #55d6aa;
  color: white;
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
  /* background: radial-gradient(100% 100% at 50% 50%, black 0%, rgb(96, 162, 140) 100%); */
}
.heading{
    width: 100%;
    height: 40%;
    background-color: aqua;
}
.wrapper.four {
    background-color: black;
    font-size: 3rem;
    font-family: "Play", sans-serif;
}
.four .type{
    padding: 2rem 1rem;
    width: auto;
    margin: auto;
}
.four h3 {
    width: 13ch;
    border-right: 4px solid rgb(255, 255, 255);
    margin: 2rem auto;
    white-space: nowrap;
    overflow: hidden;
    animation: typing 2s steps(10, end), blink-caret 0.5s step-end infinite alternate;
    color: white;
}
@-webkit-keyframes typing {
    from {
        width: 0;
    }
}
@-webkit-keyframes blink-caret {
    50% {
        border-color: transparent;
    }
}

.buttondiv{
    display: flex;
    margin: 2%;
}

.buttoncss{
    margin: 2%;
    width: 50%;
    height: 100%;
    color: black;
    padding-top: 10%;
    padding-bottom: 10%;
    background-color: white;
    border-radius: 1%;
    background: radial-gradient( 100% 100% at 50% 50%, rgb(96, 162, 140) 0%, black 100% );
    border-color: rgb(161, 215, 193);
    font-size: xx-large;
    font-weight: 700;
    font-family: 'Times New Roman', Times, serif;
}


                
</style>