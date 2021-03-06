'use strict';
var React = require('react');
var DOM = require('react-dom');


class LoginPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      username: this.props.username || '',
      password: this.props.password || '',
    };
  }

  renderError() {
    if (this.props.error) {
      return <h4 className="error">
        Your username and password didn't match. Please try again.
      </h4>
    }
  }
  renderNext() {
    if (this.props.next) {
      return <input type="hidden" name="next" value={this.props.next}/>
    }
  }

  onChange(path) {
    return (event) => {
      let change = {};
      change[path] = event.target.value;
      this.setState(change);
    };
  }

  render() {
    return <div>
      <div className="body">
        <div className="login form">
          <h3 className="title"> Log In to Spectacles </h3>
          {this.renderError()}
          <form method="post" action='/auth/login'>
            <input type="hidden"
                 name="csrfmiddlewaretoken"
                 value={this.props.csrftoken}/>
            {this.renderNext()}
            <table>
              <tbody>
                <tr>
                  <td className="label">Email:</td>
                  <td className="input">
                    <input type="text" name="username" required autoFocus value={this.state.username} onChange={this.onChange('username')}/>
                  </td>
                </tr>
                <tr>
                  <td className="label">Password:</td>
                  <td className="input">
                    <input type="password" name="password" required value={this.state.password} onChange={this.onChange('password')}/>
                  </td>
                </tr>
              </tbody>
            </table>
            <input type="submit" value="login" className="button"/>
          </form>
        </div>
      </div>
    </div>;
  }
}


DOM.render(
    <LoginPage {...PROPS}/>,
    document.getElementById('react-root'));
