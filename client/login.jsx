'use strict';
var React = require('react');
var DOM = require('react-dom');


class LoginPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      username: this.props.username,
      password: this.props.password,
    };
  }

  renderError() {
    if (this.props.error) {
      return <h5>
        Your username and password didn't match. Please try again.
      </h5>
    }
  }
  renderNext() {
    if (this.props.next) {
      return <input type="hidden" name="next" value={this.props.next}/>
    }
  }

  onChange(path) {
    return function(event) {
      this.setState({path: event.target.value});
    };
  }

  render() {
    return <div>
      <div className="body">
        <div className="login">
          <h3> Log In </h3>
          {this.renderError()}
          <form method="post" action='/auth/login'>
            <input type="hidden"
                 name="csrfmiddlewaretoken"
                 value={this.props.csrftoken}/>
            {this.renderNext()}
            <table>
              <tbody>
                <tr>
                  <td className="label">Username:</td>
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
