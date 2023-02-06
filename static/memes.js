$(document).ready(function(){
    getAPIImageList();
})

//Request function to API Meme Generator endpoint getImages, get list of image keywords stored in API
function getAPIImageList(){
    axios.get("/api/get-images-list")
        .then(response => handleList(response.data))

}

//Manipulate data to clean it, select random meme phrases and send data to be committed to db

function handleList(response){
   let phrases = response.toString().split(',')
   let randomIndices = getRandomIndices(phrases.length, 1);

   let randomImageNames = randomIndices.map(function(i) {
       return phrases[i];
   });

   axios.post('/api/post-meme-names-seed-db', randomImageNames, {
       headers: {
           'Content-Type': 'application/json'
       }
   }).then(response => {
       console.log(response.data.error)
});

//Additional function for handleList, to select random indices from response list
function getRandomIndices(length, number) {
    let indices = [];
    while (indices.length < number) {
        let randomIndex = Math.floor(Math.random() * length);
            if (!indices.includes(randomIndex)) {
            indices.push(randomIndex);
            }
    }
    return indices;
}

/*************************************************************************************************************/
$("#start-game").on("click", getAPIGenerateMeme)

//Request function to API Meme Generator endpoint, get MemeImage
function getAPIGenerateMeme() {
    axios.get('/api/get-generate-meme', {
        responseType: 'blob'
    })
        .then(response => handleMeme(response.data))
  }
  
  function handleMeme(response) {
    const blob = new Blob([response], {
      type: 'image/jpeg'
    });
    const objectURL = URL.createObjectURL(blob);
    const image = new Image();
    image.src = objectURL;
    $("#meme-results").append(image);
  }
}
/*************************************************************************************************************/
