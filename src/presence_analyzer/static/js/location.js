(function($) {
    $(document).ready(function(){
        var $dropdownGender = $('#gender'),
            $loading = $('#loading');

        getYearMonthJSON('/api/v1/presence_location_view', $loading);
        loadGenderDropdown($dropdownGender);
        $dropdownGender.show();

        $('#user-id, #gender').on('change', function(){
            var $chartDiv = $('#chart-div'),
                $errorContainer = $('#data-error'),
                selectedGender = $('#gender').val(),
                selectedMonth = $('#user-id').val();

            $errorContainer.text('');
            $chartDiv.hide();

            if(selectedMonth !== '' && selectedGender === '') {
                $loading.show();

                $.getJSON('/api/v1/location_gender_view/' + selectedMonth, function(result) {
                    function locationStacked() {
                        var chart = new google.visualization.BarChart($chartDiv[0]),
                            data,
                            options = {
                                width: 750,
                                height: 750,
                                hAxis: {
                                    minValue: 0,
                                    title: 'Hours',
                                },
                                isStacked: true,
                            }
                            rawData = [['Location', 'Male', 'Female']];

                        $.each(result, function (towns, genders) {
                            rawData.push([
                                towns,
                                genders['male'] / 360,
                                genders['female'] / 360
                            ]);
                        });

                        data=google.visualization.arrayToDataTable(rawData);
                        chart.draw(data, options);
                    }
                    drawGender(locationStacked, $loading, $chartDiv);

                }).fail(function(jqXHR) {
                    showError(jqXHR, $loading, $errorContainer);
                });
            }

            if(selectedMonth !== '' && selectedGender !== '') {
                $loading.show();

                $.getJSON('/api/v1/location_gender_view/' + selectedMonth + '/' + selectedGender, function(result) {
                    function locationGender() {
                        var chart = new google.visualization.BarChart($chartDiv[0]),
                            data,
                            options = {
                                width: 750,
                                height: 750,
                                hAxis: {
                                    minValue: 0,
                                    title: 'Hours',
                                },
                            },
                            rawData = [['Location', selectedGender]];

                        $.each(result, function (town, value) {
                            rawData.push([town, value / 360]);
                        });

                        data=google.visualization.arrayToDataTable(rawData);
                        chart.draw(data, options);
                    }
                    drawGender(locationGender, $loading, $chartDiv);

                }).fail(function(jqXHR) {
                    showError(jqXHR, $loading, $errorContainer);
                });
            }
        });
    });
})(jQuery);
