$(document).ready(function(){

  var $buttons = $(".search");

  $buttons.on("click", function(event){
    console.log("clicked");

    var searchTitle = $('#title').val();
    var searchAuthor = $('#author').val();
    var url;
    var apiKey = "AIzaSyCRABm57Bz_UqCnYI850ZUqOjFmkf5rotg";

    // GET https://www.googleapis.com/books/v1/volumes?q=flowers+inauthor:keyes&key=yourAPIKey

    if (searchAuthor && searchTitle) {
      url = `https://www.googleapis.com/books/v1/volumes?q=${searchTitle}+inauthor:${searchAuthor}&key=${apiKey}`;
    } else if (searchTitle) {
      url = `https://www.googleapis.com/books/v1/volumes?q=${searchTitle}&key=${apiKey}`;
    } else if (searchAuthor) {
      url = `https://www.googleapis.com/books/v1/volumes?inauthor:${searchAuthor}&key=${apiKey}`;
    }

    $.ajax({
      url: url,
      method: 'GET',
    }).done(function(result) {
    }).fail(function(err) {
      console.log(err);
      throw err;
    }).then(function(response){
      console.log(response);

        var $holder = $(".holder")

        // remove old list, if applicable
        var $oldBooks = $(".book");
        $oldBooks.remove();

        if(response !== undefined){
          for (var i=0; i<Math.min(response.items.length, 10); i++) {

            // make a div with class="row book" inside of holder
            var $newDiv = $("<div>");
            $newDiv.addClass("row book")
                   .css("margin-bottom", "2rem");
            $holder.append($newDiv);

            // make a div with class="col-xs-2 cover" inside of newDiv
            var $cover = $("<div>");
            $cover.addClass("col-xs-2 cover");
            $newDiv.append($cover);

            // make a div with class="col-xs-10 list" inside of newDiv
            var $list = $("<div>");
            $list.addClass("col-xs-10 list");
            $newDiv.append($list);

            var $thumb = $("<img>");
            $thumb.attr("src", response.items[i].volumeInfo.imageLinks.thumbnail);
            $cover.append($thumb);

            var $title = $("<div>")
            $title.text(response.items[i].volumeInfo.title + " by " + response.items[i].volumeInfo.authors[0])
              .addClass("newBook")
              .css("font-size", "2.5rem")
              .css("font-weight", "bold");
            $list.append($title)

            var $description = $("<div>");
            $description.text(response.items[i].volumeInfo.description)
              .addClass("description")
              .css("font-size", "2rem")
              .css("font-weight", "normal")
              .css("margin", "2rem");
            $title.append($description);

          }
        } else {
          $holder.text("No results found. Please modify your search and try again.");
        }
    });

  });

});