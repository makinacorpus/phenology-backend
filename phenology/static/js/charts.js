var cached_surveys = {};
phenoclim = phenoclim || {}
phenoclim.session = phenoclim.session || {};
phenoclim.viz = {};

phenoclim.viz.getFirstDayOfWeek = function(week, year){
  firstDay = new Date(year, 0, 1).getDay();
  var d = new Date("Jan 01, "+year+" 01:00:00");
  var w = d.getTime() -(3600000*24*(firstDay-1))+ 604800000 * (week-1)
  var n1 = new Date(w);
  return n1;
}

phenoclim.viz.getLasttDayOfWeek = function(week, year){
  firstDay = new Date(year, 0, 1).getDay();
  var d = new Date("Jan 01, "+year+" 01:00:00");
  var w = d.getTime() -(3600000*24*(firstDay-1))+ 604800000 * (week)
  var n1 = new Date(w);
  return n1;
}

phenoclim.viz.load_data = function(){
  return $.get("/portail/get_data_for_viz", function(data){
    phenoclim.session.dataviz = data;
  });
}

phenoclim.viz.refreshStages = function(){
  var species_field_value = $("select[data-id=species]").val();
  var stages_field = $("select[data-id=stages]");
  var cache_stage_value = stages_field.val();

  var species = phenoclim.session.species_list.filter(function(d){
    return d.id == species_field_value;
  });

  if (species.length > 0){
    species = species[0];
  }

  $("option", stages_field).remove();

  $.each(species.stages, function(i, item){
    var option = $("<option>").attr("value", item.id).text(item.label);
    if(cache_stage_value === item.id){
      option.attr("selected", "selected");
    }
    option.appendTo(stages_field);
  });
}

phenoclim.viz.refreshYears = function(){
  var data = phenoclim.session.dataviz || [];
  var all_years = [];
  var species_id = +$("select[data-id=species]").val();
  var stage_id = +$("select[data-id=stages]").val();
  var years = data[species_id][stage_id];
  $.each(years, function(year, Yeardata){
    if(all_years.indexOf(+year) === -1){
      all_years.push(+year);
    }
  });
  all_years.sort();
  $yearContainer = $("[data-id=years]");
  $yearContainer.children().remove();
  $.each(all_years, function(i, year){
    var $input = $("  <div class='checkbox'><label><input type='checkbox' name='years' value='"+ year +"'>" + year + "</label></div>").appendTo($yearContainer);
    if(i > (all_years.length - 3)){
      $("input", $input).attr("checked", "checked");
    }
  });
  $(".checkbox input").change(function(event){
    phenoclim.session.linechart.refresh();
    phenoclim.session.barchart.refresh();
    phenoclim.session.timebarchart.refresh();
  });
}

phenoclim.viz.getSpecies = function(){
  return $.get("/portail/get_species_list", function(data){
    var species_field = $("select[data-id=species]");
    $("option", species_field).remove();
    data = data.sort(function(a, b){
      if ( a.label < b.label ){
        return -1;
      }
      if ( a.label > b.label )
        return 1;
      return 0; });
    $.each(data, function(i, item){
      var option = $("<option>").attr("value", item.id).text(item.label);
      option.appendTo(species_field);
    });
    $("option[value='5']", species_field).attr("selected", "selected");
    phenoclim.session.species_list = data;
    phenoclim.viz.refreshStages();
  })
};

