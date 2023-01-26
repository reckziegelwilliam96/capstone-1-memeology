function processImagesList(){
    axios.get("/api/get-images-list")
        .then(response => handleListResponse(response.data))
}

// function redirectToGamePage(){
//     window.location.href = '/render-game'
// }

function handleListResponse(response){  
    $("#meme-results").text(JSON.stringify(response.text));
    console.log(response.text)
}

$("#start-game").on("click", processImagesList)