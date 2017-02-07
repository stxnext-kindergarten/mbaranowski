(function($) {
    $(document).ready(function() {
        var $loading = $('#loading');

        getDataJSON('/api/v1/users', $loading);

        $('#user-id').change(function() {
            var $chartDiv = $('#chart-div'),
                $errorContainer = $('#data-error'),
                selectedUser = $('#user-id').val();

            $errorContainer.text('');
            if(selectedUser) {
                $loading.show();
                $chartDiv.hide();

                $.getJSON('/api/v1/presence_weekday/' + selectedUser, function(result) {
                    var chart = new google.visualization.PieChart($chartDiv[0]),
                        data = google.visualization.arrayToDataTable(result),
                        options = {};

                    drawChart($chartDiv, $loading, chart, data, options);
                }).fail(function(jqXHR) {
                    showError(jqXHR, $loading, $errorContainer);
                });
            }
        });
    });
})(jQuery);
