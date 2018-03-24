(function () {
    const expectedCaches = ['page-images'];

    self.addEventListener('install', event => {
        console.log('V2 installing...');

        // Get the comic path which pages we want to cache.
        const comicPath = new URL(location).searchParams.get('comicPath');
        const numPages = new URL(location).searchParams.get('numPages');

        // Generate the list of pages to cache.
        let cacheUrls = [];
        for (let i = 0; i < numPages; i++) {
            cacheUrls.push(`/api/page/${comicPath}/${i}/`)
        }

        event.waitUntil(
            caches.open('page-images').then(function(cache) {
                return cache.addAll(cacheUrls);
            })
        );
    });

    self.addEventListener('activate', event => {
        // delete any caches that aren't in expectedCaches
        // which will get rid of static-v1
        event.waitUntil(
            caches.keys().then(keys => Promise.all(
                keys.map(key => {
                    if (!expectedCaches.includes(key)) {
                        return caches.delete(key);
                    }
                })
            )).then(() => {
                console.log('V2 now ready to handle fetches!');
            })
        );
    });
})();
