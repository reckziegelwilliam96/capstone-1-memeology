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


    showMessage(message, result, round){
        const container = $('.msg', this.board)
        container.empty()

        if (round < 6 && result === "not-correct"){
            const msg = $('<p>').text(message);
            container.addClass('error');
            container.append(msg);
        } else if (result === "game-over") {
            const msg = $('<p>').text(message);
            container.addClass('danger');
            container.append(msg);
        } else {
            const msg = $('<p>').text(message);
            container.addClass('success');
            container.append(msg);
        }
    }

    addImage(src) {
        const container = $(".image-container", this.board);
        const image = $("<img>").attr("src", src);
        container.empty()
        container.append(image);
    }

    showRound(round, result) {
        const roundElem = $(".round", this.board);
        const letters = ["M", "E", "M", "E", "O"];
      
        roundElem.empty();
        for (let i = 0; i < letters.length; i++) {
          const letter = $("<span>").text(letters[i]);
          if (round === 0) {
            letter.addClass("black");
          } else if (result === "correct" && i === round) {
            letter.addClass("green");
          } else if (result === "not-correct" && i === round) {
            letter.addClass("red");
          } else {
            letter.addClass("black");
          }
          roundElem.append(letter);
        }
      }

    addTiles(round) {
        const numRows = 4;
        const numCols = 4;

        const container = $(".tiles-container", this.board);
        container.empty();
      
        let numVisibleTiles = round === 0 ? 0 : 1; // adjust numVisibleTiles for round 0
        for (let i = 1; i <= round; i++) {
          numVisibleTiles += (i * 2) - 1;
        }
      
        for (let i = 0; i < numRows; i++) {
          for (let j = 0; j < numCols; j++) {
            const tile = $("<div>").addClass("tile");
            if (i * numCols + j < numVisibleTiles || round === 0 && i === 0 && j === 0) {
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

        const response = await axios.get('/compare-word-to-db', { params: { keyword: keyword }});
        const result = response.data.result;
        const message = response.data.message;

        if (result === "not-correct") {
            this.round++;
            this.showRound(this.round, result);
            this.addTiles(this.round);
            this.showMessage(message, result, this.round);
            this.addImage(this.imageSrc);
        }
        this.showRound(this.round, result);
        this.showMessage(message, result, this.round);
        
    };

}