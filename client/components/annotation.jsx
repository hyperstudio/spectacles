'use strict';
var React = require('react');


export class Annotation extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  renderControls() {
    let showSimilar = '';
    let ann = this.props;
    if (!this.props.selected) {
      showSimilar = <i onClick={this.props.callback}
                       className="annotation-similar icon-eye">Similar</i>;
    }
    let link;
    let linkid = ann.uuid.replace(/-/g,'');
    if (this.props.document && this.props.document.id == this.props.document_id) {
      link = <a className='annotation-link annotation-scrollto' href={`#${linkid}`}>
        <i className='icon-hashtag'> Show on page </i>
      </a>;
    } else {
      link = <a className='annotation-link' href={`/documents/${ann.document_id}#${linkid}`}>
        <i className="icon-link" >View Document</i>
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
    let ann = this.props;
    let className = "annotation active";
    if (this.props.isSelected) {
      className += " selected";
    }
    let tagsClass = 'annotation-tags';
    if (!ann.tags || !ann.tags.length) {
      tagsClass += 'no-tags';
    }
    return <div className={className} key={ann.uuid}>
      {this.renderControls()}
      <div className="annotation-body">
        <div className="annotation-quote">{ann.quote}</div>
        <div className="annotation-text"
             dangerouslySetInnerHTML={{__html: ann.text}}>
        </div>
        <div className={tagsClass}>
          {(ann.tags || []).map((t, i) => <div className="annotation-tag" key={t + '_' + i}>{t}</div>)}
        </div>
      </div>
      <div className="annotation-info-bottom">
        <div className="annotation-creator">
          <a href={`/activity/${ann.creator.id}`}>{ann.creator.name}</a>
        </div>
        <div className="annotation-timestamp">{ann.updated_at}</div>
      </div>
    </div>;
  }
}
