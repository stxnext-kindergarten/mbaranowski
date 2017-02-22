(function($) {
    $(document).ready(function(){
        var $loading = $('#loading');

        getAvatar();
        getDataJSON('/api/v1/users', $loading);

        $('#user-id').change(function(){
            var $chartDiv = $('#chart-div'),
                $errorContainer = $('#data-error'),
                selectedUser = $('#user-id').val();

            $errorContainer.text('');
            if(selectedUser) {
                $loading.show();
                $chartDiv.hide();

                $.getJSON('/api/v1/presence_start_end/' + selectedUser, function(result) {
                    var chart= new google.visualization.Timeline($chartDiv[0]),
                        data = new google.visualization.DataTable(),
                        formatter = new google.visualization.DateFormat({pattern: 'HH:mm:ss'}),
                        options = {
                            hAxis: {title: 'Weekday'}
                        };

                    $.each(result, function(index, value) {
                        value[1] = parseInterval(value[1]);
                        value[2] = parseInterval(value[2]);
                    });

                    data.addColumn('string', 'Weekday');
                    data.addColumn({type: 'datetime', id: 'Start'});
                    data.addColumn({type: 'datetime', id: 'End'});
                    data.addRows(result);
                    formatter.format(data, 1);
                    formatter.format(data, 2);

                    drawChart($chartDiv, $loading, chart, data, options);
                }).fail(function(jqXHR) {
                    showError(jqXHR, $loading, $errorContainer)
                });
            }
        });
    });
})(jQuery);
