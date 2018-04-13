'use strict';
import React from 'react';
import {AbstractSearch} from './abstract.jsx';


export class DocumentSearch extends AbstractSearch {
  static defaultProps = Object.assign({}, AbstractSearch.defaultProps, {
    endpoint: '/api/search/documents',
    placeholder: "Search Documents",
    defaultResults: {
      documents: [],
    },
  });

  render() {
    let docs = this.getResults().documents || [];
    return <div className={this.props.className}>
      <div className="search-bar body gray">
        <div className="search-bar-input">
          <input className="search-bar-query"
                 type="text"
                 placeholder={this.props.placeholder}
                 value={this.state.query}
                 onChange={this.onQuery} autoFocus/>
        </div>
      </div>
      <div className="search-results body white">
        {this.displayDocuments(docs)}
      </div>
    </div>;
  }

  displayDocuments(documents) {
    if (!documents || documents.length == 0) {
      return;
    }
    return documents.map(this.props.resultfn || ((doc) => {
      return <DocumentSearchResult key={doc.id} document={doc}/>;
    }));
  }
}


export class DocumentSearchResult extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }
  link() {
    return this.props.document &&
      "/documents/" + this.props.document.id;
  }

  renderHighlight() {
    let doc = this.props.document;
    let highlight = doc.highlight;
    if (!highlight) {
      return '';
    }
    return <div className="document-highlight">
      {highlight.text.map((t, i) =>
        <div key={i} className="document-highlight-text"
             dangerouslySetInnerHTML={{__html: t}}>
        </div>
      )}
    </div>;
  }

  render() {
    let doc = this.props.document;
    let id = doc.id;

    return <div className="document-entry" key={id}>
      <div className="document-title">
        <a href={this.link()}>{doc.title}</a>
      </div>
      <div className="document-author">
        {doc.creator.name}
      </div>
      <div className="document-meta">
        <div className="document-creator"> {doc.author}</div>
        <div className="document-timestamp"> {doc.updated_at} </div>
      </div>
      {this.renderHighlight()}
    </div>;
  }
}
