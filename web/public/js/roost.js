var appName = 'Roost';

function currentConditionData() {
  // FIXME Cache this in localStorage?
  if (window.location.hostname === 'localhost') {
    return $.getJSON('/data/conditions.json');
  } else {
    return $.getJSON('http://api.wunderground.com/api/' + settings.wuKey + '/conditions/q/60630.json?callback=?');
  }
}

function forecastData() {
  // FIXME Cache this in localStorage?
  if (window.location.hostname === 'localhost') {
    return $.getJSON('/data/forecast.json');
  } else {
    return $.getJSON('http://api.wunderground.com/api/' + settings.wuKey + '/forecast/q/60630.json?callback=?');
  }
}

function homeView() {
  function addWeatherData(forecastReq, conditionReq) {  
    var forecast = forecastReq[0].forecast.simpleforecast.forecastday;
    addCurrentConditions(forecast[0], conditionReq[0]);
    addForecast(forecast.slice(1));
  }

  function addCurrentConditions(day, conditionData) {
    conditions.empty();
    conditions.append($('<div>').addClass('span12').append(
      $('<h3>').text(day.date.weekday),
      $('<img>').
        attr('src', day.icon_url).
        attr('title', day.conditions).
        addClass('img-polaroid text-wrap'),
      $('<div>').append(
        $('<div>').text(day.high.fahrenheit + '° / ' + day.low.fahrenheit + '°'),
        $('<div>').text(day.avehumidity + '% H'),
        $('<div>').text(day.avewind.mph + "mph " + day.avewind.dir))));
  }

  function addForecast(forecastDays) {
    forecast.empty();
    _.each(forecastDays, function(day) {  
      forecast.append($('<div>').addClass('span4 small-text').append(
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
    $.when(forecastData(), currentConditionData()).then(addWeatherData) 
  }

  var conditions = $('<div>').addClass('current-conditions');
  var forecast = $('<div>').addClass('forecast-list');

  var interval = setInterval(fetchForecast, 1000 * 60 * 60);
  fetchForecast();

  var view = $('<div>').
    addClass('row-fluid').
    append(conditions, forecast);
  view.bind('Roost.viewClose', function() { clearInterval(interval); })
  return view;
}

var routes = {
  home: homeView,
  history: function() { return bannerTemplate('This is the contact view')}
}
