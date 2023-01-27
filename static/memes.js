function processImagesList(){
    axios.get("/api/get-images-list")
        .then(response => handleListResponse(response.data))
}

// function redirectToGamePage(){
//     window.location.href = '/render-game'
// }

function handleListResponse(response){
    console.log(response)
    let filteredResponse = extractWords(response);
    $("#meme-results").html(filteredResponse);
}

function extractWords(response) {
    let words = response.map(item => item.name);
    let splitWords = [];
    
    words.forEach(function(word) {
      word = word.replace(/'/g, ""); // remove apostrophes
      let wordArray = word.split("-"); // split phrase by dash
      splitWords.push(wordArray);
    });
  
    return splitWords;

    // let allWords = []
    // response.data.forEach(function(image){
    //     let words =  image.word.replace(/'/g, "").split("-");
    //     allWords.push(words);
    // });
    // return allWords;
}

$("#start-game").on("click", processImagesList)