phenoclim.viz.lineChart = function(params){
  var self = this;

  var options = {
    selector: ".graph",
    margin: {top: 20, right: 10, bottom: 30, left: 80},
    line_enable: true
  }
  $.extend(true, options, params);

  var container = d3.select(options.selector);
  var main_width = options.width || $(options.selector).width();
  var width = main_width - options.margin.left - options.margin.right;
  var height = (main_width*3/5) - options.margin.top - options.margin.bottom;

  var tooltip = container.append("div")
    .attr("class", "tooltip")
    .style("opacity", 1e-6);

  var x = d3.scale.ordinal()
    .rangeBands([0, width])
    .domain(d3.range(53));

  var y = d3.scale.linear()
    .range([height, 0]);

  //var xtime =  d3.scale.ordinal().rangePoints([0, width]).domain(d3.range(13));
  var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]

  var today = new Date()
  var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom")
    .tickFormat(function(d, i){
      var day = phenoclim.viz.getFirstDayOfWeek(d+1, today.getFullYear());
      return day.getDate() + "/" + (day.getMonth()+1)
    });

  var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .tickFormat(d3.format("d"));

  var svg = container.append("svg")
    .attr("width", width + options.margin.left + options.margin.right)
    .attr("height", height + options.margin.top + options.margin.bottom)
    .append("g")
      .attr("transform", "translate(" + options.margin.left + "," + options.margin.top + ")");

  var line = d3.svg.line()
    .x(function(d) { return x(+d.key) + x.rangeBand(); })
    .y(function(d) { return y(+d.value); });

  var xGraphAxis = svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .attr("class", "x axis");

  xGraphAxis.append("text")
    .attr("transform", "translate(" + width +", -20)")
    .attr("y", 6)
    .attr("dy", ".71em")
    .style("text-anchor", "end")
    .text("Date");

  var yGraphAxis = svg.append("g")
    .attr("class", "y axis");

  yGraphAxis.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 6)
    .attr("dy", ".71em")
    .style("text-anchor", "end")
    .text("Nb obs");

  this.refresh = function(opt){
    var opt = opt || {};
    
    // filters
    var species_id = +$("select[data-id=species]").val();
    var stage_id = +$("select[data-id=stages]").val();
    var years_selected = $(".rowyear input:checked").map(function(i, item){
      return $(item).attr("value");
    }).toArray();

    // get data
    var main_data = opt.data || phenoclim.session.dataviz;
    var dataRaw = {};
    if(main_data[species_id] && main_data[species_id][stage_id]){
      dataRaw = main_data[species_id][stage_id];
    }

    // prepare data
    var data = d3.entries(dataRaw).map(function(d){
      d.values = d3.entries(d.value).map(function(d2){
        d2.year = d.key;
        return d2;
      });
      d.values.sort(function(a, b){
        return +a.key-b.key;
      })
      return d;
    }).filter(function(d){
      return (years_selected.indexOf(d.key) > -1);
    })

    // X axis
    var minWeek = d3.min(data, function(d){ return d3.min(d.values, function(d){
      return parseInt(d.key);
    })})
    var maxWeek = d3.max(data, function(d){ return d3.max(d.values, function(d){
      return parseInt(d.key);
    })})
    x.domain(d3.range(minWeek, maxWeek + 2, 1));
    xGraphAxis.call(xAxis);

    // Y axis
    var maxNbObs = d3.max(data, function(d){ return d3.max(d.values, function(d){
      return parseInt(d.value);
    })});
    y.domain([0, maxNbObs]);
    yAxis.ticks((maxNbObs<5) ? maxNbObs : 5);
    yGraphAxis.call(yAxis);
    
    svg.selectAll("g.year").remove();

    // year group
    var year = svg.selectAll("g.year").data(data)
      .enter()
      .append("g")
        .attr("class", "year")

    // lines
    if(options.line_enable == true){
      // representing amounts of obs per week number, for a specific year
      var lines = year.append("path")
        .style('stroke', function(d) { return phenoclim.session.linechart.colors(d.key); })
        .attr("class", "line")
        .attr("d", function(d){ return line(d.values) })
        .attr("transform", null)
    }

    // circles representing the middle of the week
    var circles = year.selectAll(".dot")
      .data(function(d){ return d.values; })
      .enter()
      .append("circle")
        .attr("class", "dot")
        .attr("r", 4)
        .attr("cx", function(d) { return (x(+d.key) + x.rangeBand()); })
        .attr("cy", function(d) { return y(+d.value); })
        .style("fill", function(d) { return phenoclim.session.linechart.colors(d.year); })
        .on("mousemove", function(d){
          d3.select(this).attr("r", 7).style("fill-opacity", 0.9);
          mousemove(d);
        })
        .on("mouseout", function(d){
          d3.select(this).attr("r", 4).style("fill-opacity", 1);
          mouseout();
        })
        .on("mouseover", function(d){
          mouseover();
        });
    }

    /** TOOLTIP **/
    function mouseover() {
      tooltip.transition()
          .duration(300)
          .style("opacity", 1);
    }

    function mousemove(week_value) {
      var week = +week_value.key;
      var year = +week_value.year;
      var firstDate = phenoclim.viz.getFirstDayOfWeek(week+1, +year);
      var firstDateStr = firstDate.getDate() + "/" + (firstDate.getMonth()+1);
      var lastDate = phenoclim.viz.getLasttDayOfWeek(week+1, +year);
      var lastDateStr = lastDate.getDate() + "/" + (lastDate.getMonth()+1);
      tooltip.html(function(d){ 
        return year+"<br/><b>"+week_value.value+" obs</b><br/> ("+ firstDateStr + " - " + lastDateStr +")" })
          .style("left", (d3.event.layerX - 34) + "px")
          .style("top", (d3.event.layerY - 60) + "px");
    }

    function mouseout() {
      tooltip.transition()
          .duration(300)
          .style("opacity", 1e-6);
    }

  this.colors = d3.scale.category10().domain([1,12]);
}


