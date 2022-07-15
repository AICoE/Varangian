import React from 'react';
import {
  Grid,
  Column,
  ClickableTile,
  Layer
} from '@carbon/react';

const DocumentationSection = () => {
  return (
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

  );
};

export default DocumentationSection;
