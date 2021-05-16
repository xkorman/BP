var quill = new Quill('#editor');

$("#FormComment").submit(function(e) {
alert("ok");
var html = JSON.stringify(quill.root.innerHTML);
var titlevalue = document.getElementsByName('title')[0].value;
var category = document.getElementsByName('category')[0].value;
e.preventDefault();
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
       type: "POST",
       url: '../novy_prispevok/',
       data: {
           csrfmiddlewaretoken: csrftoken,
           'text': $(this).serializeArray()[3].value,
           'html': html,
           'title': titlevalue,
           'category': category,

        },
       success: function(data)
       {
           if (data === "Success") {
               alert("Príspevok bol úspešne pridaný.");
               window.location.href = '/forum/';
           } else {
               alert("Niekde nastala chyba, príspevok sa nepodarilo pridať");
           }
       }
     });


});
