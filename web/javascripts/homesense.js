var homesenseData;

function chartOptions(range) {
  return {
    HtmlText: false,
    title: range,
    xaxis: {
      mode: 'time',
      timeMode: 'local',
      min: Date.past(range).getTime()
    },
    yaxis: {
      title: 'Temperature (F)',
      titleAngle: 90,
      autoscale: true
    }
  };
}

function drawChart(element, data, options) {
  return Flotr.draw(element, _.values(data), options);
}

function getLSON(url) {
  return $.get(url).then(function (data) {
    return _.map(data.trimRight().split("\n"), JSON.parse);
  });
}

function startMetrics(data) {
  $('#outsideTempCharts .temp-chart').each(function() {
    drawChart(this, {temp_f: data.weather}, chartOptions($(this).data().range));
  });

  $('#insideTempCharts .temp-chart').each(function() {
    drawChart(this, data.sensors, chartOptions($(this).data().range));
  });
}

function startHome(data) {
}

function processRawData(sensorData, weatherData) {
  var sources = {};
  _.each(sensorData, function(record) {
    sources[record.source] = sources[record.source] || [];
    var timestamp = record['timestamp'];
    sources[record.source].push([timestamp, record['temp_f']]);
  });
  tempData = _.map(weatherData, function(hour) {
    var timestamp = new Date(hour.local_time_rfc822).getTime();
    return [timestamp, hour.temp_f];
  });
  return {sensors: sources, weather: tempData};
}

function fetchData() {
  return $.when(getLSON('/data/temperature/yearly/2013.lson'),
                getLSON('/data/weather/yearly/2013.lson')).
           then(processRawData);
}

var views = {
  home: startHome,
  metrics: startMetrics
}

function showView(viewName, data) {
  viewName = viewName || 'home';
  $('section').hide();
  $('section#' + viewName).show();
  views[viewName](data);
}

$(document).ready(function(argument) {
  window.onhashchange = function (e) {
    showView(e.newURL.split('#')[1], homesenseData);
    return true;
  };

  $.when(fetchData()).done(function (data) {
    homesenseData = data;
    showView(window.location.hash.split('#')[1], data);
  });
});
