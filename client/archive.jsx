'use strict';
var React = require('react');
var DOM = require('react-dom');
var Cookie = require('js-cookie');
// TODO: use a different client side request framework like `fetch`
var request = require('browser-request');
// Contributed from other scripts
var $ = window.$;

import {Tab, Tabs, TabList, TabPanel} from 'react-tabs';

import {setupCSRF, createAnnotator} from './util.jsx';
import {Annotation} from './components/annotation.jsx';
import {DocumentSearch, DocumentSearchResult} from './components/search/documents.jsx';
import {AnnotationSearch} from './components/search/annotations.jsx';
import {Navigation} from './components/nav.jsx';



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
    return <div className="archive-page grid-container">
      <Navigation user={this.props.user}/>
      <Tabs className="column pane-left scroll-y">
        <TabList>
          <Tab> All Documents </Tab>
          <Tab> Recommended Documents </Tab>
        </TabList>

        <TabPanel>
          <DocumentSearch
            className="column pane-left scroll-y"
            placeholder="Search Documents"
            defaultResults={{
              documents: this.props.documents || [],
            }}
          />
        </TabPanel>

        <TabPanel>
          {this.renderRecommendations()}
        </TabPanel>
      </Tabs>
      <AnnotationSearch
        className="column pane-right scroll-y"
        placeholder="Search Annotations"
        defaultResults={{
          annotations: dp.props.annotations || [],
        }}
      />
    </div>;
  }

  renderRecommendations() {
    return <div className="doc-recs">
      {this.props.recs.docs.map((doc) => {
        console.log('doc?', doc);
        return <DocumentSearchResult key={doc.id} document={doc}/>
      })}
    </div>;
  }
}

setupCSRF($);
DOM.render(
        <DocumentsPage {...PROPS}/>,
        document.getElementById('react-root'));
