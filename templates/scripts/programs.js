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
                    <th> ID </th>
                    <th> NAME </th>
                    <th> DATE </th>
                    <th> PDF</th>`;
    for (let i = 1; i < items.length; i++) {
        getChains += `<tr>`;
        getChains += `<td>${items[i].name}</td>`;
        getChains += `<td>${items[i].description}</td>`;
        getChains += `<td>${items[i].timestamp}</td>`;
        getChains += `<td> si tuvira un codigo ese va a aca</td>`;
        getChains += `</tr>`;
    }
    $("#resultadoCli").append(getChains);
    getChains = `</table>`;
}