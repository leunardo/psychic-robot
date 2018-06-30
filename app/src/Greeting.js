import React, { Component } from 'react';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import { withStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import Icon from '@material-ui/core/Icon';
import Grid from '@material-ui/core/Grid';
import Hidden from '@material-ui/core/Hidden';

const styles = theme => ({
    centered: {
        margin: 'auto',
        marginTop: '30px'
    },
    button: {
        textAlign: 'right'
    },
    left: {
        textAlign: 'left'
    },
    centeredTwoDots: {
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        paddingTop: '16px',
        fontSize: '1.3rem'
    },
    root: {
        display: 'flex',
        [theme.breakpoints.down('xs')]: {
            flexDirection: 'column'
        }
    }
});

class Greeting extends Component {
    state = {
        ip: '',
        port: '',
        nickname: ''
    };

    get url () {
        return `ws://${this.state.ip}:${this.state.port}`;
    }

    handleChange = name => event => {
        this.setState({
          [name]: event.target.value,
        });
    };

    render() {
        const { classes } = this.props;
        const { connect } = this.props; 
        
        return (
            <Grid container>
                <Grid className={classes.centered} item md={8} xs={10}>
                    <Card style={{ width: '100%'}}>
                    
                        <CardContent>
                            <Typography variant='headline' className={(classes.title, classes.left)} color="primary">
                                Connect to server
                            </Typography>
                            <Grid item xs={12}>
                                <form className={(classes.left, classes.formInline, classes.root)} noValidate autoComplete="off">
                                    <TextField 
                                        fullWidth
                                        label="Ip Adress"
                                        className={classes.textField}
                                        value={this.state.ip}
                                        onChange={this.handleChange('ip')}>
                                    </TextField>
                                    <Hidden only="xs">
                                        <div className={classes.centeredTwoDots}>:</div>
                                    </Hidden>
                                    <TextField 
                                        fullWidth
                                        label="Port"
                                        className={classes.textField}
                                        value={this.state.port}
                                        onChange={this.handleChange('port')}>
                                    </TextField>

                                    
                                </form>
                            </Grid>
                            <Grid>
                                <TextField
                                    fullWidth
                                    label="Nickname"
                                    value={this.state.nickname}
                                    onChange={this.handleChange('nickname')}>
                                </TextField>
                            </Grid>
                            <Grid className={classes.button} item xs={12}>
                                <Button color="primary" onClick={() => connect(this.url, this.state.nickname)}>
                                    <Icon>power</Icon>
                                    Connect
                                </Button>
                            </Grid>
                            
                        </CardContent>

                    </Card>
                </Grid>
            </Grid> 
        );
    }
}

export default withStyles(styles)(Greeting);
