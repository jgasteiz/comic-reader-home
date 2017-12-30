import React from 'react';
import ReactDOM from 'react-dom';


const READER = document.getElementById('reader');


class Reader extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            pageSrc: '',
            comicPath: READER.dataset.comicPath,
            currentPage: parseInt(READER.dataset.comicPage, 10),
            hasPreviousPage: false,
            hasNextPage: true,
        };

        // Bind the event handlers to `this`
        this.previousPageHandler = this.previousPageHandler.bind(this);
        this.nextPageHandler = this.nextPageHandler.bind(this);
    }

    render() {
        return (
            <div className={"reader reader--" + (this.state.pageSrc ? 'show' : 'loading')}>
                <Navigation
                    previousPageHandler={this.previousPageHandler}
                    nextPageHandler={this.nextPageHandler}
                    hasPreviousPage={this.state.hasPreviousPage}
                    hasNextPage={this.state.hasNextPage}
                />
                <ComicPage
                    pageSrc={this.state.pageSrc}
                />
                <Navigation
                    previousPageHandler={this.previousPageHandler}
                    nextPageHandler={this.nextPageHandler}
                    hasPreviousPage={this.state.hasPreviousPage}
                    hasNextPage={this.state.hasNextPage}
                />
                <BatmanSpinner/>
            </div>
        );
    }

    previousPageHandler() {
        if (!this.state.hasPreviousPage) {
            return;
        }
        this.setState({
            pageSrc: '',
        });
        this.fetchPageSrc(this.state.currentPage - 1);
    }

    nextPageHandler() {
        if (!this.state.hasNextPage) {
            return;
        }
        this.setState({
            pageSrc: '',
        });
        this.fetchPageSrc(this.state.currentPage + 1);
    }

    updatePageUrl(pageNum) {
        if (typeof (history.pushState) !== "undefined") {
            const obj = {
                title: `Page ${pageNum}`,
                url: `/comic/${this.state.comicPath}/${pageNum}/`
            };
            history.pushState(obj, obj.title, obj.url);
        }
    }

    fetchPageSrc(pageNum) {
        const component = this;

        const httpRequest = new XMLHttpRequest();
        httpRequest.open('GET', `/api/${this.state.comicPath}/${pageNum}/`);
        httpRequest.setRequestHeader('Content-Type', 'application/json');
        httpRequest.onreadystatechange = function () {
            if (httpRequest.readyState === XMLHttpRequest.DONE) {
                if (httpRequest.status === 200) {
                    component.setState({
                        pageSrc: JSON.parse(this.response)['page_src'],
                        currentPage: pageNum,
                        hasPreviousPage: JSON.parse(this.response)['has_previous_page'],
                        hasNextPage: JSON.parse(this.response)['has_next_page'],
                    });
                } else {
                    alert('There was a problem with the request.');
                }
            }
        };
        httpRequest.send();
        this.updatePageUrl(pageNum);
    }

    componentDidMount() {
        const component = this;
        this.fetchPageSrc(this.state.currentPage);

        // Listen for key events and go to next/previous page when
        // pressing certain keys.
        document.addEventListener('keydown', function(ev) {
            const keyName = ev.key;
            if (keyName === 'ArrowRight') {
                component.nextPageHandler();
                ev.preventDefault();
            } else if (keyName === 'ArrowLeft') {
                component.previousPageHandler();
                ev.preventDefault();
            }
        });
    }
}


class Navigation extends React.Component {
    render() {
        return (
            <nav className="page-navigation">
                <a className={"btn btn-light page-navigation-item--" + (this.props.hasPreviousPage ? 'show' : 'hidden')}
                   onClick={this.props.previousPageHandler}
                >Previous page</a>
                <a className={"btn btn-light page-navigation-item--" + (this.props.hasNextPage ? 'show' : 'hidden')}
                   onClick={this.props.nextPageHandler}
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

if (document.getElementById('reader')) {
    ReactDOM.render(
        <Reader/>,
        document.getElementById('reader')
    );
}
