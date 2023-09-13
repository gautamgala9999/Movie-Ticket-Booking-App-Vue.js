<template>
    <div>
        <button @click="downloadCSV" class="center-container">Download Shows CSV</button>
    </div>
</template>

<script>
export default {
    methods: {
        async downloadCSV() {
            try {
                const response = await fetch('http://localhost:8000/csv_shows');
                if (response.ok) {
                    const blob = await response.blob();
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'shows.csv';
                    a.style.display = 'none';
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    URL.revokeObjectURL(url);
                } else {
                    console.error('Failed to fetch CSV data.');
                }
            } catch (error) {
                console.error('An error occurred:', error);
            }
        },
    },
};
</script>
<style>
.center-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: max-content; 
  width:max-content;
}
button {
  background-color: #55d6aa;
  color: black;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 30px;
  transition: 0.3s;
  font-family: 'Times New Roman', Times, serif;

}

button:hover {
  background-color: #293f50;
  color: white;
  box-shadow: 0 0 5px #293f50;
}
</style>