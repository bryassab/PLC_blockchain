var host = 'http://127.0.0.1:5001'

$.ajax({
    url: host + '/get_chains',
    type: 'GET',
    dataType: "JSON",
    success: function (respuesta) {
        console.log(respuesta.chain);
        respuestaGetChains(respuesta.chain);
    }, error: function (e) {
        console.log(e);
        alert("Algo salió mal");
    }, error: function (e) {
        console.log(e);
        alert("Algo salió mal");
    }
});

$(document).ready(function () {
    respuestaGetChains();
})


function respuestaGetChains(items) {
    let getChains = `<table class="table table-hover" >
                    <th> NAME </th>
                    <th> DESCRIPTION </th>
                    <th> DATE </th>
                    <th> PDF</th>
                    <th> COMPRESSED</th>`;
    for (let i = 1; i < items.length; i++) {
        getChains += `<tr>`;
        getChains += `<td>${items[i].name}</td>`;
        getChains += `<td>${items[i].description}</td>`;
        getChains += `<td>${items[i].timestamp}</td>`;
        getChains += `<td id="pdf"><a target="_blank" href="http://localhost:5001/public/pdf/${items[i].path_pdf.slice(12, 34)}">${items[i].path_pdf.slice(12, 34)}</a></td > `;
        getChains += `<td id="rar"><a href="http://localhost:5001/public/compressed/${items[i].path_compressed.slice(19, 40)}" download="${items[i].path_compressed.slice(19, 40)}">${items[i].path_compressed.slice(19, 40)}</a></td > `;
        getChains += `</tr > `;
    }
    $("#resultadoCli").append(getChains);
    getChains = `</table > `;
}