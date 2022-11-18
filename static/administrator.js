$(function () {
    $("#formUpload").on("submit", function (e) {
        e.preventDefault();
        var formData = new FormData(document.getElementById("formUpload"));
        $.ajax({
            url: "http://127.0.0.1:5001/mine_block",
            type: "post",
            dataType: "html",
            data: formData,
            cache: false,
            contentType: false,
            processData: false
        })
            .done(function (res) {
                console.log("archivos subidos")
            });
    });
});
