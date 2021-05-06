var quill = new Quill('#editor');

$("#FormComment").submit(function(e) {

var about = document.querySelector('input[name=text]');
var html = JSON.stringify(quill.root.innerHTML);
about.value = JSON.stringify(quill.getContents());
var titlevalue = document.getElementById('title').value;
e.preventDefault();
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    const input = window.location.href.match(/editovat_prispevok\/[0-9]+/)[0];

$.ajax({
       type: "POST",
       url: '../edit_comment_back',
       data: {
           csrfmiddlewaretoken: csrftoken,
           'text': $(this).serializeArray()[2].value,
           'html': html,
           'title': titlevalue,
           'post_id': input.split('/')[1],

        },
       success: function(data)
       {
           alert("Zmenene");
           window.location.href = '/forum/';
       }
     });


});
