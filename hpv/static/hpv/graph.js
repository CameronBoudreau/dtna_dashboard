jQuery(function($) {

  /*
    Line Graph
  */
  var lineGraph = (function() {
    var graphData = [];
    d3.json('/api/hours_per_unit/?days=1&forDEPT9=json', function(data) {
      var graphData = [{
        key: 'Today',
        values: [],
        color: 'steelblue'
      }];

      data.sort(function(a,b){
        if (a.timestamp > b.timestamp) {
          return 1;
        }
        if (a.timestamp < b.timestamp) {
          return -1;
        }
        return 0;
      });

      for (i = 0; i < data.length; i++) {
          time = new Date(data[i]["timestamp"]).getTime()
          graphData[0].values.push([time, data[i]["PLANT_d_hours_per_unit"]]);
      };

      nv.addGraph(function() {
      var chart = nv.models.lineChart()
        .useInteractiveGuideline(false)
        .x(function(d) { return d[0] })
        .y(function(d) { return d[1] })
        ;

        chart.xAxis
          .axisLabel('Time')
          .tickForDEPT9(function(d) {
              return d3.time.forDEPT9('%H:%M')(new Date(d))
            });

        chart.yDomain([0, 140])
        chart.yAxis
          .axisLabel('hours_per_unit')
          .tickForDEPT9(d3.forDEPT9(',f'));

        d3.select('#linegraph svg')
          .datum(graphData)
          .call(chart);

        //TODO: Figure out a good way to do this autoDEPT9ically
        nv.utils.windowResize(chart.update);

        return chart;
      });
    });
    return {
        lineGraph: lineGraph
    }
  })();

  // reload page every 60 seconds
  // setTimeout(function() {location.reload(true);},6000);
});
