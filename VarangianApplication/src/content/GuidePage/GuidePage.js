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

const GuidePage = () => {
  return (

    // Background Information, CODE QL Tools, CODEQL Guidelines, CODEQL Reference Docs
    <Grid className="landing-page" fullWidth>
      <Column lg={16} md={8} sm={4} className="landing-page__banner">
        <h1 className="landing-page__heading">
          Metrics
        </h1>
      </Column>
      <Column lg={16} md={8} sm={4} className="landing-page__r2">
        <Tabs defaultSelectedIndex={0}>
          <TabList className="tabs-group" aria-label="Tab navigation">
            <Tab>Augmented Static Analysis</Tab>
            <Tab>Varangian Issue</Tab>
           
          </TabList>
          <TabPanels>
            <TabPanel>
            <Grid className="tabs-group-content">
                <Column lg={16} md={8} sm={4} className="landing-page__tab-content">
                <p><b>Sample:</b> One instance of a static analyzer output. Often called an error or a warning.</p>
                <p><b>Augmented Static Analyzer (AugSA):</b> An AI model or an ensemble of models trained on thousands of labelled samples to predict whether a sample is actually a bug.</p>
                <p><b>Positive/Negative Prediction:</b> AugSA predicts positive if it considers sample to contain a bug. It predicts negative if it considers a sample to not contain a bug.</p>
                <p><b>True Positive (TP):</b> A sample that is predicted to be a bug and is actually a bug.</p>
                <p><b>False Positive (FP):</b>A sample that is predicted to be a bug and is actually not a bug.</p>
                <p><b>Model Confidence Score:</b>The likelihood of a sample being a bug according to AugSA.</p>
                <p><b>Prediction Threshold:</b>The threshold indicates the confidence score beyond which the prediction changes. Example: If the threshold is 0.5, a confidence score of 0.51 would mean the model is predicting positive and confidence score of 0.49 would mean the model is predicting negative.</p>
   
                  
                </Column>
              </Grid>
            </TabPanel>
            <TabPanel>
              <Grid className="tabs-group-content">
                <Column lg={16} md={8} sm={4} className="landing-page__tab-content">
                {/* <div>
                <p>Rank: Ranking of bugs based on model confidence. The model confidence is calculated during an Augmented Static Analysis run over a commit. Rank 1 indicates model has the most confidence that the bug is a True Positive, compared to other bugs.</p>
                <p>Developer Experience: The number of FPs a developer has to analyze before finding a TP. This is calculated as the ratio of FP to TP (FP/TP) during AugSA testing. Example: The ideal score is 0 which means every bug the developer analyzes is a TP. A score of 3.0 would mean that the developer has to go through 3 FPs before finding a TP.</p>                <p>Bug Likelihood: Likelihood that a bug is a TP. This is graded as High, Medium and Low.</p>
                <p>Bug Likelihood - High: Developer experience of less than 1 (0 <= FP/TP < 0.5). Almost every bug that the developer analyzes is a TP or in the worst case, every alternate bug is a TP.</p>
                <p>Bug Likelihood - Medium: Developer experience of 1 to 2 (0.5 <= FP/TP < 2). Every alternate bug is a TP or in the worst case, every third bug is a TP.</p>
                <p>Bug Likelihood - Low: Developer experience of 1 to 2 (2 <= FP/TP <= 3). In the best case, every third bug is a TP.</p>
            
                </div> */}
                

                </Column>
              </Grid>
            </TabPanel>
            <TabPanel>
              
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

export default GuidePage;
