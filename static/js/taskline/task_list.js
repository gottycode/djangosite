var isStop = false;

(function ($) {
    $('#bottomOfList').on('inview', function (event, isInView) {
        console.log("called bottomOfList inview")
        if (!isInView) {
            isStop = true;
            console.log("set isStop = True")
        } else {
            isStop = false;
            $('#lazyLoadMark').show();
            console.log("set isStop = False")
        }
    });

    $('#lazyLoadMark').on('inview', function (event, isInView) {
        console.log("called lazyLoadMark inview")

        if (!isStop) {
            // 次のページ読み込み、表示
            showNextPage(isInView);
            // イベント発火のため表示/非表示切り替え
            if (isInView) {
                $(this).hide();
            } else {
                $(this).show();
            }
        }
    });
    function sleep(waitMsec) {
        var startMsec = new Date();

        // 指定ミリ秒間だけループさせる（CPUは常にビジー状態）
        while (new Date() - startMsec < waitMsec);
    }
    function showNextPage(/*page,*/ isInView) {
        var link = $('#lazyLoadMark');
        var nextPage = link.data('nextpage');
        var sort = link.data('sort');
        console.log("call showNextPage:" + nextPage + isInView);
        // sleep(2000);
        $.ajax({
            type: 'post',
            url: '/taskline/lazy_load_tasks/',
            async: false,
            data: {
                'page': nextPage,
                'sort': sort,
                'csrfmiddlewaretoken': window.CSRF_TOKEN // from index.html
            },
            success: function (data) {
                // if there are still more pages to load,
                // add 1 to the "Load More Posts" link's page data attribute
                // else hide the link
                console.log("success request");
                console.log("has next:" + data.has_next);
                // console.log(data.tasks_html);
                if (data.has_next) {
                    // #lazyLoadMarkのnextpage属性に次ページを書き込み
                    nextPage = nextPage + 1;
                    link.data('nextpage', nextPage);
                } else {
                    link.hide();
                    $('#bottomOfList').hide();
                }
                // append html to the posts div
                var $taskhtml = data.tasks_html;
                $('#tasks').append($taskhtml);
            },
            error: function (xhr, status, error) {
                console.log("failed to get next page");
            }
        });
        console.log(isInView);
        console.log("end showNextPage:" + nextPage + isInView);

    }
    $('#sort-id').on('click', function (event) {
        console.log("sort-id clicked!");
        $('#tasks').empty();
        $('#lazyLoadMark').show();
        $('#lazyLoadMark').data('nextpage', 1);
        $('#bottomOfList').show();
        var sort = $('#lazyLoadMark').data('sort');
        if (sort == "id") {
            $('#lazyLoadMark').data('sort', "-id");
        } else {
            $('#lazyLoadMark').data('sort', "id");
        }
    });
    $('#sort-name').on('click', function (event) {
        console.log("sort-name clicked!");
        $('#tasks').empty();
        $('#lazyLoadMark').show();
        $('#lazyLoadMark').data('nextpage', 1);
        $('#bottomOfList').show();
        var sort = $('#lazyLoadMark').data('sort');
        if (sort == "task_name") {
            $('#lazyLoadMark').data('sort', "-task_name");
        } else {
            $('#lazyLoadMark').data('sort', "task_name");
        }
    });

}(jQuery));
