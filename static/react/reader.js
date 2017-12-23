import React from 'react';
import ReactDOM from 'react-dom';


const READER = document.getElementById('reader');


class Reader extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            pageSrc: '',
            previousPageUrl: '',
            nextPageUrl: '',
        }
    }

    render() {
        return (
            <div className={"reader reader--" + (this.state.pageSrc ? 'show' : 'loading')}>
                <Navigation
                    nextPageUrl={this.state.nextPageUrl}
                    previousPageUrl={this.state.previousPageUrl}
                />
                <ComicPage
                    pageSrc={this.state.pageSrc}
                />
                <BatmanSpinner/>
            </div>
        );
    }

    componentDidMount() {
        this.getImageSrc();
    }

    getImageSrc() {
        const component = this;

        const httpRequest = new XMLHttpRequest();
        httpRequest.open('GET', `/api/${READER.dataset.comicPath}/${READER.dataset.comicPage}/`);
        httpRequest.setRequestHeader('Content-Type', 'application/json');
        httpRequest.onreadystatechange = function () {
            if (httpRequest.readyState === XMLHttpRequest.DONE) {
                if (httpRequest.status === 200) {
                    component.setState({
                        pageSrc: JSON.parse(this.response)['page_src'],
                        nextPageUrl: JSON.parse(this.response)['next_page'],
                        previousPageUrl: JSON.parse(this.response)['previous_page'],
                    });
                } else {
                    alert('There was a problem with the request.');
                }
            }
        };
        httpRequest.send();
    }
}


class Navigation extends React.Component {
    render() {
        return (
            <nav className="page-navigation">
                <a className="btn btn-light"
                   href={this.props.previousPageUrl}
                >Previous page</a>
                <a className="btn btn-light"
                   href={this.props.nextPageUrl}
                >Next page</a>
            </nav>
        );
    }
}


class BatmanSpinner extends React.Component {
    render() {
        return (
            <div className="batman-spinner">
                <img src="/static/img/batman.png"/>
            </div>
        )
    }
}


class ComicPage extends React.Component {
    render() {
        return (
            <img className="comic-page"
                 src={this.props.pageSrc}
            />
        );
    }
}

ReactDOM.render(
    <Reader/>,
    document.getElementById('reader')
);
