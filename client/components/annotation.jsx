'use strict';
var React = require('react');


export class Annotation extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    let ann = this.props;
    return <div className='annotation active' key={ann.uuid}>
      <div className="annotation-info">
        <div className="annotation-creator">{ann.creator.name}</div>
        <div className="annotation-timestamp">{ann.updated_at}</div>
      </div>
      <div className="annotation-quote">{ann.data.quote}</div>
      <div className="annotation-text"
           dangerouslySetInnerHTML={{__html: ann.data.text}}>
      </div>
      <div className="annotation-tags">
        {(ann.data.tags || []).map(t => <div className="annotation-tag" key={t + ann.uuid}>{t}</div>)}
      </div>
    </div>;
  }
}
