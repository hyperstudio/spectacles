'use strict';
var React = require('react');
var DOM = require('react-dom');
var Cookie = require('js-cookie');
var $ = window.$; // defined by contrib on page

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


class Document extends React.Component {
  constructor(props) {
    super(props);
    console.log(this.props);
    this.state = {};
  }
  componentDidMount() {
    console.log('componentDidMount()\n');
    this.initializeAnnotator();
  }
  componentDidUpdate() {
    console.log('componentDidUpdate()\n');
    this.initializeAnnotator();
  }

  initializeAnnotator() {
    let ann = new Annotator(this.refs.documentContent)
      .addPlugin('Auth', {
        tokenUrl: '/api/token',
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
          menubar: false,
          toolbar_items_size: 'small',
          extended_valid_elements : "iframe[src|frameborder|style|scrolling|class|width|height|name|align|id]",
          toolbar: "insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image media rubric | code ",
    		}
      });
    window.ANN = ann;
    console.log('ANN:', window.ANN);
    this.state.ann = ann;
  }

  render() {
    let doc = this.props.document;
    console.log(doc);
    if (!doc) {
      return <div>Missing Document</div>;
    }
    return <div className="document">
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
    </div>;
  }
}

DOM.render(
  <Document {...PROPS}/>,
  document.getElementById('react-root'));
