// ! Janrey "CodexLink" Licas Required Code for SmartClassrooms
// * 01/24/2019

// Mansory Dashboard View
$('.dashboard-grid').masonry({
    itemSelector: '.dashboard-item', // use a separate class for itemSelector, other than .col-
    percentPosition: true,
    transitionDuration: '0.3s',
    resize: true,
});