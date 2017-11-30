'use strict';
var React = require('react');
var DOM = require('react-dom');



class Documents extends React.Component {
    constructor(props) {
        super(props);
        console.log(this.props);
        this.state = {};
    }

    render() {
        return <div className="all-documents">
            {this.props.documents.map((d) => <DocumentEntry key={d.id} document={d}/>)}
        </div>;
    }
}

class DocumentEntry extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }
    link() {
        return this.props.document &&
               "/documents/" + this.props.document.id;
    }
    text() {
        let doc = this.props.document;
        if (!doc) {
            return '<broken>'
        }
        return doc.title + ' - ' + doc.author + ' (' + doc.creator.email + ')';
    }
    render() {
        return <div className="document-entry">
            <a href={this.link()}>{this.text()}</a>
        </div>;
    }
}

DOM.render(
        <Documents {...PROPS}/>,
        document.getElementById('react-root'));
