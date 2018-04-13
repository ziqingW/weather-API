var appid="&appid=9ecc560e5c99c8be650566914f4192e6";
 
$(document).ready(function(){
  
  $("#search").click(function(){
    var icon;
    var zip=$("#cityn").val();
    if(zip!=""){
    $.get("http://api.openweathermap.org/data/2.5/weather?q="+zip+",us"+appid,function(data){
    console.log(data);
      var cel=Math.round(data.main.temp-273);
      $("#city").html(data.name);
      $("#temp").html("<p>"+cel+"&#176C");
      $("#description").html(data.weather[0].description);
      icon=data.weather[0].icon;
      $("#icon").html("<img src='http://openweathermap.org/img/w/"+icon+".png' />");
    if(icon=="01d"){$("#module").css("background-image","url(http://t3.ftcdn.net/jpg/01/13/79/18/240_F_113791804_lENHPbB0yHLPpTzwT3tfqvOtowspaOhB.jpg)")
 }else if(icon=="02d"){$("#module").css("background-image","url(http://c1.staticflickr.com/3/2603/3698206578_d7df0d24f9_b.jpg)")
}else if(icon=="03d"||icon=="03n"){$("#module").css("background-image","url(http://i.ytimg.com/vi/z2UDZMu2GLU/maxresdefault.jpg)")
}else if(icon=="04d"||icon=="04n"){$("#module").css("background-image","url(https://2.bp.blogspot.com/-TYLTwLk6eHw/U_4M9__kQbI/AAAAAAAAAOk/p6F3pcjavkk/s1600/dramatic-clouds.jpg)")
}else if(icon=="09d"||icon=="09n"){$("#module").css("background-image","url(http://images.8tracks.com/cover/i/000/393/391/rainfall_wallpaper-wide-3780.jpg?rect=480,0,1600,1600&q=98&fm=jpg&fit=max&w=640&h=640)")
}else if(icon=="10d"||icon=="10n"){$("#module").css("background-image","url(https://s-media-cache-ak0.pinimg.com/originals/07/0d/1a/070d1ae9816c6139e54bf10138de3eb4.jpg)")
}else if(icon=="11d"||icon=="11n"){$("#module").css("background-image","url(http://www.homeadvisor.com/r/wp-content/uploads/2015/03/Dollarphotoclub_43826198-1024x680.jpg)")
 }else if(icon=="13d"||icon=="13n"){$("#module").css("background-image","url(http://media.idownloadblog.com/wp-content/uploads/2016/01/bokeh-snow-flare-water-white-splash-pattern-9-wallpaper.jpg)")
 }else if(icon=="50d"||icon=="50n"){$("#module").css("background-image","url(http://vignette1.wikia.nocookie.net/demigodshaven/images/f/f5/Mist.jpg/revision/latest?cb=20110102163040)")  
 }else if(icon=="02n"){$("#module").css("background-image","url(http://images.naldzgraphics.net/2012/10/16-cloudy-night-moon-wallpaper-cool.jpg)")  
 }else if(icon=="01n"){$("#module").css("background-image","url(http://snapshotsbykats.files.wordpress.com/2011/11/020.jpg)")  
 }
 });
}
    else{
      $("#city").html("<h3 class='notice'>Please input the city's name</h6>");
    }
});
});
 
   
