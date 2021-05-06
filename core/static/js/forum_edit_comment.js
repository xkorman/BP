var quill = new Quill('#editor');

$("#FormComment").submit(function(e) {

var html = JSON.stringify(quill.root.innerHTML);
e.preventDefault();
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    const input = window.location.href.match(/editovat_komentar\/[0-9]+/)[0];

$.ajax({
       type: "POST",
       url: '../edit_comment_back2',
       data: {
           csrfmiddlewaretoken: csrftoken,
           'text': $(this).serializeArray()[1].value,
           'html': html,
           'post_id': input.split('/')[1],

        },
       success: function(data)
       {
           alert("Zmenene");
           window.location.href = '/forum/';
       }
     });


});
