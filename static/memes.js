$("#load-btn").ready(function(){
    getMemes();
})

async function getMemes() {
    try {
      const response = await axios.get('/api/get-memes');
      const data = response.data;
      const meme = handleList(data);
      console.log(meme); // do something with the meme object
    } catch (error) {
      console.log(error);
    }
  }

const handleList = (data) => {
  const memes = data.data.memes;
  const randomMemes = [];

  for (let i = 0; i < 100; i++) {
    const randomIndex = Math.floor(Math.random() * memes.length);
    randomMemes.push({ name: memes[randomIndex].name, url: memes[randomIndex].url });
    memes.splice(randomIndex, 1); // remove the selected meme from the array
  }

  axios.post('/api/save-memes', { memes: randomMemes })
    .then(response => console.log(response.data))
    .catch(error => console.log(error));

  return randomMemes;
};

//*************************************************************************************//



