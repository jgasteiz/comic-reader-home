import React from "react";
import ReactDOM from 'react-dom';

import Navigation from './navigation';

/**
 * This component is for displaying the page <img> element.
 */
export default class ComicPage extends React.Component {
    constructor(props) {
        super(props);

        // Bind the event handlers to `this`
        this.previousPageHandler = this.previousPageHandler.bind(this);
        this.nextPageHandler = this.nextPageHandler.bind(this);
    }

    render() {
        return (
            <div ref="pageContainer">
                <img className="comic-page"
                     ref="pageImage"
                     src={this.props.pageSrc}
                     onClick={this.props.onPageClickHandler}
                />
                <Navigation
                    previousPageHandler={this.previousPageHandler}
                    nextPageHandler={this.nextPageHandler}
                    hasPreviousPage={this.props.hasPreviousPage}
                    hasNextPage={this.props.hasNextPage}
                />
            </div>
        );
    }

    /**
     * Scroll the page up if there's page to scroll before going to the
     * previous page.
     */
    previousPageHandler() {
        const pageHeight = this.refs.pageImage.height;

        // If we can still scroll up, scroll up 1/3rd of the page.
        if (window.scrollY > 0) {
            const newScrollYPosition = window.scrollY - pageHeight / 3;
            window.scrollTo({
                top: newScrollYPosition,
                behavior: "smooth"
            });
        }
        // Otherwise, previous page.
        else {
            this.props.previousPageHandler();
        }
    }

    /**
     * Scroll the page down if there's page to scroll before going to the
     * next page.
     */
    nextPageHandler() {
        const currentScroll = window.scrollY + window.innerHeight;
        const pageHeight = this.refs.pageImage.height;

        // If we can still scroll down, scroll down 1/3rd of the page.
        if (currentScroll + 10 < pageHeight) {
            const newScrollYPosition = window.scrollY + pageHeight / 3;
            window.scrollTo({
                top: newScrollYPosition,
                behavior: "smooth"
            });
        }
        // Otherwise, next page.
        else {
            this.props.nextPageHandler();
        }
    }
}
