import React, { Component } from "react";
import { withStyles } from "@material-ui/core/styles";
import {
    Button, 
    Card,
    Icon,
    TextField,
    Grid,
} from '@material-ui/core';

const styles = theme =>  ({
    dcIcon: {
        marginRight: theme.spacing.unit,
    }
});

class Messages extends Component {

    constructor(props) {
        super(props);
        this.props.messages.subscribe(msg => this.pushMessage(msg[0], [msg[1]]));
    }

    state = {
        newMsg: '',
        messages: [],
    }

    handleChange = name => event => {
        this.setState({
          [name]: event.target.value,
        });
    };

    sendMessage = (event) => {
        if (event.key !== 'Enter') return;

        this.props.send(this.state.newMsg);
        this.setState({ newMsg: '' });
    }

    pushMessage = (msg, userName) => {
        const m = `[${new Date().toLocaleString()}] ${userName}: ${msg}`
        this.state.messages.push(m);
        this.setState({ messages: this.state.messages });
    }

    render() {
        const { classes } = this.props;
        const { messages } = this.state;
        return (
            <div>
                <Card> 
                    <Button style={{ float: 'right' }}>
                        <Icon className={classes.dcIcon}>call_end</Icon>
                        Disconnect
                    </Button>
                    <p>Connected to: localhost</p>
                    <Grid container justify="center" direction="column">
                        <Grid item xs>
                            { messages.map((o, i) => <p style={{ textAlign: 'left' }} key={i}>{o}</p>)}
                        </Grid>
                        <Grid item xs>
                            <TextField
                                style={{ width: '95%', marginBottom: '10px' }}
                                label="Write a message"
                                className={classes.textField}
                                value={this.state.newMsg}
                                onChange={this.handleChange('newMsg')}
                                onKeyDown={this.sendMessage.bind(this)}>
                            </TextField>
                        </Grid>
                        
                        <Grid item xs/>
                    </Grid>
                    
                </Card> 
            </div>
        )
    }
}

export default withStyles(styles)(Messages);