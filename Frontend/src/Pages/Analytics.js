import React, { Component } from 'react'
import NordStormData from '../data/stage_4.json'
import { Chart } from 'react-google-charts'
export class Analytics extends Component {
    render() {
        var dataArray = NordStormData.most_concern
        dataArray = [['keywords', 'appearance'] , ...dataArray ];
        console.log(dataArray)
        return (
            
            <div>
               
<Chart
  width={'1300px'}
  height={'1000px'}
  chartType="BarChart"
  loader={<div>Loading Chart</div>}
  data={[
    ['Atrributes', 'cotton', 'polyester','model','crewneck','v-neck','scooped', 'tee' , 'top' , 'jersey' , 'slub' , 'stretch' , 'lace' , 'ruffle' , 'graphic' ,  'short' , 'long' ,'crop','curved', 'tie dye' , 'garment-dyed' , 'pattern' ,],
    ['fabric',         58,        26,       16,      null,     null,    null ,   null ,  null ,   null ,     null ,   null,       null ,   null ,     null,        null ,    null,    null,  null,     null,          null,         null   ,],
    ['neckline',      null ,      null ,   null ,     43 ,      18 ,     4 ,     null ,  null ,   null ,     null ,   null ,      null ,   null ,     null,        null ,    null,    null,  null,     null,          null,         null   ,],
    ['shirt',         null,       null,    null ,    null ,    null ,   null ,    60 ,    11 ,    null ,     null ,   null ,      null ,   null ,     null,        null ,    null,    null,  null,     null,          null,         null   ,],
    ['Knit',          null,       null,    null ,    null ,    null ,   null ,   null ,  null,     11,        6,        2,        null ,   null ,     null,        null ,    null,    null,  null,     null,          null,         null   ,],
    ['design',        null,       null,    null ,    null ,    null ,   null ,   null ,  null,    null ,     null ,   null,         6 ,      4 ,        4 ,        null ,    null,    null,  null,     null,          null,         null   ,],
    ['sleeve',        null,       null,    null ,    null ,    null ,   null ,   null ,  null,    null ,     null ,   null,       null ,   null,      null,         63 ,       8 ,    null,  null,     null,          null,         null   ,],
    ['length',        null,       null,    null ,    null ,    null ,   null ,   null ,  null,    null ,     null ,   null,       null ,   null,      null,        null ,    null ,    5,    null,     null,          null,         null   ,],
    ['hem',           null,       null,    null ,    null ,    null ,   null ,   null ,  null,    null ,     null ,   null,       null ,   null,      null,        null ,    null ,    null,   4,      null,          null,         null   ,],
    ['color',         null,       null,    null ,    null ,    null ,   null ,   null ,  null,    null ,     null ,   null,       null ,   null,      null,        null ,    null ,    null, null,        2,             1,          null   ,],
    ['pleat',         null,       null,    null ,    null ,    null ,   null ,   null ,  null,    null ,     null ,   null,       null ,   null,      null,        null ,    null ,    null, null,     null,          null,           1   ,],
  ]}
  options={{
    title: 'Element distrubution',
    chartArea: { width: '50%' },
    isStacked: true,
    hAxis: {
      title: 'Attributes',
      minValue: 0,
    },
    vAxis: {
      title: 'Values',
    },
  }}
  // For tests
  rootProps={{ 'data-testid': '3' }}
/>

<Chart
  width={'1300px'}
  height={'1000px'}
  chartType="LineChart"
  loader={<div>Loading Chart</div>}
  data={dataArray}
  options={{
    title: 'Customer concerns' ,
    hAxis: {
      title: 'Aspect',
    },
    vAxis: {
      title: 'Count',
    },
  }}
  rootProps={{ 'data-testid': '1' }}
/>


            </div>
        )
    }
}

export default Analytics
