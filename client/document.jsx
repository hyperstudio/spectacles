'use strict';
var React = require('react');
var DOM = require('react-dom');
var request = require('browser-request');
var Cookie = require('js-cookie');
// Contributed from other scripts
var $ = window.$;

import {Tab, Tabs, TabList, TabPanel} from 'react-tabs';

import {setupCSRF, createAnnotator} from './util.jsx';
import {Annotation} from './components/annotation.jsx';
import {AnnotationSearch} from './components/search/annotations.jsx';
import {Navigation} from './components/nav.jsx';


class DocumentPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      tab: 'search',
      annotator: null,
      annotation: undefined,
      similar: undefined,
      annotations: this.props.annotations || [],
      columnView: 'annotations',
    };
  };

  componentDidMount() {
    this.initializeAnnotator();
  }

  initializeAnnotator() {
    let dp = this;
    let onUpdate = (action) => (ann) => {
      if (!ann) {
        return;
      }
      var new_annotations = dp.state.annotations.slice();
      if (action === 'update') {
        var changed = false;
        var i;
        for (i = 0; i < new_annotations.length; i++) {
          var x = new_annotations[i];
          if (x.id == ann.id) {
            new_annotations[i] = Object.assign(x, ann);
            changed = true;
            break;
          }
        }

        if (changed) {
          dp.setState({annotations: new_annotations});
        } else {
          var new_annotations = dp.state.annotations.slice();
          new_annotations.push(ann);
          dp.setState({
            annotations: new_annotations,
          });
        }
        return;
      }

      if (action === 'delete') {
        var new_annotations = dp.state.annotations.filter((x) => x.id !== ann.id);
        dp.setState({
          annotations: new_annotations,
        });
        return;
      }

      if (action === 'create') {
        var new_annotations = dp.state.annotations.slice();
        new_annotations.push(ann);
        dp.setState({
          annotations: new_annotations,
        });
        return;
      }
    };
    let ann = createAnnotator(
        dp.refs.documentContent,
        onUpdate,
        dp.props.user.email,
        dp.props.document.id
    );
    this.setState({annotator: ann});
  }

  searchResult(ann) {
    let dp = this;
    let callback = (e) => {
      console.log('clicked back!');
      dp.setState({annotation: ann});
      request({
        method: 'POST',
        uri: '/api/similar/annotation/' + ann.uuid,
        headers: {'X-CSRFToken': Cookie.get('csrftoken')},
        json: true,
      }, function(error, response, body) {
        // Ignore results that have been superceded
        if (error) {
          console.error(error, response, body);
          dp.setState({
            similar: [],
          });
          return;
        }
        dp.setState({
          similar: body,
        });
      });
      return false;
    };
    return <Annotation callback={callback} key={ann.id} {...ann}/>;
  }

  render() {
    let dp = this;
    let doc = dp.props.document;
    return <div id="ann-wrapper" className="document-page grid-container">
      <Navigation doc={doc} user={this.props.user}/>

      {/* Document pane */}
      <div className="column document-pane scroll-y">
        <div className="document-title">{doc.title}</div>
        <div className="document-author">{doc.author}</div>
        <div className="document-content" ref="documentContent">
          {/* For compatibility with existing annotation range definitions; */}
          {/* the previous site must have introduced this div wrapper */}
          <div className="document-content-inner"
               ref="documentContentInner"
               dangerouslySetInnerHTML={{__html: doc.text}}>
          </div>
        </div>
      </div>

      {/* Annotation pane */}
      <Tabs className="column pane-right scroll-y" defaultIndex={0}>
        <TabList>
          <Tab> Annotations </Tab>
          <Tab> Related </Tab>
          <Tab> Information </Tab>
        </TabList>

        <TabPanel>
          {this.state.annotation ? this.renderAnnotation() : this.renderSearch()}
        </TabPanel>

        <TabPanel>
          <h1> Similar Documents </h1>
        </TabPanel>

        <TabPanel>
          <h1> Document Information </h1>
        </TabPanel>
      </Tabs>
    </div>;
  }


  renderAnnotation() {
    let dp = this;
    let ann = this.state.annotation;
    if (!ann) {
      return <div> No Annotation To Display </div>;
    }
    return <div className="column pane-right scroll-y">
      <button onClick={(e) => dp.setState({annotation: undefined})}>Back</button>
      <Annotation key={ann.id} {...ann} isSelected={true}/>
      <div className="similar-annotations"> Similar Annotations</div>
      {(this.state.similar || []).map((x) => <Annotation key={x.id} {...x}/>)}
    </div>;
  }

  renderSearch() {
    let dp = this;
    return <AnnotationSearch className="column annotations-pane scroll-y" resultfn={this.searchResult.bind(this)}
    callback={(ann) => dp.setState({annotation: ann})}
    payload={{
    document_id: dp.props.document.id,
    }}
    defaultResults={{
    annotations: dp.state.annotations,
    }}/>;
  }

}


setupCSRF($);
DOM.render(
  <DocumentPage {...PROPS}/>,
  document.getElementById('react-root'));
