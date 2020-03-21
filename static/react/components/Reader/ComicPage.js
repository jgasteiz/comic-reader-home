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
        if (!this.refs.pageImage) {
            this.props.previousPageHandler();
        }
        const pageHeight = this.refs.pageImage.height;
        const pageScreenRatioDividend = this.getPageScreenRatioDividend(pageHeight);

        // If we can still scroll up, scroll up 1/3 of the page.
        if (window.scrollY > 0) {
            const newScrollYPosition = window.scrollY - pageHeight / pageScreenRatioDividend + window.innerHeight / pageScreenRatioDividend;
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
        if (!this.refs.pageImage) {
            this.props.nextPageHandler();
        }
        const pageHeight = this.refs.pageImage.height;
        const pageScreenRatioDividend = this.getPageScreenRatioDividend(pageHeight);

        // If we can still scroll down, scroll down 1/3 of the page.
        if (currentScroll + 10 < pageHeight) {
            const newScrollYPosition = window.scrollY + pageHeight / pageScreenRatioDividend - window.innerHeight / pageScreenRatioDividend;
            console.log(`Current ${window.scrollY}, New ${newScrollYPosition}, Page height ${pageHeight}`);
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

    /**
     * Get the page/screen height ratio dividend to decide whether the page should be scrolled in 3, 2 or 1 jump.
     */
    getPageScreenRatioDividend(pageHeight) {
        const pageHeightScreenHeightRatio = pageHeight / window.innerHeight;
        console.log(`pageHeightScreenHeightRatio: ${pageHeightScreenHeightRatio}`);

        let dividend;
        // If the page height is more than 2.75 times taller than the screen, scroll in 3 jumps.
        if (pageHeightScreenHeightRatio >= 2.75) {
            dividend = 3;
        }
        // If the page height is more than 2.25 times taller than the screen, scroll in 2 jumps.
        else if (pageHeightScreenHeightRatio >= 2.25) {
            dividend = 2;
        // If the page height is less than 2.25 times taller than the screen, scroll in 1 jump.
        } else {
            dividend = 1;
        }
        return dividend;
    }
}
