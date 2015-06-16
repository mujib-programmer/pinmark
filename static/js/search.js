$(document).ready(function () {
    $("#search-form").submit(search_submit);
});

function search_submit() {
    /*
    The function first gets the query string from the text field using the
    val() method.
    */
    var query = $("#id_query").val();

    /*
    We use the load() method to get search results from the search_page view,
    and insert the search results into the #search-results div. The request
    URL is constructed by first calling encodeURIComponent on query , which
    works exactly like the urlencode filter we used in Django templates. Calling
    this function is important to ensure that the constructed URL remains valid
    even if the user enters special characters into the text field such as & . After
    escaping query , we concatenate it with /search/?ajax&query= . This URL
    invokes the search_page view and passes the GET variables ajax and query
    to it. The view returns search results, and the load() method in turn loads
    the results into the #search-results div.
    */
    $("#search-results").load(
        "/search/?ajax&query=" + encodeURIComponent(query)
    );

    /*
    We return false from the function to tell the browser not to submit the
    form after calling our handler. If we don't return false in the function, the
    browser will continue to submit the form as usual, and we don't want that.
    */
    return false;
}

