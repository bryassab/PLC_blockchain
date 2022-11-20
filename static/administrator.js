
function newBlock() {
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
            .done(function (data) {
                console.log("archivos subidos")
                console.log(data)
            });
    });

}

function nodeConnect() {
    /* Para obtener el valor */
    var cod = document.getElementById("producto").value;
    var combo = document.getElementById("producto");

    $.ajax({
        url: cod,
        type: "post",
        dataType: "html",
        data: JSON.stringify({
        }),
        cache: false,
        contentType: "application/json",
        processData: false
    })
        .done(function (data) {
            console.log("nodo actualizado")
            console.log(data)
        });
}