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

function getAvatar() {
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
}

function getYearMonthJSON(url, loading) {
    $.getJSON(url, function(result) {
        var $dropdown = $('#user-id');

        $.each(result, function(item) {
            $dropdown.append($('<option/>', {
                'val': this.key,
                'text': this.val
            }));
        });

        $dropdown.show();
        loading.hide();
    });
}

function isDataAvailable(data, start) {
    for(var i = start, sum = 0; i < data.length; i++) {
        sum += data[i][1];
    }
    return sum !== 0;
}

function drawGender(fun, loading, chartDiv){
    google.charts.load('current', {packages: ['corechart', 'bar']});
    loading.hide();
    google.charts.setOnLoadCallback(fun);
    chartDiv.show();
}

function loadGenderDropdown(dropdown) {
    $.each(['male', 'female'], function (index, gender) {
        dropdown.append($('<option/>', {
            'val': gender,
            'text': gender,
        }));
    });
}
