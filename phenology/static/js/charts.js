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

phenoclim.viz.load_data = function(){
  return $.get("/portail/get_data_for_viz", function(data){
    phenoclim.session.dataviz = data;
    phenoclim.viz.refreshYears();
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

phenoclim.viz.lineChart = function(){
  var self = this;

  var margin = {top: 20, right: 10, bottom: 30, left: 80};
  var width = 960 - margin.left - margin.right;
  var height = 500 - margin.top - margin.bottom;
  var x = d3.scale.ordinal().rangeBands([0, width]).domain(d3.range(53));
  var y = d3.scale.linear().range([height, 0]);
  //var xtime =  d3.scale.ordinal().rangePoints([0, width]).domain(d3.range(13));
  var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]

  var today = new Date()
  var xAxis = d3.svg.axis()
  .scale(x)
  .orient("bottom")
  .tickFormat(function(d, i){
    var day = phenoclim.viz.getFirstDayOfWeek(d, today.getFullYear());
    return day.getDate() + " " + months[day.getMonth()]
  })

  var yAxis = d3.svg.axis()
  .scale(y)
  .orient("left")
  .ticks(5);
  var container = d3.select(".graph");

  var svg = container.append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  var line = d3.svg.line()
  .x(function(d) { return x(+d.key); })
  .y(function(d) { return y(+d.value); });

  var xGraphAxis = svg.append("g")
  .attr("transform", "translate(0," + height + ")")
  .attr("class", "x axis");

  var yGraphAxis = svg.append("g")
  .attr("class", "y axis");

  this.refresh = function(){

    var species_id = +$("select[data-id=species]").val();
    var stage_id = +$("select[data-id=stages]").val();
    var years_selected = $(".checkbox input:checked").map(function(i, item){
      return $(item).attr("value");
    }).toArray();

    var dataRaw = phenoclim.session.dataviz[species_id][stage_id] || {};
    var data = d3.entries(dataRaw).map(function(d){
      d.values = d3.entries(d.value).map(function(d2){
        d2.year = d.key;
        return d2;
      });
      return d;
    }).filter(function(d){
      return (years_selected.indexOf(d.key) > -1);
    })


    var minWeek = d3.min(data, function(d){ return d3.min(d.values, function(d){
      return parseInt(d.key);
    })})
    var maxWeek = d3.max(data, function(d){ return d3.max(d.values, function(d){
      return parseInt(d.key);
    })})
    x.domain(d3.range(minWeek, maxWeek + 1, 1));

    var maxNbObs = d3.max(data,
      function(d){
        return d3.max(d.values, function(d){
          return parseInt(d.value);
        })});
    y.domain([0, maxNbObs]);

    xGraphAxis.call(xAxis);
    yGraphAxis.call(yAxis);
    svg.selectAll("g.year").remove();

    var year = svg.selectAll("g.year").data(data)
    .enter()
    .append("g")
    .attr("class", "year")

    // representing amounts of obs per week number, for a specific year
    var lines = year.append("path")
      .style('stroke', function(d) { return phenoclim.session.linechart.colors(d.key); })
      .attr("class", "line")
      .attr("d", function(d){ return line(d.values) })
      .attr("transform", null)

    // circles representing the middle of the week
    var circles = year.selectAll(".dot")
      .data(function(d){ return d.values; })
      .enter()
      .append("circle")
        .attr("class", "dot")
        .attr("r", 4)
        .attr("cx", function(d) { return x(+d.key); })
        .attr("cy", function(d) { return y(+d.value); })
            .style("fill", function(d) { return phenoclim.session.linechart.colors(d.year); });

      circles.on("mouseenter", function(d){
        d3.select(this).attr("r", 7).style("fill-opacity", 0.9);
      });
      circles.on("mouseout", function(d){
        d3.select(this).attr("r", 4).style("fill-opacity", 1);
      });
    }
  this.colors = d3.scale.category10().domain([1, 12]);
}


phenoclim.viz.barChart = function(){
  var self = this;

  var margin = {top: 20, right: 10, bottom: 30, left: 80};
  var width = 960 - margin.left - margin.right;
  var height = 500 - margin.top - margin.bottom;
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
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  var xGraphAxis = svg.append("g")
  .attr("transform", "translate(0," + height + ")")
  .attr("class", "x axis");

  var yGraphAxis = svg.append("g")
  .attr("class", "y axis");

  this.refresh = function(){

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
    var ageNames = data[0].values.map(function(d){
      return d.key;
    })
    x1.domain(ageNames).rangeRoundBands([0, x.rangeBand()]);
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
      .data(function(d) { console.log(d);return d.values; })
      .enter().append("rect")
        .attr("width", x1.rangeBand())
        .attr("x", function(d) { console.log(d.key);return x1(d.key); })
        .attr("y", function(d) { return y(d.amount); })
        .attr("height", function(d) { return height - y(d.amount); })
        .style("fill", function(d) { return phenoclim.session.barchart.colors(d.key); });
      }
      this.colors = d3.scale.category10().domain([1, 12]);
    }



    phenoclim.viz.timeBarChart = function(){
      var self = this;

      var margin = {top: 20, right: 0, bottom: 30, left: 80};
      var width = 960 - margin.left - margin.right;
      var height = 500 - margin.top - margin.bottom;
      var x = d3.scale.ordinal().rangeBands([0, width]);
      var x1 = d3.scale.ordinal();
      var y = d3.scale.ordinal().rangeRoundBands([0, height], .1);
      var y1 = d3.scale.ordinal();

      var today = new Date()
      var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom")
      .tickFormat(function(d, i){
        var day = phenoclim.viz.getFirstDayOfWeek(d, today.getFullYear());
        return ""//day.getDate() + "/" + (+day.getMonth()+1)
      })

      var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left")

      var container = d3.select(".graph-bars-time");

      var svg = container.append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      var xGraphAxis = svg.append("g")
        .attr("transform", "translate(0," + height + ")")
         .attr("class", "x axis");

      var yGraphAxis = svg.append("g")
        .attr("class", "y axis");

      this.refresh = function(){
        console.log("on refresh time chart");
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
            d2.values = d3.entries(d2.value).map(function(d4){d4.name = d.name; return d4})
            return d2;
          })
          return d;
        });

        var stages_id = data.map(function(d){ return d.name });
        y.domain(stages_id);
        x.domain(d3.range(53));
        xGraphAxis.call(xAxis);
        yGraphAxis.call(yAxis);
          svg.selectAll(".state").remove();
          var state = svg.selectAll(".state")
          .data(data)
          .enter().append("g")
          .attr("class", function(d){ console.log("enter", d); return "state"})
          
          var state2 = state.selectAll(".state2")
          .data(function(d){ return d.values;})
          .enter().append("g")
          .attr("class", "state2")

          state2.selectAll("rect")
          .data(function(d) { console.log(d);return d.values; })
          .enter().append("rect")
          .attr("width", x.rangeBand()+1)
          .attr("x", function(d) { console.log(d);return x(d.key); })
          .attr("y", function(d) { return y(d.name); })
          .attr("height", function(d) { return y.rangeBand() })
          .style("fill", function(d) { return self.colors(d.name) });
          }
          this.colors = d3.scale.category10();
        }
