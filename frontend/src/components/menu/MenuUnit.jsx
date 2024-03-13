import React from 'react';
import { Link } from 'react-router-dom';
import './menu_unit.css';

const MenuUnit = ({ point, to }) => {
    return (
        <Link to={to} className='menu_point'>
            {point}
        </Link>
    );
}

export default MenuUnit;