$("#restart-btn").ready(function(){
    captionImages();
})

async function captionImages(){
    try {
        const response = await axios.post('/api/caption-images');
        const data = response.data;
        const meme = handleList(data);
        console.log(meme); // do something with the meme object
      } catch (error) {
        console.log(error);
      }
}