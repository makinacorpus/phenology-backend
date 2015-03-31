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

 phenoclim.viz.minMaxChart = function(params) {
 
    var chart = phenoclim.viz.chart(params)
    var parentDraw = chart.draw;
    var currentYear = moment().year();

    var line = d3.svg.line()
      .x(function(d) {
        return chart.options.xScale(parseInt(d.year)) + (chart.options.xScale.rangeBand()/2) ;})
      .y(function(d) {
        return chart.options.yScale(moment(d.date).year(currentYear))})

    chart._xScale = function(d){
        chart.xScale().rangeBands([0, chart._width()]);
    }
    
    chart.draw = function(selection){
      selection.each(function(data) {
        data = data || [];
        chart.options.colors.domain(data.map(function(d){
          return d.key;
        }))
        var dates = [];
        var years = [];
        $.each(data, function(i, item){
          var tmp = item.values.map(function(d){ 
            var date1 = new Date(d.date);
            if(years.indexOf(d.year) == -1){
              years.push(d.year);
            }
            date1.setFullYear(currentYear);
            return date1
          });
          dates = dates.concat(tmp);
        });
        years.sort();
        var minDate = d3.min(dates);
        var maxDate = d3.max(dates);

        chart.options.yScale.domain([minDate, maxDate]);
        chart.options.xScale.domain(years);
        chart.options.yAxis = chart.options.yAxis.ticks(5).tickFormat(function(d){
          var date = moment(d);
          if(date.date() === 1){
            return date.format("MMMM");
          }
          else{
            return date.format("D MMM");
          }
        })

        parentDraw(d3.select(this));

        d3.select(this).select(".x.axis text.legend")
          .text("Year")
        d3.select(this).select(".y.axis text.legend")
          .text("Date")

        var svg = d3.select(this).select("svg g")

          var group = svg.selectAll("g.values").data(data)
          group.exit().remove();
          var gEnter = group.enter()
               .append("g")
               .attr("class", "values");
          
          gEnter.append("path")
              .style('stroke-width', 1)
              .style("stroke-opacity", 0.7)
              .attr("class", "line");

          gEnter.append("text")
              .attr("class", "legend");

          var dots = group.selectAll(".dot").data(function(d){
            d.values.sort(function(a,b){
              return d3.ascending(+a.year, +b.year);
            })
            return d.values.map(function(d2){
              d2.type = d.key;
              return d2;
            });
          })

          dots.enter()
            .append("circle")
            .attr("class", "dot")
            .attr("r", 3.5)
            .style("fill-opacity", 0.8)
            .on('mousemove', function(d){
              d3.select(this).attr("r", 7);
              chart.tooltip.show(d);
            })
            .on('mouseout', function(d){
              chart.tooltip.hide();
              d3.select(this).attr("r", 3.5);
            })

          dots.exit()
              .remove()

          group.selectAll(".dot")
            .transition()
            .duration(150)
            .attr("cx", function(d){
               return chart.options.xScale(parseInt(d.year)) + (chart.options.xScale.rangeBand()/2);
            })
            .attr("cy", function(d){
               var date1 = new Date(d.date);
               date1.setFullYear(currentYear);
               return chart.options.yScale(date1);
            })
            .attr("fill", function(d){
              return chart.options.colors(d.type);
            })
          group.select(".line")
            .transition()
            .duration(150)
            .attr("d", function(d){
              var v = line(d.values) || "M0,0";
              return v;
            })
            .style("stroke", function(d){
              return chart.options.colors(d.key);
            })
          if(chart.options.textLegend){
          group.select(".legend")
            .attr("transform", "translate(10)")
            .transition()
            .duration(150)
            .text(function(d){
              return d.label;
            })
            .attr("x", function(d){
              var last = d.values[d.values.length-1];
              if(last)
                return chart.options.xScale(last.year) + (chart.options.xScale.rangeBand()/2)
              else
                return 0
            })
           .attr("y", function(d){
              var last = d.values[d.values.length-1];
              if(last)
                return chart.options.yScale(last.date);
              else
               { 
                example = chart;
                return chart._height();
                }
            })
          }
      })
    }
    chart.tooltip.text = function(d){
      return moment(d.date).year(d.year).format("ddd DD MMMM YYYY");
    }
    chart.options.xScale = d3.scale.ordinal();
    chart.options.yScale = d3.time.scale();
    return chart;
  }

 phenoclim.viz.areaChart = function(params) {
 
    var chart = phenoclim.viz.minMaxChart(params)
    var parentDraw = chart.draw;
    var currentYear = moment().year();

    chart.options.yAxis.tickFormat(function(d){
      return moment(d).format("DD/MM")
    }).ticks(4)

    return chart;
}

phenoclim.viz.SnowingChart2 = function(params){

    var options = {
      margin: {top: 20, right: 30, bottom: 30, left: 30},
    }
    $.extend(true, options, params);

    var chart = phenoclim.viz.chart(options)
    chart._height = function(d){
      return (chart.options.width*2/5) - chart.options.margin.top - chart.options.margin.bottom;
    }
    var parentDraw = chart.draw;
    chart.draw = function(selection){
      selection.each(function(data) {

        chart.options.xScale.domain([data.minDate, data.maxDate]);
        var maxHeight = d3.max(data.values, function(d){
          return +d.height;
        })
        chart.options.yScale.domain([0, data.maxHeight + 10])

        parentDraw(d3.select(this));

        var height = chart._height();
        var fulldates = []; // Array of day of year
        var tmpDate = moment(data.minDate);
        while(tmpDate <= data.maxDate){
          fulldates.push(tmpDate.format("DDD"));
          tmpDate.add(1, "days");
        }
        chart.options.x2.rangeBands([0, chart._width()]).domain(fulldates);
        d3.select(this).selectAll(".x.axis .tick text").attr("transform", "translate(" + chart.options.x2.rangeBand()*15 +", 0)")
        d3.select(this).select("svg g").selectAll(".bar").remove()
        var rect = d3.select(this).select("svg g").selectAll(".bar")
                      .data(data.values)
                      .enter()
                      .append("rect")
                      .attr("class", "bar")
                      .attr("width", chart.options.x2.rangeBand()+1)
                      .attr("x", function(d){ return chart.options.x2(d.date.format("DDD")); })
                      .attr("y", function(d) { return chart.options.yScale(0); })
                      .attr("height", function(d) { return 0; })
                      .on('mousemove', function(d){
                          chart.tooltip.show(d);
                        })
                        .on('mouseout', function(d){
                          chart.tooltip.hide();
                        })
      rect.transition()
          .duration(200)
          .delay(function(d, i) { return i*2; })
          .attr("y", function(d) { return chart.options.yScale(+d.height); })
          .attr("height", function(d) { return height - chart.options.yScale(+d.height); });
      })
    }
    
    chart.options.x2 =  d3.scale.ordinal();
    chart.options.xScale = d3.time.scale();
    chart.options.yScale = d3.scale.linear();
    chart.options.xAxis.tickFormat(function(d){
      return moment(d).format("MMMM");
    });
    chart.tooltip.text = function(d){
      return d.date.format("D MMM YYYY") + " <br/><b>"+d.height+"cm</b><br/>";
    }
    return chart;
}