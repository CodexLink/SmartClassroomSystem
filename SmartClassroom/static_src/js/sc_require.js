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

// ! Packery Login and Logout View
$('.auth-grid').isotope({
    itemSelector: '.auth-item',
    layoutMode: 'packery',
    resize: true,
    packery: {
        columnWidth: '.auth-item',
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
});

// ! Isotope Filtering System for Logs Level
$('.tab-card-filter').on('click', 'li a', function () {
    var filterValue = $(this).attr('data-filter');
    $('.log-grid').isotope({ filter: filterValue });
});

// ! Isotope Filtering System for Type Queries
$('.filter-card-elements').on('input', function () {
    var filterValue = $(this).val();
    $('.log-grid, .schedule-grid').isotope({
        filter: function () {
            var titleSearch = $(this).find('.card-title').text();
            if (!filterValue.length)
            {
                return true;
            }
            else
            {
                return (filterValue.toUpperCase() === titleSearch.toUpperCase()) ? true : false;
            }
        }
    });
});

$(document).ready(function (e) {
    $('.schedule-grid').isotope({ sortBy: 'timestart' });
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
    var strDiffLiteral = (rawHour >= 19) ? " hour" : " hours";
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
        var strLast_SessionDone = "Work Dismissed.";

        var rawHour = TimeData.getHours();
        var processedHour = (rawHour > 12) ? rawHour - 12 : rawHour;

        var rawMin = TimeData.getMinutes().toString();
        var processedMin = (rawMin.length <= 1) ? "0" + rawMin : rawMin;

        var rawSec = TimeData.getSeconds().toString();
        var processedSec = (rawSec.length <= 1) ? "0" + rawSec : rawSec;

        var meridian = (rawHour > 12) ? "PM" : "AM";

        var timeDiff = Math.abs(rawHour - 20); // This signifies all working time up until 8.
        var strDiffLiteral = (rawHour >= 19) ? " hour before dismissal." : " hours before dismissal.";
        var strContent = strInitTemplate + processedHour + ":" + processedMin + ":" + processedSec + " " + meridian + strSeperator + timeDiff + strDiffLiteral;

        // Progress Bar Width Setter
        progressWidth = ((Math.abs(TimeData.getHours() / 22) * 100))

        $('.time-width').width(progressWidth + '%');

        return $('.local_time_display').text(strContent);
    }, 1000);
}

// ! Clear Auth Credential Fields
$('.auth-clear-entry').click(function (e) {
    $('.form-control').val('');
});

// ! HTML Device Command Bypass Back to Root classroom/<uuid:classUniqueID>/control
$(document).ready(function (event) {
    // ! Add More, Especially In Thank You Page Or On Anything else.
    if (window.location.pathname.split('/')[1] == "classroom" && window.location.pathname.split('/')[3] == "control" && window.location.pathname.split('/')[4]) {
        window.history.replaceState(null, document.title, "/" + window.location.pathname.split('/')[1] + "/" + window.location.pathname.split('/')[2] + "/" + window.location.pathname.split('/')[3] + "/");
        window.location.reload();
    }
})