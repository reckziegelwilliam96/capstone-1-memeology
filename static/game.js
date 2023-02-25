class MemeoGame{
    constructor(boardId, imageSrc){
        
        this.board = $("#" + boardId);
        this.round = 0;
        this.result = '';
        this.imageSrc = imageSrc;
        this.addImage(this.imageSrc);
        this.addTiles(this.round);
        this.showRound(this.round, this.result);

        $(".add-keyword", this.board).on("submit", this.handleSubmit.bind(this));

    }


    showMessage(message, result, round, phrase=null){
        const container = $('.msg', this.board)
        container.empty()

        if (round < 5 && result === "not-correct"){
            const msg = $('<p>').text(message);
            container.addClass('error');
            container.append(msg);
        } else if (result === "game-over") {
          const msg = $('<p>').text(message);
          container.addClass('danger');
          container.append(msg);
          if (phrase !== null && phrase !== "") {
              const phraseMsg = $('<p>').text(`The phrase was: ${phrase}`);
              container.append(phraseMsg);
        } else {
            const msg = $('<p>').text(message);
            container.addClass('success');
            container.append(msg);
        }
    }
    }
    addImage(src) {
        const container = $(".image-container", this.board);
        const image = $("<img>").attr("src", src);
        container.empty()
        container.append(image);
    }

    showRound(round, result) {
        const container = $(".score-container");
        const letters = [$("#letter-1"), $("#letter-2"), $("#letter-3"), $("#letter-4"), $("#letter-5")];
    
        for (let i = 0; i < letters.length; i++) {
            const letter = letters[i];
            if (i === round - 1) {
                if (result === "correct") {
                  letter.addClass("green");
                } else if (result === "not-correct") {
                  letter.addClass("red");
                }
                container.append(letter);
        }
      }
    }

    addTiles(round) {
        const numRows = 4;
        const numCols = 4;
        const container = $(".tiles-container", this.board);
        container.empty();
      
        let numVisibleTiles = 1;
        for (let i = 1; i <= round; i++) {
          numVisibleTiles += (i * 2) - 1;
        }
      
        // Generate shuffled list of tile indices
        const tileIndices = [...Array(numCols * numRows).keys()];
        shuffle(tileIndices);
      
        // Assign visibility status based on shuffled list
        for (let i = 0; i < numRows; i++) {
          for (let j = 0; j < numCols; j++) {
            const tile = $("<div>").addClass("tile");
            const tileIndex = i * numCols + j;
            if (tileIndices.indexOf(tileIndex) < numVisibleTiles) {
              tile.addClass("visible");
            } else {
              tile.addClass("hidden");
            }
            container.append(tile);
          }
        }
      }
      

    async handleSubmit(evt){
        evt.preventDefault();
        const inputField = $('.keyword');
        const keyword = inputField.val();
        inputField.val('');

        const response = await axios.get('/update-game-meme', { params: { keyword: keyword }});
        const result = response.data.result;
        const message = response.data.message;

        if (result === "not-correct") {
            this.round++;
            this.showRound(this.round, result);
            this.addTiles(this.round);
            this.showMessage(message, result, this.round);
            this.addImage(this.imageSrc);
        } else if (result === "game-over") {
            const message = response.data.message;
            const phrase = response.data.phrase;
            this.showRound(this.round, result);
            this.showMessage(message, result, this.round, phrase);
            setTimeout(() => {
              window.location.href = '/game-over';
            }, 5000);
        } else {
          const phrase = response.data.phrase;
            this.showRound(this.round, result);
            this.showMessage(message, result, this.round, phrase);
            setTimeout(() => {
              window.location.href = '/game-over';
            }, 5000);
        }
    };

}

function shuffle(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}