var host = 'http://127.0.0.1:5001/'

function peticionGet() {
    $.ajax({
        url: host + 'get_chains',
        type: 'Get',
        dataTyoe: "JSON",
        succes: function (respuesta) {
            console.log(respuesta);
            respuestaGetChains(respuesta);
            console.log("funciona")
        }, error: function (e) {
            console.log(e);

        }

    })
}

$(document).ready(function () {
    peticionGet();
})

function respuestaGetChains(items) {
    let getChains = `<table BORDER CELLPADDING=2 BORDERCOLOR='#7c65b1'><th scope='col'> ID </th><th> NAME </th><th> DATE </th><th> PROGRAM </th>`;
    for (let i = 0; i < items.length; i++) {
        getChains += `<tr>`;
        getChains += `<td>${items[i].idClient}</td>`;
        getChains += `<td>${items[i].email}</td>`;
        getChains += `<td>${items[i].name}</td>`;
        getChains += `<td>${items[i].age}</td>`;
        getChains += `<td> <button onclick="finishActuCli('${items[i].email}','${items[i].password}','${items[i].name}', ${items[i].age} )" style="background-color:#7c65b1; border-color:#563856; color:white;">Change</button></td>`;
        getChains += `<td> <button onclick="borrarInformacionCli(${items[i].idClient})" style="background-color:#7c65b1; border-color:#563856; color:white;">Delete</button></td>`;
        getChains += `</tr>`;
    }
    $("#resultadoCli").append(getChains);
    getChains = `</table>`;
}