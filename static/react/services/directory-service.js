export default class DirectoryService {

    static getDirectoryDetails(directoryPath=null, callback) {
        fetch(directoryPath ? `/api/directory/${directoryPath}/` : '/api/directory/')
            .then(res => res.json())
            .then(res => callback(res));
    }
}
