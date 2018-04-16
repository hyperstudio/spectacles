'use strict';
var React = require('react');


export class Annotation extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  renderControls() {
    return <span className="annotation-controls">
      <i className="annotation-scrollto icon-link">Find</i>
      <i className="annotation-bookmark icon-star">Bookmark</i>
      <i onClick={this.props.callback} className="annotation-similar icon-eye">Similar</i>
    </span>
  }

  render() {
    let ann = this.props;
    let className = "annotation active";
    if (this.props.isSelected) {
      className += " selected";
    }
    return <div className={className} key={ann.uuid}>
      <div className="annotation-info-top">
        <a className="annotation-link" href={`/documents/${ann.document_id}`}>View Document</a>
        {this.renderControls()}
      </div>
      <div className="annotation-quote">{ann.quote}</div>
      <div className="annotation-text"
           dangerouslySetInnerHTML={{__html: ann.text}}>
      </div>
      <div className="annotation-tags">
        {(ann.tags || []).map((t, i) => <div className="annotation-tag" key={t + '_' + i}>{t}</div>)}
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
