# Trashedy

Repository for the Trashedy project. A five weeks school project aiming to develop a ML object detection model to help map river litter.

## Authors

- Maximilien Dufau
- Benoit Claudic
- Rémi Legrand
- Luc Manceau
- Amélie Jond

We used Pytorch 1.9.0 as the main Deep Learning library.

## Content

The project is divided in three main parts :

- The "production" part with the website and the integrated ML model.
- The research part with notebooks used to train and test the model.
- The .sql database dump, for you to easily install our database with MySQL.

### ml-models-environment

* Notebooks :
  * Train : This notebook can be use to train a pretrained faster rccn model on a specific dataset.
  * Load and execute Model : This notebook is a walk-through presenting how to load a saved model and perform prediction on images in a dataset.

* Saved model and datasets : More informations on the purpose of these folders can be found in the [main readme](https://github.com/Maxew42/ML).

### web-site

The website was created with VueJS 3.0.1. It is working in pair with an homemade API powered by Flask 2.0.1
This is a development website.

#### Website installation steps

1. Install required python libraries with `pip3 install -r requirements.txt --no-index`
2. Setup the database :
  * Import `dbTrashedy.sql` in MySQL
  * Modify connection information in `server/main.py`to fit your own database.
3. Launch the Vue.js app with `npm install` then `npm run serve`
4. Launch the Flask API with `python server/main.py`