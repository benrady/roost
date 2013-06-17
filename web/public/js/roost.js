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
    addCurrentConditions(forecast[0], conditionReq[0].current_observation);
    addForecast(forecast.slice(1));
  }

  function statusRow(label, value) {
    return $('<div>').text(label + ": " + value);
  }

  function addCurrentConditions(day, conditionData) {
    conditions.empty();
    conditions.append($('<div>').addClass('span12').append(
      $('<h1>').text(day.date.weekday),
      $('<img>').
        attr('src', day.icon_url).
        attr('title', day.conditions).
        addClass('img-polaroid text-wrap'),
      $('<div>').addClass('text-wrap fixed-height').append(
        $('<div>').addClass('big-text').text(Math.round(+conditionData.temp_f) + '°'),
        $('<div>').addClass('small-text').text(conditionData.weather)),
      $('<div>').append(
        statusRow('High',day.high.fahrenheit + '° /  Low: ' + day.low.fahrenheit + '°'),
        statusRow('Humidity', day.avehumidity + "%"),
        statusRow('Wind', day.avewind.mph + "mph " + day.avewind.dir))));
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

  function updateZones(zoneData) {  
    zoneList.empty();
    _.each(zoneData.zones, function(data, zone) {  
      zoneList.append($('<div>').addClass('span6 text-center well').append(
        $('<h2>').text(data.name),
        $('<span>').addClass('big-text').text(Math.round(data.tempF) + '°')
      ));
    });
  }

  function refreshData() {
    $.when(forecastData(), currentConditionData()).then(addWeatherData) 
    $.getJSON('/services/env_sensors/properties', updateZones);
  }

  var conditions = $('<div>').addClass('current-conditions row-fluid bottom-margin');
  var forecast = $('<div>').addClass('forecast-list row-fluid');
  var zoneList = $('<div>').addClass('zone-list row-fluid top-margin');

  var interval = setInterval(refreshData, 1000 * 60 * 60);
  refreshData();

  var view = $('<div>').
    append(conditions, forecast, zoneList);
  view.bind('Roost.viewClose', function() { clearInterval(interval); })
  return view;
}

var routes = {
  home: homeView,
  history: function() { return bannerTemplate('This is the contact view')}
}
