// URL url = new URL("https://financialmodelingprep.com/api/v3/stock_news?tickers=AAPL,FB,GOOG,AMZN&apikey=96b47c522f00a29fe1b11cfd2b0b02d9");

// try (BufferedReader reader = new BufferedReader(new InputStreamReader(url.openStream(), "UTF-8"))) {
//     for (String line; (line = reader.readLine()) != null;) {
//     System.out.println(line);
//   }
// }


var api = 'https://financialmodelingprep.com/api/v3/stock_news?tickers=';
// var ticker = 'AAPL';
var apikey = '&apikey=96b47c522f00a29fe1b11cfd2b0b02d9';

var input;


function setup(){
  // createCanvase(600,400)  
  var button =select('#search');
    button.mousePressed(callNews);

    input = select('#ticker');
}

function callNews(){
  var url = api + input.value() +apikey;
  loadJSON(url, gotData); 

}

function gotData(data){
  println(data);
}