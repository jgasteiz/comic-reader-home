import React from 'react';
import ReactDOM from 'react-dom';

import ReaderApp from './components/reader-app';

if (document.getElementById('reader')) {
    ReactDOM.render(
        <ReaderApp/>,
        document.getElementById('reader')
    );
}
