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
            if (!filterValue.length) {
                return true;
            }
            else {
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


// ! Based from https://stackoverflow.com/questions/24980827/difference-between-two-times-as-percentage-in-javascript
function totalSeconds(time) {
    var parts = time.split(':');
    return parts[0] * 3600 + parts[1] * 60 + parts[2];
}

// ! Set the Progress Bar First.
$(document).ready(function (e) {
    getTimePercentage();
});

// ! Do Repeat the process of the function above.
if (document.querySelector('.local_time_display') !== null) {
    setInterval(function (event) {
        getTimePercentage();
    }, 1000);
}

function getTimePercentage() {
    var strInitTemplate = "Current Time is ";
    var strSeperator = " | ";
    var strSession = "Work Dismissed.";

    var baseTime = new Date();

    var rawHour = baseTime.getHours().toString();

    var rawMin = baseTime.getMinutes().toString();
    var baseMinModified = (rawMin.length <= 1) ? "0" + rawMin : rawMin;

    var rawSec = baseTime.getSeconds().toString();
    var baseSecModified = (rawSec.length <= 1) ? "0" + rawSec : rawSec;

    var rawHourInt = parseInt(rawHour);
    var processedHour = (rawHourInt > 12) ? rawHourInt - 12 : rawHourInt;
    var baseHourModified = (processedHour.toString().length <= 1) ? "0" + processedHour.toString() : processedHour.toString();
    var meridian = (rawHourInt > 12) ? " PM" : " AM";

    var timeTodayReadCompatible = baseHourModified + ":" + baseMinModified + ":" + baseSecModified + meridian; // time elapsed




    var timeToday = rawHour + ":" + baseMinModified + ":" + baseSecModified; // time elapsed
    var timeTarget = "20:00:00"; // total time
    var timePercentDiff = (100 * totalSeconds(timeToday) / totalSeconds(timeTarget)).toFixed(2);

    if (baseTime.getHours() == 12) {
        strSession = "Lunch Time."
    }
    else if (baseTime.getHours() > 20) {
        strSession = "Work Dismissed."
    }
    else {
        strSession = "Typical Work Hours"
    }

    $('.time-width').width(timePercentDiff + '%');

    var strContent = strInitTemplate + timeTodayReadCompatible + strSeperator + strSession;
    return $('.local_time_display').text(strContent);
}

$(document).ready(function (event) {
    sal({
        threshold: 0,
        once: false,
    });
});



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
