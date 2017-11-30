'use strict';
var React = require('react');
var ReactDOM = require('react-dom');

var {cssurl, backgroundImg, collectionsLink} = require('./utils.jsx');

export class CollectionRow extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    render() {
        var c = this.props.collection;
        var className = "collections-row";
        var art = c.artworks.slice(0, 10);
        if (this.props.small) {
            className += " small";
        }
        return <div className={className}>
            <div className="collections-row-text">
                <a className="collections-row-title" href={collectionsLink(c.id)}> {c.title} &rarr; </a>
            </div>
            <div className="collections-row-art">
                {art.map((a) => {
                    return <div className="collections-row-artwork"
                                key={a.id}
                                style={backgroundImg(a.image_url_small)}>
                    </div>;
                })}
            </div>
        </div>;
    }
}
