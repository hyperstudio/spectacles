'use strict';
import React from 'react';
import {AbstractSearch} from './abstract.jsx';


export class AnnotationSearch extends AbstractSearch {
  static defaultProps = Object.assign({}, AbstractSearch.defaultProps, {
    endpoint: '/api/search/annotations',
    placeholder: "Search Annotations",
    defaultResults: {
      annotations: [],
    },
  });

  displayAnnotations(annotations) {
    if (!annotations || annotations.length == 0) {
      return;
    }
    return annotations.map(this.props.resultfn || ((ann) => {
      return <AnnotationSearchResult key={ann.id} annotation={ann}/>;
    }));
  }

  render() {
    let anns = this.getResults().annotations || [];
    return <div className={this.props.className}>
      <div className="body gray">
        <div className="search-bar body gray">
          <div className="search-bar-input">
            <input className="search-bar-query"
                   type="text"
                   placeholder={this.props.placeholder}
                   value={this.state.query}
                   onChange={this.onQuery} autoFocus/>
          </div>
        </div>
      </div>
      <div className="search-results body white">
        {this.displayAnnotations(anns)}
      </div>
    </div>;
  }
}


export class AnnotationSearchResult extends React.Component {
  constructor(props) {
      super(props);
      this.state = {};
  }
  render() {
    let ann = this.props.annotation;
    return <div className='annotation active' key={ann.uuid}>
      <div className="annotation-info">
        <div className="annotation-creator">{ann.creator.name}</div>
        <a href={`/documents/${ann.document_id}`} className="annotation-link">View Document</a>
      </div>
      <div className="annotation-quote">{ann.quote}</div>
      <div className="annotation-text"
           dangerouslySetInnerHTML={{__html: ann.text}}>
      </div>
      <div className="annotation-tags">
        {(ann.tags || []).map(t => <div className="annotation-tag" key={t + ann.uuid}>{t}</div>)}
      </div>
    </div>;
  }
}
