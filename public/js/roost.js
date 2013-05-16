var appName = 'Roost';
var weatherData; // This should be a promise!

function homeView() {
  function addForecast(data) {
    _.each(data.forecast.simpleforecast.forecastday, function(day) {  
      forecast.append($('<div>').addClass('span3').append(
        $('<h3>').text(day.date.weekday),
        $('<img>').
          attr('src', day.icon_url).
          attr('title', day.conditions).
          addClass('img-polaroid text-wrap'),
        $('<div>').append(
          $('<div>').text(day.high.fahrenheit + '° / ' + day.low.fahrenheit + '°'),
          $('<div>').text(day.avehumidity + '% Humidity'),
          $('<div>').text(day.avewind.mph + "mph " + day.avewind.dir))));
    });
  }
  $.getJSON('http://api.wunderground.com/api/' + settings.wuKey + '/forecast/q/60630.json?callback=?', addForecast);
  //$.getJSON('/data/forecast.json', addForecast);

  var forecast = $('<div>').addClass('forecast-list');
  var view = $('<div>').
    addClass('row-fluid').
    append(forecast);

  return view;
}

var routes = {
  home: homeView,
  history: function() { return bannerTemplate('This is the contact view')},
};

