'use strict';
var React = require('react');
var DOM = require('react-dom');
var Cookie = require('js-cookie');
// TODO: use a different client side request framework like `fetch`
var request = require('browser-request');
// Contributed from other scripts
var $ = window.$;

import {setupCSRF, createAnnotator} from './util.jsx';
import {Annotation} from './components/annotation.jsx';
import {DocumentSearch} from './components/search/documents.jsx';
import {AnnotationSearch} from './components/search/annotations.jsx';


// TODO: Two separate SearchPanes, one over documents, one over annotations.
// Both use the elasticsearch backend route.
class DocumentsPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};

    // FUSE client-side filtering library
    this.inputProps = {
      placeholder: "Fuzzy filter...",
    }
    this.fuseConfig = {
      keys: ['author', 'title', 'creator.name', 'creator.email'],
      shouldSort: true,
    }
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
          <DocumentSearch
            className="search-page docs-pane column"
            placeholder="Search Documents"
            defaultResults={{
              documents: dp.props.documents || [],
            }}
          />
          <AnnotationSearch
            className="search-pane column"
            placeholder="Search Annotations"
            defaultResults={{
              annotations: dp.props.annotations || [],
            }}
          />
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

setupCSRF($);
DOM.render(
        <DocumentsPage {...PROPS}/>,
        document.getElementById('react-root'));
