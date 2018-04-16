import React from 'react';
import ReactDOM from 'react-dom';

import App from './components/App';


if (document.getElementById('reader-app')) {
    ReactDOM.render(<App/>, document.getElementById('reader-app'));
}
