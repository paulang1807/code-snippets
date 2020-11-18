// load this data set from an external location
d3.json(
    "https://gist.githubusercontent.com/andyreagan/d32b101903b1246aa8c418abd8e6520b/raw/a918dbe038fb82d987d5e73eae3cefa349447950/gapminder.json",
    function(error, data) {
      
    //   console.log(data);
      // convert the data from an object into a list
      var datalist = [];
      for (var key in data) {
        //   console.log(key, data[key].lifeExp.length);
        // make sure the data is defined for all of the countries
        if (data[key].lifeExp[data[key].lifeExp.length-1] & data[key].gdp[data[key].gdp.length-1]) {
          datalist.push(data[key]);
          datalist[datalist.length-1]["country"] = key;
        }
      }
    // console.log(datalist);
    // peek at the most recent GDP data for each country
    // console.log(datalist.map(function(d) { return d.gdp[d.gdp.length-1]; }).sort(d3.ascending));
    // The d3.extent function is used to get the min and the max of the values returned by the map array 
      var gdp_range = d3.extent(datalist.map(function(d) { return d.gdp[d.gdp.length-1]; }).sort(d3.ascending));
      var lifeExp_range = d3.extent(datalist.map(function(d) { return d.lifeExp[d.lifeExp.length-1]; }).sort(d3.ascending));
      
      //function to return different symbols based on continent
      var contSymbol = function(contName) {
        switch (contName) {
          case "North America":
            return d3.symbolCross;
          case "Sub-Saharan Africa":
            return d3.symbolDiamond;
          case "Asia":
            return d3.symbolSquare;
          case "Europe":
            return d3.symbolStar;
          case "Central America and the Caribbean":
            return d3.symbolTriangle;
          case "South America":
            return d3.symbolWye;
          case "Oceania":
            return d3.symbolCross;
          default:
            return d3.symbolCircle;
        }
      }
      
      // create svg element
      var svg = d3.select("svg");
  
      // border rectangle
      svg
        .append("rect")
        .attr("width", 240)
        .attr("height", 240)
        .attr("x", 5)
        .attr("y", 5);
  
      // add each data point to the svg
      // through the select->enter->append idiom
      svg
        .selectAll("path.pt") // this is an empty selection
        .data(datalist) // the selection is still empty, but the enter selection contains the number elements in data. (the exit selection is empty).
        .enter() // our selection now contains just the *new* data elements, and since our initial selection was empty, this is everything in var data
        .append("path") // append a path to each element
        .attr("class", "pt") // give attributes to each element
        .attr("d", d3.symbol().type(function(d){
          return contSymbol(d.continent);
        }).size(function(d){
            return Math.floor(d.pop[d.pop.length-1]/1000000);
        }))
        .style("fill", function(d) {
            popVal = Math.floor(d.pop[d.pop.length-1]/1000000);
            r = popVal > 255 ? 255: popVal;
            return "rgb(" + r+ ", 51, 51)";
        })
        .attr("transform", function(d) {
          // console.log(d)
          // uncomment the previous to see the data element that gets passed into each of these callbacks
          var rotate = "";
          if (d.continent == "Oceania"){
            rotate = " rotate(45)"
          };
          return "translate(" + 
            (10 + (d.gdp[d.gdp.length-1] - gdp_range[0])/(gdp_range[1]-gdp_range[0])*225) + 
            "," + 
            (240 - (d.lifeExp[d.lifeExp.length-1] - lifeExp_range[0])/(lifeExp_range[1]-lifeExp_range[0])*225) + 
            ")" +
            rotate;
        })
        ;
  
      // tip: define a function callback for the "d" attribute (line 28)
      // use d3.symbol.size(), and d.pop[0]
      // see https://github.com/d3/d3-shape#symbols
    }
  );
  