# Simple Demo application
This is just a simple example of how backend made with flask and the rasp bi, which takes the images, could be used in the project.

The idea is that the image taking raspberry pi is going to send the image periodically to the backend server. The server is then going to pass the image to whatever for example it could be made into an NFT.

This uses couple of libaries which are `requests`, `Pillow` and obviously `flask`. `requests` is used to send HTTP requests *shocking* I know. `pillow` library is used to open the image file and examine the metadata attached to it.

## Just some thoughts about the project
If we would like to turn these images into NFTs whe should be thinking about the storage system. Should the NFTs be stored in the chain or off the chain? The more popular system seems to be the off the chain one.