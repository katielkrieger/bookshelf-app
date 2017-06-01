$(document).ready(function(){

  // initiliaze carousel
  $('.carousel').slick({
    "arrows": true,
    "dots": true,
    "infinite": false
  });


  // add event listener for search button
  var $search = $(".search");
  var array = [];

  $search.on("click", function(event){
    // console.log("clicked");

    var searchTitle = $('#searchTitle').val();
    var searchAuthor = $('#searchAuthor').val();
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
      // throw err;
    }).then(function(response){
      // console.log(response);
      // show click instructions
      $click = $(".click");
      $click.css("visibility","visible");

        var $holder = $(".holder")

        // remove old list, if applicable
        var $oldBooks = $(".book");
        $oldBooks.remove();
        array = [{},{},{},{},{},{},{},{},{},{},];

        if(response !== undefined){
          for (var i=0; i<Math.min(response.items.length, 10); i++) {

            // populate object with response info
            if (response.items[i].volumeInfo) {
              array[i].title = response.items[i].volumeInfo.title || "None found";
              array[i].author = response.items[i].volumeInfo.authors || "None found";
              array[i].categories = response.items[i].volumeInfo.categories || "None found";
              array[i].description = response.items[i].volumeInfo.description || "None found";
              array[i].pages = response.items[i].volumeInfo.pageCount || "None found";
              array[i].preview_url = response.items[i].volumeInfo.previewLink || "None found";
              array[i].date_published = response.items[i].volumeInfo.publishedDate || "None found"; 
              if (response.items[i].volumeInfo.imageLinks) {
                array[i].image_url = response.items[i].volumeInfo.imageLinks.thumbnail || "None found";
              } else {
                array[i].image_url = "None found";
              }
            } else {
              array[i].title = "None found";
              array[i].author = "None found";
              array[i].categories = "None found";
              array[i].description = "None found";
              array[i].pages = "None found";
              array[i].image_url = "None found";
              array[i].preview_url = "None found";
              array[i].date_published = "None found";
            }
            if (response.items[i].searchInfo) {
              array[i].snippet = response.items[i].searchInfo.textSnippet || "None found";
            } else {
              array[i].snippet = "None found";
            }
            
            // make a div with class="row book" inside of holder
            var $newDiv = $("<div>");
            $newDiv.addClass("row book")
                   .attr("data-info","" + i + "")
                   .css("margin-bottom", "3rem");
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
            $thumb.attr("src", array[i].image_url)
                  .css("width","100%");
            $cover.append($thumb);

            var $title = $("<h4>")
            $title.text(array[i].title + " by " + array[i].author)
              .addClass("newBook")
            $list.append($title)

            var $description = $("<div>");
            $description.text(array[i].description)
              .addClass("description")
              .css("font-size", "1.65rem")
              .css("font-weight", "normal")
              .css("margin-top", "1rem");
            $list.append($description);

          }
        } else {
          $holder.text("No results found. Please modify your search and try again.");
        }
    });

    // ajax call to NYT for review

    var urlNYT = "https://api.nytimes.com/svc/books/v3/reviews.json";
    urlNYT += '?' + $.param({
      'api-key': "3baa47a8549145ffb79ca653ab42a969",
      'title': searchTitle,
      'author': searchAuthor
    });
    $.ajax({
      url: urlNYT,
      method: 'GET',
    }).done(function(result) {
      console.log(result);
    }).fail(function(err) {
      throw err;
    }).then(function(response){
      var nyt_review_url = response.results[0].url;

    });  

  });

  // add event listener for selection of one of the books

  $(".holder").on("click", ".cover, .list", function(event){


      $target = $(event.target);
      if ($target.hasClass("cover") || $target.hasClass("list")) {
        $selectedBook = $(event.target).parent();
      } else {
        $selectedBook = $(event.target).parent().parent();
      }

      var i = parseInt($selectedBook.attr('data-info'));

      // var $title = $('input[name=title]');
      var $title = $('#title');
      var $author = $('#author');
      var $categories = $('#categories');
      var $snippet = $('#snippet');
      var $description = $('#description');
      var $pages = $('#pages');
      var $image_url = $('#image_url');
      var $preview_url = $('#preview_url');
      var $date_published = $('#date_published');
      var $nyt_review_url = $('#nyt_review_url');

      $title.val(array[i].title);
      // $title.val(array[i].title);
      if(array[i].author.length === 0) {
          $author.val(array[i].author);
        } else {
          $author.val(array[i].author[0]);
        }
      if (array[i].categories.length === 0) {
        $categories.val(array[i].categories);
      } else {
        $categories.val(array[i].categories[0]);
      }
      $snippet.val(array[i].snippet);
      $description.val(array[i].description);
      $pages.val(array[i].pages);
      $image_url.val(array[i].image_url);
      $preview_url.val(array[i].preview_url);
      $date_published.val(array[i].date_published);
      $nyt_review_url.val(nyt_review_url);

      // show form-hidden
      $hiddenForm = $(".form-hidden");
      $hiddenForm.css("display","block")
                 .appendTo($selectedBook);

      // unstyle any other books
      $otherBooks = $(".book");
      $otherBooks.css("borderStyle", "hidden")
                 .css("borderWidth", "0rem")
                 .css("padding-top","0rem")
                 .css("padding-bottom","0rem");

      // style book selected
      $selectedBook.css("borderStyle","solid")
                   .css("borderWidth",".5rem")
                   .css("borderRadius","3rem")
                   .css("padding-top","1rem")
                   .css("padding-bottom","1rem");


  });


  // add an event listener to mark a book as read or email recommendation

  $markRead = $(".btn-info");
  $hiddenForm = $(".row-hidden");
  $hiddenForm.slideUp(0);
  $active = $(".active");

  $markRead.on("click", function(event){

    $hiddenForm.css("visibility","visible")
               .slideToggle();

    $active.focus();


  });



});