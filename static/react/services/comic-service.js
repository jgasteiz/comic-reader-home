

export default class ComicService {

    static fetchPageSrc(pageNum, comicPath, callback) {
        const httpRequest = new XMLHttpRequest();
        httpRequest.open('GET', `/api/comic/${comicPath}/${pageNum}/`, true);
        httpRequest.setRequestHeader('Content-Type', 'application/json');
        httpRequest.onload = function () {
            if (httpRequest.readyState === XMLHttpRequest.DONE) {
                if (httpRequest.status === 200) {
                    const jsonResponse = JSON.parse(this.response);
                    callback({
                        pageSrc: jsonResponse['page_src'],
                        currentPage: pageNum,
                        hasPreviousPage: jsonResponse['has_previous_page'],
                        hasNextPage: jsonResponse['has_next_page'],
                        numPages: jsonResponse['num_pages']
                    });
                }
            }
        };
        httpRequest.send();
        ComicService.updatePageUrl(pageNum, comicPath);
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
