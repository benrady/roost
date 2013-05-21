var appName = 'Roost';

function homeView() {
  function addForecast(data) {
    forecast.empty();
    _.each(data.forecast.simpleforecast.forecastday, function(day) {  
      forecast.append($('<div>').addClass('span3 small-text').append(
        $('<h4>').text(day.date.weekday),
        $('<img>').
          attr('src', day.icon_url).
          attr('title', day.conditions).
          addClass('img-polaroid text-wrap'),
        $('<div>').append(
          $('<div>').text(day.high.fahrenheit + '° / ' + day.low.fahrenheit + '°'),
          $('<div>').text(day.avehumidity + '% H'),
          $('<div>').text(day.avewind.mph + "mph " + day.avewind.dir))));
    });
  }

  function fetchForecast() {
    if (window.location.hostname === 'localhost') {
      $.getJSON('/data/forecast.json', addForecast);
    } else {
      $.getJSON('http://api.wunderground.com/api/' + settings.wuKey + '/forecast/q/60630.json?callback=?', addForecast);
    }
  }

  var forecast = $('<div>').addClass('forecast-list');

  var interval = setInterval(fetchForecast, 1000 * 60 * 60);
  fetchForecast();

  var view = $('<div>').
    addClass('row-fluid').
    append(forecast);
  view.bind('Roost.viewClose', function() { clearInterval(interval); })
  return view;
}

var routes = {
  home: homeView,
  history: function() { return bannerTemplate('This is the contact view')},
};
