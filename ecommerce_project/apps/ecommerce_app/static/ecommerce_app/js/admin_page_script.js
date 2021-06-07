$(document).ready(function() {

    // $('.colorinput').on('change', function() {
    //     var result = "false";
    //     var value = $(this).val();
    //     if (value === "") {result = "false"};
    //     if (value === "inherit") {result =  "false"};
    //     if (value === "transparent") {result =  "false"};

    //     var image = $(document).append("<img>");
    //     image.style.color = "rgb(0, 0, 0)";
    //     image.style.color = value;
    //     if (image.style.color !== "rgb(0, 0, 0)") {result =  "true"};
    //     image.style.color = "rgb(255, 255, 255)";
    //     image.style.color = value;
    //     if (image.style.color !== "rgb(255, 255, 255)") {result = "true"};

    //     $('.hiddencolor').val(result)
    //     console.log(result)
    // })

    // $('.colorinput').on('input', function() {
    //     $('.hiddencolor').val(validTextColor(this.value))
    // })



    function validTextColor(stringToTest) {
        if (stringToTest === "") {return "false"};
        if (stringToTest === "inherit") {return "false"};
        if (stringToTest === "transparent") {return "false"};

        var image = document.createElement("img");
        image.style.color = "rgb(0, 0, 0)";
        image.style.color = stringToTest;
        if (image.style.color != "rgb(0, 0, 0)") {return "true"};
        image.style.color = "rgb(255, 255, 255)";
        image.style.color = stringToTest;
        if (image.style.color != "rgb(255, 255, 255)") {return "true"};
    }

    document.getElementById("colorinput").addEventListener("input", function() {
        document.getElementById("hiddencolor").value = validTextColor(this.value);
    });

    document.getElementById("imageuploadFile").addEventListener("change", function() {
        if (document.getElementById("imageuploadFile").files.length > 0) {
            document.getElementById("hiddenfile").value = "true"
        }
    });
})