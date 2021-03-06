// Submit Button handler
function handleSubmit() {
    // Prevent the page from refreshing
    d3.event.preventDefault();
    // Select the input value from the form
    var stock = d3.select("#stockInput").node().value;
    console.log(stock);
    // clear the input value
    d3.select("#stockInput").node().value = "";
    // Build the plot with the new stock
    buildPlot(stock);
  }
  function mlPlot(stock) {
    var url = `API endpoint here`;
    fetch(url)
    d3.json(url).then(function(data) {
      var name = data.symbol;
      var dates = data.historical.map(row => row['date']);
      var closingPrices = data.prediction.map(row => row['close']);
    //   var predictionPrice = data.prediction.map(row => row['prediction']);
      var startDate = dates[dates.length - 1];
      var endDate = dates[0];
      // plot the actual closing prices
      var trace1 = {
        type: "scatter",
        mode: "lines",
        name: name,
        x: dates,
        y: closingPrices,
        line: {
          color: "#17BECF"
        }
      };
      // plot the predicted prices
      var trace2 = {
          type: "scatter",
          mode: "lines",
          name: name,
          x: dates,
          y: predictionPrice,
          line: {
              color: "#f08080"
          }
      };
    //   var data = [trace1, trace2];
    var data = [trace1];
      var layout = {
        title: `${stock} Closing Prices`,
        xaxis: {
          range: [startDate, endDate],
          type: "date"
        },
        yaxis: {
          autorange: true,
          type: "linear"
        }
      };
      Plotly.newPlot("plot2", data, layout);
    });
  }
  // Add event listener for submit button
  d3.select("#submit").on("click", handleSubmit);