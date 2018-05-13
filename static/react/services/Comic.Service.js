export default class ComicService {

    /**
     * Get the api url for the given comic path on the given page number.
     *
     * @param pageNum
     * @param comicPath
     * @returns {string}
     */
    static getPageSrc(pageNum, comicPath) {
        return `/api/page/${comicPath}/${pageNum}/`;
    }

    /**
     * Create a bookmark for the given comicPath on the given pageNum.
     *
     * @param pageNum
     * @param comicPath
     */
    static bookmarkPage(pageNum, comicPath) {
        const payload = JSON.stringify({'comic_path': comicPath, 'page_num': pageNum});

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
            .then(res => alert(`Page ${res['page_num']} bookmarked.`));
    }

    /**
     * Method to fetch a comic page with 5 retries.
     * 
     * @param pageNum
     * @param comicPath
     * @param callback
     * @param attempts
     */
    static fetchPageImage(pageNum, comicPath, callback, attempts=5) {
        if (attempts === 0) {
            alert(`It hasn't been possible to load the page ${pageNum}`);
            return;
        }
        // Preload the next pages.
        ComicService.preloadComicPages(pageNum, comicPath);

        fetch(ComicService.getPageSrc(pageNum, comicPath))
            .then(_ => callback())
            .catch(error => ComicService.fetchPageImage(pageNum, comicPath, callback, attempts - 1));
    }

    /**
     * Preload the next 4 comic pages of the given page number.
     */
    static preloadComicPages(pageNum, comicPath) {
        for (let i = pageNum; i < pageNum + 4; i++) {
            const imagePath = `/api/page/${comicPath}/${i}/`;
            new Image().src = imagePath;
            console.log(`Preloaded ${imagePath}`);
        }
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
