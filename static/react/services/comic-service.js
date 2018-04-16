export default class ComicService {

    static getPageSrc(pageNum, comicPath) {
        return `/api/page/${comicPath}/${pageNum}/`;
    }

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

    static updatePageUrl(pageNum, comicPath) {
        if (typeof (history.pushState) !== "undefined") {
            const obj = {
                title: `Page ${pageNum}`,
                url: `/comic/${comicPath}/${pageNum}/`
            };
            history.pushState(obj, obj.title, obj.url);
        }
    }
}
