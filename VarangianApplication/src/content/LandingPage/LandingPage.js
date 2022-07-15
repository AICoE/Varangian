import React from 'react';
import AboutSection from './tabs/About';
import PagesSection from './tabs/Pages';
import GuidesSection from './tabs/Guides';
import DocumentationSection from './tabs/Documentation';
import FooterSection from './tabs/Footer';



import {
  Button,
  Tabs,
  Tab,
  TabList,
  TabPanels,
  TabPanel,
  Grid,
  Column,
  ClickableTile,
  Layer,
  Tile,
  Link,
} from '@carbon/react';

const LandingPage = () => {
  return (

    // Background Information, CODE QL Tools, CODEQL Guidelines, CODEQL Reference Docs
    <Grid className="landing-page" fullWidth>
      <Column lg={16} md={8} sm={4} className="landing-page__banner">
        <h1 className="landing-page__heading">
          Using IBM Varangian
        </h1>
      </Column>
      <Column lg={16} md={8} sm={4} className="landing-page__r2">
        <Tabs defaultSelectedIndex={0}>
          <TabList className="tabs-group" aria-label="Tab navigation">
            <Tab>About</Tab>
            <Tab>Projects</Tab>
            <Tab>Guides</Tab>
            <Tab>Reference Documents</Tab>
          </TabList>
          <TabPanels>
            <TabPanel>
              <AboutSection/>
            </TabPanel>
            <TabPanel>
            <PagesSection/>
            </TabPanel>
            <TabPanel>
            <GuidesSection/>
            </TabPanel>
            <TabPanel>
            <DocumentationSection/>
            </TabPanel>
           
          </TabPanels>
        </Tabs>
      </Column>
      <FooterSection/>
    </Grid>
  );
};

export default LandingPage;
