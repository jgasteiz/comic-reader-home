import React from "react";

/**
 * This component renders two invisible navigation items on the left/right
 * sides of the screen for navigating to the previous/right pages.
 */
export default class Navigation extends React.Component {
    render() {
        return (
            <nav className="page-navigation">
                <a className={"page-navigation-item page-navigation-item--previous page-navigation-item--" + (this.props.hasPreviousPage ? 'show' : 'hidden')}
                   onClick={this.props.previousPageHandler}
                />
                <a className={"page-navigation-item page-navigation-item--next page-navigation-item--" + (this.props.hasNextPage ? 'show' : 'hidden')}
                   onClick={this.props.nextPageHandler}
                />
            </nav>
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
                component.props.nextPageHandler();
                ev.preventDefault();
            } else if (keyName === 'ArrowLeft') {
                component.props.previousPageHandler();
                ev.preventDefault();
            }
        });
    }
}
