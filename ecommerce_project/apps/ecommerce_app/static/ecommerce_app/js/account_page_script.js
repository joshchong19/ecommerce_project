$(document).ready(function() {
    $('.vertnav-item').mouseenter(function() {
        $(this).css('background-color', '#dfdfdf')
    });
    
    $('.vertnav-item').mouseleave(function() {
        $(this).css('background-color', '')
    })
})