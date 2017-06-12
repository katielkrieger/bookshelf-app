$(document).ready(function(){

  // D3 Code looks good!

  // add d3 vizualiation on user home page

  var height = 400;
  var padding = 80;
  var paddingTop = 20;
  var width = Math.min(window.innerWidth - 2*padding, 600);
  var svg = d3.select('svg')
                .attr('width', width)
                .attr('height', height);

  var tooltip = d3.select("body")
                    .append("div")
                    .attr("class", "tooltip");

  // get user_id
  var url = window.location.href;
  var user_id = url.split('users/')[1];

  d3.queue()
        .defer(d3.json, user_id + "/d3.json")
        .await(function(error, data) {
            if (error) console.log(error);

            // console.log(data);
            var xMin = d3.min(data.map(d => d.pages));
            var yMin = d3.min(data.map(d => d.rating));
            var xMax = d3.max(data.map(d => d.pages));
            var yMax = d3.max(data.map(d => d.rating));

            // console.log(xMax,yMax);

            var yScale = d3.scaleLinear()
                           .domain([0,10])
                           .range([height - padding, paddingTop]); // flipping y axis
            var xScale = d3.scaleLinear()
                           .domain([0,xMax])
                           .range([padding, width - padding]);

            var horizontalAxis = d3.axisBottom(xScale);
            var verticalAxis = d3.axisLeft(yScale);

            svg.append("g")
                .attr("transform", `translate(0,${height - padding})`)
                .style('font-family', 'Abril Fatface')
                .call(horizontalAxis);

            svg.append("g")
                .attr("transform", `translate(${padding}, 0)`)
                .style('font-family', 'Abril Fatface')
                .call(verticalAxis);


            svg.selectAll("circle")
              .data(data)
              .enter()
                .append('circle')
                .attr('cx', d => xScale(d.pages)) // pages
                .attr('cy', d => yScale(d.rating)) // rating
                .attr('r', d => 7) // fixed
                .attr('fill', "#8899BF") // fixed
                .attr('stroke', 'black')
                .on("mouseenter", function(d) {
                    tooltip.html(`<strong><span style='color:#8899BF'>${d.title}:</span></strong> ${d.rating} out of 10`)
                           .style('font-family', 'Abril Fatface')
                           .style("opacity", .9)
                           .style("left", d3.event.pageX+"px")
                           .style("top", d3.event.pageY+"px")
                })
                .on("mouseout", function() {
                    tooltip.style("opacity", 0)
                })
                .on("click", function(d) {
                  location.href = `/users/${user_id}/bookshelves/${d.bookshelf_id}`
                });

            svg.append("text")
              .attr("transform", "rotate(-90)")
              .attr("y", 0 + padding/6)
              .attr("x",0 - (height / 2))
              .attr("dy", "1em")
              .style("text-anchor", "middle")
              .style('font-family', 'Abril Fatface')
              .text("Rating");

            svg.append("text")
              // .attr("transform", "rotate(-90)")
              .attr("y", height - padding/2)
              .attr("x", width/2)
              .attr("dy", "1em")
              .style("text-anchor", "middle")
              .style('font-family', 'Abril Fatface')
              .text("Pages");

        });


});
