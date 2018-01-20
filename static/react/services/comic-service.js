
export default function fetchPageSrc(pageNum, comicPath, callback) {
    const httpRequest = new XMLHttpRequest();
    httpRequest.open('GET', `/api/${comicPath}/${pageNum}/`);
    httpRequest.setRequestHeader('Content-Type', 'application/json');
    httpRequest.onreadystatechange = function () {
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
    updatePageUrl(pageNum, comicPath);
}


function updatePageUrl(pageNum, comicPath) {
    if (typeof (history.pushState) !== "undefined") {
        const obj = {
            title: `Page ${pageNum}`,
            url: `/comic/${comicPath}/${pageNum}/`
        };
        history.pushState(obj, obj.title, obj.url);
    }
}
