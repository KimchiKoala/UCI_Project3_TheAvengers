const searchForm = document.querySelector('.search');
        const input = document.querySelector('.input');
        

        searchForm.addEventListener('submit', retrieve)

        function retrieve(e) {
            
            const newsList = document.querySelector('.news-list');    

            //show 'error' message box when input field is empty 
            if (input.value == ''){
                alert('Input field is empty')
                return
            }

            input.value = input.value.toUpperCase();

            //clears the previous search results
            newsList.innerHTML ='';

            e.preventDefault();

            const apiKey = '96b47c522f00a29fe1b11cfd2b0b02d9'; 

            let ticker = input.value;

            let url ='https://financialmodelingprep.com/api/v3/stock_news?tickers='+ ticker + '&limit=5&apikey=' + apiKey;
            

            fetch(url).then((res) => {
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

            }).catch((error)=>{
                console.log(error);
           })

            console.log(ticker)

        }
