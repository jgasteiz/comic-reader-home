import React from "react";

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
                     alt="Current comic page"
                />
                <nav className="page-navigation">
                    <a className=
                       {
                            "page-navigation-item " +
                            "page-navigation-item--previous " +
                            "page-navigation-item--" +
                            (this.props.hasPreviousPage ? 'show' : 'hidden')
                        }
                       onClick={this.previousPageHandler}
                    />
                    <a className=
                       {
                            "page-navigation-item " +
                            "page-navigation-item--next " +
                            "page-navigation-item--" +
                            (this.props.hasNextPage ? 'show' : 'hidden')
                        }
                       onClick={this.nextPageHandler}
                    />
                </nav>
            </div>
        );
    }

    /**
     * When the component is ready and mounted, initialize key bindings:
     * - arrow right: next page handler
     * - arrow left: previous page handler
     */
    componentDidMount() {
        const component = this;

        // Listen for key events and go to next/previous page when
        // pressing certain keys.
        document.addEventListener('keydown', function (ev) {
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

    /**
     * Scroll the page up if there's page to scroll before going to the
     * previous page.
     */
    previousPageHandler() {
        if (!this.refs.pageImage) {
            this.props.previousPageHandler();
        }
        const pageHeight = this.refs.pageImage.height;
        const pageScreenRatioDiv = this.getPageScreenRatioDividend(pageHeight);

        // If we can still scroll up, scroll up 1/3 of the page.
        if (window.scrollY > 0) {
            const newScrollYPosition = window.scrollY
                - pageHeight / pageScreenRatioDiv
                + window.innerHeight / pageScreenRatioDiv;
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
        const pageScreenRatioDiv = this.getPageScreenRatioDividend(pageHeight);

        // If we can still scroll down, scroll down 1/3 of the page.
        if (currentScroll + 10 < pageHeight) {
            const newScrollYPosition = window.scrollY
                + pageHeight / pageScreenRatioDiv
                - window.innerHeight / pageScreenRatioDiv;
            console.debug(
                `Current ${window.scrollY}, New ${newScrollYPosition},
                 Page height ${pageHeight}`
            );
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
     * Get the page/screen height ratio dividend to decide whether the page
     * should be scrolled in 3, 2 or 1 jump.
     */
    getPageScreenRatioDividend(pageHeight) {
        const pageHeightScreenHeightRatio = pageHeight / window.innerHeight;
        console.debug(`pageHeightScreenHeightRatio: ${pageHeightScreenHeightRatio}`);

        let dividend;
        // If the page height is more than 2.75 times taller than the screen,
        // scroll in 3 jumps.
        if (pageHeightScreenHeightRatio >= 2.75) {
            dividend = 3;
        }
        // If the page height is more than 2.25 times taller than the screen,
        // scroll in 2 jumps.
        else if (pageHeightScreenHeightRatio >= 2.25) {
            dividend = 2;
        // If the page height is less than 2.25 times taller than the screen,
            // scroll in 1 jump.
        } else {
            dividend = 1;
        }
        return dividend;
    }
}
