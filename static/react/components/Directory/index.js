import React from 'react';
import { Link } from "react-router-dom";

import FileItemService from '../../services/FileItem.Service';


export default class Directory extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            directories: [],
            comics: [],
            parentId: null,
            name: null,
            fileItemId: null,
        };
    }

    render() {
        if (this._getFileItemDetails()) {
            return (
                <div>
                    {this._renderHeader()}

                    <section className="container">
                        <header>
                            <div className="row">
                                <h1 className="col">
                                    {this.state.name}
                                </h1>
                                <div className="col-auto">
                                    {this._renderBackLink()}
                                </div>
                            </div>
                        </header>

                        {this._renderComics()}
                        {this._renderDirectories()}
                    </section>
                </div>
            );
        }
        return (
            <div>Loading...</div>
        );
    }

    componentDidMount() {
        this._getFileItemDetails();
    }

    deleteBookmarkHandler(comicId) {
        FileItemService.deleteBookmark(comicId);
    }

    // Private functions

    _getFileItemDetails() {
        const urlSearch = new URLSearchParams(this.props.location.search);
        if (urlSearch.get('q')) {
            if (this.state.fileItemId !== -1) {
                FileItemService.getFileItemSearchResults(urlSearch.get('q'), (res) => {
                    const directories = res.filter(child => child['file_type'] === 'directory');
                    const comics = res.filter(child => child['file_type'] === 'comic');
                    this.setState({
                        name: `Search results of \`${urlSearch.get('q')}\``,
                        directories: directories,
                        comics: comics,
                        parentId: undefined,
                        fileItemId: -1,
                    });
                    this.render();
                });
                return false;
            }
        } else {
            if (this.state.fileItemId !== this.props.match.params.id) {
                const newFileItemId = this.props.match.params.id;
                FileItemService.getFileItemDetails(newFileItemId, (res) => {
                    const directories = res['children'].filter(child => child['file_type'] === 'directory');
                    const comics = res['children'].filter(child => child['file_type'] === 'comic');
                    this.setState({
                        name: res['name'],
                        directories: directories,
                        comics: comics,
                        parentId: res['parent'],
                        fileItemId: newFileItemId
                    });
                    this.render();
                });
                return false;
            }
        }
        return true;
    }

    // Custom render functions

    _renderHeader() {
        return (
            <header className="navbar navbar-dark bg-dark sticky-top navbar-expand-md">
                <div className="container d-flex justify-content-between">
                    <a href="/"
                       className="navbar-brand d-flex align-items-center">
                        <strong>Comic Reader</strong>
                    </a>
                    <form className="form-inline my-2 my-lg-0" method="get">
                        <input className="form-control mr-sm-2"
                               type="search"
                               name="q"
                               placeholder="Search for a comic or a directory"
                        />
                        <button
                            className="btn btn-outline-success my-2 my-sm-0"
                            type="submit"
                        >Search</button>
                    </form>
                </div>
            </header>
        );
    }

    _renderBackLink() {
        const component = this;
        return  (function() {
            if (component.state.parentId) {
                return (
                    <Link className="btn btn-secondary" to={`/dir/${component.state.parentId}/`}>Back</Link>
                );
            } else {
                return '';
            }
        })();
    }

    _renderComics() {
        if (this.state.comics.length === 0) {
            return '';
        }
        const component = this;

        const comicRows = this.state.comics.map(function (comic, index) {
            return (<tr key={comic["pk"]}>
                <td>
                    {index + 1}
                </td>
                <td>
                    {comic.name}
                </td>
                <td className="text-right">
                    {comic["bookmarked_page"] !== null &&
                        <div className="mb-2 btn-group" role="group">
                            <Link to={`/comic/${comic["pk"]}/${comic["bookmarked_page"]}/`} className="btn btn-primary btn-sm">
                                Continue
                            </Link>
                            <button
                                className="btn btn-danger btn-sm"
                                onClick={() => component.deleteBookmarkHandler(comic["pk"])}
                            >Delete bookmark</button>
                        </div>
                    }
                    <div>
                        <Link to={`/comic/${comic["pk"]}/0/`} className="btn btn-primary btn-sm">
                            Read
                        </Link>
                    </div>
                </td>
            </tr>);
        });

        return (
            <div>
                <h2>Comics</h2>

                <table className="table table-striped">
                    <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Comic name</th>
                        <th scope="col" className="text-right">Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                        {comicRows}
                    </tbody>
                </table>
            </div>
        );
    }

    _renderDirectories() {
        if (this.state.directories.length === 0) {
            return '';
        }
        const directoryRows = this.state.directories.map(function (directory, index) {
            return (<tr key={directory.pk}>
                <td>
                    {index + 1}
                </td>
                <td>
                    {directory.name}
                </td>
                <td className="text-right">
                    <Link to={`/dir/${directory.pk}/`} className="btn btn-secondary btn-sm">
                        Go
                    </Link>
                </td>
            </tr>);
        });

        return (
            <div>
                <h2>Directories</h2>

                <table className="table table-striped">
                    <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Directory name</th>
                        <th scope="col" className="text-right">Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                        {directoryRows}
                    </tbody>
                </table>
            </div>
        );
    }


}
