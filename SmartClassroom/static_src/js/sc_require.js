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
    percentPosition: true,
});

// ! Update View ACcording to Layout Changes Since Card is at Absolute Position
$('.quick-actions-handler').click(function (event) {
    setTimeout(function ()
    {
        $('.dashboard-grid').isotope("arrange");
    }, 260);
});