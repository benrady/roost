describe("Roost", function() {
  describe('Home View', function() {
    var view;
    beforeEach(function() {
      var forecast = generateForecast("Tuesday");
      spyOn(window, 'currentConditionData').andReturn([{
        current_observation:{
          temp_f: '70.2',
          weather: 'Overcast'
        }
      }]);
      spyOn(window, 'forecastData').andReturn([{forecast: {simpleforecast: {forecastday: [
        generateForecast('Tuesday'), 
        generateForecast('Wednesday')
      ]}}}]);
      view = homeView();
    });
    
    it("should show the current conditions for today", function() {
      expect(view.find('.current-conditions h1')).toHaveText('Tuesday');
      expect(view.find('.current-conditions img')).toHaveAttr('src', 'http://icons-ak.wxug.com/i/c/k/partlycloudy.gif');
    });

    it('should show the forecast for the next three days', function() {
      expect(view.find('.forecast-list h4')).toHaveText('Wednesday');
    });
  });
});
