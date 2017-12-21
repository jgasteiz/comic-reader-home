(function () {

    function goToNextPage() {
        if (reader.nextPageUrl) {
            window.location = reader.nextPageUrl;
        }
    }

    function goToPreviousPage() {
        if (reader.previousPageUrl) {
            window.location = reader.previousPageUrl;
        }
    }

    $(document).keydown(function(e) {
        // left, up: previous page
        if (e.which === 37 || e.which === 38) {
            goToPreviousPage();
        }
        else if (e.which === 39 || e.which === 40) {
            goToNextPage();
        }
    });

    var $comicPages = $(".comic-page");
    $comicPages.on("swipeleft", goToNextPage);
    $comicPages.on("swiperight", goToPreviousPage);
})();
