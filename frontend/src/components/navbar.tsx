import React from 'react';
import { NavLink as Link } from 'react-router-dom';
import styled from 'styled-components';

export const Nav = styled.nav`
    display: flex;
    justify-content: space-between;
    background-color: #f1f1f1;
    color: black;
    height: fit-content;
`;

export const NavLink = styled(Link)`
    
`;

export function Navbar() {
    return (
        <Nav>
            <NavLink to="/about">
                About
            </NavLink>
        </Nav>
    );
}