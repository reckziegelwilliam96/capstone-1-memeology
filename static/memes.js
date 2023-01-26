function processImagesList(){
    axios.get("/api/get-images-list")
        .then(response => handleListResponse(response.data))
        .catch(error => console.log(error))
}

function handleListResponse(response){
    console.log(response)
}

$("#start-game").on("click", procesImagesList)