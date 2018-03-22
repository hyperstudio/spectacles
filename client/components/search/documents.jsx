'use strict';
import React from 'react';
import {AbstractSearch} from './abstract.jsx';


export class DocumentSearch extends AbstractSearch {
  static defaultProps = Object.assign(AbstractSearch.defaultProps, {
    endpoint: '/api/search/documents',
  });

  constructor(props) {
    super(props);
  }

  displayDocuments(documents) {
    if (!documents || documents.length == 0) {
      return;
    }
    return documents.map(this.props.resultfn);
  }

  render() {
    let r = this.state.results || {};
    let docs = r.documents || [];
    let className = 'search-page docs-pane column';
    return <div className={className}>
      <div className="search-bar body gray">
        <div className="search-bar-input">
          <input className="search-bar-query"
                 type="text"
                 placeholder="Filter Documents"
                 value={this.state.query}
                 onChange={this.onQuery} autoFocus/>
        </div>
        <p className="search-bar-results">
          {this.renderStatus()}
        </p>
      </div>
      <div className="search-results body white">
        {this.displayDocuments(docs)}
      </div>
    </div>;
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
