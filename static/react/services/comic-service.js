

export default class ComicService {

    static getPageSrc(pageNum, comicPath) {
        return `/api/page/${comicPath}/${pageNum}/`;
    }

    static bookmarkPage(pageNum, comicPath, callback) {
        const httpRequest = new XMLHttpRequest();
        const payload = JSON.stringify({'comic_path': comicPath, 'page_num': pageNum});

        httpRequest.open('POST', '/api/bookmark/', true);
        httpRequest.setRequestHeader('Content-Type', 'application/json');
        httpRequest.onreadystatechange = function () {
            if (httpRequest.readyState === XMLHttpRequest.DONE) {
                if (httpRequest.status === 200) {
                    const jsonResponse = JSON.parse(this.response);
                    alert(`Page ${jsonResponse['page_num']} bookmarked.`);
                    // TODO: run the callback with the right args.

                } else if (httpRequest.status === 400) {
                    const jsonResponse = JSON.parse(this.response);
                    alert(jsonResponse);
                }
            }
        };
        httpRequest.send(payload);
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
        const service = this;
        const httpRequest = new XMLHttpRequest();
        const url = ComicService.getPageSrc(pageNum, comicPath);

        httpRequest.open('GET', url, true);
        httpRequest.onreadystatechange = function () {
            if (httpRequest.readyState === XMLHttpRequest.DONE) {
                if (httpRequest.status === 200) {
                    callback();
                } else {
                    // Keep trying
                    service.fetchPageImage(pageNum, comicPath, callback, attempts - 1);
                }
            }
        };
        httpRequest.send();
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
