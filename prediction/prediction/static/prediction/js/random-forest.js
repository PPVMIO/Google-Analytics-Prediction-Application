var width = 360;
var height = 360;
var radius = Math.min(width, height) / 2;
var donutWidth = 75;
var legendRectSize = 18;                                  
var legendSpacing = 4;                                    
var color = d3.scaleOrdinal(d3.schemeCategory20b);
var svg = d3.select('#chart')
    .append('svg')
    .attr('width', width)
    .attr('height', height)
    .append('g')
    .attr('transform', 'translate(' + (width / 2) +
    ',' + (height / 2) + ')');
var arc = d3.arc()
    .innerRadius(radius - donutWidth)
    .outerRadius(radius);
var pie = d3.pie()
    .value(function(d) { return d.count; })
    .sort(null);
var tooltip = d3.select('#chart')                               
      .append('div')                                                
      .attr('class', 'tooltip');                                    
    tooltip.append('div')                                           
      .attr('class', 'label');                                      
    tooltip.append('div')                                           
      .attr('class', 'count');                                      
    tooltip.append('div')                                           
      .attr('class', 'percent');   

dataset = []
featureImportanceNames = []
featureImportance = []


//optimal pie chart

d3.json('models/random-forest/', function(error, data){
    if(error)
        console.log(error)
    
    featureImportanceNames = data.featureInfo.optCombinedFeatureImportanceNames
    featureImportance = data.featureInfo.optCombinedFeatureImportance
    featureNameDict = data.featureInfo.orgFeatureNameDict
    
    featureInputDOM = document.querySelectorAll(".feature-input")
    featureOptionsDOM = document.querySelectorAll(".feature-list")
    
    
    for(i = 0; i < featureImportanceNames.length; i++){
        var options = ''
        for(name in featureNameDict[featureImportanceNames[i]]){
            options += '<option value="' + featureNameDict[featureImportanceNames[i]][name] + '" />';
        }
            
        featureOptionsDOM[i].innerHTML = options
        featureInputDOM[i].name = featureImportanceNames[i]
        
    }
    


    var dataset= [];
    for(var i = 0; i < featureImportance.length; i++){
        var temp = new Object()
        if(featureImportance[i] > 0){
            temp = {
                'label': featureImportanceNames[i],
                'count': featureImportance[i]
            }
            
            dataset.push(temp);
        }
    }
    

    var path = svg.selectAll('path')
        .data(pie(dataset))
        .enter()
        .append('path')
        .attr('d', arc)
        .attr('fill', function(d, i) {
          return color(d.data.label);
    });
    
    path.on('mouseover', function(d) {                            
            var total = d3.sum(dataset.map(function(d) {                
              return d.count;                                           
            }));                                                        
            var percent = Math.round(1000 * d.data.count / total) / 10; 
            var countNum = Math.round(100 * d.data.count)/ 100
            tooltip.select('.label').html(d.data.label);                
            tooltip.select('.count').html(countNum);                
            tooltip.select('.percent').html(percent + '%');             
            tooltip.style('display', 'block');                          
          });                                                           

          path.on('mouseout', function() {                              
            tooltip.style('display', 'none');                           
          });       

    var legend = svg.selectAll('.legend')
        .data(color.domain())
        .enter()
        .append('g')
        .attr('class', 'legend')
        .attr('transform', function(d, i) {
          var height = legendRectSize + legendSpacing;
          var offset =  height * color.domain().length / 2;
          var horz = -2 * legendRectSize;
          var vert = i * height - offset;
          return 'translate(' + horz + ',' + vert + ')';
    });

    legend.append('rect')
        .attr('width', legendRectSize)
        .attr('height', legendRectSize)
        .style('fill', color)
        .style('stroke', color);

    legend.append('text')
        .attr('x', legendRectSize + legendSpacing)
        .attr('y', legendRectSize - legendSpacing)
        .text(function(d) { return d; });
})

//original pie chart
/*d3.json('models/random-forest/', function(error, data){
    if(error)
        console.log(error)
    
    featureImportanceNames = data.featureInfo.orgCombinedFeatureImportanceNames
    featureImportance = data.featureInfo.orgCombinedFeatureImportance
    featureNameDict = data.featureInfo.orgFeatureNameDict
    
    featureInputDOM = document.querySelectorAll(".feature-input")
    featureOptionsDOM = document.querySelectorAll(".feature-list")
    
    
    for(i = 0; i < featureImportanceNames.length; i++){
        var options = ''
        for(name in featureNameDict[featureImportanceNames[i]]){
            options += '<option value="' + featureNameDict[featureImportanceNames[i]][name] + '" />';
        }
            
        featureOptionsDOM[i].innerHTML = options
        featureInputDOM[i].name = featureImportanceNames[i]
        
    }
    


    var dataset= [];
    for(var i = 0; i < featureImportance.length; i++){
        var temp = new Object()
        if(featureImportance[i] > 0){
            temp = {
                'label': featureImportanceNames[i],
                'count': featureImportance[i]
            }
            
            dataset.push(temp);
        }
    }
    

    var path = svg.selectAll('path')
        .data(pie(dataset))
        .enter()
        .append('path')
        .attr('d', arc)
        .attr('fill', function(d, i) {
          return color(d.data.label);
    });
    
    path.on('mouseover', function(d) {                            
            var total = d3.sum(dataset.map(function(d) {                
              return d.count;                                           
            }));                                                        
            var percent = Math.round(1000 * d.data.count / total) / 10; 
            var countNum = Math.round(100 * d.data.count)/ 100
            tooltip.select('.label').html(d.data.label);                
            tooltip.select('.count').html(countNum);                
            tooltip.select('.percent').html(percent + '%');             
            tooltip.style('display', 'block');                          
          });                                                           

          path.on('mouseout', function() {                              
            tooltip.style('display', 'none');                           
          });       

    var legend = svg.selectAll('.legend')
        .data(color.domain())
        .enter()
        .append('g')
        .attr('class', 'legend')
        .attr('transform', function(d, i) {
          var height = legendRectSize + legendSpacing;
          var offset =  height * color.domain().length / 2;
          var horz = -2 * legendRectSize;
          var vert = i * height - offset;
          return 'translate(' + horz + ',' + vert + ')';
    });

    legend.append('rect')
        .attr('width', legendRectSize)
        .attr('height', legendRectSize)
        .style('fill', color)
        .style('stroke', color);

    legend.append('text')
        .attr('x', legendRectSize + legendSpacing)
        .attr('y', legendRectSize - legendSpacing)
        .text(function(d) { return d; });
})*/



