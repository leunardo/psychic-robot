import React, { Component } from 'react';
import './App.css';

import { withStyles } from '@material-ui/core/styles';

import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import  Greeting from './Greeting';
import LinearProgress from '@material-ui/core/LinearProgress';
import Snackbar from '@material-ui/core/Snackbar';
import Messages from './Messages';

import { fromEvent, Observable, Subject } from 'rxjs';

const styles = {

};

class App extends Component {
  state = {
    nickname: '',
    loading: false,
    snackBar: {
      open: false,
      msg: ''
    },
    connection: null,
    connected: false,
    message$: new Subject(),
  };

  connectToServer = (url, nickname) => {
    if (!nickname || !url) return;

    this.setState({ loading: true, nickname: nickname });
    const connection = new WebSocket(url);
    const open = fromEvent(connection, 'open');
    const message = fromEvent(connection, 'message');
    const error = fromEvent(connection, 'error');
    
    error.subscribe(e => {
      this.setState({
        snackBar: { open: true, msg: 'An error ocurred while connecting!' },
        loading: false,
      });
    });

    open.subscribe(e => {
      this.setState({ 
        snackBar: { open: true, msg: 'Connection success!' },
        loading: false,
        connected: true,
        connection: connection,
      });

      connection.send(`[HI]${this.state.nickname}[|HI]\n`);
    });

    message.subscribe(event => {
      const msg = event.data;
      const letter = this.extractMessage(msg, '@MSG');
      const from = this.extractMessage(msg, '@FROM');

      this.state.message$.next([letter, from]);
    })
  }

  extractMessage(msg, tag) {
    const index = msg.indexOf(tag);
    const indexPar1 = msg.indexOf('(', index);
    const indexPar2 = msg.indexOf(')', index);

    return msg.substring(indexPar1+1, indexPar2);
  }

  sendMessage = msg => {
    this.state.connection.send(`[SEND]
    @MSG(${msg})\n
    @FROM(${this.state.nickname})\n
    [|SEND]\n`);
  }

  closeSnackBar = () => {
    this.setState({ snackBar: { open: false, msg: '' } })
  }

  getNickname () {
    return this.state.nickname;
  }

  render() {
    const { loading, connected } = this.state;

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
        { loading !== false && <LinearProgress color="secondary"/> }

        { connected !== true && <Greeting connect={this.connectToServer}/> }

        { connected === true && <Messages messages={this.state.message$} nickname={this.getNickname.bind(this)} send={this.sendMessage.bind(this)} style={{ height:'100%' }}/> }
      </div>
    );
  }
}

export default withStyles(styles)(App);
