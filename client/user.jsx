'use strict';
var React = require('react');
var DOM = require('react-dom');
// Contributed from other scripts
var $ = window.$;

import {setupCSRF, createAnnotator} from './util.jsx';
import {AnnotationSearch} from './components/search/annotations.jsx';
import {DocumentSearch} from './components/search/documents.jsx';
import {Annotation} from './components/annotation.jsx';
import {Navigation} from './components/nav.jsx';
import {Tab, Tabs, TabList, TabPanel} from 'react-tabs';


let sortByTransform = (f) => (a, b) => {
  if (f(a) < f(b)) return -1;
  if (f(a) > f(b)) return 1;
  return 0;
};

class UserPage extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    this.props.annotations.sort(
      sortByTransform((x) => new Date(x.updated_at)),
      -1
    );

    let {documents, annotations, user, logged_in} = this.props;

    return <div className="user-page grid-container">
        <Navigation doc={null} user={logged_in}/>

        <div className="user-display pane-left">
          <div className="user-name"> {user.name} </div>
          <div className="user-email"> {user.email} </div>
          <div className="item-counts">
            <div className="item-count annotations"> {annotations.length} <br/> annotations </div>
            <div className="item-count documents"> {documents.length} <br/> documents </div>
          </div>
        </div>
        <Tabs className="column pane-right scroll-y" defaultIndex={0}>
          <TabList>
            <Tab> {annotations.length} annotations </Tab>
            <Tab> {documents.length} documents </Tab>
          </TabList>

          <TabPanel>
            <AnnotationSearch
              className="column annotations-pane scroll-y"
              payload={{
                creator_id: this.props.user.id,
              }}
              defaultResults={{
                annotations: this.props.annotations
              }}
            />
          </TabPanel>

          <TabPanel>
            <DocumentSearch
              payload={{
                creator_id: this.props.user.id,
              }}
              defaultResults={{
                documents: this.props.documents
              }}
            />
          </TabPanel>
        </Tabs>
    </div>;
  }
}

setupCSRF($);
DOM.render(
  <UserPage {...PROPS}/>,
  document.getElementById('react-root'));
