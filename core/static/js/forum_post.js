var quill = new Quill('#editor');

$("#FormComment").submit(function(e) {

var about = document.querySelector('input[name=text]');
var html = JSON.stringify(quill.root.innerHTML)
about.value = JSON.stringify(quill.getContents());


// console.log("Submitted", $(form).serialize(), $(form).serializeArray());
// alert("Submitted", $(form).serialize(), $(form).serializeArray())
e.preventDefault(); // avoid to execute the actual submit of the form.

var csrftoken = $("[name=csrfmiddlewaretoken]").val();
// console.log("Submitted",about.value,"\n", $(form).serialize(),'\n',$(form).serializeArray()[1].value, )
    const input = window.location.href.match(/prispevok\/[0-9]+/)[0]

$.ajax({
       type: "POST",
       url: '../send_comment',
       data: {
           csrfmiddlewaretoken: csrftoken,
           'text': $(this).serializeArray()[1].value,
           'html': html,
           'post_id': input.split('/')[1],
       // {#    'offset': currentResult,#}
       // {#    'id': "{{ contact.id }}",#}
        },
       success: function(data)
       {
           window.location.reload()
       }
     });


});
