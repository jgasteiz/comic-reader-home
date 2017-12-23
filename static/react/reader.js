import React from 'react';
import ReactDOM from 'react-dom';

class ComicPage extends React.Component {
    render() {
        const pageSrc = document.getElementById('page').attributes.getNamedItem('data-src').value;
        return (
            <img className="comic-page" src={pageSrc}/>
        );
    }
}

ReactDOM.render(
    <ComicPage/>,
    document.getElementById('page')
);
