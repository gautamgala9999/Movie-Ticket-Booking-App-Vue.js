import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'
<template>
    <div class="navbar">
        <Navbar />
    </div>
    <h1></h1>
    <div class="formContainer">
        <h1  style="text-align: center; color: white;">
      Log In
    </h1>
        <form @submit.prevent="submitForm">
            <label for="email">Email:</label>
            <input v-model="email" type="email" id="email" required>

            <label for="password">Password:</label>
            <input v-model="password" type="password" id="password" required>

            <button type="submit">Submit</button>

        </form>
    </div>
    <div class="footer">
        <Footer />
    </div>
</template>

<script>
export default {
    name: 'login',
    data() {
        return {
            email: '',
            password: '',
        }
    },
    methods: {
        submitForm() {
            const formData = {
                email: this.email,
                password: this.password,
            }
            const requestOptions = {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            };
            fetch('http://localhost:8000/login', requestOptions)
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    formData['id']=data.user_id;
                    formData['name']=data.user_name;
                    formData['role']=data.role;
                    formData['token']=data.token;
                    if (!data.error){
                        localStorage.setItem('user', JSON.stringify(formData));
                        this.$router.push('/');
                    }
                    else{
                        alert(data.error);
                    }
                });
        }
    }
}
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
input{
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