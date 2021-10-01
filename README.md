# Auctions-Web3-App

<h2>:bookmark_tabs:	Commission </h2>

A client asked me to build an auction platform where everyone could sell and buy items<br>  

<h2>:open_file_folder: About The Project</h2>

As you can image, this is an Auction platform.<br>
On this simulation you can sell and buy items in USD and aUSD. This one is a<br>
special ERC-20 token minted from [Aphrodite](https://github.com/MikeMoresi/Auctions-App/blob/main/App/Aphrodite.sol) smart contract<br>
(suppose 1 USD = 1 aUSD)

<h2>:thinking: How To Use It</h2>
The first thing that you need to do is sign up. <br> 
After that, you can sell and bit items. If you are a seller, while you are uploading your item,<br>
you can choose if insert your ethereum address or not.<br>
If you do that you will sell your item in aUSD.<br>
At the end of the auction, the seller will be paid and the losers will be refunded. 

<h2>:desktop_computer:	Database </h2>
On this project, I chose to use Django default database and Redis. <br>
All the offers and the aUSD transaction events will be saved on Redis. <br>
Due to not pay too many fees on the ethereum blockchain<br>
all the offers will be sent on chain every 24h 

<h2>🔧 Build With</h2>
 Django <br>
 Remix <br>
 Ganache and Ropsten <br>
 Redis <br>

