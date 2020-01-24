// ! Janrey "CodexLink" Licas Required Code for SmartClassrooms
// * 01/24/2019

// Mansory Dashboard View
$('.dashboard-grid').isotope({
    itemSelector: '.dashboard-item',
    layoutMode: 'packery',
    packery: {
        columnWidth: '.dashboard-item',
        horizontal: false
    },
    percentPosition: true,
});

$('.quick-actions-handler').click(function (event) {
    setTimeout(function ()
    {
        $('.dashboard-grid').isotope("arrange");
    }, 200);
});