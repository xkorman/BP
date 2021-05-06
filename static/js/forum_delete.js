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
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    var id = element.id;
    // console.log("OK");
    // alert(id);
    $.ajax({
       type: "POST",
       url: '../delete_comment',
       data: {
           csrfmiddlewaretoken: csrftoken,
           'id': id,
        },
       success: function(data)
       {
           alert("Vas prispevok bol zmazany!")
           window.location.reload()
       },
       error: function() {
          alert("Chyba pri mazani prispevku - nahlaste chybu spravcovi, dakujeme.")
       }
     });

    //make call ajax to delete it
}