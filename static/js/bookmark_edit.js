function bookmark_edit() {

    /*
    Because this function handles click events on an edit link, the variable this refers
    to the edit link itself. Wrapping it in the jQuery $() function and calling parent()
    returns the parent of the edit link, which is the <li> element of the bookmark
    */
    var item = $(this).parent();
    var url = item.find(".title").attr("href");

    /*
    Next, we use the load() method to put an editing form in place of the bookmark's
    HTML. This time we are calling load() with two extra arguments in addition to the
    URL; load() takes two optional parameters:
    • An object of key/value pairs if we are sending a POST request. Since we get
        the edit form from the server-side view using a GET request, we pass null for
        this parameter.
    • A function that is called when jQuery finishes loading the URL into the
        selected element. The function we are passing attaches bookmark_save
        (which we are going to write next) to the form that we've just retrieved.
    */
    item.load("/save/?ajax&url=" + escape(url), null, function () {
        $("#save-form").submit(bookmark_save);
    });

    /*
    Finally, the function returns false to tell the browser not to follow the edit link.
    */
    return false;
}

/*
Now we need to attach the bookmark_edit function to the event of clicking an edit
link using $(document).ready() :
*/
$(document).ready(function () {
    $("ul.bookmarks .edit").click(bookmark_edit);
});

/*
function to save bookmark with ajax
*/
function bookmark_save() {
    /*
    this refers to the edit form because we are handling the event
    of submitting a form.
    */
    var item = $(this).parent();

    /*
    retrieves the
    updated data from the form, using the ID of each form field and the val() method.
    */
    var data = {
        url: item.find("#id_url").val(),
        title: item.find("#id_title").val(),
        tags: item.find("#id_tags").val(),
        csrfmiddlewaretoken: item.find('input[name=csrfmiddlewaretoken]').val()
    };

    /*
    Then it uses a method called $.post() to send data back to the server.
    */
    $.post("/save/?ajax", data, function (result) {
        if (result != "failure") {
            item.before($("li", result).get(0));
            item.remove();
            $("ul.bookmarks .edit").click(bookmark_edit);
        }
        else {
            alert("Failed to validate bookmark before saving.");
        }
    });

    /*
    returns false to prevent the browser from submitting the form.
    */
    return false;
}