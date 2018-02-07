function makeCharts(title, xaxis, dates, yaxis, seriesName, data, mx) {
	console.log(title, xaxis, dates, yaxis, seriesName, data);
  dates = dates.split(",");
  for (var i = 0; i < dates.length; i++) {
    console.log(typeof dates[i], dates[i]);
    dates[i] = dates[i].replace('&#39;', '');
    dates[i] = dates[i].replace('&#39;', '');
  }
  

 	Highcharts.chart('container', {

    title: {
      text: title //title
    },

    xAxis: {
      title: {
        text: xaxis, //xaxis title
      },
      categories: dates //dates
    },

    yAxis: {
      title: {
        text: yaxis, //y-axis title
      },
      min: 0,
      max: mx
    },

    legend: {
      layout: 'vertical',
      align: 'right',
      verticalAlign: 'middle'
    },

    plotOptions: {
      series: {
        label: {
          connectorAllowed: false
        }
      }
    },

    series: [
	    {
	      name: seriesName, //series name
	      data: data //data
	    }, 
    ],

    responsive: {
      rules: [
      	{
        	condition: {
          maxWidth: 500
        },
        chartOptions: {
	        legend: {
	            layout: 'horizontal',
	            align: 'center',
	            verticalAlign: 'bottom'
	          }
	        }
      	}]
    	}
		})
	}
// });

// if (title === "Sleep Tracker")
// make_chart(title, "Hours", ["1/21/94", "1/13/94", "1/24/68"], "Hours", "Hours", [7, 8, 9]);
