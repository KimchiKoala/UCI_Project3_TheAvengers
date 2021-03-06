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
  
  function buildPlot(stock) {
    var api_key = "96b47c522f00a29fe1b11cfd2b0b02d9";

    var url = `https://financialmodelingprep.com/api/v3/historical-price-full/${stock}?apikey=${api_key}`;

    d3.json(url).then(function(data) {
      // console.log(url)

      var name = data.symbol;

      var dates = data.historical.map(row => row['date']);
      // console.log(dates);
      var closingPrices = data.historical.map(row => row['close']);
      // console.log(closingPrices);

      var startDate = dates[dates.length - 1];
      // console.log(startDate);
      var endDate = dates[0];

      // console.log(endDate);
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

      Plotly.newPlot("plot", data, layout);
    });
  }
  
  // Add event listener for submit button
  d3.select("#submit").on("click", handleSubmit);
  