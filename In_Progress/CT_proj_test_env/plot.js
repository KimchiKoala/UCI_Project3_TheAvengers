// /**
//  * Helper function to select stock data
//  * Returns an array of values
//  * @param {array} rows
//  * @param {integer} index
//  * index 0 - Date
//  * index 1 - Open
//  * index 2 - High
//  * index 3 - Low
//  * index 4 - Close
//  * index 5 - Volume
//  */

// Submit Button handler
function handleSubmit() {
    // Prevent the page from refreshing
    d3.event.preventDefault();
  
    // Select the input value from the form
    var stock = d3.select("#stockInput").node().value;
    console.log(stock);

    stock = stock.toUpperCase()
  
    // clear the input value
    d3.select("#stockInput").node().value = "";
  
    // Build the plot with the new stock
    buildPlot(stock);

  }
  
  function buildPlot(stock) {
    var apiKey = "ouscx_8Py41g3a53MjCR";
  
    var url = `https://www.quandl.com/api/v3/datasets/WIKI/${stock}.json?start_date=2016-10-01&end_date=2017-10-01&api_key=${apiKey}`;
  
    d3.json(url).then(function(data) {
      // Grab values from the response json object to build the plots
      var name = data.dataset.name;
      var stock = data.dataset.dataset_code;
      var startDate = data.dataset.start_date;
      var endDate = data.dataset.end_date;
      // Print the names of the columns
      console.log(data.dataset.column_names);
      // Print the data for each day
      console.log(data.dataset.data);
      var dates = data.dataset.data.map(row => row[0]);
      // console.log(dates);
      var closingPrices = data.dataset.data.map(row => row[4]);
      // console.log(closingPrices);
  
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
        title: `${stock} closing prices`,
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

    // News code below: 

    const newsList = document.querySelector('.news-list');    

    //show 'error' message box when input field is empty 
    if (stock == ''){
        alert('Input field is empty')
        return
    }

    //clears the previous search results
    newsList.innerHTML ='';

    const apiKey2 = '96b47c522f00a29fe1b11cfd2b0b02d9'; 

    let url2 ='https://financialmodelingprep.com/api/v3/stock_news?tickers='+ stock + '&limit=5&apikey=' + apiKey2;
    

    fetch(url2).then((res) => {
        return res.json();
    
    }).then((data) => {
        console.log(data);
        
        data.forEach(data =>{
            let li=document.createElement('li');
            let a = document.createElement('a');
            a.setAttribute('href', data.url);
            a.setAttribute('target','_blank'); //opens another tab
            a.textContent = data.title;
            li.appendChild(a);
            newsList.appendChild(li);
        })
  });

}

  
  // Add event listener for submit button
  d3.select("#submit").on("click", handleSubmit);