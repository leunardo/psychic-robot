import React, { Component } from 'react';
import './App.css';

import { withStyles } from '@material-ui/core/styles';

import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import  Greeting from './Greeting';
import LinearProgress from '@material-ui/core/LinearProgress';
import Snackbar from '@material-ui/core/Snackbar';

import { fromEvent } from 'rxjs';

const styles = {

};

class App extends Component {
  state = {
    loading: false,
    snackBar: {
      open: false,
      msg: ''
    },
  };

  connectToServer = (url) => {
    this.setState({ loading: true });
    const connection = new WebSocket(url);
    connection.addEventListener('open', () => { console.log('opened')})
    const open = fromEvent(connection, 'open');
    const message = fromEvent(connection, 'message');
    const error = fromEvent(connection, 'error');
    
    error.subscribe(e => {
      this.setState({
        snackBar: { open: true, msg: 'An error ocurred while connecting!' },
        loading: false,
      });
    });

    message.subscribe(e => {
      this.setState({ 
        snackBar: { open: true, msg: 'Connection success!' },
        loading: false,
      })
    });

    open.subscribe(e => {
      this.setState({ 
        snackBar: { open: true, msg: 'Connection success!' },
        loading: false,
      })
    });
  }

  closeSnackBar = () => {
    this.setState({ snackBar: { open: false, msg: '' } })
  }

  render() {
    const { loading } = this.state;
    return (
      <div className="App">
        <Snackbar
          anchorOrigin={{
            vertical: 'top',
            horizontal: 'center',
          }}
          open={this.state.snackBar.open}
          autoHideDuration={6000}
          message={<span id="message-id">{this.state.snackBar.msg}</span>}
          onClose={this.closeSnackBar}
        />
        <AppBar position="static" color="primary">
        
          <Toolbar>
            <Typography variant="title" color="inherit">
              Da like 
            </Typography>
          </Toolbar>
        </AppBar>
        {loading !== false && <LinearProgress color="secondary"/>}

        <Greeting connect={this.connectToServer.bind(this)}/>
      </div>
    );
  }
}

export default App;
