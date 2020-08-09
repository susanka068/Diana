import React from 'react'
import {Navbar , Nav , Image } from 'react-bootstrap'
import Logo from '../Img/logos/favicon-32x32.png'
import {Link} from 'react-router-dom'
export default function HomePage() {
    return (
<Navbar bg="light" expand="lg">
  <Image href="/" src={Logo} thumbnail />
  <Navbar.Toggle aria-controls="basic-navbar-nav" />
  <Navbar.Collapse id="basic-navbar-nav">
    <Nav className="mr-auto" style={{'float' : 'right'}}>
      <Link to="/"><Nav.Link href="/">Home</Nav.Link></Link>
      <Link to='/products'><Nav.Link href="/products">Itemlist</Nav.Link></Link>
      <Link to='/analytics' ><Nav.Link href="/analytics">Analytics</Nav.Link></Link>
    </Nav>
  </Navbar.Collapse>
</Navbar>
    )
}
