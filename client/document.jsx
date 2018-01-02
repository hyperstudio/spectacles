'use strict';
var React = require('react');
var DOM = require('react-dom');
var Cookie = require('js-cookie');
// Contributed from other scripts
var $ = window.$;
var tinyMCEPopup = window.tinyMCEPopup;
var Annotator = window.Annotator;

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
    this.state = { annotations: []};
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
      console.log('GOT AN UPDATE');
      dp.setState({annotations: ANN.dumpAnnotations()});
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

    return <div className="document-page main">
      <div className="page-header">
        <a className="nav-item nav-archive" href="/documents"> Example Archive </a>
        <span className="nav-item nav-spacer"> > </span>
        <a className="nav-item nav-document" href={"/documents/" + doc.id}> {doc.title} </a>
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
            {this.renderAnnotations()}
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
    return annotations.map(ann => {
      return <div className="annotation" key={ann.id}>
        <div className="annotation-quote">{ann.quote}</div>
        <div className="annotation-text">{ann.text}</div>
        <div className="annotation-tags">
          {ann.tags.map(t => <div className="annotation-tag" key={t + ann.id}>{t}</div>)}
        </div>
        <div className="annotation-creator">{ann.user}</div>
      </div>
    })
  }
}

DOM.render(
  <DocumentPage {...PROPS}/>,
  document.getElementById('react-root'));
