describe("Roost", function() {
  describe('Home View', function() {
    var view;
    beforeEach(function() {
      var forecast = {
        "date":{
          "epoch":"1368586800",
          "pretty":"10:00 PM CDT on May 14, 2013",
          "day":14,
          "month":5,
          "year":2013,
          "yday":133,
          "hour":22,
          "min":"00",
          "sec":0,
          "isdst":"1",
          "monthname":"May",
          "weekday_short":"Tue",
          "weekday":"Tuesday",
          "ampm":"PM",
          "tz_short":"CDT",
          "tz_long":"America/Chicago"
        },
      "period":1,
      "high": {
        "fahrenheit":"91",
        "celsius":"33"
      },
      "low": {
        "fahrenheit":"68",
        "celsius":"20"
      },
      "conditions":"Partly Cloudy",
      "icon":"partlycloudy",
      "icon_url":"http://icons-ak.wxug.com/i/c/k/partlycloudy.gif",
      "skyicon":"mostlysunny",
      "pop":0,
      "qpf_allday": {
        "in": 0.00,
        "mm": 0.0
      },
      "qpf_day": {
        "in": 0.00,
        "mm": 0.0
      },
      "qpf_night": {
        "in": 0.00,
        "mm": 0.0
      },
      "snow_allday": {
        "in": 0,
        "cm": 0
      },
      "snow_day": {
        "in": 0,
        "cm": 0
      },
      "snow_night": {
        "in": 0,
        "cm": 0
      },
      "maxwind": {
        "mph": 13,
        "kph": 21,
        "dir": "SSW",
        "degrees": 199
      },
      "avewind": {
        "mph": 11,
        "kph": 18,
        "dir": "SW",
        "degrees": 215
      },
      "avehumidity": 43,
      "maxhumidity": 55,
      "minhumidity": 28
      };
      spyOn(window, 'currentConditionData').andReturn([{
        current_observation:{
          temp_f: '70.2',
          weather: 'Overcast'
        }
      }]);
      spyOn(window, 'forecastData').andReturn([{forecast: {simpleforecast: {forecastday: [forecast]}}}]);
      view = homeView();
    });
    
    it("should show the current conditions for today", function() {
      expect(view.find('.current-conditions h3')).toHaveText('Tuesday');
      expect(view.find('.current-conditions img')).toHaveAttr('src', 'http://icons-ak.wxug.com/i/c/k/partlycloudy.gif');
    });

    it('should show the forecast for the next three days', function() {
      expect(view.find('.current-conditions h3')).toHaveText('Tuesday');
    });
  });
});
