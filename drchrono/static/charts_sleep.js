
var chart = Highcharts.chart('container', {

    title: {
      text: 'Sleep Tracker'
    },

    xAxis: {
      title: {
        text: 'Date',
      }
    },

    yAxis: {
      title: {
        text: 'Hours',
      },
      min: 0,
      max: 24
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
        },
        pointStart: 1
        // {{ start_date }}
      }
    },

    series: [
	    {
	      name: 'Hours of Sleep',
	      data: [4, 9, 10]
	      // {{ hours }}
	    }, 
    ],

    responsive: {
      rules: [{
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
});