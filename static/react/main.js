import React from 'react';
import ReactDOM from 'react-dom';

import Reader from './components/reader';

if (document.getElementById('reader')) {
    ReactDOM.render(
        <Reader/>,
        document.getElementById('reader')
    );
}
