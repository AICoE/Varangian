import React, { useState } from 'react';
import Papa from "papaparse";
import results_top20 from "./libtpms-top20/results-top20.csv";
import bug_3207 from "./libtpms-top20/bug_3207.txt";


import {
  Link,
  DataTableSkeleton,
  Pagination,
  Grid,
  Column,
  Accordion,
  AccordionItem,
  Layer,
  MultiSelect,
  CodeSnippet,
  Button,
  ButtonSet,
} from '@carbon/react';





const IssuePage = () => {

  const items = [
    {
      id: "option-1",
      label: "Option 1"
    },
    {
      id: "option-2",
      label: "Option 2"
    },
    {
      id: "option-3",
      label: "Option 3"
    },
    {
      id: "option-4",
      label: "Option 4"
    },
    {
      id: "option-5",
      label: "Option 5"
    }
  ];
  // State to store parsed data
  const [parsedData, setParsedData] = useState([]);

  //State to store table Column name
  const [tableRows, setTableRows] = useState([]);

  //State to store the values
  const [values, setValues] = useState([]);
  const newtext = useState();

  //const changeHandler = (event) => {
  const changeHandler = (event) => {

    console.log(event.target.files[0]);
    console.log(event.target.files);
    console.log('new');

    // testing for getting the bugs
    fetch(bug_3207)
        .then(t => t.text()).then(text => {
            console.log(text)
            newtext= text;
        })

    // Passing file data (event.target.files[0]) to parse using Papa.parse
    Papa.parse(event.target.files[0], {
      header: true,
      skipEmptyLines: true,
      complete: function (results) {
        const rowsArray = [];
        const valuesArray = [];

        // Iterating data to get column name and their values
        results.data.map((d) => {
          rowsArray.push(Object.keys(d));
          valuesArray.push(Object.values(d));
        });

        // Parsed Data Response in array format
        setParsedData(results.data);

        // Filtered Column Names
        setTableRows(rowsArray[0]);

        // Filtered Values
        setValues(valuesArray);
      },


    });
  };

  return (

    <div>
      {/* File Uploader */}
      <input
        type="file"
        name="file"
        onChange={changeHandler}
        accept=".csv"
        style={{ display: "block", margin: "10px auto" }}
      />
      <br />
      <br />
      {/* Table */}
      <table>
        <thead>
          <tr>
            {tableRows.map((rows, index) => {
              return <th key={index}>{rows}</th>;
            })}
          </tr>
        </thead>
      </table>

      <Grid>
        <Column lg={16} md={8} sm={4}>
          <Accordion>
            {values.map((value, index) => {
              return (
                <AccordionItem title={values[index][3]}>
                  <p>id: {values[index][0]}</p>
                  <p>iid: {values[index][1]}</p>
                  <p>Bug Location: {values[index][2]}</p>
                  <p>Report Name: {values[index][3]}</p>
                  <p>Bug Type: {values[index][4]}</p>
                  <p>Score: {values[index][5]}</p>
                  <p>Priority: {values[index][6]}</p>

                  <CodeSnippet>
                   

                  </CodeSnippet>
                </AccordionItem>
              );
            })}
          </Accordion>
        </Column>
      </Grid>
    </div>
  );
};





// const IssuePage = () => {

//   const items = [
//     {
//       id: "option-1",
//       label: "Option 1"
//     },
//     {
//       id: "option-2",
//       label: "Option 2"
//     },
//     {
//       id: "option-3",
//       label: "Option 3"
//     },
//     {
//       id: "option-4",
//       label: "Option 4"
//     },
//     {
//       id: "option-5",
//       label: "Option 5"
//     }
//   ];




//   return (
//      <>
//       <Grid className="landing-page" fullWidth>
//         <Column lg={16} md={8} sm={4} className="landing-page__banner">
//           <h1 className="landing-page__heading">
//           Github Repo: AICoE/Varangian
//           </h1>
//         </Column>
//         <Column lg={16} md={8} sm={4}>
//           <h1>
//             Alert Filters
//           </h1>
//         </Column>

