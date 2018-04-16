import React from 'react';
import { BrowserRouter, Route } from 'react-router-dom';

import Directory from './Directory';
import Reader from './Reader';


const App = () => (
    <BrowserRouter
        basename="/"
        forceRefresh={true}
    >
        <div>
            <Route exact path="/" component={Directory} />
            <Route sensitive strict path="/dir/:dirPath" component={Directory}/>
            <Route sensitive strict path="/comic/:comicPath/:pageNum?" component={Reader}/>
        </div>
    </BrowserRouter>
);

export default App;
