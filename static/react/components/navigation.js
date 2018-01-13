import React from "react";


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
