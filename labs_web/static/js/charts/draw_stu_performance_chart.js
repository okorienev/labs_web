/**
 * Created by Alex Korienev on 8/26/18.
 */
$(document).ready(function () {
    google.charts.load('current', {'packages': ['line', 'bar']});
    /** @namespace google.charts */
    google.charts.setOnLoadCallback(drawChart);


    function drawChart() {
        let dataTable = new google.visualization.DataTable();
        dataTable.addColumn('number', 'Lab number');
        dataTable.addColumn('number', 'My Result');
        dataTable.addColumn('number', 'Group average');
        dataTable.addColumn('number', 'Course Average');

        let options = {
            chart: {
                title: 'Academic Performance',
            },
            width: 750,
            height: 500
        };
        let chart = new google.charts.Bar($("#PerformanceChart")[0]);
        chart.draw(dataTable, google.charts.Bar.convertOptions(options));
        let btnSelector = $(".PerformanceChartControlButton");
        btnSelector.click(function (event) {
            let id = event.target.id;
            console.log("event caught at button № ", id);
            $.get({
                url: "/student/performance-chart/{id}/".replace("{id}", id),
                success: function (data, status, XHRObject) {
                    options.chart.subtitle = "in course {full} - ({shortened})".
                    replace("{full}", data.name).replace("{shortened}", data.shortened);
                    console.log('XHR succeeded');
                    let rowsCount = dataTable.getNumberOfRows();
                    console.log('current dataset has ', rowsCount, ' rows');
                    if(rowsCount !== 0){
                        dataTable.removeRows(0, dataTable.getNumberOfRows());
                    }
                    dataTable.addRows(data.data);
                    console.log('rows added, now ', dataTable.getNumberOfRows(), ' rows');
                    chart.draw(dataTable, google.charts.Bar.convertOptions(options))
                }
            })
        });
        btnSelector.first().click();
    }
});