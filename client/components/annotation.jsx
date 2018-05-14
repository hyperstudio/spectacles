'use strict';
var React = require('react');


export class Annotation extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  renderControls() {
    let {current_document, selected, callback, annotation} = this.props;

    let showSimilar = '';
    if (!selected) {
      showSimilar = <i onClick={callback}
                       className="annotation-similar icon-eye">Similar</i>;
    }

    let link;
    let linkid = annotation.uuid.replace(/-/g,'');
    let ann_doc_id = annotation.document_id || (annotation.document && annotation.document.id) || null;
    let ann_doc_title = annotation.document_title || (annotation.document && annotation.document.title) || null;
    if (current_document && current_document.id == ann_doc_id) {
      link = <a className='annotation-link annotation-scrollto' href={`#${linkid}`}>
        <i className='icon-hashtag'> Show on page </i>
      </a>;
    } else {
      link = <a className='annotation-link' href={`/documents/${ann_doc_id}#${linkid}`}>
        <i className="icon-link" >{ann_doc_title || 'View Document'}</i>
      </a>;
    }

    return <div className="annotation-info-top">
      {link}
      <span className="annotation-spacer"></span>
      <span className="annotation-controls">
        {/*<i className="annotation-bookmark icon-star">Bookmark</i>*/}
        {showSimilar}
      </span>
    </div>;
  }

  render() {
    let {current_document, selected, callback, annotation, isSelected} = this.props;

    let className = "annotation active";
    if (isSelected) {
      className += " selected";
    }
    let tagsClass = 'annotation-tags';
    if (!annotation.tags || !annotation.tags.length) {
      tagsClass += 'no-tags';
    }
    return <div className={className} key={annotation.uuid}>
      {this.renderControls()}
      <div className="annotation-body">
        <div className="annotation-quote">{annotation.quote}</div>
        <div className="annotation-text"
             dangerouslySetInnerHTML={{__html: annotation.text}}>
        </div>
        <div className={tagsClass}>
          {(annotation.tags || []).map((t, i) => {
            return <div className="annotation-tag" key={t + '_' + i}>{t}</div>;
          })}
        </div>
      </div>
      <div className="annotation-info-bottom">
        <div className="annotation-creator">
          <a href={`/activity/${annotation.creator.id}`}>{annotation.creator.name}</a>
        </div>
        <div className="annotation-timestamp">{annotation.updated_at}</div>
      </div>
    </div>;
  }
}
