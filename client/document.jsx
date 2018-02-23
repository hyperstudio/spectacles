'use strict';
var React = require('react');
var DOM = require('react-dom');
// Contributed from other scripts
var $ = window.$;

import {setupCSRF, createAnnotator} from './util.jsx';
import {Annotation} from './components/annotation.jsx';
import {AnnotationSearch} from './components/annotationSearch.jsx';


class DocumentPage extends React.Component {
  constructor(props) {
    super(props);
    console.log(this.props);
    this.state = {
      annotator: null,
      annotations: this.props.annotations || [],
      columnView: 'annotations',
    };
  };

  componentDidMount() {
    this.initializeAnnotator();
  }

  initializeAnnotator() {
    let dp = this;
    let onUpdate = (ann) => {
      if (!ann) {
        return;
      }
      // Figure out if the annotation was updated
      var changed = false;
      var i;
      for (i = 0; i < dp.state.annotations.length; i++) {
        var x = dp.state.annotations[i];
        if (x.data.id == ann.id) {
          x.data.text = ann.text;
          x.data.tags = ann.tags;
          changed = true;
          break;
        }
      }
      if (changed) {
        dp.setState({annotations: dp.state.annotations});
        return;
      }
      // TODO: Figure out if the annotation was created or deleted
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
    return <Annotation key={ann.uuid} {...ann}/>;
  }

  render() {
    let dp = this;
    let doc = dp.props.document;
    return <div className="document-page main">
      <div className="page-header">
        <div className="header-left">
          <a className="nav-item nav-archive" href="/documents"> Example Archive </a>
          <span className="nav-item nav-spacer"> > </span>
          <a className="nav-item nav-document" href={"/documents/" + doc.id}> {doc.title} </a>
        </div>
        <div className="header-center"></div>
        <div className={"header-right " + dp.state.columnView}>
          <div className="state-choice choice-info">Information</div>
          <div className="state-choice choice-sim">Similar Documents</div>
          <div className="state-choice choice-ann">Annotations</div>
        </div>
      </div>
      <div className="page-content content">
        <div className="box">
          {/* Document pane */}
          <div className="column document-pane">
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
          <div className="column annotations-pane">
            <AnnotationSearch
              document_id={this.props.document.id}
              resultfn={this.searchResult.bind(this)}
              annotations={dp.props.annotations}
            />
          </div>
        </div>
      </div>
    </div>;
  }
}


setupCSRF($);
DOM.render(
  <DocumentPage {...PROPS}/>,
  document.getElementById('react-root'));
