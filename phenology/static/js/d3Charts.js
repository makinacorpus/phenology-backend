phenoclim.viz.chart = function chart(params) {
  var options = {
      margin : {top: 20, right: 20, bottom: 20, left: 70},
      xValue : function(d) { return d[0]; },
      yValue : function(d) { return d[1]; },
      xScale : d3.scale.linear(),
      textLegend: false,
      yScale : d3.scale.linear(),
      max_width: 920,
      colors:  d3.scale.category10()
  };
  $.extend(true, options, params);
  options.xAxis = d3.svg.axis().orient("bottom").tickSize(6, 0);
  options.yAxis = d3.svg.axis().orient("left");

  function chart(selection) {
    chart.draw(selection);
  }

  chart.options = options;
  chart.tooltip = {}
  chart.draw = function(selection){
    selection.each(function(data) { 
        chart.options.xAxis.scale(chart.options.xScale);
        chart.options.yAxis.scale(chart.options.yScale);

        chart.tooltip.object = d3.select(this).selectAll(".tooltip").data([data])
        chart.tooltip.object.enter().append("div").attr("class", "tooltip")
            .style("opacity", 1e-6);

        chart.options.width = options.width || $(this).width();
        if (chart.options.width > options.max_width){
          chart.options.width = options.max_width;
        }
        var width = chart._width();
        var height = chart._height();
        chart.options.yScale.range([height, 0]);
        console.log(height);
        chart._xScale();
        var svg = d3.select(this).selectAll("svg").data([data]);

        var gEnter = svg.enter().append("svg").append("g")
        gEnter.append("g").attr("class", "x axis")
            .append("text")
              .attr("class", "legend")

        gEnter.append("g").attr("class", "y axis")
            .append("text")
              .attr("class", "legend")
        // Update the outer dimensions.
        svg .attr("width", width + chart.options.margin.left + chart.options.margin.right)
            .attr("height", height + chart.options.margin.bottom + chart.options.margin.top);

        // Update the inner dimensions.
        var g = svg.select("g")
            .attr("transform", "translate(" + chart.options.margin.left + "," + chart.options.margin.top + ")");

        // Update the x-axis.
        var xGraphAxis = g.select(".x.axis")
            .attr("transform", "translate(0," + (height) + ")")
            .call(options.xAxis);        

        var yGraphAxis = g.select(".y.axis")
            .call(chart.options.yAxis);

        xGraphAxis.selectAll("text.legend")
          .attr("transform", "translate(" + width +", -20)")
          .attr("y", 6)
          .attr("dy", ".71em")
          .style("text-anchor", "end");

        yGraphAxis.selectAll("text.legend")
          .attr("transform", "rotate(-90)")
          .attr("y", 6)
          .attr("dy", ".71em")
          .style("text-anchor", "end");
    });
  }
  
  chart.tooltip.hide = function() {
    chart.tooltip.object.transition()
        .style("opacity", 1e-6);
  }
  chart.tooltip.text = function(d){
    return "<b>"+d.value+"</b>";
  }
  chart.tooltip.show = function(d) {
    chart.tooltip.object.html(function(d2){ return  chart.tooltip.text(d)})
      .style("left", (d3.event.layerX - 34) + "px")
      .style("top", (d3.event.layerY - 40) + "px")
    chart.tooltip.object.transition()
      .style("opacity", 1);
 }

  chart._xScale = function(d){
      chart.options.xScale.range([0, chart._width()]);
  }

  chart._width = function(d){
    return chart.options.width - chart.options.margin.left - chart.options.margin.right;
  }

  chart._height = function(d){
    return (chart.options.width*3/5) - chart.options.margin.top - chart.options.margin.bottom;
  }

  chart.yScale = function(_) {
    if (!arguments.length) return chart.options.yScale;
    chart.options.yScale = _;
    return chart;
  };

  chart.xScale = function(_) {
    if (!arguments.length) return options.xScale;
    options.xScale = _;
    return chart;
  };

  chart.margin = function(_) {
    if (!arguments.length) return options.margin;
    options.margin = _;
    return chart;
  };

  chart.width = function(_) {
    if (!arguments.length) return options.width;
    options.width = _;
    return chart;
  };

  chart.height = function(_) {
    if (!arguments.length) return options.height;
    options.height = _;
    return chart;
  };


  return chart;
}

