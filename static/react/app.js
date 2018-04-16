import React, { Fragment } from 'react';
import ReactDOM from 'react-dom';

import { BrowserRouter, Route, Switch, Link } from 'react-router-dom';

import Directory from './components/directory';
import Reader from './components/reader';


if (document.getElementById('reader-app')) {
    ReactDOM.render(
        <BrowserRouter>
            <div>
                <Route exact path="/" component={Directory} />
                <Route path="/dir/:dirPath/" component={Directory}/>
                <Route path="/comic/:comicPath/" component={Reader}/>
            </div>
        </BrowserRouter>,
        document.getElementById('reader-app')
    );
}
