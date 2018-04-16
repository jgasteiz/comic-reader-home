export default class DirectoryService {

    /**
     * Fetch a directory details.
     *
     * @param directoryPath
     * @param callback
     */
    static getDirectoryDetails(directoryPath=null, callback) {
        fetch(directoryPath ? `/api/directory/${directoryPath}/` : '/api/directory/')
            .then(res => res.json())
            .then(res => callback(res));
    }
}
