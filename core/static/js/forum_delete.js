function openModal(element) {
    var id = element.id

    var myModal = new bootstrap.Modal(document.getElementById('exampleModal'), {
      keyboard: true
    })
    myModal.toggle();
    var yesbutton = document.getElementById('yesButton');
    yesbutton.id = id.split('-')[1];
}

function deleteIt(element) {
    var id = element.id

    //make call ajax to delete it
}