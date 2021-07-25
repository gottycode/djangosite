(function ($) {

    $('#lazyLoadLink').on('inview', function (event, isInView) {
        var link = $(this);
        // TODO page->nextpage
        var nextPage = link.data('nextpage');

        function showNextPage(page) {
            $.ajax({
                type: 'post',
                url: '/taskline/lazy_load_tasks/',
                data: {
                    'page': page,
                    'csrfmiddlewaretoken': window.CSRF_TOKEN // from index.html
                },
                success: function (data) {
                    // if there are still more pages to load,
                    // add 1 to the "Load More Posts" link's page data attribute
                    // else hide the link
                    console.log("success");

                    if (data.has_next) {
                        nextPage = nextPage + 1;
                        link.data('nextpage', nextPage);
                        // link.remove();

                    } else {
                        link.hide();
                    }
                    // append html to the posts div
                    $('#tasks').append(data.tasks_html);
                    console.log(isInView);
                },
                error: function (xhr, status, error) {
                    console.log("failed to get next page");
                }
            });
            console.log("ここきたよん");
            console.log(isInView);
            console.log(page);
            console.log(nextPage);
            // if (isInView) {
            //     showNextPage(nextPage);
            // }

        }
        console.log("call showNextPage" + nextPage);
        showNextPage(nextPage);
    });
}(jQuery));
