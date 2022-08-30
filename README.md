<p align="center">
  <img width="735" alt="image" src="https://user-images.githubusercontent.com/2076274/187502469-b07b62d7-0d59-4b79-b5f0-e08b65640430.png">
</p>

# PockeTour
Historical landmark recognition backend service.   
Providing information on historical landmarks in Jerusalem based on image and location.
Developed for the Jerusalem Municipality to shed light on the thousands of historical landmarks the city has to offer.

<p float="left">
  <img width="200" alt="image" src="https://user-images.githubusercontent.com/2076274/187502744-ae430bb0-b321-4cf1-9ad3-f5544b0f2f38.png">
  <img width="200" alt="image" src="https://user-images.githubusercontent.com/2076274/187502905-c4fb7460-d755-4a3f-be40-a8e70be5706b.png">
</p>

## Usage
Simply run the python server by running `python pocket_server.py` and send a POST request to `/image` containing:
* base64 - base 64 encoded image of the landmark you wish to locate
* gps - the lat and lng of the your immidiate vacinity if possible

## Modification
As this is the original codebase and was not intended for high load, we use a sqlite DB which you can simply change for your specific sites.
