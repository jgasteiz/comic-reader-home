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
}
