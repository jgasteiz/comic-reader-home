import React from 'react';
import ReactDOM from 'react-dom';

import ReaderApp from './components/readerApp';

if (document.getElementById('reader')) {
    ReactDOM.render(
        <ReaderApp/>,
        document.getElementById('reader')
    );
}
