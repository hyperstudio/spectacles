'use strict';
import React from 'react';
import {AbstractSearch} from './abstract.jsx';
import {Annotation} from '../annotation.jsx';
import _ from 'underscore';


export class AnnotationSearch extends AbstractSearch {
  static defaultProps = Object.assign({}, AbstractSearch.defaultProps, {
    endpoint: '/api/search/annotations',
    placeholder: "Search Annotations",
    defaultResults: {
      annotations: [],
    },
  });

  defaultResultFn(ann) {
    return <Annotation
      current_document={null}
      selected={null}
      callback={null}
      key={ann.id}
      annotation={ann}
    />;
  }

  displayAnnotations(annotations) {
    if (!annotations || annotations.length == 0) {
      return;
    }
    return _.sortBy(annotations, (ann) => {
      // Todo: calculate actual distance in text?
      if (!ann.ranges) return 0;
      return ann.ranges.length ? ann.ranges[0].startOffset : 0;
    }).map(this.props.resultfn || this.defaultResultFn.bind(this));
  }

  render() {
    let anns = this.getResults().annotations || [];
    let children = this.props.children || this.displayAnnotations(anns);
    return <div className={this.props.className}>
        <div className="search-bar gray">
          <div className="search-bar-input">
            <input className="search-bar-query"
                   type="text"
                   placeholder={this.props.placeholder}
                   value={this.state.query}
                   onChange={this.onQuery} autoFocus/>
          </div>
        </div>
      <div className="search-results">
        {this.state.query ? this.displayAnnotations(anns) : children}
      </div>
    </div>;
  }
}
