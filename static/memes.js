function getAPIImageList(){
    axios.get("/api/get-images-list")
        .then(response => parseList(response.data))
}


function parseList(response){
    
    var phrases = response.split(',');
    var randomIndices = getRandomIndices(phrases.length, 20);

    var randomImages = randomIndices.map(function(i) {
        return phrases[i];
    });

    axios.post('http://127.0.0.1:500/add-images-to-db', {
        data: randomImages
    })
        .then(response => getAPImeme(response.data))

}

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


$("#start-game").on("click", processImagesList)