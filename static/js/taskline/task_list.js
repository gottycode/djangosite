(function ($) {

    $('#lazyLoadLink').on('inview', function (event, isInView) {
        console.log("called inview")
        var link = $(this);
        // TODO page->nextpage
        var nextPage = link.data('nextpage');

        showNextPage(/*nextPage,*/ isInView);
    });
    function sleep(waitMsec) {
        var startMsec = new Date();

        // 指定ミリ秒間だけループさせる（CPUは常にビジー状態）
        while (new Date() - startMsec < waitMsec);
    }
    function showNextPage(/*page,*/ isInView) {
        var link = $('#lazyLoadLink');
        var nextPage = link.data('nextpage');
        console.log(typeof (nextPage));
        // var nextPage = page + 1;
        console.log("call showNextPage:" + nextPage + isInView);
        sleep(2000);
        $.ajax({
            type: 'post',
            url: '/taskline/lazy_load_tasks/',
            async: false,
            data: {
                'page': nextPage,
                'csrfmiddlewaretoken': window.CSRF_TOKEN // from index.html
            },
            success: function (data) {
                // if there are still more pages to load,
                // add 1 to the "Load More Posts" link's page data attribute
                // else hide the link
                console.log("success");
                console.log(data.has_next);
                console.log(data.tasks_html);
                if (data.has_next) {
                    nextPage = nextPage + 1;
                    link.data('nextpage', nextPage);
                    // link.remove();

                } else {
                    link.hide();
                }
                // append html to the posts div
                var $taskhtml = data.tasks_html;
                $('#tasks').append($taskhtml);
                // console.log(isInView);
            },
            error: function (xhr, status, error) {
                console.log("failed to get next page");
            }
        });
        console.log(isInView);
        if (isInView) {
            // sleep(1500);
            showNextPage(isInView);
        }
        console.log("end showNextPage:" + nextPage + isInView);

    }
}(jQuery));
