pragma solidity ^0.8.7;

import 'https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol';


contract Aphrodite is ERC20{
    address owner;
    constructor() ERC20('Aphrodite','aUSD'){
        _mint(msg.sender,10000*10**18);
        owner=msg.sender;
    }
}


