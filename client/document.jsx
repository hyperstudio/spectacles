'use strict';
var React = require('react');
var DOM = require('react-dom');
var Cookie = require('js-cookie');
import fuzzyFilterFactory from 'react-fuzzy-filter';
const {InputFilter, FilterResults} = fuzzyFilterFactory();
// Contributed from other scripts
var $ = window.$;
var tinyMCEPopup = window.tinyMCEPopup;
var Annotator = window.Annotator;
const fuseConfig = {
  keys: ['data.text', 'data.quote', 'data.tags', 'creator.email', 'creator.name'],
  shouldSort: true,
};

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
      console.log('SENDING');
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            var csrf = Cookie.get('csrftoken');
            console.log('csrf?', csrf);
            xhr.setRequestHeader("X-CSRFToken", csrf);
        }
    }
});

Annotator.Plugin.StoreLogger = function (element, callbacks) {
  console.log('StoreLogger initialized!');
  return {
    pluginInit: function () {
        console.log('pluginInit called');
      this.annotator
          .subscribe("annotationCreated", function (annotation) {
            if (callbacks.create) {
              callbacks.create(annotation);
            }
            console.info("The annotation: %o has just been created!", annotation)
          })
          .subscribe("annotationUpdated", function (annotation) {
            if (callbacks.update) {
              callbacks.update(annotation);
            }
            console.info("The annotation: %o has just been updated!", annotation)
          })
          .subscribe("annotationDeleted", function (annotation) {
            if (callbacks.delete) {
              callbacks.delete(annotation);
            }
            console.info("The annotation: %o has just been deleted!", annotation)
          });
    }
  }
};



class DocumentPage extends React.Component {
  constructor(props) {
    super(props);
    console.log(this.props);
    this.state = {
      annotations: this.props.annotations || [],
      columnView: 'annotations',
    };
  }
  componentDidMount() {
    console.log('componentDidMount()\n');
    this.initializeAnnotator();
  }
  componentDidUpdate() {
    console.log('componentDidUpdate()\n');
    //this.initializeAnnotator();
  }

  initializeAnnotator() {
    let dp = this;

    let UPDATE = (ann) => {
      console.log('GOT AN UPDATE', ann);
      if (!ann) {
        return;
      }
      var changed = false;
      var i;
      for (i = 0; i < this.state.annotations.length; i++) {
        var x = this.state.annotations[i];
        if (x.data.id == ann.id) {
          x.data.text = ann.text;
          x.data.tags = ann.tags;
          changed = true;
          break;
        }
      }
      if (changed) {
        dp.setState({annotations: this.state.annotations});
        return;
      }
    };

    let ann = new Annotator(this.refs.documentContent)
      .addPlugin('Auth', {
        tokenUrl: '/api/token',
      })
      .addPlugin('StoreLogger', {
        update: UPDATE,
        delete: UPDATE,
        create: UPDATE,
      })
      .addPlugin('Tags', {})
      .addPlugin('Permissions', {
        user: this.props.user.email,
      })
      .addPlugin('Store', {
        prefix: `/api/store/${this.props.document.id}`,
        urls: {
          create:  '',
          read:    '',
          update:  '/:id',
          destroy: '/:id',
          search:  '/search',
        },
        annotationData: {
          // TODO: what to do about this ID?
          uri: this.props.document.id,
        },
        //loadFromSearch: {
        //  uri: this.props.document.id,
        //},
      })
      .addPlugin('RichText', {
        editor_enabled: true,
        tinymce: {
          selector: "li.annotator-item textarea",
          plugins: "media image insertdatetime link code",
          toolbar_items_size: 'small',
          extended_valid_elements : "iframe[src|frameborder|style|scrolling|class|width|height|name|align|id]",
          toolbar: [
            'undo',
            'redo',
            '|',
            'styleselect',
            '|',
            'bold',
            'italic',
            '|',
            'bullist',
            'numlist',
            'outdent',
            'indent',
            '|',
            'link',
            'image',
            'media',
            'rubric'
          ].join(' '),
    		}
      });
    window.ANN = ann;
    //tinyMCEPopup.init();
    console.log('ANN:', window.ANN);
    UPDATE();
    //this.setState({
    //  annotations: ann.dumpAnnotations(),
    //});

  }

  render() {
    let doc = this.props.document;
    console.log(doc);
    if (!doc) {
      return <div>Missing Document</div>;
    }

    let inputProps = {
      placeholder: "Fuzzy filter...",
    }


    return <div className="document-page main">
      <div className="page-header">
        <div className="header-left">
          <a className="nav-item nav-archive" href="/documents"> Example Archive </a>
          <span className="nav-item nav-spacer"> > </span>
          <a className="nav-item nav-document" href={"/documents/" + doc.id}> {doc.title} </a>
        </div>
        <div className="header-center"></div>
        <div className={"header-right " + this.state.columnView}>
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
            <InputFilter inputProps={inputProps}/>
            <FilterResults items={this.state.annotations} fuseConfig={fuseConfig}>
              {filteredItems => {
                console.log('got results:', filteredItems);
                return <div className='annotations-results'>
                  {filteredItems.map(ann => <Annotation {...ann}/>)}
                </div>;
              }}
            </FilterResults>
          </div>
        </div>
      </div>
    </div>;
  }

  renderAnnotations() {
    let annotations = this.state.annotations;
    if (!annotations) {
      return <div> Missing Annotations> </div>;
    }
    console.log('returning a bunch of annotations', annotations);
    return annotations.map(ann => <Annotation {...ann}/>);
  }
}

class Annotation extends React.Component {
  constructor(props) {
    super(props);
    console.log(this.props);
    this.state = {active: true};
  }
  clicked() {
    //this.setState({active: !this.state.active});
  }
  render() {
      let ann = this.props;
      let xxx = this;
      console.log('rendering!', this.state);
      if (xxx.state.active) {
        return <div className='annotation active' key={ann.uuid}>
          <div className="annotation-info">
            <div className="annotation-creator">{ann.creator.name}</div>
            <div className="annotation-timestamp" onClick={xxx.clicked.bind(xxx)}>{ann.updated_at}</div>
          </div>
          <div className="annotation-quote">{ann.data.quote}</div>
          <div className="annotation-text"
               dangerouslySetInnerHTML={{__html: ann.data.text}}>
          </div>
          <div className="annotation-tags">
            {(ann.data.tags || []).map(t => <div className="annotation-tag" key={t + ann.uuid}>{t}</div>)}
          </div>
        </div>;
      } else {
        return <div className='annotation' key={ann.uuid}>
          <div className="annotation-info">
            <div className="annotation-creator">{ann.creator.name}</div>
            <div className="annotation-timestamp" onClick={xxx.clicked.bind(xxx)}>{ann.updated_at}</div>
          </div>
          <div className="annotation-text"
               dangerouslySetInnerHTML={{__html: ann.data.text}}>
          </div>
        </div>;
      }
  }
}



DOM.render(
  <DocumentPage {...PROPS}/>,
  document.getElementById('react-root'));


