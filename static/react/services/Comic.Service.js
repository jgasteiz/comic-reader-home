export default class ComicService {

    /**
     * Get the api url for the given comic path on the given page number.
     *
     * @param pageNum
     * @param comicId
     * @returns {string}
     */
    static getPageSrc(pageNum, comicId) {
        return `/api/page/${comicId}/${pageNum}/`;
    }

    /**
     * Create a bookmark for the given comicPath on the given pageNum.
     *
     * @param comicId
     * @param pageNum
     */
    static bookmarkPage(comicId, pageNum) {
        const payload = JSON.stringify({'comic_id': comicId, 'page_number': pageNum});

        fetch(
            '/api/bookmark/',
            {
                body: payload,
                cache: 'no-cache',
                credentials: 'same-origin',
                headers: {
                    'content-type': 'application/json'
                },
                method: 'POST'
            })
            .then(res => res.json())
            // TODO: better error handling
            .catch(error => alert(error))
            .then(res => alert(`Page ${res['page_number']} bookmarked.`));
    }

    /**
     * Method to fetch a comic page with 5 retries.
     *
     * @param pageNum
     * @param comicId
     * @param callback
     * @param attempts
     */
    static fetchPageImage(pageNum, comicId, callback, attempts=5) {
        if (attempts === 0) {
            alert(`It hasn't been possible to load the page ${pageNum}`);
            return;
        }
        // Preload the next pages.
        ComicService.preloadComicPages(pageNum, comicId);

        fetch(ComicService.getPageSrc(pageNum, comicId))
            .then(_ => callback())
            .catch(error => ComicService.fetchPageImage(pageNum, comicId, callback, attempts - 1));
    }

    /**
     * Preload the next 4 comic pages of the given page number.
     */
    static preloadComicPages(pageNum, comicId) {

        const _loadPage = (pageNum, pageUrl, pagesLeftToLoad) => {
            if (pagesLeftToLoad < 0) {
                return;
            }
            const image = new Image();
            image.onload = () => {
                _loadPage(pageNum + 1, pageUrl, pagesLeftToLoad - 1);
            };
            image.src = `${pageUrl}/${pageNum}/`;
            console.debug(`Preloaded ${pageUrl}, ${pageNum}`);
        };

        const pageUrl = `/api/page/${comicId}`;
        _loadPage(pageNum, pageUrl, 5);
    }

    /**
     * Update the browser url.
     *
     * @param pageNum
     * @param comicId
     */
    static updatePageUrl(pageNum, comicId) {
        if (typeof (history.pushState) !== "undefined") {
            const obj = {
                title: `Page ${pageNum}`,
                url: `/comic/${comicId}/${pageNum}/`
            };
            history.pushState(obj, obj.title, obj.url);
        }
    }
}