//         <Column lg={4} md={8} sm={8}>
//           <MultiSelect
//             label="MultiSelect label"
//             items={items}
//             onChange={({ selectedItems }) => {
//               console.log(selectedItems);
//             }}
//           />
//         </Column>
//         <Column lg={4} md={8} sm={8}>
//           <MultiSelect
//             label="MultiSelect label"
//             items={items}
//             onChange={({ selectedItems }) => {
//               console.log(selectedItems);
//             }}
//           />
//         </Column>
//         <Column lg={4} md={8} sm={8}>
//           <MultiSelect
//             label="MultiSelect label"
//             items={items}
//             onChange={({ selectedItems }) => {
//               console.log(selectedItems);
//             }}
//           />
//         </Column>
//         <Column lg={4} md={8} sm={8}>
//           <MultiSelect
//             label="MultiSelect label"
//             items={items}
//             onChange={({ selectedItems }) => {
//               console.log(selectedItems);
//             }}
//           />
//         </Column>





//         <Column lg={16} md={8} sm={4}>
//           <Accordion>
//             <AccordionItem title="Error Type: INTEGER_OVERFLOW_L2-libtiff/tif_read.c:616-HIGH">
//               <h4>Description:</h4>
//               <p>Infer bug type: INTEGER_OVERFLOW_L2</p>
//               <p>Location: libtiff/tif_read.c:616</p>
//               <p>Description: libtiff/tif_read.c:616:26: Binary operation: (9223372036854775807 - [-1, 9223372036854775807]):signed64 by call to TIFFReadRawStrip</p>
//               <p>Likelihood: HIGH</p>
//               <h4>Possible Bug Location</h4>
//               <CodeSnippet type="multi" feedback="Copied to clipboard">
//                 {`libtiff/tif_read.c:616:26: Binary operation: (9223372036854775807 - [-1, 9223372036854775807]):signed64 by call to "TIFFReadRawStrip"
//     614.                     n=0;
//     615.                 }
//     616.                 else if( ma > TIFF_TMSIZE_T_MAX - size )
//                                   ^
//     617.                 {
//     618.                     n=0;`}
//               </CodeSnippet>
//               <h4>All Traces</h4>
//               <h5><i>Bug Rank: 1</i></h5>
//               <CodeSnippet type="multi" feedback="Copied to clipboard">
//                 {`#2708
// tools/tiff2pdf.c:2387: error: Integer Overflow L2
//   (9223372036854775807 - [-1, 9223372036854775807]):signed64 by call to 'TIFFReadRawStrip'.
// `}
//               </CodeSnippet>
//               <Layer>
//                 <CodeSnippet type="multi" feedback="Copied to clipboard">
//                   {`tools/tiff2pdf.c:2387:21: Call
// 2385. 	buffer[bufferoffset++]=(0xd0 | ((i-1)%8));
// 2386. 	}
// 2387. 	bufferoffset+=TIFFReadRawStrip(input, 
//                           ^
// 2388. 	i, 
// 2389. 	(tdata_t) &(((unsigned char*)buffer)[bufferoffset]), `}
//                 </CodeSnippet>
//                 <Layer>
//                   <CodeSnippet type="multi" feedback="Copied to clipboard">
//                     {`libtiff/tif_read.c:681:1: Parameter 'size'
//   679.  * Read a strip of data from the file.
//   680.  */
//   681. tmsize_t
//        ^
//   682. TIFFReadRawStrip(TIFF* tif, uint32_t strip, void* buf, tmsize_t size)
//   683. {`}
//                   </CodeSnippet>
//                 </Layer>
//               </Layer>

//               <ButtonSet>
//                 <Button kind="danger--tertiary">
//                   Bug - Needs Fix
//                 </Button>
//                 &nbsp;
//                 <Button kind="primary" >
//                   Bug - Does Not Need Fix
//                 </Button>
//                 &nbsp;
//                 <Button kind="secondary">
//                   Not a Bug
//                 </Button>
//               </ButtonSet>
//             </AccordionItem>
//           </Accordion>
//         </Column>
//       </Grid>






//     </>

//   );
// };

export default IssuePage;
