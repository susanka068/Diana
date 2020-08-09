import React from 'react'
import { Button , Image ,Card } from 'react-bootstrap'
import Diana from '../Img/diana.png'
import {Link} from 'react-router-dom'
import '../index.css';
export default function HomePage() {
    return (
        <React.Fragment>
<section id="banner" style={{"padding" : "100px 20px"}}>
    <div className="container">
        <div className="row">
            <div className="col-lg-5">
            <h1>Diana</h1>
                    <h3>Designed to augment Fashion Designers</h3> 
                    <p>
                    Diana uses natural language processing and image classification technologies to extract data from E-Portals. Using statistical analysis, it helps developers identify the crucial elements in Garment Designing. 
                    </p>
                    <Button className="btn btn-primary mybtn" variant="primary">Learn more</Button>
                    
            </div>
            <div className="col-lg-7">
                <Image src={Diana} style={{"maxWidth": "100%" , width:"400px" , height:"500px"}}/>
            </div>
        </div>
    </div>
</section>
        <section style={{background : '#ececec'}} >
            <div className='container' >
                <div className="row" >
                    <div className="col-lg-6" >
                   <Card style={{ maxWidth: '18rem' }}>
                    <Card.Body>
                        <Card.Title>Itemlist</Card.Title>
                        <Card.Text>
                        List containing items sorted according to their score
                        </Card.Text>
                        <Link to="/products"><Button className="btn btn-primary mybtn" variant="primary">Check Items</Button></Link>
                    </Card.Body>
                    </Card>
                    </div>
                    <div className="col-lg-6" >
                    <Card style={{ maxWidth: '18rem' , margin:'5px' }}>
                    <Card.Body>
                        <Card.Title>Analytics</Card.Title>
                        <Card.Text>
                        Charts to aid designers
                        </Card.Text>
                        <Link to="/analytics"><Button className="btn btn-primary mybtn" variant="primary">Analytics</Button></Link>
                    </Card.Body>
                    </Card>
                    </div>
                </div>
            </div>
        </section>
        </React.Fragment>
    )
}
