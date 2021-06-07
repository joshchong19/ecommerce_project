$(document).ready(function(){

    // $('.dropbtnMen').click(function() {
    //     $('#myDropdownMens').toggle();
    // })

    // $(document).click(function(e) {
    //     if(!$(e.target).closest('.dropbtnMen').length) {
    //         $('#myDropdownMens').hide();
    //     }
    // })

    // $('.dropbtnWomen').click(function() {
    //     $('#myDropdownWomens').toggle();
    // })

    // $(document).click(function(e) {
    //     if(!$(e.target).closest('.dropbtnWomen').length) {
    //         $('#myDropdownWomens').hide();
    //     }
    // })

    $('.dropbtnMen').mouseover(function() {
            $('#myDropdownMens').show()
    });

    $(document).mouseover(function(e) {
        if(!$(e.target).closest('.dropbtnMen').length && !$(e.target).closest('#myDropdownMens').length) {
            $('#myDropdownMens').hide();
        }
    });


    $('.dropbtnWomen').mouseover(function() {
        $('#myDropdownWomens').show();
    });

    $(document).mouseover(function(e) {
        if(!$(e.target).closest('.dropbtnWomen').length && !$(e.target).closest('#myDropdownWomens').length) {
            $('#myDropdownWomens').hide();
        }
    });


    $('.dropbtnUser').mouseover(function() {
        $('#myDropdownUsers').show()
    });

    $(document).mouseover(function(e) {
        if(!$(e.target).closest('.dropbtnUser').length && !$(e.target).closest('#myDropdownUsers').length) {
            $('#myDropdownUsers').hide();
        }
    });



    $('.navitem').hover(
        function() {
            $(this).addClass("hover");
        },
        function() {
            $(this).removeClass("hover");
        });
});