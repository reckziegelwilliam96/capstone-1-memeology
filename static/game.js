class MemeoGame{
    constructor(boardId){
        this.round = 0;
        this.board = $("#" + boardId);
        
        this.addTiles(this.round);

        $(".add-keyword", this.board).on("submit", this.handleSubmit.bind(this));

    }

    showRound(){
        $(".round", this.board).text(this.round)
    }

    addTiles(round){
        const container = $(".image-container");
        container.empty();
        let numTiles = (round + 1) * round / 2 + 1;
        const remainingTiles = 16 - numTiles;
        const visibleTiles = numTiles - remainingTiles;
        for (let i = 0; i < visibleTiles; i++){
            const tile = $("<div>").addClass("tile visible");
            container.append(tile);
        }
        for (let i = 0; i < remainingTiles; i++){
            const tile = $("<div>").addClass("tile hidden");
            container.append(tile);
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
        const msgElement = $('<p>').text(message);
        if (result === "not-correct") {
            msgElement.addClass('error');
            this.round++;
            this.addTiles(this.round);
            this.showRound()
        }
        $('.msg').append(msgElement);
        
    };

}