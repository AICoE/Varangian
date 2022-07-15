import React, { Component } from 'react';
import './app.scss';
import { Content, Theme } from '@carbon/react';
import Header from './components/Header';
import { Route, Switch } from 'react-router-dom';
import LandingPage from './content/LandingPage';
import RepoPage from './content/RepoPage';
import IssuePage from './content/IssuePage';
import ParseCSVTest from './content/ParseCSVTest';
import GuidePage from './content/GuidePage';
import { BrowserRouter, Link, useParams } from 'react-router-dom';

class App extends Component {
  render() {
    return (
      <>
        <Theme theme="g100">
          <Header />
        </Theme>
        <Content>
          <Switch>
            <Route exact path="/" component={LandingPage} />
            <Route path="/repos" component={RepoPage} />
            <Route path="/issues" component={IssuePage} />
            {/* <Route path={'/issues/:id'} component={() => <IssuePage name={name}/>}/> */}
            <Route path="/parse" component={ParseCSVTest} />
            <Route path="/guide" component={GuidePage} />
          </Switch>
        </Content>
      </>
    );
  }
}

export default App;
