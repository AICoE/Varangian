import React from 'react';
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
            <Tab>Research</Tab>
          </TabList>
          <TabPanels>
            <TabPanel>
              <Grid className="tabs-group-content">
                <Column md={4} lg={7} sm={4} className="landing-page__tab-content">
                  <h2 className="landing-page__subheading">What is Varangian?</h2>
                  <p className="landing-page__p">
                    Varangian is an augmented static analyzer that uses machine learning to prioritize
                    defects identified by static analyzers based on their likelihood of being actual defects.
                  </p>
                  <Button onclick="https://github.com/AICoE/Varangian">
                    <p>Github </p>
                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-github" viewBox="0 0 16 16">
                      <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z" />
                    </svg>
                  </Button>
                </Column>
                <Column md={4} lg={{ span: 8, offset: 7 }} sm={4}>
                  <img
                    className="landing-page__illo"
                    src={`${process.env.PUBLIC_URL}/tab-illo.png`}
                    alt="Carbon illustration"
                  />
                </Column>
              </Grid>
            </TabPanel>
            <TabPanel>
              <Grid className="tabs-group-content">
                <Column lg={16} md={8} sm={4} className="landing-page__tab-content">
                  <Grid>
                    <Column sm={4}>
                      <Tile>
                        Project #1
                        <br />
                        <br />
                        <Link href="https://www.carbondesignsystem.com">Link</Link>
                      </Tile>
                    </Column>
                    <Column sm={4}>
                      <Tile>
                        Project #2
                        <br />
                        <br />
                        <Link href="https://www.carbondesignsystem.com">Link</Link>
                      </Tile>
                    </Column>
                    <Column sm={4}>
                      <Tile>
                        Project #3
                        <br />
                        <br />
                        <Link href="https://www.carbondesignsystem.com">Link</Link>
                      </Tile>
                    </Column>
                    <Column sm={4}>
                      <Tile>
                        Project #4
                        <br />
                        <br />
                        <Link href="https://www.carbondesignsystem.com">Link</Link>
                      </Tile>
                    </Column> 
                  </Grid>
                </Column>
              </Grid>
            </TabPanel>
            <TabPanel>
              <Grid className="tabs-group-content">
                <Column lg={16} md={8} sm={4} className="landing-page__tab-content">
                  <ClickableTile href="#">
                    Varangian MSR paper (L4T1)
                  </ClickableTile>
                  <Layer>
                    <ClickableTile href="#">
                      D2A paper (L4T2)
                    </ClickableTile>
                  </Layer>
                  <ClickableTile href="#">
                    C-BERT paper (L4T3)
                  </ClickableTile>
                  <Layer>
                    <ClickableTile href="#">
                      DISCO paper (L4T4)
                    </ClickableTile>
                  </Layer>
                </Column>
              </Grid>
            </TabPanel>
          </TabPanels>
        </Tabs>
      </Column>
      <Column lg={16} md={8} sm={4} className="landing-page__r3">
        <Grid>
          <Column md={4} lg={4} sm={4}>
            <h3 className="landing-page__label">The Principles</h3>
          </Column>
          <Column md={4} lg={4} sm={4}>
            Carbon is Open
          </Column>
          <Column md={4} lg={4} sm={4}>
            Carbon is Modular
          </Column>
          <Column md={4} lg={4} sm={4}>
            Carbon is Consistent
          </Column>
        </Grid>
      </Column>
    </Grid>
  );
};

export default LandingPage;
