'use strict';
var React = require('react');
var DOM = require('react-dom');
var Cookie = require('js-cookie');
// TODO: use a different client side request framework like `fetch`
var request = require('browser-request');
// Contributed from other scripts
var $ = window.$;

import fuzzyFilterFactory from 'react-fuzzy-filter';
import {setupCSRF, createAnnotator} from './util.jsx';
import {Annotation} from './components/annotation.jsx';
import {AnnotationSearch} from './components/annotationSearch.jsx';


// TODO: Two separate SearchPanes, one over documents, one over annotations.
// Both use the elasticsearch backend route.
class DocumentsPage extends React.Component {
  constructor(props) {
    super(props);
    console.log(this.props);
    this.state = {};

    // FUSE client-side filtering library
    this.inputProps = {
      placeholder: "Fuzzy filter...",
    }
    this.fuseConfig = {
      keys: ['author', 'title', 'creator.name', 'creator.email'],
      shouldSort: true,
    };
    const {InputFilter, FilterResults} = fuzzyFilterFactory();
    this.InputFilter = InputFilter;
    this.FilterResults = FilterResults;
  }

  render() {
    let dp = this;
    return <div className="documents-page main">
      <div className="page-header">
        <div className="header-left">
          <a className="nav-item nav-archive" href="/documents"> Example Archive </a>
        </div>
        <div className="header-center"></div>
        <div className="header-right">
          <div className="state-choice">{dp.renderUser()}</div>
        </div>
      </div>
      <div className="content">
        <div className="box">
          <div className="docs-pane column">
            <dp.InputFilter inputProps={dp.inputProps}/>
            <dp.FilterResults items={dp.props.documents} fuseConfig={dp.fuseConfig}>
              {filteredItems => {
                return <div className='docs-results'>
                  {filteredItems.map(d => <DocumentEntry key={d.id} document={d}/>)}
                </div>;
              }}
            </dp.FilterResults>
          </div>
          <div className="search-pane column">
            <AnnotationSearch/>
          </div>
        </div>
      </div>
    </div>;
  }

  renderUser() {
    let name = 'Anonymous';
    let email = '?';
    if (this.props.user) {
      name = this.props.user.name;
      email = this.props.user.email;
    }
    return <span>{name} ({email})</span>
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
  render() {
    let doc = this.props.document;
    return <div className="document-entry">
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
    </div>;
  }
}

setupCSRF($);
DOM.render(
        <DocumentsPage {...PROPS}/>,
        document.getElementById('react-root'));
