import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'
<template>
    <div class="navbar">
        <Navbar />
    </div>
   <h1></h1>
    <div class="formContainer">
        <h1 style="text-align: center; color: white;">
  {{ successMessage ? successMessage : 'Sign Up' }}
  
</h1>
        <form @submit.prevent="submitForm">
            <div v-if="errors.length" class="error-messages">
                <p v-for="error in errors" :key="error">{{ error }}</p>
            </div>
            <div v-if="successMessage" class="success-message">
                {{ successMessage }}
            </div>

            <label for="name">Name:</label>
            <input v-model="name" type="text" id="name" required>

            <label for="email">Email:</label>
            <input v-model="email" type="email" id="email" required>

            <label for="password1">Password:</label>
            <input v-model="password1" type="password" id="password1" required>

            <label for="password2">Re-enter:</label>
            <input v-model="password2" type="password" id="password2" required>

            <button type="submit">Submit</button>
        </form>
    </div>
    <div class="footer">
        <Footer />
    </div>
</template>

<script>
export default {
    name: 'Signup',
    data() {
        return {
            name: '',
            email: '',
            password1: '',
            password2: '',
            errors: [],
            successMessage: ''
        }
    },
    methods: {
        submitForm() {
            const formData = {
                name: this.name,
                email: this.email,
                password1: this.password1,
                password2: this.password2
            }
            this.errors = [];
            if (this.name === '') {
                this.errors.push('Name required.');
            } else if (this.name.length < 3) {
                this.errors.push('Name must be at least 3 characters.');
            }
            if (this.email === '') {
                this.errors.push('Email required.');
            }
            if (this.email === '') {
                this.errors.push('Email required.');
            } else if (this.email.length < 6) {
                this.errors.push('Email must be at least 6 characters.');
            }
            if (this.password1 === '') {
                this.errors.push('Password required.');
            } else if (this.password1.length < 8) {
                this.errors.push('Password must be at least 8 characters.');
            }

            if (this.password2 === '') {
                this.errors.push('Confirm password required.');
            } else if (this.password2.length < 8) {
                this.errors.push('Passwords must match.');
            }
            if (this.password2 === '') {
                this.errors.push('Confirm password required.');
            }
            if (this.password1 !== this.password2) {
                this.errors.push('Passwords must match.');
            }
            if (this.errors.length === 0) {
                this.successMessage = 'Form submitted successfully.';
            }
            const requestOptions = {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            };
            fetch('http://localhost:8000/signup', requestOptions)
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                });

            this.$router.push('/login');
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