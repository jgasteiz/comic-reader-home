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
                   title="Previous page"
                />
                <a className={"page-navigation-item page-navigation-item--next page-navigation-item--" + (this.props.hasNextPage ? 'show' : 'hidden')}
                   onClick={this.props.nextPageHandler}
                   title="Next page"
                />
            </nav>
        );
    }
}
