(function($) {
    $(document).ready(function() {
        var $loading = $('#loading');

        getAvatar();
        getDataJSON('/api/v1/users', $loading);

        $('#user-id').change(function() {
            var $chartDiv = $('#chart-div'),
                $errorContainer = $('#data-error'),
                selectedUser = $('#user-id').val();

            $errorContainer.text('');
            $chartDiv.hide();
            if(selectedUser) {
                $loading.show();

                $.getJSON('/api/v1/presence_weekday/' + selectedUser, function(result) {
                    if(isDataAvailable(result, 1)) {
                        var chart = new google.visualization.PieChart($chartDiv[0]),
                            data = google.visualization.arrayToDataTable(result),
                            options = {};

                        drawChart($chartDiv, $loading, chart, data, options);
                    } else {
                        $loading.hide();
                        $errorContainer.text('User has no data.');
                    }
                });
            }
        });
    });
})(jQuery);
