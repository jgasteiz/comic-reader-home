import React from "react";

import Navigation from './Navigation';

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
            <div className="comic-page-container">
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
        // TODO: improve this, not good yet.
        // const pageHeight = this.refs.pageImage.height;
        //
        // // If we can still scroll up, scroll up 1/3 of the page.
        // if (window.scrollY > 0) {
        //     const newScrollYPosition = window.scrollY - pageHeight / 2 + window.innerHeight / 2;
        //     window.scrollTo({
        //         top: newScrollYPosition,
        //         behavior: "smooth"
        //     });
        // }
        // // Otherwise, previous page.
        // else {
        //     this.props.previousPageHandler();
        // }

        this.props.previousPageHandler();
    }

    /**
     * Scroll the page down if there's page to scroll before going to the
     * next page.
     */
    nextPageHandler() {
        // TODO: improve this, not good yet.
        // const currentScroll = window.scrollY + window.innerHeight;
        // const pageHeight = this.refs.pageImage.height;
        //
        // // If we can still scroll down, scroll down 1/3 of the page.
        // if (currentScroll + 10 < pageHeight) {
        //     const newScrollYPosition = window.scrollY + pageHeight / 2 - window.innerHeight / 2;
        //     console.log(`Current ${window.scrollY}, New ${newScrollYPosition}, Page height ${pageHeight}`);
        //     window.scrollTo({
        //         top: newScrollYPosition,
        //         behavior: "smooth"
        //     });
        // }
        // // Otherwise, next page.
        // else {
        //     this.props.nextPageHandler();
        // }

        this.props.nextPageHandler();
    }
}
