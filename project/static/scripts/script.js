$(document).ready(function(){


  // add event listener for search button
  var $search = $(".search");
  var array = [];

  $search.on("click", function(event){
    console.log("clicked");

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
      throw err;
    }).then(function(response){
      console.log(response);

        var $holder = $(".holder")

        // remove old list, if applicable
        var $oldBooks = $(".book");
        $oldBooks.remove();


        var objEach0 = {
          title: null,
          author: null,
          categories: null,
          snippet: null,
          description: null,
          pages: null,
          image_url: null,
          preview_url: null,
          date_published: null
        };
        var objEach1 = {
          title: null,
          author: null,
          categories: null,
          snippet: null,
          description: null,
          pages: null,
          image_url: null,
          preview_url: null,
          date_published: null
        };
        var objEach2 = {
          title: null,
          author: null,
          categories: null,
          snippet: null,
          description: null,
          pages: null,
          image_url: null,
          preview_url: null,
          date_published: null
        };
        var objEach3 = {
          title: null,
          author: null,
          categories: null,
          snippet: null,
          description: null,
          pages: null,
          image_url: null,
          preview_url: null,
          date_published: null
        };
        var objEach4 = {
          title: null,
          author: null,
          categories: null,
          snippet: null,
          description: null,
          pages: null,
          image_url: null,
          preview_url: null,
          date_published: null
        };
        var objEach5 = {
          title: null,
          author: null,
          categories: null,
          snippet: null,
          description: null,
          pages: null,
          image_url: null,
          preview_url: null,
          date_published: null
        };
        var objEach6 = {
          title: null,
          author: null,
          categories: null,
          snippet: null,
          description: null,
          pages: null,
          image_url: null,
          preview_url: null,
          date_published: null
        };
        var objEach7 = {
          title: null,
          author: null,
          categories: null,
          snippet: null,
          description: null,
          pages: null,
          image_url: null,
          preview_url: null,
          date_published: null
        };
        var objEach8 = {
          title: null,
          author: null,
          categories: null,
          snippet: null,
          description: null,
          pages: null,
          image_url: null,
          preview_url: null,
          date_published: null
        };
        var objEach9 = {
          title: null,
          author: null,
          categories: null,
          snippet: null,
          description: null,
          pages: null,
          image_url: null,
          preview_url: null,
          date_published: null
        };
        array = [
          objEach0,
          objEach1,
          objEach2,
          objEach3,
          objEach4,
          objEach5,
          objEach6,
          objEach7,
          objEach8,
          objEach9,
        ];
        if(response !== undefined){
          for (var i=0; i<Math.min(response.items.length, 10); i++) {

            // populate object with response info
            if (response.items[i].volumeInfo) {
              array[i].title = response.items[i].volumeInfo.title || "None found";
              array[i].author = response.items[i].volumeInfo.authors || "None found";
              array[i].categories = response.items[i].volumeInfo.categories || "None found";
              array[i].description = response.items[i].volumeInfo.description || "None found";
              array[i].pages = response.items[i].volumeInfo.pageCount || "None found";
              if (response.items[i].volumeInfo.imageLinks) {
                array[i].image_url = response.items[i].volumeInfo.imageLinks.thumbnail || "None found";
              } else {
                array[i].image_url = "None found";
              }
              array[i].preview_url = response.items[i].volumeInfo.previewLink || "None found";
              array[i].date_published = response.items[i].volumeInfo.publishedDate || "None found"; 
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
              array[i].snippet = response.items[i].searchInfo.snippet || "None found";
            } else {
              array[i].snippet = "None found";
            }
            
            // make a div with class="row book" inside of holder
            var $newDiv = $("<div>");
            $newDiv.addClass("row book")
                   .attr("data-info","" + i + "")
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
            $thumb.attr("src", array[i].image_url);
            $cover.append($thumb);

            var $title = $("<div>")
            $title.text(array[i].title + " by " + array[i].author)
              .addClass("newBook")
              .css("font-size", "2.5rem")
              .css("font-weight", "bold");
            $list.append($title)

            var $description = $("<div>");
            $description.text(array[i].description)
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

  // add event listener for selection of one of the books

  $(".holder").on("click", "img", function(event){
      console.log("book selected!!");

      var i = parseInt($(event.target).parent().parent().attr('data-info'));

      // var $title = $('input[name=title]');
      var $title = $('#title');
      var $author = $('#author');
      var $categories = $('#categories');
      var $snippet = $('#snippet');
      var $description = $('#description');
      var $pages = $('#pages');
      var $image_url = $('#image_url');
      var $preview_url = $('#date_published');
      var $date_published = $('#date_published');

      console.log("title");

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
      $pages.val(array[i].pageCount);
      $image_url.val(array[i].thumbnail);
      $preview_url.val(array[i].previewLink);
      $date_published.val(array[i].publishedDate);

      console.log("Updated")

  });



});