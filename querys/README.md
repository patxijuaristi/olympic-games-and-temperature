🌡️🥇 Olympic Games and Temperature analysis 🥇🌡️
===

This is a project done for the Data Science subject of the Computer Engineering master's degree in the University of Málaga.

The project aims to analyze the relation between the results of the olympic games and the temperature in the games.

To use the scripts and the program, first it's necessary to create a virtual environemt and then install the required dependencies with pip in it. For that the next commands may be used:

```
virtualenv env
.\env\Scripts\activate

pip install -r .\requirements.txt
```

Then the environmental variable of the MongoDB connection URL has to be set. For that, we will copy the sample file and edit it including the MongoDB URL. It can be done with the next commands:

```
cp .env.sample .env
nano .env
```