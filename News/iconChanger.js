//We create the function
//Note: This function is user defined (Call it any thing you want).
function IconChanger(){
    
    //initialize the icon - the first search icon to be displayed.
    let icon = document.getElementById("icons");
    icon.innerHTML = "search";
    
    
    //Here we change the icon
    //Set the time out limit - how long its takes before switching to another icon
    setTimeout(function(){
        icon.innerHTML = "public";
    },2000);
    
  
  
  //Time out limit here is 4s  / (s) seconds
   setTimeout(function(){
        icon.innerHTML = "person_pin";
    },4000);

  }
  
  
  
  //Here we call the function to run
  IconChanger();
  
  
  
  //This will continue to loop throught the setTimeout functions.
  //It will always run after every 6s / (s) seconds.
  //Note: it is set depending on the seconds you gave to the setTimeout functions.
  setInterval(IconChanger,6000);