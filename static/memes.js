
//Request function to API Meme Generator endpoint getImages, get list of image keywords stored in API
function getAPIImageList(){
    axios.get("/api/get-images-list")
        .then(response => handleList(response.data))

}

//Manipulate data to clean it, select random meme phrases and send data to be committed to db

function handleList(response){
   let phrases = response.toString().split(',')
   let randomIndices = getRandomIndices(phrases.length, 20);

   let randomImageNames = randomIndices.map(function(i) {
       return phrases[i];
   });

   axios.post('/api/post-meme-names-seed-db', randomImageNames, {
       headers: {
           'Content-Type': 'application/json'
       }
   }).then(response => {
       if (response.data.error) {
           console.log(response.data.error)
       } else {
           getAPIGenerateMeme(response.data)
       }
   })
}

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

//Request function to API Meme Generator endpoint, get MemeImage
function getAPIGenerateMeme(image){
    const options = {
        method: 'GET',
        url: 'https://ronreiter-meme-generator.p.rapidapi.com/meme',
        params: {
          top: '.',
          bottom: '.',
          meme: `${image}`,
          font_size: '1',
          font: 'Impact'
        },
        headers: {
          'X-RapidAPI-Key': '4107f9a719msh7b803084f28bdd6p10d9b2jsn4c84f0422879',
          'X-RapidAPI-Host': 'ronreiter-meme-generator.p.rapidapi.com'
        }
      };
      
    axios.request(options)
        .then(response => handleMeme(response.data))
        .catch(function (error) {
          console.error(error);
      });
    // axios.get("/api/get-generate-meme")
        // .then(response => handleMeme(response.data))
}

function handleMeme(response){
    $("#meme-results").append(response)
}


$("#start-game").on("click", getAPIImageList)