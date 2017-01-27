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
