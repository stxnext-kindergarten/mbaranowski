function parseInterval(value) {
    var result = new Date(1, 1, 1);
    result.setMilliseconds(value * 1000);
    return result;
}

function getDataJSON(url, loading) {
    $.getJSON(url, function(result) {
        var $dropdown = $('#user-id');

        $.each(result, function(item) {
            $dropdown.append($('<option/>', {
                'val': this.user_id,
                'text': this.name
            }));
        });
        $dropdown.show();
        loading.hide();
    });
}

function drawChart(chartDiv, loading, chart, data, options) {
    chartDiv.show();
    loading.hide();
    chart.draw(data, options);
}

function showError(jqXHR, loading, errorContainer) {
    loading.hide();
    if (jqXHR.status === 404) {
        errorContainer.text('There is no data available.');
    }
}

(function($) {
    $(document).ready(function() {
        $('#user-id').change(function() {
            var $avatarUrl = $('#avatar'),
                selectedUser = $('#user-id').val(),
                $userName = $('#user-name');

            $avatarUrl.hide();
            $userName.hide();

            $.getJSON('/api/v1/users/' + selectedUser, function(result) {
                $avatarUrl.empty().prepend($('<img>', {src: result.avatar})).show();
            });
        });
    });
})(jQuery);
