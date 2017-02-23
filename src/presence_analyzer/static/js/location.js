(function($) {
    $(document).ready(function(){
        var $loading = $('#loading');

        getYearMonthJSON('/api/v1/presence_location_view', $loading);

        $('#user-id').change(function(){
            var $chartDiv = $('#chart-div'),
                $errorContainer = $('#data-error'),
                selectedMonth = $('#user-id').val();

            $errorContainer.text('');
            $chartDiv.hide();
            if(selectedMonth) {
                $loading.show();
                $.getJSON('/api/v1/presence_location_view/' + selectedMonth, function(result) {
                    function drawLocation() {
                        var chart = new google.visualization.BarChart($chartDiv[0]),
                            data,
                            options = {
                                width: 750,
                                height: 750,
                                hAxis: {minValue: 0},
                            },
                            rawData = [['Location', 'Hours']];

                        $.each(result['locations'], function (index, value) {
                            rawData.push([index, value / (60 * 60)]);
                        });

                        data=google.visualization.arrayToDataTable(rawData);
                        chart.draw(data, options);
                    }

                    google.charts.load('current', {packages: ['corechart', 'bar']});
                    $loading.hide();
                    google.charts.setOnLoadCallback(drawLocation);
                    $chartDiv.show();
                }).fail(function(jqXHR) {
                    showError(jqXHR, $loading, $errorContainer);
                });
            }
        });
    });
})(jQuery);
