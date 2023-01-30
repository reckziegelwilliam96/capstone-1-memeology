
//Request function to API Meme Generator endpoint getImages, get list of image keywords stored in API
function getAPIImageList(){
    axios.get("/api/get-images-list")
        .then(response => handleList(response.data))

}

//Manipulate data to clean it, select random meme phrases and send data to be committed to db
function handleList(response){
    var phrases = response.split(',');
    var randomIndices = getRandomIndices(phrases.length, 20);

    var randomMemeNames = randomIndices.map(function(i) {
        return phrases[i];
    });

    axios.post('http://127.0.0.1:500/add-images-to-db', {
        data: randomMemeNames
    })
        .then(response => getAPImeme(response.data))

}

//Additional function for handleList, to select random indices from response list
function getRandomIndices(length, number) {
    var indices = [];
    while (indices.length < number) {
        var randomIndex = Math.floor(Math.random() * length);
            if (!indices.includes(randomIndex)) {
            indices.push(randomIndex);
            }
    }
    return indices;
}

//Request function to API Meme Generator endpoint, get MemeImage
function getAPIGenerateMeme(){
    axios.get("/api/get-generate-meme")
        .then(response => handleMeme(response.data))
}

function handleMeme(response)


$("#start-game").on("click", getAPIImageList)