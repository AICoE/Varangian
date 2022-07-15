import React from 'react';
import {
  Grid,
  Column,
  Tile,
  Link,
} from '@carbon/react';

const PagesSection = () => {
  return (
    <Grid className="tabs-group-content">
      <Column lg={16} md={8} sm={4} className="landing-page__tab-content">
        <Grid>
          <Column sm={4}>
            <Tile>
              Project #1
              <br />
              <Link href="https://www.carbondesignsystem.com">Link</Link>
            </Tile>
          </Column>
          <Column sm={4}>
            <Tile>
              Project #2
              <br />
              <Link href="https://www.carbondesignsystem.com">Link</Link>
            </Tile>
          </Column>
          <Column sm={4}>
            <Tile>
              Project #3
              <br />
              <Link href="https://www.carbondesignsystem.com">Link</Link>
            </Tile>
          </Column>
          <Column sm={4}>
            <Tile>
              Project #4
              <br />
              <Link href="https://www.carbondesignsystem.com">Link</Link>
            </Tile>
          </Column>
        </Grid>
      </Column>
    </Grid>

  );
};

export default PagesSection;
