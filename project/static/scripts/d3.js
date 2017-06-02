$(document).ready(function(){


  // add d3 vizualiation on user home page

  var height = 400;
  var padding = 30; 
  var width = 600; // giving it room to breathe
  var svg = d3.select('svg')
                .attr('width', width)
                .attr('height', height);

  var tooltip = d3.select("body")
                    .append("div")
                    .attr("class", "tooltip");

  d3.queue()
    // window.location.href --> url, parse to get user_id
    // make request to users/<user_id>/json
        .defer(d3.json, "d3.json")
        .await(function(error, data) {
            if (error) console.log(error);

            // console.log(data);
            var xMin = d3.min(data.map(d => d.pages));
            var yMin = d3.min(data.map(d => d.rating));
            var xMax = d3.max(data.map(d => d.pages));
            var yMax = d3.max(data.map(d => d.rating));

            // console.log(xMax,yMax);

            var yScale = d3.scaleLinear()
                           .domain([yMin,yMax])
                           .range([height - padding, padding]); // flipping y axis
            var xScale = d3.scaleLinear()
                           .domain([xMin,xMax]) 
                           .range([padding, width - padding]);

            var horizontalAxis = d3.axisBottom(xScale);
            var verticalAxis = d3.axisLeft(yScale);

            svg.append("g")
                .attr("transform", `translate(0,${height - padding})`)
                .style('font-family', '"Source Sans Pro",Calibri,Candara,Arial,sans-serif')
                .call(horizontalAxis);

            svg.append("g")
                .attr("transform", `translate(${padding}, 0)`) // Y shift was -padding
                .style('font-family', '"Source Sans Pro",Calibri,Candara,Arial,sans-serif')
                .call(verticalAxis);


            svg.selectAll("circle")
              .data(data)
              .enter()
                .append('circle')
                .attr('cx', d => xScale(d.pages)) // pages
                .attr('cy', d => yScale(d.rating)) // rating
                .attr('r', d => 7) // fixed
                .attr('fill', "green") // fixed
                .attr('stroke', 'black')
                .on("mouseenter", function(d) {
                    tooltip.html(`Rating: ${d[0]} out of 10`)
                           .style("opacity", .9)
                           .style("left", d3.event.pageX)
                           .style("top", d3.event.pageY)
                })
                .on("mouseout", function() {
                    tooltip.style("opacity", 0)
                });

        });


});







