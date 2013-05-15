var appName = 'Roost';
var weatherData; // This should be a promise!

function homeView() {
  function addForecast(data) {
    _.each(data.forecast.simpleforecast.forecastday, function(day) {  
      forecast.append($('<li>').append(
        $('<div>').text(day.date.weekday),
        $('<img>').attr('src', day.icon_url).addClass('img-polaroid'),
        $('<div>').text("HI " + day.high.fahrenheit + " / LOW " + day.low.fahrenheit),
        $('<div>').text("Wind " + day.avewind.mph + " " + day.avewind.dir)));
    });
  }
  $.getJSON('http://api.wunderground.com/api/' + settings.wuKey + '/forecast/q/60630.json?callback=?', addForecast);
  //$.getJSON('/data/forecast.json', addForecast);

  var forecast = $('<ul>').addClass('inline forecast-list');
  var view = $('<div>').
    addClass('row-fluid').
    append(forecast);

  return view;
}

var routes = {
  home: homeView,
  history: function() { return bannerTemplate('This is the contact view')},
};

