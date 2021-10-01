# Auctions-Web3-App

<h2>:bookmark_tabs:	Commission </h2>

A client asked me to build an auction platform where everyone could sell and buy items<br>  

<h2>:open_file_folder: About The Project</h2>

As you can image, this is an Auction platform.<br>
On this simulation you can sell and buy items in USD and aUSD. This one is a<br>
special ERC-20 token minted from [Aphrodite](https://github.com/MikeMoresi/Auctions-App/blob/main/App/Aphrodite.sol) smart contract<br>
(suppose 1 USD = 1 aUSD)

<h2>:thinking: How To Use It</h2>
Firstly you sign up, and then you can sell and bit items. <br>
If you want to sell an item, you can decide wheter to include<br>
your ethereum address or not, and in case you decide to include it,<br>
your item will be sold in aUSD.<br>
Once the auction is terminated, the bidders who did not win will be <br>
immediately refunded, while the seller will get paid.

<h2>:desktop_computer:	Database </h2>
This project is based on Django default database and Redis. <br>
All the offers and the aUSD transaction events will be saved on Redis. <br>
In order to not pay too many fees, all the Redis offers data will be sent on ethereum blockchain every 24h 

<h2>🔧 Build With</h2>
 Django <br>
 Remix <br>
 Ganache and Ropsten <br>
 Redis <br>