phenoclim.viz.barChart = function(params){
  var self = this;

  var options = {
    selector: ".graph-bars",
    margin: {top: 20, right: 10, bottom: 30, left: 80},
  }
  $.extend(true, options, params);

  var container = d3.select(options.selector);
  var main_width = options.width || $(options.selector).width();
  var width = main_width - options.margin.left - options.margin.right;
  var height = (main_width*3/5) - options.margin.top - options.margin.bottom;

  var x = d3.scale.ordinal().rangeBands([0, width], 0.1);
  var x1 = d3.scale.ordinal();
  var y = d3.scale.linear().range([height, 0]);

  var today = new Date()
  var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom")

  var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .ticks(5);

  var container = d3.select(".graph-bars");

  var svg = container.append("svg")
    .attr("width", width + options.margin.left + options.margin.right)
    .attr("height", height + options.margin.top + options.margin.bottom)
    .append("g")
      .attr("transform", "translate(" + options.margin.left + "," + options.margin.top + ")");

  var xGraphAxis = svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .attr("class", "x axis");
  
  xGraphAxis.append("text")
    .attr("transform", "translate(" + width +", -20)")
    .attr("y", 6)
    .attr("x", 5)
    .attr("dy", ".71em")
    .style("text-anchor", "end")
    .text("Stade");
  
  var yGraphAxis = svg.append("g")
    .attr("class", "y axis");

  yGraphAxis.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 6)
    .attr("dy", ".71em")
    .style("text-anchor", "end")
    .text("Nb obs");

  this.refresh = function(){
    //console.log("on refresh");
    var species_id = +$("select[data-id=species]").val();
    var years_selected = $(".checkbox input:checked").map(function(i, item){
      return $(item).attr("value");
    }).toArray();

    var stages = phenoclim.session.species_list.filter(function(d){
      return d.id == species_id;
    })[0].stages

    var dataRaw = phenoclim.session.dataviz[species_id] || {};

    var data = d3.entries(dataRaw)
      .map(function(d){
        d.name = stages.filter(function(d2){
          return +d2.id === +d.key;
        })[0].label;
        d.values = d3.entries(d.value).filter(function(fitem){
          return years_selected.indexOf(fitem.key) > -1;
        }).map(function(d2){
          d2.amount = d3.sum(d3.entries(d2.value), function(d5){
            return +d5.value;
          });
          return d2;
        });
        return d;
      });

    var stages_id = data.map(function(d){ return d.name });
    x.domain(stages_id);
    
    var years = data[0].values.map(function(d){
      return d.key;
    })
    x1.domain(years).rangeRoundBands([0, x.rangeBand()]);
    
    var maxNbObs = d3.max(data,
      function(d){
        return d3.max(d.values, function(d){
          return parseInt(d.amount);
        })})
    y.domain([0, maxNbObs]);
    
    xGraphAxis.call(xAxis);
    yGraphAxis.call(yAxis);
    
    svg.selectAll(".state").remove();
    
    var state = svg.selectAll(".state")
      .data(data)
      .enter().append("g")
      .attr("class", "state")
      .attr("transform", function(d) { return "translate(" + x(d.name) + ",0)"; });

    state.selectAll("rect")
      .data(function(d) { return d.values; })
      .enter().append("rect")
        .attr("width", x1.rangeBand())
        .attr("x", function(d) { return x1(d.key); })
        .attr("y", function(d) { return y(d.amount); })
        .attr("height", function(d) { return height - y(d.amount); })
        .style("fill", function(d) { return phenoclim.session.barchart.colors(d.key); });
      }
      this.colors = d3.scale.category10().domain([1,12]);
    }



    phenoclim.viz.timeBarChart = function(params){
      var self = this;

      var options = {
        selector: ".graph-bars-time",
        margin: {top: 20, right: 10, bottom: 30, left: 80},
      }
      $.extend(true, options, params);

      var container = d3.select(options.selector);
      var main_width = options.width || $(options.selector).width();
      var width = main_width - options.margin.left - options.margin.right;
      var height = (main_width*3/5) - options.margin.top - options.margin.bottom;

      var x = d3.scale.ordinal().rangeBands([0, width]);
      var x1 = d3.scale.ordinal();
      var y = d3.scale.ordinal().rangeRoundBands([0, height], .1);
      var y1 = d3.scale.ordinal();

      var today = new Date()
      var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom")
      .tickFormat(function(d, i){
        if(i%2 == 0){
          var day = phenoclim.viz.getFirstDayOfWeek(d+1, today.getFullYear());
          return day.getDate() + "/" + (+day.getMonth()+1)
        }
        return ""
      })

      var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left")

      var container = d3.select(".graph-bars-time");

      var svg = container.append("svg")
      .attr("width", width + options.margin.left + options.margin.right)
      .attr("height", height + options.margin.top + options.margin.bottom)
      .append("g")
      .attr("transform", "translate(" + options.margin.left + "," + options.margin.top + ")");

      var xGraphAxis = svg.append("g")
        .attr("transform", "translate(0," + height + ")")
         .attr("class", "x axis");
      
      xGraphAxis.append("text")
        .attr("transform", "translate(" + width +", -20)")
        .attr("y", 10)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Date");

      var yGraphAxis = svg.append("g")
        .attr("class", "y axis");

      yGraphAxis.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Stades");

      this.refresh = function(){
        //console.log("on refresh time chart");
        var species_id = +$("select[data-id=species]").val();
        var years_selected = $(".checkbox input:checked").map(function(i, item){
          return $(item).attr("value");
        }).toArray();

        var stages = phenoclim.session.species_list.filter(function(d){
          return d.id == species_id;
        })[0].stages;

        var dataRaw = phenoclim.session.dataviz[species_id] || {};
        var data = d3.entries(dataRaw)
        .map(function(d){
          d.name = stages.filter(function(d2){
            return +d2.id === +d.key;
          })[0].label;
          d.values = d3.entries(d.value).filter(function(fitem){
            return years_selected.indexOf(fitem.key) > -1;
          }).map(function(d2){
            d2.values = d3.entries(d2.value).map(function(d4){d4.name = d.name; return d4})
            return d2;
          })
          return d;
        });

        var minWeek = d3.min(data, function(d){ 
          return d3.min(d.values, function(d2){
            return d3.min(d2.values, function(d4){
                return parseInt(d4.key);
            })
          })
        });
        var maxWeek = d3.max(data, function(d){ 
          return d3.max(d.values, function(d2){
            return d3.max(d2.values, function(d4){
                return parseInt(d4.key);
            });
          });
        });

        var stages_id = data.map(function(d){ return d.name });

        x.domain(d3.range(minWeek, maxWeek + 2, 1));
        y.domain(stages_id);

        xGraphAxis.call(xAxis);
        xGraphAxis.selectAll(".tick line")
          .attr("display", function(d,i){ if(i%2 == 1){ return "none"}});
                    
        yGraphAxis.call(yAxis);
        svg.selectAll(".state").remove();

        var state = svg.selectAll(".state")
          .data(data)
          .enter().append("g")
          .attr("class", "state");

        var state2 = state.selectAll(".state2")
          .data(function(d){ return d.values;})
          .enter().append("g")
          .attr("class", "state2");

        state2.selectAll("rect")
          .data(function(d) { return d.values; })
          .enter().append("rect")
            .attr("width", x.rangeBand()+1)
            .attr("x", function(d) { return x(+d.key) + (x.rangeBand()/2); })
            .attr("y", function(d) { return y(d.name); })
            .attr("height", function(d) { return y.rangeBand() })
            .style("fill", function(d) { return self.colors(d.name) });
        }
        this.colors = d3.scale.category20b().domain([10,11,12,13,14,15,17,18]);
    }
    phenoclim.viz.SnowingChart = function(params){
      var self = this;

      var options = {
        selector: ".graph",
        margin: {top: 20, right: 30, bottom: 30, left: 30},
        line_enable: true,
        max_width: 920,
      }
      $.extend(true, options, params);

      var container = d3.select(options.selector);
      var main_width = options.width || $(options.selector).width();
      if (main_width > options.max_width){
        main_width = options.max_width;
      }
      var width = main_width - options.margin.left - options.margin.right;
      var height = (main_width*2/5) - options.margin.top - options.margin.bottom;
      var tooltip = container.append("div")
        .attr("class", "tooltip")
        .style("opacity", 1e-6);

      var x = d3.scale.ordinal()
        .rangeBands([0, width])

      var xTime = d3.time.scale()
        .range([0, width])

      var y = d3.scale.linear()
        .range([height, 0]);

      var xAxis = d3.svg.axis()
        .scale(xTime)
        .orient("bottom")
        .tickFormat(phenoclim.tools.myTimeFormatter);

      var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")

      var svg = container.append("svg")
        .attr("width", width + options.margin.left + options.margin.right)
        .attr("height", height + options.margin.top + options.margin.bottom)
        .append("g")
          .attr("transform", "translate(" + options.margin.left + "," + options.margin.top + ")");
      
      var xGraphAxis = svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .attr("class", "x axis");

      xGraphAxis.append("text")
        .attr("transform", "translate(" + width +", -20)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Date");

      var yGraphAxis = svg.append("g")
        .attr("class", "y axis");

      yGraphAxis.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Height");

      this.refresh = function(r_params){
        var data = r_params.data;
        var year = +r_params.year;
        var snowings = data.snowings.map(function(d){
          d.date = moment(d.date);
          return d;
        });

        var minDate = moment([year-1, 9, 1]) // fixed
        var maxDate = moment([year, 4, 1]); // fixed

        var filtered = snowings.filter(function(d){
          return d.date <= maxDate && d.date >= minDate;
        })
        filtered.sort(function(a, b){
          if(a.date > b.date){
            return 1;
          }
          else{
            return -1;
          }
        });
        var maxHeight = d3.max(filtered, function(d){
          return +d.height;
        })

        var fulldates = []; // Array of day of year
        var tmpDate = moment(minDate);
        while(tmpDate <= maxDate){
          fulldates.push(tmpDate.format("DDD"));
          tmpDate.add(1, "days");
        }
        xTime.domain([minDate, maxDate]);
        x.domain(fulldates);
        y.domain([0, data.maxHeight + 10]);
        xGraphAxis.call(xAxis);
        xGraphAxis.selectAll(".tick text").attr("transform", "translate(" + x.rangeBand()*15 +", 0)")
        yGraphAxis.call(yAxis);
        svg.selectAll(".bar").remove();
        var rect = svg.selectAll(".bar")
                      .data(filtered)
                      .enter()
                      .append("rect")
                      .attr("class", "bar")
                      .attr("width", x.rangeBand()+1)
                      .attr("x", function(d){
                        return x(d.date.format("DDD"));
                      })
                      .attr("y", function(d) { return y(0); })
                      .attr("height", function(d) { return 0; })
       .on("mousemove", function(d){
          mousemove(d);
        })
        .on("mouseout", function(d){
          mouseout();
        })
        .on("mouseover", function(d){
          mouseover();
        });

      rect.transition()
          .duration(200)
          .delay(function(d, i) { return i*2; })
          .attr("y", function(d) { return y(+d.height); })

          .attr("height", function(d) { return height - y(+d.height); });

      /** TOOLTIP **/
      function mouseover() {
        tooltip.transition()
            .duration(300)
            .style("opacity", 1);
      }

      function mousemove(data) {
        tooltip.html(function(d){ 
          return data.date.format("D MMM YYYY") + " <br/><b>"+data.height+"cm</b><br/>"})
            .style("left", (d3.event.layerX - 34) + "px")
            .style("top", (y(+data.height) + 5) + "px");
      }

      function mouseout() {
        tooltip.transition()
            .duration(300)
            .style("opacity", 1e-6);
      }
      }
      this.colors = d3.scale.category10();
    }