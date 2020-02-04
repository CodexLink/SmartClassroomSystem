/*
    ! sc_require.js
    * Created by Janrey Licas
    * Created on 01/24/2019
    * This was added to make front-end customizations and other such stuff such as AJAX.
*/

// ! Mansory Dashboard View
$('.dashboard-grid').isotope({
    itemSelector: '.dashboard-item',
    layoutMode: 'packery',
    resize: true,
    packery: {
        columnWidth: '.dashboard-item',
        horizontal: false
    },
    sortAscending: true,
    transistion: 300,
    percentPosition: true,
});

// ! Mansory + Isotope View for Logs
$('.log-grid').isotope({
    itemSelector: '.log-item',
    layoutMode: 'packery',
    resize: true,
    packery: {
        columnWidth: '.log-item',
        horizontal: false
    },
    sortAscending: true,
    transistion: 300,
    percentPosition: true,
});

// ! Mansory + Isotope View for Logs
$('.actions-grid').isotope({
    itemSelector: '.actions-item',
    layoutMode: 'packery',
    resize: true,
    packery: {
        columnWidth: '.actions-item',
        horizontal: false
    },
    sortAscending: true,
    transistion: 300,
    percentPosition: true,
});

// ! Mansory + Isotope View for Schedule
$('.schedule-grid').isotope({
    itemSelector: '.schedule-item',
    layoutMode: 'packery',
    resize: true,
    packery: {
        columnWidth: '.schedule-item',
        horizontal: false
    },
    getSortData: {
        name: '.schedule-item',
        schedule: '[day-schedule]',
        timestart: '[time-start]'
    },
    sortBy: ['timestart', 'schedule'],
    sortAscending: true,
    transistion: 300,
    percentPosition: true,
});

// ! Isotope Filtering System for Schedule
$('.tab-card-filter').on('click', 'li a', function () {
    var filterValue = $(this).attr('data-filter');
    var sortValue = $(this).attr('data-sort-by');
    $('.schedule-grid').isotope({ filter: filterValue });
    $('.schedule-grid').isotope({ sortBy: sortValue });
});

// ! Isotope Filtering System for Logs Level
$('.tab-card-filter').on('click', 'li a', function () {
    var filterValue = $(this).attr('data-filter');
    $('.log-grid').isotope({ filter: filterValue });
});

$(document).ready(function (e)
{
    $('.schedule-grid').isotope({ sortBy: 'timestart' });
});


// ! Update View ACcording to Layout Changes Since Card is at Absolute Position
$('.quick-actions-handler').click(function (event) {
    setTimeout(function () {
        $('.dashboard-grid').isotope("arrange");
    }, 260);
});

// ! Close Sidebar Upon Click
$('.close-sidebar').click(function (event) {
    $('#navdrawer').navdrawer('hide');
})

// ! Live Dashboard Time with Progress Bar

// ! Set the Progress Bar First.
$(document).ready(function (e) {
    var TimeData = new Date();

    var strInitTemplate = "Time is ";
    var strSeperator = " | ";
    var strLastTemplate = " before dismissal.";

    var rawHour = TimeData.getHours();
    var processedHour = (rawHour > 12) ? rawHour - 12 : rawHour;

    var rawMin = TimeData.getMinutes().toString();
    var processedMin = (rawMin.length <= 1) ? "0" + rawMin : rawMin;

    var rawSec = TimeData.getSeconds().toString();
    var processedSec = (rawSec.length <= 1) ? "0" + rawSec : rawSec;

    var meridian = (rawHour > 12) ? "PM" : "AM";

    var timeDiff = Math.abs(rawHour - 20); // This signifies all working time up until 8.
    var strDiffLiteral = (rawHour == 19) ? " hour" : " hours";
    var strContent = strInitTemplate + processedHour + ":" + processedMin + ":" + processedSec + " " + meridian + strSeperator + timeDiff + strDiffLiteral + strLastTemplate;

    // Progress Bar Width Setter
    progressWidth = ((Math.abs(TimeData.getHours() / 22) * 100))

    $('.time-width').width(progressWidth + '%');

    return $('.local_time_display').text(strContent);
})

// ! Do Repeat the process of the function above.


if (document.querySelector('.local_time_display') !== null) {
    setInterval(function (event) {
        var TimeData = new Date();

        var strInitTemplate = "Time is ";
        var strSeperator = " | ";
        var strLastTemplate = " before dismissal.";

        var rawHour = TimeData.getHours();
        var processedHour = (rawHour > 12) ? rawHour - 12 : rawHour;

        var rawMin = TimeData.getMinutes().toString();
        var processedMin = (rawMin.length <= 1) ? "0" + rawMin : rawMin;

        var rawSec = TimeData.getSeconds().toString();
        var processedSec = (rawSec.length <= 1) ? "0" + rawSec : rawSec;

        var meridian = (rawHour > 12) ? "PM" : "AM";

        var timeDiff = Math.abs(rawHour - 20); // This signifies all working time up until 8.
        var strDiffLiteral = (rawHour == 19) ? " hour" : " hours";
        var strContent = strInitTemplate + processedHour + ":" + processedMin + ":" + processedSec + " " + meridian + strSeperator + timeDiff + strDiffLiteral + strLastTemplate;

        // Progress Bar Width Setter
        progressWidth = ((Math.abs(TimeData.getHours() / 22) * 100))

        $('.time-width').width(progressWidth + '%');

        return $('.local_time_display').text(strContent);
    }, 1000);
}
