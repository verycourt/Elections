var fileInput = document.querySelector('#file');

fileInput.addEventListener('change', function() {
    var reader = new FileReader();
    reader.addEventListener('load', function() {
        //alert('Contenu du fichier "' + fileInput.files[0].name + '" :\n\n' + reader.result);
        alert(data.data[0][0]);
    });
    reader.readAsText(fileInput.files[0]);
});