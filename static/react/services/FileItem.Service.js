export default class FileItemService {

    /**
     * Fetch a FileItem details.
     *
     * @param fileItemId
     * @param callback
     */
    static getFileItemDetails(fileItemId=null, callback) {
        fetch(fileItemId ? `/api/fileitems/${fileItemId}/` : '/api/fileitems/')
            .then(res => res.json())
            .then(res => {
                // If there was a fileItemId, the API will return an object,
                // which is what we always want to return here.
                if (fileItemId) {
                    return res;
                }
                // Otherwise, it'll be a list. In that case, return the first item.
                return res[0];
            })
            .then(res => callback(res));
    }

    /**
     * Search FileItems given a query.
     *
     * @param query
     * @param callback
     */
    static getFileItemSearchResults(query, callback) {
        fetch(`/api/fileitems/?q=${query}`)
            .then(res => res.json())
            .then(res => callback(res));
    }

    /**
     * Delete a bookmark from a comic.
     *
     * @param comicId
     */
    static deleteBookmark(comicId) {
        const payload = JSON.stringify({'comic_id': comicId});

        fetch(
            '/api/delete-bookmark/',
            {
                body: payload,
                cache: 'no-cache',
                credentials: 'same-origin',
                headers: {
                    'content-type': 'application/json'
                },
                method: 'POST'
            })
            // TODO: better error handling
            .catch(error => alert(error))
            .then(_ => {
                window.location.reload();
            });
    }
}
